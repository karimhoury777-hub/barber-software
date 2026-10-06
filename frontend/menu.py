import streamlit as st
import requests
import urllib.parse
import os
import base64

API_URL = "https://salon-steve.onrender.com"
BARBER_PHONE = "96181750142" 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

st.set_page_config(page_title="Salon Steve | Exclusive Grooming", layout="wide", initial_sidebar_state="collapsed")

def add_bg_from_local():
    logo_path = None
    for ext in ["jpeg", "jpg", "png", "webp"]:
        temp_path = os.path.join(ASSETS_DIR, f"logo.{ext}")
        if os.path.exists(temp_path):
            logo_path = temp_path
            break
    
    if logo_path:
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(10, 10, 10, 0.88), rgba(15, 15, 15, 0.98)), url(data:image/{"png"};base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

add_bg_from_local()

# --- HIGH-END CSS INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }
    
    .hero-title {
        text-align: center; 
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem; 
        font-weight: 600; 
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 15px;
        margin-bottom: 0px;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.8);
    }
    .hero-subtitle {
        text-align: center; 
        font-family: 'Montserrat', sans-serif;
        color: #D4AF37; 
        letter-spacing: 8px;
        font-size: 1.2rem;
        font-weight: 300;
        text-transform: uppercase;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 400;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
        margin-top: 50px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .section-title::before, .section-title::after {
        content: "";
        flex: 1;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        margin: 0 20px;
    }

    /* ---------------------------------------------------
       MAGIC: TRANSFORMING NATIVE BUTTONS INTO LUXURY CARDS 
       --------------------------------------------------- */
    
    /* Secondary Buttons (The Service Cards) */
    button[kind="secondary"] {
        background: rgba(20, 20, 20, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        border-left: 3px solid #D4AF37 !important;
        color: #FFFFFF !important;
        padding: 25px !important;
        min-height: 120px !important;
        height: 100% !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
        border-radius: 4px !important;
    }
    button[kind="secondary"]:hover {
        transform: translateY(-5px) !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        border-left: 3px solid #D4AF37 !important;
        background: rgba(30, 30, 30, 0.8) !important;
        box-shadow: 0 15px 40px rgba(212, 175, 55, 0.1) !important;
    }
    /* Force left alignment on text inside the button */
    button[kind="secondary"] * {
        text-align: left !important;
        font-family: 'Montserrat', sans-serif !important;
        white-space: pre-wrap !important;
    }

    /* Primary Button (The Checkout Button) */
    button[kind="primary"] {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 2px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #F3E5AB !important;
        transform: scale(1.02) !important;
    }

    /* 📱 RESPONSIVE MOBILE ADJUSTMENTS */
    @media (max-width: 768px) {
        .block-container { padding-top: 1rem !important; }
        .hero-title { font-size: 3.2rem !important; letter-spacing: 6px !important; line-height: 1.1 !important; margin-bottom: 10px;}
        .hero-subtitle { font-size: 0.85rem !important; letter-spacing: 4px !important; margin-top: 0px; }
        .section-title { font-size: 1.5rem !important; margin-top: 30px !important; margin-bottom: 20px !important; }
        .section-title::before, .section-title::after { margin: 0 10px; }
        button[kind="secondary"] { padding: 15px !important; min-height: 90px !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("<h1 class='hero-title'>SALON STEVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>The Art of Gentlemen's Grooming</p>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <a href="https://www.instagram.com/majd_houry?stkn=dDgxaG83Zzh2eXhm" target="_blank" 
       style="display: inline-block; padding: 10px 30px; border: 1px solid #D4AF37; color: #D4AF37; text-decoration: none; font-family: 'Montserrat', sans-serif; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; border-radius: 2px; transition: all 0.3s;">
       ✦ Follow on Instagram ✦
    </a>
</div>
""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 1. FETCH PROMOTIONS ---
active_promos = []
try:
    promo_res = requests.get(f"{API_URL}/promotions/")
    if promo_res.status_code == 200:
        active_promos = promo_res.json()
        if active_promos:
            banner_text = "   |   ".join([f"✦ {p['title']}: {p['discount_percentage']}% OFF ✦" for p in active_promos])
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.1), transparent); 
                        border-top: 1px solid rgba(212, 175, 55, 0.3); border-bottom: 1px solid rgba(212, 175, 55, 0.3);
                        color: #D4AF37; padding: 15px; text-align: center; font-family: "Montserrat", sans-serif; 
                        font-size: 0.9rem; font-weight: 400; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 3px;'>
                {banner_text}
            </div>
            """, unsafe_allow_html=True)
except:
    pass

# --- 2. FETCH SERVICES ---
try:
    response = requests.get(f"{API_URL}/services/")
    services = response.json() if response.status_code == 200 else []
except:
    services = []
    st.error("Cannot connect to server.")

# --- 3. DYNAMIC 2-COLUMN MENU (CLICKABLE CARDS) ---
if services:
    categories = sorted(list(set([svc.get("category", "General") for svc in services])))
    
    for cat in categories:
        st.markdown(f"<div class='section-title'>{cat}</div>", unsafe_allow_html=True)
        cat_services = [s for s in services if s.get("category", "General") == cat and s['is_active']]
        
        for i in range(0, len(cat_services), 2):
            cols = st.columns(2)
            
            with cols[0]:
                svc = cat_services[i]
                best_discount = max([p['discount_percentage'] for p in active_promos if p['service_id'] in (None, svc['id'])] + [0.0])
                display_price = svc['base_price'] * (1 - (best_discount / 100))
                
                in_cart = svc['name'] in st.session_state.cart
                desc = svc.get('description', '')
                
                # Format text inside the button based on selection
                if in_cart:
                    btn_label = f"✔️ {svc['name']} — ${display_price:.2f}\n[ADDED TO CART]"
                else:
                    btn_label = f"➕ {svc['name']} — ${display_price:.2f}\n{desc}"
                
                # The button acts as the entire card now
                if st.button(btn_label, key=f"btn_{svc['id']}", use_container_width=True):
                    if in_cart:
                        del st.session_state.cart[svc['name']]
                    else:
                        st.session_state.cart[svc['name']] = display_price
                    st.rerun()

            if i + 1 < len(cat_services):
                with cols[1]:
                    svc = cat_services[i+1]
                    best_discount = max([p['discount_percentage'] for p in active_promos if p['service_id'] in (None, svc['id'])] + [0.0])
                    display_price = svc['base_price'] * (1 - (best_discount / 100))
                    
                    in_cart = svc['name'] in st.session_state.cart
                    desc = svc.get('description', '')
                    
                    if in_cart:
                        btn_label = f"✔️ {svc['name']} — ${display_price:.2f}\n[ADDED TO CART]"
                    else:
                        btn_label = f"➕ {svc['name']} — ${display_price:.2f}\n{desc}"
                    
                    if st.button(btn_label, key=f"btn_{svc['id']}", use_container_width=True):
                        if in_cart:
                            del st.session_state.cart[svc['name']]
                        else:
                            st.session_state.cart[svc['name']] = display_price
                        st.rerun()

# --- PREMIUM MASONRY GALLERY (FIXED IMAGE WARNINGS) ---
st.markdown("<div class='section-title'>THE EXPERIENCE</div>", unsafe_allow_html=True)
g_col1, g_col2, g_col3, g_col4 = st.columns(4)

img_pole = os.path.join(ASSETS_DIR, "pole.jpeg")
img_scissors = os.path.join(ASSETS_DIR, "scissors.jpeg")
img_clippers = os.path.join(ASSETS_DIR, "clippers.jpeg")
img_desk = os.path.join(ASSETS_DIR, "desk.jpeg")

with g_col1:
    if os.path.exists(img_pole): st.image(img_pole, use_container_width=True)
with g_col2:
    if os.path.exists(img_clippers): st.image(img_clippers, use_container_width=True)
with g_col3:
    if os.path.exists(img_scissors): st.image(img_scissors, use_container_width=True)
with g_col4:
    if os.path.exists(img_desk): st.image(img_desk, use_container_width=True)

# --- 4. LUXURY CHECKOUT & WHATSAPP ---
st.markdown("<div class='section-title'>RESERVE</div>", unsafe_allow_html=True)

_, checkout_col, _ = st.columns([1, 2, 1])

with checkout_col:
    if st.session_state.cart:
        total_price = sum(st.session_state.cart.values())
        
        st.markdown("""
        <div style="background: rgba(20, 20, 20, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(212, 175, 55, 0.15); border-radius: 4px; padding: 25px; margin-bottom: 20px;">
            <h3 style='color: #fff; font-family: Playfair Display; margin-top:0;'>Selected Services</h3>
        """, unsafe_allow_html=True)
        
        for item, price in st.session_state.cart.items():
            st.markdown(f"<div style='display: flex; justify-content: space-between; font-family: Montserrat; color: #bbb;'><span>{item}</span><span>${price:.2f}</span></div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; border-top: 1px solid rgba(212,175,55,0.3); margin-top: 15px; padding-top: 15px;'>
            <span style='font-family: Montserrat; color: #fff; font-weight: 600; font-size: 1.2rem;'>TOTAL</span>
            <span style='font-family: Montserrat; color: #D4AF37; font-weight: 600; font-size: 1.2rem;'>${total_price:.2f}</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        cust_name = st.text_input("Full Name", placeholder="e.g. John Doe")
        cust_phone = st.text_input("Phone Number", placeholder="e.g. +961...")
        st.write("")
        
        # Using type="primary" tells our CSS to style this as the gold checkout button
        if st.button("Confirm Order", type="primary", use_container_width=True):
            if cust_name and cust_phone:
                selected_items_str = ", ".join(st.session_state.cart.keys())
                payload = {
                    "customer_name": cust_name,
                    "customer_phone": cust_phone,
                    "services_ordered": selected_items_str,
                    "total_price": total_price
                }
                requests.post(f"{API_URL}/orders/", json=payload)
                
                msg = f"💈 *NEW ORDER* 💈\n\n"
                msg += f"*Client:* {cust_name}\n"
                msg += f"*Phone:* {cust_phone}\n\n"
                msg += f"*Services Requested:*\n"
                for item, price in st.session_state.cart.items():
                    msg += f"- {item} (${price:.2f})\n"
                msg += f"\n*Total Due:* ${total_price:.2f}"
                
                encoded_msg = urllib.parse.quote(msg)
                whatsapp_url = f"https://wa.me/{BARBER_PHONE}?text={encoded_msg}"
                
                st.success("Request received. Proceed to WhatsApp to finalize your booking.")
                st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #D4AF37; color: #000; text-align: center; padding: 15px; border-radius: 2px; font-family: Montserrat; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; transition: 0.3s; box-shadow: 0 4px 15px rgba(212,175,55,0.3);">
                        Finalize via WhatsApp
                    </div>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.error("Client details are required to proceed.")
    else:
        st.markdown("<p style='text-align: center; color: #888; font-family: Montserrat;'>Your itinerary is currently empty. Please select a service from the menu above.</p>", unsafe_allow_html=True)