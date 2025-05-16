"""
Creating IBKR importer from scratch.
"""

from datetime import date
from beancount.core.data import Entries
import beangulp
import beangulp.importer
from beancount.core import data


class Importer(beangulp.Importer):
    """IBKR importer"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return "IBKR importer"

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        raise NotImplementedError
        # return True

    def account(self, filepath: str) -> data.Account:
        """Return the account associated with the given file."""
        raise NotImplementedError

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        """Extract transactions and other directives from a document.
        Existing entries are received as an argument, if Beancount file was
        specified.
        Deduplication is done against these.
        A list of imported directives should be returned.
        """
        raise NotImplementedError

    def date(self, filepath: str) -> date | None:
        """Archival date of the file"""
        raise NotImplementedError
        # return super().date(filepath)

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        raise NotImplementedError
        # return super().deduplicate(entries, existing)
