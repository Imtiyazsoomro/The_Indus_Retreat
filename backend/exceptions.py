# backend/exceptions.py
"""Domain exceptions for The Indus Retreat."""

class ResortError(Exception):
    """Base error for The Indus Retreat domain logic."""
    pass

class RoomUnavailableError(ResortError):
    """Raised when an attempt is made to reserve a suite that is not available."""
    pass

class ItemOutOfStockError(ResortError):
    """Raised when an ordered food item is out of stock."""
    pass

class EmptyCartCheckoutError(ResortError):
    """Raised when checkout is attempted with an empty cart."""
    pass

class InvalidBookingDurationError(ResortError):
    """Raised when booking check-out date is not strictly after check-in date."""
    pass
