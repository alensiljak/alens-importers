"""Test the ibflex importer"""
import pytest
from alens.importers import ibflex

from tests.test_setup import ibflex_config, run_importer_test_with_existing_entries
from tests.testutils import run_test


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


def test_div_interest():
    """Test interest distribution"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "div-interest.xml")


def test_simple_whtax():
    """Simple withholding tax"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "simple-whtax.xml")


def test_stock_balances():
    """Stock balances"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "stock-balances.xml")


def test_deposits_withdrawals():
    """Handle deposits and withdrawals"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "deposits-withdrawals.xml")


def test_broker_interest_recvd():
    """Handle broker interest received"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "brk-int-recvd.xml")


def test_tax_adjustments():
    """
    Handle tax adjustments
    This is normally the case when the tax is lowered. One amount is refunded
    and another one is charged.
    """
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "tax-adjustment.xml")


def test_read_tuple_symbols():
    """Read symbols from a tuple array"""
    symbols = [
        ("AAPL", "US0378331005"),
        ("MSFT", "US5949181045")
    ]
    importer = ibflex.Importer(ibflex_config)
    importer.create_symbol_dictionaries(symbols)


def test_stock_trades():
    """Handle stock trades"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "stock-trades.xml")


def test_commissions():
    """Commissions + Taxes"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "commissions.xml")


def test_combine_fx():
    """Test combining forex transactions"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "forex-combine.xml")

def test_stock_trades_merge():
    """Merge stock trades"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "stock-trades-merge.xml")


def test_one_decimal():
    """Numbers should not have only one decimal!"""
    run_test("one-decimal.xml")


def test_multiple_symbols_one_isin():
    """
    The same ISIN can be dual-listed under different beancount symbols
    (e.g. DGSE.MI / WTED.DE). IBKR's report only gives the base ticker
    (e.g. "DGSE"), so the importer must disambiguate against the
    configured symbols for that ISIN.
    """
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "multiple-symbols-one-isin.xml")
