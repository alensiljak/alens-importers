'''
Tests for the N26 CSV importer.
'''
import pathlib
from decimal import Decimal

from alens.importers import n26

CSV = str(pathlib.Path(__file__).parent / "n26.csv")
CONFIG = {
    "account": "Assets:Bank:N26",
    "isin_to_symbol": {"LU0335044896": "XDWD"},
    "payee_renames": {r"^Lidl": "Lidl"},
    "categories": {r"^Lidl": "Expenses:Food:Groceries"},
}


def test_identify():
    assert n26.Importer(CONFIG).identify(CSV)


def test_extract():
    entries = n26.Importer(CONFIG).extract(CSV, [])
    assert len(entries) == 7
    lidl = entries[0]
    assert lidl.payee == "Lidl"
    assert lidl.postings[0].units.number == Decimal("-10.3")
    assert lidl.postings[1].account == "Expenses:Food:Groceries"
    div = entries[2]
    assert div.postings[1].account == "Income:Dividends:XDWD"
    assert div.postings[0].units.number == Decimal("6.86")
    assert entries[-1].postings[1].account == "Expenses:FIXME"
