"""
Creating IBKR importer from scratch.
"""

from collections import defaultdict
from datetime import date

import beangulp # type: ignore
import beangulp.importer # type: ignore
from beancount.core import data
from beancount.core.data import Entries
from ibflex import Types, parser


class Importer(beangulp.Importer):
    """IBKR importer"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property  # type: ignore
    def name(self) -> str:
        return "IBKR importer"

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        # File is xml
        if filepath.endswith(".xml"):
            return True
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # The main XML tag is FlexQueryResponse


        raise NotImplementedError
        # return True

    def account(self, filepath: str) -> data.Account:
        """Return the account associated with the given file."""
        return "ib-aus"

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        """
        Extract transactions and other directives from a document.
        Existing entries are received as an argument, if Beancount file was
        specified.
        Deduplication is done against these.
        A list of imported directives should be returned.
        """
        # if False and self.use_existing_holdings and existing_entries is not None:
        #     self.holdings_map = self.get_holdings_map(existing_entries)
        # else:
        #     self.holdings_map = defaultdict(list)
        # statement = parser.parse(open(filename))
        # assert isinstance(statement, Types.FlexQueryResponse)
        # poi = statement.FlexStatements[0]  # point of interest
        # transactions = (
        #     self.Trades(poi.Trades)
        #     + self.cash_transactions(poi.CashTransactions)
        #     + self.Balances(poi.CashReport)
        #     + self.corporate_actions(poi.CorporateActions)
        # )

        # transactions = self.merge_dividend_and_withholding(transactions)
        # # self.adjust_closing_trade_cost_basis(transactions)
        # return self.autoopen_accounts(transactions, existing_entries) + transactions

        return []

    def date(self, filepath: str) -> date | None:
        """Archival date of the file"""
        raise NotImplementedError
        # return super().date(filepath)

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        raise NotImplementedError
        # return super().deduplicate(entries, existing)
