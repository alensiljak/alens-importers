"""
Debug test for mime type detection in ibflex identify().
Set a breakpoint inside identify() or here to inspect mime type behavior.
"""
import pathlib

from beangulp import cache

from alens.importers import ibflex
from tests.test_setup import ibflex_config


TESTS_DIR = pathlib.Path(__file__).resolve().parent
XML_FILE = TESTS_DIR / "cash-balances.xml"


def test_mime_type_debug():
    """Inspect the detected mime type for an XML file."""
    cached = cache.get_file(str(XML_FILE))
    mime = cached.mimetype()

    print(f"\nFile: {XML_FILE}")
    print(f"Detected mime type: {mime}")

    importer = ibflex.Importer(ibflex_config)
    result = importer.identify(str(XML_FILE))

    print(f"identify() returned: {result}")
    assert result is True
