"""Test the ibflex importer"""
from alens.importers import ibflex

from tests.test_setup import ibflex_config, run_importer_test_with_existing_entries


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


def test_read_tuple_symbors():
    """Read symbols from a tuple array"""
    symbols = [
        ("AAPL", "US0378331005"),
        ("MSFT", "US5949181045")
    ]
    importer = ibflex.Importer(ibflex_config)
    importer.create_symbol_dictionaries(symbols)
