"""Common code for tests."""
import os
from collections import namedtuple

from beancount import loader
from beangulp import extract
from beangulp.testing import _run, compare_expected


fund_codes = [
    ["AMLP", "US00162Q4525"],
    ["OPI", "US67623C1099"],
    ["PFXF", "US92189F4292"],
    ["VACF.AX", "AU00000VACF9"],
    ["VAP.AX", "AU000000VAP7"],
    ["VGOV_F", "IE00B42WWV65"],
    ["VHY.AX", "AU000000VHY4"],
]

interest_symbols = [
    "VGOV_F",
]

ibflex_config = {
    "cash_account": "Assets:Investments:IB:Cash-{currency}",
    "stock_account": "Assets:Investments:IB:Stocks:{symbol}",
    "dividend_account": "Income:Investments:Dividend:IB:{currency}:{symbol}",
    "dividend_payee": "{symbol} distribution",
    "interest_account": "Income:Investments:Interest:IB:{symbol}",
    "capgain_account": "Income:Investment:Capital-Gains:IB",
    "broker_interest_account": "Income:Investments:Interest:IB:Cash",
    "fees_account": "Expenses:Financial:IB",
    "whtax_account": "Expenses:Investments:IB:WithholdingTax",
    "txfer-EUR": "Assets:Bank-Accounts:EUR",
    "txfer-AUD": "Assets:Bank-Accounts:AUD",
    "symbols": fund_codes,
    "interest_symbols": interest_symbols,
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
    expected_filename = os.path.join(base_path, filename + ".beancount")
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
