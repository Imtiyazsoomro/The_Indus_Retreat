# The Indus Retreat: Heritage Resort & Fine Dining Engine

An elite 5-star heritage resort web application celebrating Sindhi and Thari gastronomy and luxury hospitality, powered by Python, SQLite, and Streamlit.

---

## Architecture Overview

```text
Indus_hotel/
├── backend/
│   ├── __init__.py
│   ├── exceptions.py       # Domain-specific resort exceptions
│   ├── models.py           # OOP models (BillableItem, FoodItem, HotelSuite)
│   ├── database.py         # Self-healing SQLite schema & seeder
│   └── indus_retreat.db    # Auto-generated SQLite database
├── frontend/
│   ├── app.py              # Luxury Streamlit application
│   ├── Banner.png          # Hero header visual
│   ├── logo.png            # Heritage resort logo
│   ├── 1.jpg - 70.jpg      # 70 Fine dining culinary assets
│   └── room_*.png          # Luxury suite visuals
├── requirements.txt
└── README.md
```

---

## Key Features

1. **The Heritage Dining Collection:**
   - 70 authentic Sindhi, Thari, and Continental culinary specialties.
   - Interactive category tabs (Main Course, Heritage Bread, Starter, Seafood, Vegetarian, Continental, Dessert, Beverage).
   - High-fidelity visual cards with instant "Add to Order" folio integration.

2. **Royal Suites & Private Residences:**
   - 4 elite luxury suite tiers (Presidential, Executive, Deluxe, Family Residence).
   - Real-time room availability status and instant guest reservation booking engine.

3. **Concierge Folio & Billing:**
   - Itemized folio charges with live item removal.
   - Transparent provincial sales tax calculation (13% Sindh Sales Tax / PST).
   - Guest invoice generation committed to database ledger.

4. **General Manager Analytics:**
   - Real-time KPI metrics: Gross Revenue, Occupancy Rate, Settled Folios, and Top Demand Segment.
   - Native Python table representation for room inventory and invoice transaction records.

---

## Quick Start

### 1. Initialize Database
```bash
python backend/database.py
```

### 2. Launch the Web Application
```bash
streamlit run frontend/app.py
```

Visit `http://localhost:8501` in your browser.
