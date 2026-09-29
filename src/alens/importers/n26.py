'''
Importer for N26 CSV files.
It handles:
- payee renames
- distributions (income account)
- automatic categorization

Configuration (dict, first argument):
    account:            N26 asset account, e.g. "Assets:Bank:N26"
    currency:           account currency, default "EUR"
    default_expense:    account for uncategorized outgoing payments
    default_income:     account for uncategorized incoming payments
    dividend_account:   template for distributions, e.g. "Income:Dividends:{symbol}".
                        {symbol} is resolved through `isin_to_symbol`, or the ISIN itself.
    isin_to_symbol:     dict, ISIN -> commodity symbol
    payee_renames:      dict, regex -> payee name
    categories:         dict, regex (matched against payee, then reference) -> account
'''
import csv
import datetime
import os
import re
from decimal import Decimal

import beangulp  # type: ignore
from beancount.core import amount, data, flags
from loguru import logger

HEADER_START = '"Booking Date","Value Date","Partner Name"'
ISIN_RE = re.compile(r"\bISIN\s+([A-Z]{2}[A-Z0-9]{9}\d)\b")
DIVIDEND_RE = re.compile(r"cash dividend", re.IGNORECASE)


class Importer(beangulp.Importer):
    """N26 CSV importer for Beancount"""

    def __init__(self, config: dict | None = None, *args, **kwargs):
        self.config = config or {}
        self.currency = self.config.get("currency", "EUR")
        self.payee_renames = [
            (re.compile(k, re.IGNORECASE), v)
            for k, v in self.config.get("payee_renames", {}).items()
        ]
        self.categories = [
            (re.compile(k, re.IGNORECASE), v)
            for k, v in self.config.get("categories", {}).items()
        ]
        self.isin_to_symbol = self.config.get("isin_to_symbol", {})
        super().__init__(**kwargs)

    @property  # type: ignore
    def name(self) -> str:
        return "AS N26 importer"

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        if not filepath.lower().endswith(".csv"):
            return False
        try:
            with open(filepath, encoding="utf-8-sig") as f:
                return f.readline().startswith(HEADER_START)
        except (OSError, UnicodeDecodeError):
            return False

    def account(self, filepath: str) -> data.Account:
        return self.config.get("account", "Assets:Bank:N26")

    def filename(self, filepath: str) -> str | None:
        return "n26." + os.path.basename(filepath)

    def date(self, filepath: str) -> datetime.date | None:
        """Latest booking date in the file."""
        rows = self._read_rows(filepath)
        if not rows:
            return None
        return max(self._date(r["Booking Date"]) for r in rows)

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        logger.debug(f"Extracting {filepath}")
        entries = []
        for idx, row in enumerate(self._read_rows(filepath), start=2):
            entries.append(self._transaction(filepath, idx, row))
        return entries

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        return super().deduplicate(entries, existing)

    # ---- internals

    @staticmethod
    def _read_rows(filepath: str) -> list[dict]:
        with open(filepath, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _date(text: str) -> datetime.date:
        return datetime.date.fromisoformat(text)

    def _transaction(self, filepath: str, lineno: int, row: dict) -> data.Transaction:
        value = Decimal(row["Amount (EUR)"])
        reference = row["Payment Reference"].strip()
        partner = row["Partner Name"].strip()
        units = amount.Amount(value, self.currency)

        meta = data.new_metadata(filepath, lineno)
        if row["Value Date"] != row["Booking Date"]:
            meta["value_date"] = row["Value Date"]
        orig_cur = row["Original Currency"]
        if orig_cur and orig_cur != self.currency:
            meta["original_amount"] = f'{row["Original Amount"]} {orig_cur}'
            meta["exchange_rate"] = row["Exchange Rate"]

        isin = self._dividend_isin(partner, reference)
        if isin:
            payee = None
            narration = f"Dividend {self.isin_to_symbol.get(isin, isin)}"
            meta["isin"] = isin
            other = self._dividend_account(isin)
        else:
            payee = self._rename_payee(partner)
            narration = reference
            other = self._categorize(partner, reference, value)

        postings = [
            data.Posting(self.account(filepath), units, None, None, None, None),
            data.Posting(other, -units if other else None, None, None, None, None)
            if other else data.Posting("Expenses:FIXME", -units, None, None, None, None),
        ]
        return data.Transaction(
            meta, self._date(row["Booking Date"]), flags.FLAG_OKAY,
            payee, narration, data.EMPTY_SET, data.EMPTY_SET, postings,
        )

    @staticmethod
    def _dividend_isin(partner: str, reference: str) -> str | None:
        if not DIVIDEND_RE.search(reference):
            return None
        m = ISIN_RE.search(reference)
        return m.group(1) if m else None

    def _dividend_account(self, isin: str) -> str:
        template = self.config.get("dividend_account", "Income:Dividends:{symbol}")
        return template.format(symbol=self.isin_to_symbol.get(isin, isin))

    def _rename_payee(self, partner: str) -> str | None:
        for pattern, new_name in self.payee_renames:
            if pattern.search(partner):
                return new_name
        return partner or None

    def _categorize(self, partner: str, reference: str, value: Decimal) -> str | None:
        for pattern, account in self.categories:
            if pattern.search(partner) or (reference and pattern.search(reference)):
                return account
        if value < 0:
            return self.config.get("default_expense", "Expenses:FIXME")
        return self.config.get("default_income", "Income:FIXME")
