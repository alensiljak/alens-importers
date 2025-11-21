'''
Test identifying XML files
'''
import pathlib
import pytest
from alens.importers import ibflex

from tests.test_setup import ibflex_config, run_importer_test_with_existing_entries
from tests.testutils import run_test


def test_identify():
    '''
    Run XML file identification.
    '''
    importer = ibflex.Importer(ibflex_config)
    current_file_path = pathlib.Path(__file__).resolve()
    tests_directory = current_file_path.parent
    xml_absolute_path = tests_directory / "cash-balances.xml"
    importer.identify(xml_absolute_path)
