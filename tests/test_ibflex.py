"""Test the ibflex importer"""

# from common import run_importer_test_with_existing_entries
import os
from collections import namedtuple

from beancount import loader
from beangulp import extract
from beangulp.testing import _run, compare_expected

# from uabean.importers.ibkr import get_test_importer
from importers import ibflex


ibflex_config = {
    "cash_account": "Assets:Investments:IB:Cash-{currency}",
    "dividend_account": "Income:Investments:Dividend:IB:{currency}:{symbol}",
    "interest_account": "Income:Investments:IB:{symbol}:Interest",
    "whtax_account": "Expenses:Investments:IB:WithholdingTax",
}

Context = namedtuple("Context", ["importers"])


def run_importer_test(importer, capsys):
    """?"""
    documents = [os.path.abspath("tests/")]
    _run(
        Context([importer]),
        documents,
        "",
        0,
        0,
    )
    captured = capsys.readouterr()
    assert "PASSED" in captured.out
    assert "ERROR" not in captured.out


def run_importer_test_with_existing_entries(importer, filename):
    """Runs the test with existing entries"""
    # base_path = os.path.abspath(f"tests/importers/{importer.account('')}")
    base_path = os.path.abspath("tests/")
    expected_filename = os.path.join(base_path, f"{filename}.beancount")

    document = os.path.join(base_path, filename)
    existing_entries_filename = document + ".beancount"
    existing_entries = loader.load_file(
        os.path.join(base_path, existing_entries_filename)
    )[0]

    account = importer.account(document)
    date = importer.date(document)
    name = importer.filename(document)
    entries = extract.extract_from_file(importer, document, existing_entries)
    diff = compare_expected(expected_filename, account, date, name, entries)

    if diff:
        for line in diff:
            print(line)

    assert not diff


def test_run_importer():
    """Use the default run method"""
    run_importer_test(ibflex.Importer(ibflex_config), None)


def test_div_tax():
    """Divident + tax"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "div-tax.xml")


def test_tax_reversal():
    """WhTax reversal"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "tax-reversal.xml")


def test_commission_adjustment():
    """Commission adjustment"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "commission-adjustment.xml")


def test_cash_balances():
    """Cash balances"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "cash-balances.xml")
