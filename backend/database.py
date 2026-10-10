# backend/database.py
"""SQLite database management & self-healing seeder for The Indus Retreat."""
import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "indus_retreat.db"

def get_connection():
    """Provides a connection with standard timeout and row factory helper."""
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Builds required schema: menu, suites, and invoices."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                image_filename TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suites (
                room_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tier TEXT DEFAULT 'Deluxe',
                price_per_night REAL NOT NULL,
                status TEXT DEFAULT 'AVAILABLE',
                image_filename TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                contact TEXT NOT NULL,
                total_amount REAL NOT NULL,
                order_breakdown TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def seed_resort_data(force_reseed=False):
    """Seeds 70 authentic heritage dishes and 4 luxury suites."""
    setup_database()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        if force_reseed:
            cursor.execute("DELETE FROM menu")
            cursor.execute("DELETE FROM suites")
            conn.commit()

        # Check menu count: if empty or fewer than 70 items, seed/reseed
        cursor.execute("SELECT COUNT(*) FROM menu")
        current_count = cursor.fetchone()[0]
        if current_count < 70:
            if current_count > 0:
                cursor.execute("DELETE FROM menu")
                conn.commit()

            menu_items = [
                ("Thari Bajre Roti", "Heritage Bread", 400.0, "1.jpg"),
                ("Sindhi Biryani", "Main Course", 1800.0, "2.jpg"),
                ("Chicken Biryani", "Main Course", 1600.0, "3.jpg"),
                ("Mutton Biryani", "Main Course", 2200.0, "4.jpg"),
                ("Beef Nihari", "Main Course", 2400.0, "5.jpg"),
                ("Mutton Paya", "Main Course", 2100.0, "6.jpg"),
                ("Grilled Salmon", "Continental", 4500.0, "7.jpg"),
                ("Truffle Pasta", "Continental", 3200.0, "8.jpg"),
                ("Karela Pyaz Masala", "Vegetarian", 900.0, "9.jpg"),
                ("Roghani Naan", "Heritage Bread", 250.0, "10.jpg"),
                ("Roti Basket", "Heritage Bread", 600.0, "11.jpg"),
                ("Lahori Chargha", "Main Course", 2500.0, "12.jpg"),
                ("Authentic Beef Biryani", "Main Course", 2000.0, "13.jpg"),
                ("Palla Machhi", "Seafood", 3800.0, "14.jpg"),
                ("Sindhi Kadi Chawal", "Main Course", 1100.0, "15.jpg"),
                ("Sai Bhaji & Bhuga Chawal", "Main Course", 1250.0, "16.jpg"),
                ("Hyderabadi Rabri", "Dessert", 850.0, "17.jpg"),
                ("Bheh ji Bhaji", "Vegetarian", 950.0, "18.jpg"),
                ("Mutton Nalli Nihari", "Main Course", 2900.0, "19.jpg"),
                ("Shinwari Karahi", "Main Course", 3100.0, "20.jpg"),
                ("Beef Seekh Kebab", "Starter", 1400.0, "21.jpg"),
                ("Dum Pukht Lamb", "Main Course", 3500.0, "22.jpg"),
                ("Shahi Haleem", "Main Course", 1700.0, "23.jpg"),
                ("Chicken Tikka Boti", "Starter", 1300.0, "24.jpg"),
                ("Balochi Sajji", "Main Course", 3000.0, "25.jpg"),
                ("Lahori Fried Fish", "Seafood", 2200.0, "26.jpg"),
                ("Mutton Kunna", "Main Course", 2800.0, "27.jpg"),
                ("Chapli Kebab", "Starter", 1200.0, "28.jpg"),
                ("Murgh Malai Boti", "Starter", 1500.0, "29.jpg"),
                ("Chicken Handi", "Main Course", 2200.0, "30.jpg"),
                ("Tawa Chicken Fry", "Main Course", 2000.0, "31.jpg"),
                ("Pistachio Kulfi", "Dessert", 600.0, "32.jpg"),
                ("Mango Lassi", "Beverage", 500.0, "33.jpg"),
                ("Kashmiri Pink Chai", "Beverage", 350.0, "34.jpg"),
                ("Grilled Beef Steak", "Continental", 4200.0, "35.jpg"),
                ("Mutton Pepper Steak", "Continental", 4000.0, "36.jpg"),
                ("Wild Mushroom Risotto", "Continental", 3400.0, "37.jpg"),
                ("Mutton Yakhni Pulao", "Main Course", 2300.0, "38.jpg"),
                ("Aloo Gosht Shorba", "Main Course", 1700.0, "39.jpg"),
                ("Bhindi Do Pyaza", "Vegetarian", 950.0, "40.jpg"),
                ("Daal Chawal & Shami Kebab", "Main Course", 1150.0, "41.jpg"),
                ("Maghaz Masala", "Main Course", 2100.0, "42.jpg"),
                ("Lahori Murgh Chholay", "Main Course", 1600.0, "43.jpg"),
                ("Charsi Tikka", "Main Course", 2900.0, "44.jpg"),
                ("Palak Gosht", "Main Course", 2200.0, "45.jpg"),
                ("Chicken White Karahi", "Main Course", 2400.0, "46.jpg"),
                ("Keema Shimla Mirch", "Main Course", 1800.0, "47.jpg"),
                ("Lamb Rib Chops", "Continental", 4800.0, "48.jpg"),
                ("Mash ki Daal", "Vegetarian", 900.0, "49.jpg"),
                ("Prawn Karahi", "Seafood", 3600.0, "50.jpg"),
                ("Shahi Tukray", "Dessert", 850.0, "51.jpg"),
                ("Saffron Gulab Jamun", "Dessert", 700.0, "52.jpg"),
                ("Matka Kheer", "Dessert", 650.0, "53.jpg"),
                ("Sheer Khurma", "Dessert", 800.0, "54.jpg"),
                ("Gajar ka Halwa", "Dessert", 750.0, "55.jpg"),
                ("Authentic Daal Pakwan", "Starter", 600.0, "56.jpg"),
                ("Sindhi Koki with Curd", "Starter", 450.0, "57.jpg"),
                ("Traditional Breakfast Platter", "Main Course", 1200.0, "58.jpg"),
                ("Crisp Puri Paratha", "Heritage Bread", 150.0, "59.jpg"),
                ("Shahi Mutton Qorma", "Main Course", 2400.0, "60.jpg"),
                ("Chicken Manchurian & Rice", "Chinese", 1800.0, "61.jpg"),
                ("Beef Chilli Dry", "Chinese", 2100.0, "62.jpg"),
                ("Hot & Sour Soup", "Starter", 750.0, "63.jpg"),
                ("Fresh Kachumber Salad", "Salad", 300.0, "64.jpg"),
                ("Creamy Russian Salad", "Salad", 600.0, "65.jpg"),
                ("Cardamom Karak Chai", "Beverage", 350.0, "66.jpg"),
                ("Traditional Salted Lassi", "Beverage", 400.0, "67.jpg"),
                ("Rich Sweet Lassi", "Beverage", 450.0, "68.jpg"),
                ("Rooh Afza Lemonade", "Beverage", 250.0, "69.jpg"),
                ("Malai Boti Paratha Roll", "Starter", 800.0, "70.jpg")
            ]
            cursor.executemany(
                "INSERT INTO menu (name, category, price, image_filename) VALUES (?, ?, ?, ?)",
                menu_items
            )
            conn.commit()

        # Check suites
        cursor.execute("SELECT COUNT(*) FROM suites")
        if cursor.fetchone()[0] == 0:
            # --- SEEDING THE HOTEL SUITES (8 ROOMS) ---
            suites = [
                (101, "The Royal Ajrak Suite", 45000.0, "AVAILABLE", "room_royal.jpg"),
                (102, "The Indus Balcony Room", 25000.0, "AVAILABLE", "room_balcony.jpg"),
                (103, "The Courtyard Standard Room", 15000.0, "AVAILABLE", "room_standard.jpg"),
                (104, "The Heritage Family Suite", 35000.0, "AVAILABLE", "room_family.jpg"),
                (105, "The Indus Presidential Penthouse", 65000.0, "AVAILABLE", "room_penthouse.jpg"),
                (106, "The Mehran Riverside Suite", 30000.0, "AVAILABLE", "room_mehran.jpg"),
                (107, "The Sufi Heritage Suite", 40000.0, "AVAILABLE", "room_sufi.jpg"),
                (108, "The Royal Honeymoon Villa", 55000.0, "AVAILABLE", "room_honeymoon.jpg")
            ]
            cursor.executemany("INSERT INTO suites (room_number, name, price_per_night, status, image_filename) VALUES (?, ?, ?, ?, ?)", suites)
            conn.commit()

if __name__ == "__main__":
    setup_database()
    seed_resort_data(force_reseed=True)
    print("Database schema verified and data successfully seeded.")