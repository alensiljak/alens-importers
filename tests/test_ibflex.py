"""Test the ibflex importer"""

import os
from collections import namedtuple

from beancount import loader
from beangulp import extract
from beangulp.testing import _run, compare_expected

# from uabean.importers.ibkr import get_test_importer
from alens.importers import ibflex


fund_codes = [["OPI", "US67623C1099"], ["VAP.AX", "AU000000VAP7"]]

ibflex_config = {
    "cash_account": "Assets:Investments:IB:Cash-{currency}",
    "stock_account": "Assets:Investments:IB:Stocks:{symbol}",
    "dividend_account": "Income:Investments:Dividend:IB:{currency}:{symbol}",
    "dividend_payee": "{symbol} distribution",
    "interest_account": "Income:Investments:Interest:IB:{symbol}",
    "broker_interest_account": "Income:Investments:Interest:IB:Cash",
    "fees_account": "Expenses:Commissions:IB",
    "whtax_account": "Expenses:Investments:IB:WithholdingTax",
    "txfer-EUR": "Assets:Bank-Accounts:EUR",
    "txfer-AUD": "Assets:Bank-Accounts:AUD",
    "symbols": fund_codes,
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
    if not os.path.exists(expected_filename):
        raise ValueError(f"Missing expected file: {expected_filename}")

    document = os.path.join(base_path, filename)
    existing_entries_filename = document + ".beancount"
    existing_entries_path = os.path.join(base_path, existing_entries_filename)
    existing_entries = loader.load_file(existing_entries_path)[0]

    account = importer.account(document)
    date = importer.date(document)
    name = importer.filename(document)
    entries = extract.extract_from_file(importer, document, existing_entries)
    diff = compare_expected(expected_filename, account, date, name, entries)

    if diff:
        for line in diff:
            print(line.strip())

    assert not diff


# def test_run_importer():
#     """Use the default run method"""
#     run_importer_test(ibflex.Importer(ibflex_config), None)

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


def test_simple_div():
    """Simple dividend"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "simple-div.xml")


def test_simple_whtax():
    """Simple withholding tax"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "simple-whtax.xml")


def test_stock_balances():
    """Stock balances"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "stock-balances.xml")


def test_other_fees():
    """Other fees"""
    assert False


def test_deposits_withdrawals():
    """Handle deposits and withdrawals"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "deposits-withdrawals.xml")


def test_broker_interest_recvd():
    """Handle broker interest received"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "brk-int-recvd.xml")


def test_report_unknown_records():
    """Report unknown records to the console?"""
    assert False

def test_tax_adjustments():
    """
    Handle tax adjustments
    This is normally the case when the tax is lowered, refunded, and a 
    smaller amount is charged.
    """
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "tax-adjustments.xml")
    assert False

def test_corporate_actions():
    """Handle corporate actions"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "corp-actions.xml")
    assert False

def test_stock_merger():
    """Handle stock merger"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "stock-merger.xml")
    assert False

def test_stock_split():
    """Handle stock split"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "stock-split.xml")
    assert False

def test_issue_change():
    """Handle issue change"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "issue-change.xml")
    assert False

def test_forex():
    """Handle forex"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "forex.xml")
    assert False

def test_stock_trades():
    """Handle stock trades"""
    # importer = ibflex.Importer(ibflex_config)
    # run_importer_test_with_existing_entries(importer, "stock-trades.xml")
    assert False
