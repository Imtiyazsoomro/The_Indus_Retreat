import streamlit as st
import sqlite3
import os
import json
from pathlib import Path
from datetime import datetime, date

# Robust Dynamic Path Resolver
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DB_FILE = BACKEND_DIR / "indus_retreat.db"
LOGO_FILE = CURRENT_DIR / "logo.png"

# ---------------------------------------------------------
# 1. LUXURY PAGE CONFIGURATION & ARCHITECTURE
# ---------------------------------------------------------
st.set_page_config(
    page_title="The Indus Retreat | Heritage Resort & Fine Dining",
    page_icon=str(LOGO_FILE) if LOGO_FILE.exists() else "🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def resolve_asset_path(filename: str) -> Path | None:
    """Safely locates asset files with case-insensitive and fuzzy fallback."""
    direct_path = CURRENT_DIR / filename
    if direct_path.exists():
        return direct_path
    
    # Fuzzy / case-insensitive search
    lower_target = filename.lower()
    for item in CURRENT_DIR.iterdir():
        if item.is_file() and item.name.lower() == lower_target:
            return item
        if lower_target in item.name.lower():
            return item
    return None

# Database Connection & Query Helpers
def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all(query: str, params: tuple = ()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def fetch_one(query: str, params: tuple = ()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

def execute_query(query: str, params: tuple = ()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

# Auto-heal database schema & seeding
def auto_heal_db():
    try:
        from backend.database import seed_resort_data
        seed_resort_data()
    except Exception:
        pass

auto_heal_db()

# ---------------------------------------------------------
# 2. STRICT LUXURY DESIGN SYSTEM (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Canvas styling */
    .stApp {
        background-color: #FDFBF7;
        color: #1F2937;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4, .brand-font {
        font-family: 'Playfair Display', 'Georgia', serif;
        color: #1F2937;
        letter-spacing: -0.01em;
    }

    h1 {
        font-size: 2.3rem !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-size: 1.75rem !important;
        color: #8E1616 !important;
        border-bottom: 2px solid #F3ECE1;
        padding-bottom: 8px;
        margin-top: 1rem;
        margin-bottom: 1.25rem;
    }

    /* Cards */
    .luxury-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .luxury-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(142, 22, 22, 0.08);
        border-color: #FCA5A5;
    }

    /* Price tags */
    .price-display {
        font-family: 'Cinzel', 'Playfair Display', serif;
        color: #8E1616;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 8px 0;
    }

    /* Badges */
    .badge-category {
        display: inline-block;
        background-color: #FEF2F2;
        color: #8E1616;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 10px;
        border-radius: 9999px;
        border: 1px solid #FECACA;
        margin-bottom: 8px;
    }

    .badge-tier-presidential {
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        border: 1px solid #FDE68A;
    }

    .badge-available {
        background-color: #ECFDF5;
        color: #059669;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        border: 1px solid #A7F3D0;
    }

    .badge-booked {
        background-color: #FEF2F2;
        color: #DC2626;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        border: 1px solid #FECACA;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #8E1616 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(142, 22, 22, 0.2) !important;
    }

    div.stButton > button:hover {
        background-color: #701111 !important;
        box-shadow: 0 4px 10px rgba(142, 22, 22, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* Subtle divider */
    hr {
        border: 0;
        height: 1px;
        background: #E5E7EB;
        margin: 1.5rem 0;
    }

    /* Tab Styling - explicit high contrast */
    button[data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 8px 16px !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #8E1616 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #8E1616 !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #8E1616 !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }

    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 0.9rem !important;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #1F2937 !important;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

# Synchronized Cart Calculations
cart_subtotal = sum(item['price'] for item in st.session_state.cart)
cart_pst = round(cart_subtotal * 0.13, 2)
cart_grand_total = round(cart_subtotal + cart_pst, 2)

# ---------------------------------------------------------
# 4. SIDEBAR CONCIERGE & NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    logo_path = resolve_asset_path("logo.png")
    if logo_path:
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center;'>THE INDUS RETREAT</h2>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; font-size: 1.15rem; font-weight: 700; color:#8E1616; letter-spacing:0.05em; margin-bottom: 12px; font-family: Playfair Display, serif;'>The Indus Retreat</div>", unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    navigation = st.radio(
        "RESORT CONCIERGE",
        [
            "The Heritage Menu",
            "Suite Reservations",
            "Our Story & Location",
            "Contact & Concierge",
            "Concierge Cart & Billing"
        ],
        index=0
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #6B7280; font-weight: 600; letter-spacing: 0.05em;">Active Folio</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #8E1616; margin: 4px 0;">{len(st.session_state.cart)} Items</div>
            <div style="font-size: 0.95rem; color: #1F2937;">Subtotal: <strong>PKR {cart_subtotal:,.2f}</strong></div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.cart:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Clear Folio", key="sidebar_clear_cart"):
            st.session_state.cart = []
            st.rerun()

    st.markdown("<hr style='margin-top: 24px; margin-bottom: 12px;'/>", unsafe_allow_html=True)
    
    # Hidden Admin Portal (Staff Login)
    with st.expander("🛡️ Staff & Admin Access", expanded=st.session_state.admin_authenticated):
        if not st.session_state.admin_authenticated:
            admin_code = st.text_input("Enter Access Code", type="password", key="admin_access_code_input")
            if admin_code:
                if admin_code == "IndusAdmin2026":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Access Code")
        else:
            st.success("Authorized: General Manager")
            if st.button("Logout of Admin Portal", key="admin_logout_btn"):
                st.session_state.admin_authenticated = False
                st.rerun()

# ---------------------------------------------------------
# BANNER HERO PRESENTATION
# ---------------------------------------------------------
banner_path = resolve_asset_path("Banner.png") or resolve_asset_path("banner.png")
if banner_path:
    st.image(str(banner_path), use_container_width=True)

# ---------------------------------------------------------
# CONDITIONAL ROUTING: ADMIN DASHBOARD VS PUBLIC GUEST SITE
# ---------------------------------------------------------
if st.session_state.admin_authenticated:
    st.markdown("<h1>Resort Executive Analytics</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.1rem;'>"
        "Real-time operational KPIs, revenue aggregates, room inventory, and recent transaction logs."
        "</p>",
        unsafe_allow_html=True
    )

    # Admin Control Bar with Quick Logout
    admin_bar_col1, admin_bar_col2 = st.columns([4, 1])
    with admin_bar_col1:
        st.info("🛡️ Authenticated Session: General Manager Executive Portal")
    with admin_bar_col2:
        if st.button("Logout to Guest Site", key="admin_top_logout_btn", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.rerun()

    # Aggregates from Invoices
    all_invoices = fetch_all("SELECT * FROM invoices ORDER BY invoice_id DESC")
    total_revenue = sum(inv['total_amount'] for inv in all_invoices)
    total_orders = len(all_invoices)

    # Suite Occupancy Metrics
    all_rooms = fetch_all("SELECT * FROM suites")
    total_rooms_count = len(all_rooms)
    occupied_count = len([r for r in all_rooms if r['status'] == "BOOKED"])
    occupancy_rate = (occupied_count / total_rooms_count * 100.0) if total_rooms_count > 0 else 0.0

    # Top Ordered Category Computation
    category_counts = {}
    for inv in all_invoices:
        try:
            items = json.loads(inv['order_breakdown'])
            for it in items:
                category_counts[it.get('type', 'Other')] = category_counts.get(it.get('type', 'Other'), 0) + 1
        except Exception:
            pass
    top_category = max(category_counts, key=category_counts.get) if category_counts else "None"

    # Executive Metric Display
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Revenue", f"PKR {total_revenue:,.2f}")
    m2.metric("Occupancy Rate", f"{occupancy_rate:.1f}%", f"{occupied_count}/{total_rooms_count} Suites")
    m3.metric("Folios Settled", f"{total_orders}")
    m4.metric("Top Demand Segment", f"{top_category}")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Live Suite Room Status
    st.markdown("### Luxury Suite Inventory")
    suite_data = [
        {
            "Room #": s['room_number'],
            "Suite Name": s['name'],
            "Tier": s.get('tier') or 'Executive',
            "Tariff (PKR)": f"{s['price_per_night']:,.2f}",
            "Current Status": s['status']
        }
        for s in all_rooms
    ]
    st.table(suite_data)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Recent Invoices Ledger
    st.markdown("### Settled Transaction Ledger")
    if all_invoices:
        invoice_table = [
            {
                "Invoice ID": f"INV-{inv['invoice_id']:04d}",
                "Guest Name": inv['guest_name'],
                "Contact": inv['contact'],
                "Settled Amount (PKR)": f"{inv['total_amount']:,.2f}",
                "Date & Time": inv['timestamp']
            }
            for inv in all_invoices[:20]
        ]
        st.table(invoice_table)
    else:
        st.info("No invoices settled in the current ledger period.")

# ---------------------------------------------------------
# PUBLIC PAGES DISPATCH
# ---------------------------------------------------------
elif navigation == "The Heritage Menu":
    st.markdown("<h1>The Heritage Dining Collection</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.1rem;'>"
        "Savor recipes curated across five millennia of Indus Valley gastronomy, prepared with traditional clay ovens and spices."
        "</p>",
        unsafe_allow_html=True
    )

    all_dishes = fetch_all("SELECT * FROM menu ORDER BY item_id ASC")

    if not all_dishes:
        st.warning("Menu is being refreshed by the Executive Chef. Please check back shortly.")
    else:
        # Dynamic categories with 'All' tab first
        raw_categories = sorted(list(set([dish['category'] for dish in all_dishes])))
        categories = ["All Specialties"] + raw_categories
        active_tabs = st.tabs(categories)

        for tab_idx, cat_name in enumerate(categories):
            with active_tabs[tab_idx]:
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                if cat_name == "All Specialties":
                    filtered_dishes = all_dishes
                else:
                    filtered_dishes = [d for d in all_dishes if d['category'] == cat_name]

                cols = st.columns(3)
                for index, dish in enumerate(filtered_dishes):
                    with cols[index % 3]:
                        st.markdown('<div class="luxury-card">', unsafe_allow_html=True)

                        img_file = dish['image_filename']
                        img_path = resolve_asset_path(img_file)
                        if img_path and img_path.exists():
                            st.image(str(img_path), use_container_width=True)
                        else:
                            st.markdown(
                                f"<div style='height: 190px; background-color: #F9FAFB; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 1px dashed #D1D5DB; color: #9CA3AF;'>{dish['name']}</div>",
                                unsafe_allow_html=True
                            )

                        st.markdown(f"<span class='badge-category'>{dish['category']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<h3 style='margin: 4px 0 6px 0; font-size: 1.25rem;'>{dish['name']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='price-display'>PKR {dish['price']:,.2f}</div>", unsafe_allow_html=True)

                        btn_key = f"add_dish_{dish['item_id']}_{tab_idx}"
                        if st.button("Add to Order", key=btn_key):
                            st.session_state.cart.append({
                                "id": dish['item_id'],
                                "name": dish['name'],
                                "price": float(dish['price']),
                                "type": "Food"
                            })
                            st.toast(f"Added {dish['name']} to your Folio!", icon="🍽️")
                            st.rerun()

                        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 2: SUITE RESERVATIONS
# ---------------------------------------------------------
elif navigation == "Suite Reservations":
    st.markdown("<h1>Royal Suites & Private Residences</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.1rem;'>"
        "Retreat to sanctuary-grade suites featuring handwoven  tapestries, Sindhi Ajrak motifs, and private river terraces."
        "</p>",
        unsafe_allow_html=True
    )

    suites = fetch_all("SELECT * FROM suites ORDER BY room_number ASC")

    amenities_lookup = {
        "Presidential": "Private Terrace • Personal Butler • Plunge Pool • Sindhi Ajrak Silk Linens • Panoramic Indus View",
        "Executive": "River Balcony • Espresso Bar • Woodcarvings • Marble Bath • Sunset Lounge Access",
        "Deluxe": "Courtyard Garden • King Bed • Hand-painted Frescos • High-Speed Satellite Wi-Fi",
        "Family": "Two Master Bedrooms • Private Veranda • Dedicated Dining Pavilion • Handcrafted Folk Décor"
    }

    for suite in suites:
        with st.container():
            st.markdown('<div class="luxury-card" style="padding: 24px;">', unsafe_allow_html=True)
            col_img, col_details = st.columns([1.2, 1.8], gap="large")

            with col_img:
                suite_img = resolve_asset_path(suite['image_filename'])
                if suite_img and suite_img.exists():
                    st.image(str(suite_img), use_container_width=True)
                else:
                    st.markdown(
                        "<div style='height: 240px; background-color: #F3F4F6; border-radius: 8px; display:flex; align-items:center; justify-content:center; color:#9CA3AF;'>Suite Imagery</div>",
                        unsafe_allow_html=True
                    )

            with col_details:
                suite_tier = suite.get('tier') or 'Executive'
                tier_badge = f"<span class='badge-tier-presidential'>{suite_tier} Tier</span>"
                status_badge = (
                    "<span class='badge-available'>AVAILABLE</span>"
                    if suite['status'] == "AVAILABLE"
                    else "<span class='badge-booked'>OCCUPIED</span>"
                )

                st.markdown(f"{tier_badge} &nbsp; {status_badge}", unsafe_allow_html=True)
                st.markdown(f"<h3 style='margin: 8px 0; font-size: 1.6rem;'>{suite['name']} (Suite {suite['room_number']})</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='price-display'>PKR {suite['price_per_night']:,.2f} <span style='font-size:0.9rem; color:#6B7280; font-family:Inter,sans-serif;'>/ Night (Excl. Tax)</span></div>", unsafe_allow_html=True)

                amenities = amenities_lookup.get(suite_tier, "Fine Amenities, Indus River Views & 24/7 Royal Concierge Service")
                st.markdown(f"<p style='font-size: 0.95rem; color: #4B5563; margin-bottom: 16px;'><strong>Exclusive Inclusions:</strong> {amenities}</p>", unsafe_allow_html=True)

                if suite['status'] == "AVAILABLE":
                    with st.expander(f"Reserve {suite['name']} (Room {suite['room_number']})", expanded=False):
                        with st.form(key=f"reserve_form_{suite['room_number']}"):
                            f_col1, f_col2 = st.columns(2)
                            with f_col1:
                                guest_name = st.text_input("Primary Guest Name", placeholder="e.g. Asad Ali Khan")
                                guest_cnic = st.text_input("CNIC / Passport Number", placeholder="42201-XXXXXXX-X")
                            with f_col2:
                                guest_phone = st.text_input("Mobile Contact", placeholder="+92 300 XXXXXXX")
                                today = date.today()
                                booking_dates = st.date_input(
                                    "Stay Dates (Check-in / Check-out)",
                                    value=(today, today)
                                )

                            submit_reservation = st.form_submit_button("Confirm & Add Suite to Folio")

                            if submit_reservation:
                                if not guest_name.strip() or not guest_phone.strip():
                                    st.error("Please enter complete guest credentials.")
                                elif isinstance(booking_dates, (tuple, list)) and len(booking_dates) == 2:
                                    ci, co = booking_dates
                                    nights = (co - ci).days
                                    if nights <= 0:
                                        nights = 1  # Standard minimum 1 night
                                    total_tariff = float(suite['price_per_night']) * nights

                                    # Update Room Status to BOOKED
                                    execute_query(
                                        "UPDATE suites SET status = 'BOOKED' WHERE room_number = ?",
                                        (suite['room_number'],)
                                    )

                                    st.session_state.cart.append({
                                        "id": suite['room_number'],
                                        "name": f"{suite['name']} ({nights} Night{'s' if nights > 1 else ''})",
                                        "price": total_tariff,
                                        "type": "Suite",
                                        "guest": guest_name,
                                        "dates": f"{ci.strftime('%b %d')} - {co.strftime('%b %d')}"
                                    })
                                    st.toast(f"Reserved {suite['name']} for {guest_name}!", icon="🏨")
                                    st.rerun()
                                else:
                                    st.error("Please select valid check-in and check-out dates.")
                else:
                    st.markdown("<p style='color: #DC2626; font-size: 0.95rem; font-weight: 500;'>Currently occupied by checked-in guest.</p>", unsafe_allow_html=True)
                    if st.button("Mark Available (Reception Desk)", key=f"rel_{suite['room_number']}"):
                        execute_query(
                            "UPDATE suites SET status = 'AVAILABLE' WHERE room_number = ?",
                            (suite['room_number'],)
                        )
                        st.success(f"Suite {suite['room_number']} is now open for bookings.")
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3: CONCIERGE CART & BILLING
# ---------------------------------------------------------
elif navigation == "Concierge Cart & Billing":
    st.markdown("<h1>Resort Folio & Settlement</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.1rem;'>"
        "Review itemized room charges, gastronomic selections, and settled resort transactions."
        "</p>",
        unsafe_allow_html=True
    )

    if not st.session_state.cart:
        st.markdown("""
            <div style="background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px; padding: 48px; text-align: center; margin-top: 1rem;">
                <div style="font-size: 3rem; margin-bottom: 12px;">🛎️</div>
                <h3 style="color: #1F2937 !important;">Your Folio is Empty</h3>
                <p style="color: #6B7280;">Explore The Heritage Menu or reserve a private suite to curate your retreat stay.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col_ledger, col_summary = st.columns([1.6, 1.0], gap="large")

        with col_ledger:
            st.markdown("### Itemized Charges")
            for idx, item in enumerate(st.session_state.cart):
                st.markdown(f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: {'#8E1616' if item['type']=='Food' else '#B45309'}; background: #FEF2F2; padding: 2px 8px; border-radius: 9999px;">
                                {item.get('type', 'Item')}
                            </span>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #1F2937; margin-top: 4px;">{item['name']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.15rem; font-weight: 700; color: #8E1616; font-family: Playfair Display, serif;">PKR {item['price']:,.2f}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("Remove", key=f"remove_item_{idx}"):
                    # If removing a suite, release it back to AVAILABLE in database
                    removed_item = st.session_state.cart[idx]
                    if removed_item.get('type') == 'Suite':
                        execute_query(
                            "UPDATE suites SET status = 'AVAILABLE' WHERE room_number = ?",
                            (removed_item['id'],)
                        )
                    st.session_state.cart.pop(idx)
                    st.rerun()

        with col_summary:
            st.markdown("### Settlement Summary")
            st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 1.05rem;">
                        <span style="color: #6B7280;">Subtotal</span>
                        <span style="font-weight: 600;">PKR {cart_subtotal:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 1.05rem;">
                        <span style="color: #6B7280;">Sindh Sales Tax (13% PST)</span>
                        <span style="font-weight: 600;">PKR {cart_pst:,.2f}</span>
                    </div>
                    <hr style="margin: 12px 0;"/>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 16px; font-size: 1.3rem;">
                        <span style="font-weight: 700; color: #1F2937;">Grand Total</span>
                        <span style="font-weight: 700; color: #8E1616; font-family: 'Playfair Display', serif;">PKR {cart_grand_total:,.2f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            with st.form(key="checkout_ledger_form"):
                st.markdown("#### Guest Billing Information")
                c_name = st.text_input("Guest Billing Name", placeholder="e.g. Asad Ali Khan")
                c_phone = st.text_input("Guest Contact Phone / Email", placeholder="+92 300 1234567")
                confirm_checkout = st.form_submit_button("Settle Folio & Generate Invoice")

                if confirm_checkout:
                    if not c_name.strip() or not c_phone.strip():
                        st.error("Please supply valid guest contact information.")
                    else:
                        breakdown_json = json.dumps(st.session_state.cart)
                        invoice_id = execute_query(
                            """
                            INSERT INTO invoices (guest_name, contact, total_amount, order_breakdown)
                            VALUES (?, ?, ?, ?)
                            """,
                            (c_name.strip(), c_phone.strip(), cart_grand_total, breakdown_json)
                        )
                        st.session_state.cart = []
                        st.success(f"Invoice #{invoice_id:04d} successfully processed and recorded in resort ledger!")
                        st.balloons()
                        st.rerun()

# ---------------------------------------------------------
# MODULE 4: OUR STORY & LOCATION
# ---------------------------------------------------------
elif navigation == "Our Story & Location":
    st.markdown("<h1>Our Story & Provenance</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.15rem; font-style: italic; margin-bottom: 24px;'>"
        "“Where five thousand years of civilization embrace the quiet majesty of the Indus waters.”"
        "</p>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------------
    # Section 1: The Whispering Waters of the Indus
    # Layout 1: Image on Left (indus_river.jpg), Text on Right
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        img_p1 = resolve_asset_path("indus_river.jpg")
        if img_p1 and os.path.exists(str(img_p1)):
            st.image(str(img_p1), caption="The Whispering Waters of the Indus River", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">The Whispering Waters of the Indus</span>
            <h3 style="color: #8E1616; margin-top: 6px;">The Lifeline of Civilization</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                Nestled directly upon the serene banks of the majestic Indus River (Mehran), The Indus Retreat offers a window into history. The Indus is not merely a river; it is the soul of Sindh. Guests awaken to the tranquil melody of gentle ripples and mesmerising golden sunsets reflecting off the waters that have nurtured empires, poets, and mystics for thousands of years.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 2: Cradle of the Indus Valley
    # Layout 2: Text on Left, Image on Right (mohenjo.jpg)
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">Cradle of the Indus Valley</span>
            <h3 style="color: #8E1616; margin-top: 6px;">The Legacy of Mohenjo-Daro</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                Inspired by the 5,000-year-old legacy of Mohenjo-Daro, our retreat embodies the advanced urban planning and peaceful prosperity of the ancient Indus civilization. The meticulous baked-brick architecture and grid-like precision of antiquity are seamlessly integrated into the structural philosophy of our modern sanctuary, bridging millennia of human ingenuity.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        img_p2 = resolve_asset_path("mohenjo.jpg")
        if img_p2 and os.path.exists(str(img_p2)):
            st.image(str(img_p2), caption="The Ancient Citadel of Mohenjo-Daro", use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 3: Echoes of Neroon Kot
    # Layout 1: Image on Left (qillo.jpg), Text on Right
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        img_p3 = resolve_asset_path("qillo.jpg")
        if img_p3 and os.path.exists(str(img_p3)):
            st.image(str(img_p3), caption="Pacco Qillo — The Historic Fortress of Hyderabad", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">Echoes of Neroon Kot</span>
            <h3 style="color: #8E1616; margin-top: 6px;">The Fortress of Hyderabad</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                Hyderabad, historically known as <em>Neroon Kot</em>, has long been the pulsating heart of Sindhi culture and culinary prestige. Guarding the city's rich history is the formidable Pacco Qillo (The Fort of Hyderabad), established in 1768 by Mian Ghulam Shah Kalhoro. Our resort echoes the historic valor and regal court traditions of this grand era.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 4: Splendor of the Amirs
    # Layout 2: Text on Left, Image on Right (tomb.jpg)
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">Splendor of the Amirs</span>
            <h3 style="color: #8E1616; margin-top: 6px;">Architectural Mastery</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                From the vibrant blue glaze of authentic Hala tiles to the geometric mastery of hand-woven Ajrak, our interiors pay homage to the magnificent tombs of the Kalhora and Talpur dynasties. Every corridor and courtyard is designed to reflect the Sufi serenity, intricate craftsmanship, and artistic brilliance of the lower Indus Valley.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        img_p4 = resolve_asset_path("tomb.jpg")
        if img_p4 and os.path.exists(str(img_p4)):
            st.image(str(img_p4), caption="Architectural Splendor of the Historical Tombs", use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 5: The City of Windcatchers
    # Layout 1: Image on Left (windcatcher.jpg), Text on Right
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        img_p5 = resolve_asset_path("windcatcher.jpg")
        if img_p5 and os.path.exists(str(img_p5)):
            st.image(str(img_p5), caption="Windcatchers (Manghan) of Hyderabad", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">The City of Windcatchers</span>
            <h3 style="color: #8E1616; margin-top: 6px;">The Breeze of Manghan</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                For centuries, Hyderabad has been celebrated as the <em>City of Windcatchers (Manghan)</em>. The city’s ancient skyline was defined by these architectural marvels designed to capture the refreshing breezes wafting off the Indus River. Our open-air riverfront verandas harness this exact natural comfort, offering timeless serenity without reliance on modern machinery.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 6: A Tapestry of Eras
    # Layout 2: Text on Left, Image on Right (navalrai.jpg)
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown("""
        <div class="luxury-card" style="height: 100%;">
            <span class="badge-category">A Tapestry of Eras</span>
            <h3 style="color: #8E1616; margin-top: 6px;">The Colonial & Cultural Crossroads</h3>
            <p style="color: #374151; line-height: 1.8; font-size: 1rem;">
                The iconic Navalrai Market Clock Tower stands as a testament to the city's overlapping eras of history, where colonial-era masonry met traditional Sindhi commerce. The Indus Retreat celebrates this rich tapestry, serving as a cultural crossroads where international luxury meets the authentic, warm hospitality that Sindh has offered travelers for centuries.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        img_p6 = resolve_asset_path("navalrai.jpg")
        if img_p6 and os.path.exists(str(img_p6)):
            st.image(str(img_p6), caption="Navalrai Market Clock Tower, Hyderabad", use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 7: Visionary Leadership
    # Layout: Centered text (No columns, no image)
    # ---------------------------------------------------------
    st.markdown("""
    <div class="luxury-card" style="border-left: 5px solid #8E1616; padding: 28px; text-align: center; max-width: 900px; margin: 0 auto;">
        <span class="badge-category">Visionary Leadership</span>
        <h2 style="color: #8E1616; margin-top: 8px; margin-bottom: 12px; border-bottom: none; text-align: center;">Meet the Founder: Imtiyaz Soomro</h2>
        <p style="color: #374151; line-height: 1.9; font-size: 1.05rem; max-width: 780px; margin: 0 auto;">
            Imtiyaz Soomro is the founder and developer of The Indus Retreat, conceptualizing this sanctuary to showcase the grandeur of indigenous Sindhi heritage on the world stage, blending modern technological precision with century-old culinary and royal hospitality traditions.
        </p>
        <div style="display: flex; justify-content: center; gap: 24px; margin-top: 18px; font-size: 0.92rem; color: #6B7280;">
            <div>📍 <em>Hyderabad, Sindh</em></div>
            <div>🏛️ <em>Heritage Preservation</em></div>
            <div>✨ <em>Hospitality Visionary</em></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 8: The Culinary Masters
    # ---------------------------------------------------------
    st.markdown("### The Culinary Masters")

    col1, col2 = st.columns(2)
    with col1:
        img_sindhi = resolve_asset_path("chef_sindhi.jpg")
        if img_sindhi and os.path.exists(str(img_sindhi)):
            st.image(str(img_sindhi), use_container_width=True)
        st.subheader("Ustad Fazal - Heritage Chef")
        st.write(
            "Ustad Fazal carries deep ancestral roots in Sindh, having spent decades mastering "
            "the ancient clay ovens (tandoors) and indigenous spices of the Indus Valley. "
            "His authentic culinary craft preserves centuries-old traditional recipes and royal flavors."
        )

    with col2:
        img_dubai = resolve_asset_path("chef_dubai.jpg")
        if img_dubai and os.path.exists(str(img_dubai)):
            st.image(str(img_dubai), use_container_width=True)
        st.subheader("Chef Tariq - Executive Chef")
        st.write(
            "Chef Tariq brings over 10 years of culinary leadership in luxury 5-star hotels in Dubai. "
            "Renowned for precision and modern creativity, he infuses Michelin-star plating techniques "
            "and international gourmet fusion into every Indus signature dish."
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Section 9: Culinary Artistry Video (The Art of Plating)
    # ---------------------------------------------------------
    st.markdown("### The Art of Plating")

    # Safe video path resolver checking for local video files (plating.mp4 / plated.mp4)
    video_path = None
    for candidate_name in ["plated.mp4", "plating.mp4"]:
        resolved = resolve_asset_path(candidate_name)
        if resolved and os.path.exists(str(resolved)):
            video_path = str(resolved)
            break
        direct_candidate = os.path.join("frontend", candidate_name)
        if os.path.exists(direct_candidate):
            video_path = direct_candidate
            break

    if video_path and os.path.exists(video_path):
        st.video(video_path)
    else:
        st.video("https://www.youtube.com/watch?v=YOUR_PLACEHOLDER")


# ---------------------------------------------------------
# MODULE 5: CONTACT & CONCIERGE
# ---------------------------------------------------------
elif navigation == "Contact & Concierge":
    st.markdown("<h1>Contact & Royal Concierge Desk</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #4B5563; font-size: 1.1rem;'>"
        "Our dedicated concierge team is at your beck and call 24 hours a day to orchestrate every detail of your stay."
        "</p>",
        unsafe_allow_html=True
    )

    col_info, col_form = st.columns([5, 6])

    with col_info:
        st.markdown("""
        <div class="luxury-card">
            <span class="badge-category">Direct Connections</span>
            <h3 style="color: #8E1616; margin-top: 8px;">Concierge Information</h3>
            <p style="color: #4B5563; font-size: 0.95rem; margin-bottom: 20px;">
                Whether you wish to arrange a private riverboat excursion, customize a bespoke royal banquet, 
                or inquire about presidential suite amenities, we are delighted to assist.
            </p>
            <div style="margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1F2937; font-size: 0.95rem;">📍 Resort Address</div>
                <div style="color: #4B5563; font-size: 0.92rem;">The Indus River Bank, Near Giddu Barrage, Hyderabad, Sindh, Pakistan</div>
            </div>
            <div style="margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1F2937; font-size: 0.95rem;">📞 Direct Concierge Helpline</div>
                <div style="color: #4B5563; font-size: 0.92rem;">+92 22 111 222 333 &nbsp;|&nbsp; +92 22 277 8899</div>
            </div>
            <div style="margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1F2937; font-size: 0.95rem;">✉️ Official Inquiries</div>
                <div style="color: #4B5563; font-size: 0.92rem;"><a href="mailto:info@indusretreat.com.pk" style="color:#8E1616; text-decoration: none; font-weight:600;">info@indusretreat.com.pk</a></div>
            </div>
            <div style="margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1F2937; font-size: 0.95rem;">🕒 Service Hours</div>
                <div style="color: #4B5563; font-size: 0.92rem;">Concierge Desk: 24 Hours / 7 Days a Week</div>
            </div>
            <div style="background-color: #FEF2F2; border-radius: 6px; padding: 12px; border: 1px dashed #FCA5A5; margin-top: 12px;">
                <div style="font-size: 0.85rem; color: #8E1616; font-weight: 600;">Valet & Helicopter Landing Available</div>
                <div style="font-size: 0.8rem; color: #7F1D1D;">Complimentary chauffeured airport transfers from Karachi and Hyderabad for Presidential Suite patrons.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("""
        <div style="margin-bottom: 14px;">
            <h3 style="color: #1F2937; margin-bottom: 4px;">Message the Concierge</h3>
            <p style="color: #6B7280; font-size: 0.9rem;">Submit your inquiry below and our Lead Concierge will respond within minutes.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="concierge_contact_form", clear_on_submit=True):
            guest_full_name = st.text_input("Guest Full Name", placeholder="e.g. Tariq Al-Mansoor")
            guest_email = st.text_input("Email Address", placeholder="e.g. guest@indusretreat.com.pk")
            contact_subject = st.selectbox(
                "Inquiry Category",
                ["Suite Reservation Inquiry", "Private Dining & Banquet", "Cultural River Tour", "Feedback & Compliment", "General Inquiry"]
            )
            guest_message = st.text_area("Your Message / Special Requests", placeholder="Describe your preferred arrangements, dates, or specific dietary requests...", height=130)

            submitted = st.form_submit_button("Transmit Message to Concierge", use_container_width=True)

            if submitted:
                if not guest_full_name.strip():
                    st.error("Please provide your full name so our concierge may address you properly.")
                elif not guest_email.strip() or "@" not in guest_email:
                    st.error("Please provide a valid email address for our correspondence.")
                elif not guest_message.strip():
                    st.error("Please enter a brief message for the concierge desk.")
                else:
                    st.success(f"Thank you, {guest_full_name.strip()}. Your message regarding '{contact_subject}' has been dispatched to the Concierge. We will attend to your request promptly.")
                    st.toast("Message received by the Concierge desk!", icon="✨")
