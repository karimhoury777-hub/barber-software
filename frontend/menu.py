import streamlit as st
import requests
import urllib.parse
import time
import os

API_URL = "https://salon-steve.onrender.com"
BARBER_PHONE = "96181750142" 

st.set_page_config(page_title="Salon Steve | Menu", layout="centered")

# --- CUSTOM CSS FOR B&W PREMIUM DESIGN ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .shop-title {
        text-align: center; 
        font-size: 4.5rem; 
        font-weight: 900; 
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 8px;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    
    .service-card {
        background-color: #111111;
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        border-left: 4px solid #888888;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    
    .service-name {
        margin: 0; 
        color: #FFFFFF; 
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .service-desc {
        margin: 5px 0 0 0; 
        color: #777777; 
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION & BRANDING ---
col1, col2 = st.columns([1, 2])
with col1:
    if os.path.exists("WhatsApp Image 2026-10-05 at 8.49.58 PM.jpeg"):
        st.image("WhatsApp Image 2026-10-05 at 8.49.58 PM.jpeg", use_column_width=True) # Barber pole & hours
with col2:
    st.write("") # Spacing
    st.markdown("<h1 class='shop-title'>SALON<br>STEVE</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888888; margin-top: 10px;'>PREMIUM GROOMING</h4>", unsafe_allow_html=True)

st.divider()

if os.path.exists("WhatsApp Image 2026-10-05 at 8.49.58 PM (1).jpeg"):
    st.image("WhatsApp Image 2026-10-05 at 8.49.58 PM (1).jpeg", use_column_width=True) # Smoky scissors

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 1. FETCH PROMOTIONS ---
active_promos = []
try:
    promo_res = requests.get(f"{API_URL}/promotions/")
    if promo_res.status_code == 200:
        active_promos = promo_res.json()
        if active_promos:
            banner_text = "  •  ".join(
                [f"🔥 {p['title']}: GET {p['discount_percentage']}% OFF! 🔥" for p in active_promos]
            )
            st.markdown(
                f"""
                <div style='background-color: #333333; color: white; padding: 15px; 
                            text-align: center; font-size: 1.2rem; font-weight: bold; 
                            border-radius: 8px; margin-bottom: 30px;'>
                    {banner_text}
                </div>
                """,
                unsafe_allow_html=True,
            )
except requests.exceptions.RequestException as exc:
    st.warning(f"Could not load promotions: {exc}")
                        