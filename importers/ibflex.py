"""
Creating IBKR importer from scratch.
"""

import re
from datetime import date

import beangulp  # type: ignore
from beancount.core import amount, data, flags, position, realization
from beangulp import cache
from beangulp.importers.mixins.identifier import identify
from ibflex import Types, parser
from ibflex.enums import BuySell, CashAction, OpenClose, Reorg
from loguru import logger


class Importer(beangulp.Importer):
    """IBKR Flex Query XML importer for Beancount"""

    def __init__(self, *args, **kwargs):
        logger.debug("Initializing IBKR importer")

        # self.config = config
        # TODO: get config

        super().__init__(*args, **kwargs)

    @property  # type: ignore
    def name(self) -> str:
        logger.debug("Getting importer name")

        return "AS IBKR importer (new)"

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        logger.debug(f"Identifying {filepath}")

        matchers = {
            # File is xml
            "mime": [re.compile(r"text/xml")],
            # The main XML tag is FlexQueryResponse
            "content": [re.compile(r"<FlexQueryResponse ")],
        }

        return identify(matchers, None, cache.get_file(filepath))

    def account(self, filepath: str) -> data.Account:
        """Return the archiving account associated with the given file."""
        logger.debug(f"Getting account for {filepath}")

        # TODO : return the correct account
        return "ib-aus"

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        """
        Extract transactions and other directives from a document.
        Existing entries are received as an argument, if Beancount file was
        specified.
        Deduplication is done against these.
        A list of imported directives should be returned.
        """
        logger.debug(f"Extracting from {filepath}")

        # if False and self.use_existing_holdings and existing_entries is not None:
        #     self.holdings_map = self.get_holdings_map(existing_entries)
        # else:
        #     self.holdings_map = defaultdict(list)
        statements = parser.parse(open(filepath, "r", encoding="utf-8"))
        assert isinstance(statements, Types.FlexQueryResponse)

        statement = statements.FlexStatements[0]
        transactions = (
        #     self.Trades(statement.Trades) +
            self.cash_transactions(statement.CashTransactions)
        #     + self.Balances(statement.CashReport)
        #     + self.corporate_actions(statement.CorporateActions)
        )

        # transactions = self.merge_dividend_and_withholding(transactions)
        # # self.adjust_closing_trade_cost_basis(transactions)
        # return self.autoopen_accounts(transactions, existing_entries) + transactions

        # TODO : read transactions
        return []

    def get_account_name(self, account_str, symbol=None, currency=None):
        if symbol is not None:
            account_str = account_str.replace("{symbol}", symbol.replace(" ", ""))
        if currency is not None:
            account_str = account_str.replace("{currency}", currency)
        return account_str

    def get_liquidity_account(self, currency):
        return self.get_account_name(self.cash_account, currency=currency)

    def cash_transactions(self, ct):
        '''Extract cash transactions'''
        transactions = []
        for index, row in enumerate(ct):
            if row.type == CashAction.DEPOSITWITHDRAW:
                # TODO : implement
                # transactions.append(self.deposit_from_row(index, row))
                pass
            elif row.type in (CashAction.BROKERINTRCVD, CashAction.BROKERINTPAID):
                # TODO : implement
                # transactions.append(self.Interest_from_row(index, row))
                pass
            elif row.type in (CashAction.FEES, CashAction.COMMADJ):
                # TODO : implement
                # transactions.append(self.fee_from_row(index, row))
                pass
            elif row.type in (
                CashAction.WHTAX,
                CashAction.DIVIDEND,
                CashAction.PAYMENTINLIEU,
            ):
                transactions.append(
                    self.dividends_and_withholding_tax_from_row(index, row)
                )
            else:
                raise RuntimeError(f"Unknown cash transaction type: {row.type}")
        return transactions

    def dividends_and_withholding_tax_from_row(self, idx, row):
        """Converts dividends, payment inlieu of dividends and withholding tax to a 
        beancount transaction.
        Stores div type in metadata for the merge step to be able to match tax withdrawals 
        to the correct div.
        """
        amount_ = amount.Amount(row.amount, row.currency)

        text = row.description
        # Find ISIN in description in parentheses
        isin = re.findall(r"\(([a-zA-Z]{2}[a-zA-Z0-9]{9}\d)\)", text)[0]
        pershare_match = re.search(r"(\d*[.]\d*)(\D*)(PER SHARE)", text, re.IGNORECASE)
        # payment in lieu of a dividend does not have a PER SHARE in description
        pershare = pershare_match.group(1) if pershare_match else ""

        meta = {"isin": isin, "per_share": pershare}
        # TODO : remove
        account = "temp account"
        if row.type == CashAction.WHTAX:
            # TODO : implement
            # account = self.get_wht_account(row.symbol)
            type_ = (
                CashAction.PAYMENTINLIEU
                if re.search("payment in lieu of dividend", text, re.IGNORECASE)
                else CashAction.DIVIDEND
            )
        else:
            # TODO : implement
            # account = self.get_div_income_account(row.currency, row.symbol)
            type_ = row.type
            meta["div"] = True
        meta["div_type"] = type_.value
        postings = [
            data.Posting(account, -amount_, None, None, None, None),
            data.Posting(
                self.get_liquidity_account(row.currency),
                amount_,
                None,
                None,
                None,
                None,
            ),
        ]
        meta = data.new_metadata(
            "dividend",
            0,
            meta,
        )

        return data.Transaction(
            meta,
            row.reportDate,
            flags.FLAG_OKAY,
            row.symbol,  # payee
            text,
            data.EMPTY_SET,
            data.EMPTY_SET,
            postings,
        )

    def date(self, filepath: str) -> date | None:
        """Archival date of the file"""
        logger.debug(f"Getting date for {filepath}")

        return super().date(filepath)

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        logger.debug(f"Deduplicating {len(entries)} entries")

        return super().deduplicate(entries, existing)
