"""
Common utilities.
"""

from decimal import Decimal
from typing import Union


def get_number_of_decimal_places(number: Decimal) -> int:
    """
    Get the number of decimal places in a Decimal number.
    
    Args:
        number: A Decimal number
        
    Returns:
        The number of decimal places in the number (excluding trailing zeros)
    """
    # Normalize the decimal to remove trailing zeros
    normalized = number.normalize()
    
    # Get the exponent from the tuple representation
    # The exponent is negative of the number of decimal places
    # Handle special cases where exponent might be a string ('n', 'N', 'F')
    exponent = normalized.as_tuple().exponent
    
    # For special values (NaN, Infinity), return 0
    if isinstance(exponent, str):
        return 0
    
    # For regular numbers, if exponent is negative, return its absolute value
    # If exponent is positive or zero, return 0 (no decimal places)
    if exponent < 0:
        return -exponent
    else:
        return 0
