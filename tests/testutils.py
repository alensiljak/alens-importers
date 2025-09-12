"""
Common test utilities
"""

from alens.importers import ibflex
from tests.test_setup import ibflex_config, run_importer_test_with_existing_entries


def run_test(xml_input_filename: str):
    """
    Runs import with the specified XML file.
    """
    importer = ibflex.Importer(ibflex_config)
    run_importer_test_with_existing_entries(importer, xml_input_filename)
