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


def test_get_number_of_decimal_places_extended():
    """Extended tests for decimal places"""
    # Integers
    assert get_number_of_decimal_places(Decimal("0")) == 0
    assert get_number_of_decimal_places(Decimal("100")) == 0
    assert get_number_of_decimal_places(Decimal("-5")) == 0

    # Decimals
    assert get_number_of_decimal_places(Decimal("0.1")) == 1
    assert get_number_of_decimal_places(Decimal("0.12")) == 2
    assert get_number_of_decimal_places(Decimal("0.123")) == 3

    # Trailing zeros (normalized away)
    assert get_number_of_decimal_places(Decimal("1.0")) == 0
    assert get_number_of_decimal_places(Decimal("1.10")) == 1
    assert get_number_of_decimal_places(Decimal("1.100")) == 1

    # Small numbers
    assert get_number_of_decimal_places(Decimal("0.0001")) == 4

    # Large numbers
    assert get_number_of_decimal_places(Decimal("12345.6789")) == 4
