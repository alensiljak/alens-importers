"""
Vanguard Australia, mutual funds

Download the JSON from
Distributions:
https://www.vanguard.com.au/personal/api/data/products/product-distribution/8105

Invoke with:
    curl <url> -o vanguard-8105.json

Import from JSON file.
"""
from dataclasses import dataclass
import os
import re

import beangulp  # type: ignore
from beangulp import cache
from beancount.core import amount, data, flags, position, realization
from beangulp.importers.mixins.identifier import identify
from loguru import logger


@dataclass
class DistributionEntry:
    """
    Distribution entry
    """
    asOfDate: str
    declarationDate: str
    exDividendDate: str
    recordDate: str
    payableDate: str
    reinvestPrice: float
    reinvestmentDate: str
    scheduleType: dict
    taxDetails: list


@dataclass
class DistributionDto:
    """
    Distribution DTO
    """
    statusCode: int
    message: str
    data: dict[str, list[DistributionEntry]]


class Importer(beangulp.Importer):
    """Vanguard Australia mutual fund importer for Beancount"""

    def __init__(self, *args, **kwargs):
        pass

    def account(self, filepath: str) -> data.Account:
        """Return the archiving account associated with the given file."""
        return "Vanguard-Australia"

    def filename(self, filepath: str) -> str | None:
        """Returns the archival filename for the report"""
        return os.path.basename(filepath)

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        logger.debug(f"Identifying {filepath}")

        matchers = {
            # File is json
            "mime": [re.compile(r"text/json")],
        }

        return identify(matchers, None, cache.get_file(filepath))

    # def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
    #     """Extract the data from the given file"""
    #     pass

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        logger.debug(f"Deduplicating {len(entries)} entries")

        return super().deduplicate(entries, existing)
