"""
Tests for the utility functions.
"""

from decimal import Decimal
from alens.importers.utilities import get_number_of_decimal_places


def test_decimal_places():
    """Test the recognition of decimal places"""
    assert get_number_of_decimal_places(Decimal("1.2300")) == 2  # 2
    assert get_number_of_decimal_places(Decimal("100")) == 0     # 0
    assert get_number_of_decimal_places(Decimal("0.00045")) == 5 # 5
