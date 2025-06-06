"""
Test Forex parsing
"""
from alens.importers import ibflex

from tests.test_setup import ibflex_config, run_importer_test_with_existing_entries


def test_forex():
    """Handle forex"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "forex.xml")


def test_dont_mix_transactions():
    """Do not use wrong transaction types for FX and do not explode"""
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, "forex-mix.xml")
