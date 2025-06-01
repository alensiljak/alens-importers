"""
Creating IBKR importer from scratch.
"""

import re
from datetime import date

import beangulp  # type: ignore
from beancount.core import data
from beangulp import cache
from beangulp.importers.mixins.identifier import identify
from loguru import logger


class Importer(beangulp.Importer):
    """IBKR Flex Query XML importer for Beancount"""

    def __init__(self, *args, **kwargs):
        logger.debug("Initializing IBKR importer")

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
        """Return the account associated with the given file."""
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
        logger.debug(f"Getting date for {filepath}")

        return super().date(filepath)

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        logger.debug(f"Deduplicating {len(entries)} entries")

        return super().deduplicate(entries, existing)
