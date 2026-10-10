# backend/models.py
"""Domain models for The Indus Retreat."""
from datetime import date
from typing import Optional
from backend.exceptions import RoomUnavailableError, InvalidBookingDurationError

class BillableItem:
    """Base class for any billable amenity or product in the resort."""
    def __init__(self, item_id: int, name: str, price: float):
        self.item_id = item_id
        self.name = name
        self.price = float(price)

    def get_total(self, tax_rate: float = 0.13) -> float:
        """Calculates total price inclusive of PST (Default: 13%)."""
        return round(self.price * (1.0 + tax_rate), 2)


class FoodItem(BillableItem):
    """Subclass representing fine-dining culinary offerings."""
    def __init__(
        self,
        item_id: int,
        name: str,
        price: float,
        category: str,
        image_filename: str = "",
        is_available: bool = True
    ):
        super().__init__(item_id, name, price)
        self.category = category
        self.image_filename = image_filename
        self.is_available = is_available


class HotelSuite(BillableItem):
    """Subclass representing luxury resort accommodations."""
    def __init__(
        self,
        item_id: int,
        name: str,
        price: float,
        room_number: int,
        tier: str,
        status: str = "AVAILABLE",
        image_filename: str = ""
    ):
        super().__init__(item_id, name, price)
        self.room_number = room_number
        self.tier = tier
        self.status = status
        self.image_filename = image_filename
        self.guest_name: Optional[str] = None
        self.booking_dates: Optional[tuple] = None

    def book(self, guest_name: str, dates: tuple[date, date]) -> str:
        """Reserves the suite for a verified guest across valid dates."""
        if self.status != "AVAILABLE":
            raise RoomUnavailableError(f"Room {self.room_number} ({self.name}) is currently unavailable.")
        
        check_in, check_out = dates
        if check_out <= check_in:
            raise InvalidBookingDurationError("Check-out date must be strictly after check-in date.")

        self.status = "BOOKED"
        self.guest_name = guest_name
        self.booking_dates = dates
        return f"Successfully reserved Room {self.room_number} ({self.name}) for {guest_name}."

    def release(self) -> str:
        """Releases the suite back into the available pool."""
        self.status = "AVAILABLE"
        self.guest_name = None
        self.booking_dates = None
        return f"Room {self.room_number} ({self.name}) has been marked AVAILABLE."