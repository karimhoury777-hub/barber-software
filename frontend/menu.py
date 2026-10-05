import streamlit as st
import requests
import time

API_URL = "https://salon-steve.onrender.com"

st.set_page_config(page_title="Barber Menu", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; font-size: 5rem;'>PREMIUM CUTS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray; margin-bottom: 50px;'>Walk-ins Welcome</h3>", unsafe_allow_html=True)

# --- CUSTOM CSS FOR PREMIUM DESIGN ---
st.markdown("""
<style>
    /* Hide the Streamlit top menu and footer for a clean TV display */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style the main title */
    .shop-title {
        text-align: center; 
        font-size: 5rem; 
        font-weight: 900; 
        color: #d4af37; /* Gold accent */
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    /* Style the service cards */
    .service-card {
        background-color: #1a1c23;
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
        border-left: 5px solid #d4af37;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    
    .service-card:hover {
        transform: scale(1.02);
    }
    
    .service-name {
        margin: 0; 
        color: #FFFFFF; 
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    .service-desc {
        margin: 8px 0 0 0; 
        color: #a0aab5; 
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)



# --- 1. FETCH ACTIVE PROMOTIONS ---
active_promos = []
try:
    promo_res = requests.get(f"{API_URL}/promotions/")
    if promo_res.status_code == 200:
        active_promos = promo_res.json()
        if active_promos:
            banner_text = "  •  ".join([f"🔥 {p['title']}: GET {p['discount_percentage']}% OFF! 🔥" for p in active_promos])
            st.markdown(f"""
            <div style='background-color: #d32f2f; color: white; padding: 15px; 
                        text-align: center; font-size: 2rem; font-weight: bold; 
                        border-radius: 10px; margin-bottom: 30px; 
                        text-transform: uppercase; letter-spacing: 2px;'>
                {banner_text}
            </div>
            """, unsafe_allow_html=True)
except:
    pass # Fail silently if promos are unavailable

# --- 2. FETCH SERVICES AND APPLY MATH ---
try:
    response = requests.get(f"{API_URL}/services/")
    if response.status_code == 200:
        services = response.json()
        col1, col2 = st.columns(2)
        
        for index, svc in enumerate(services):
            target_col = col1 if index % 2 == 0 else col2
            
            # Check if this specific service has a discount applied
            best_discount = 0.0
            for p in active_promos:
                if p['service_id'] is None or p['service_id'] == svc['id']:
                    if p['discount_percentage'] > best_discount:
                        best_discount = p['discount_percentage']
            
            # Format the price HTML based on whether a sale is active
            original_price = svc['base_price']
            if best_discount > 0:
                discounted_price = original_price * (1 - (best_discount / 100))
                price_html = f"<span style='color: #d32f2f; text-decoration: line-through; font-size: 1.5rem; margin-right: 10px;'>${original_price:.2f}</span> <span style='color: #4CAF50;'>${discounted_price:.2f}</span>"
            else:
                price_html = f"<span style='color: #4CAF50;'>${original_price:.2f}</span>"

            # Render the final box
            with target_col:
                st.markdown(f"""
                <div class="service-card">
                    <div class="service-name">{svc['name']} <span style="float: right;">{price_html}</span></div>
                    <div class="service-desc">{svc['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
except requests.exceptions.ConnectionError:
    st.error("Menu currently offline.")

# Auto-refresh
time.sleep(30)
st.rerun()