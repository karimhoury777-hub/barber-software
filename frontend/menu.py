import streamlit as st
import requests
import urllib.parse
import os
import base64

API_URL = "https://salon-steve.onrender.com"
BARBER_PHONE = "96181750142" 

# Paths for images
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

st.set_page_config(page_title="Salon Steve | Premium Grooming", layout="centered")

# --- BACKGROUND IMAGE INJECTION ---
def add_bg_from_local():
    logo_path = None
    # Auto-detect if the logo is a jpeg, jpg, or png
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
                background-image: url(data:image/{"png"};base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

add_bg_from_local()

# --- CLASSY, ELEGANT CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Elegant Title */
    .shop-title {
        text-align: center; 
        font-size: 5rem; 
        font-weight: 300; 
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 12px;
        margin-bottom: 0px;
        font-family: 'Didot', 'Bodoni MT', 'Times New Roman', serif;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.9);
    }
    .shop-subtitle {
        text-align: center; 
        color: #B89768; /* Luxury Gold Accent */
        letter-spacing: 6px;
        font-size: 1.1rem;
        font-weight: 400;
        text-transform: uppercase;
        margin-top: -10px;
        margin-bottom: 40px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
    }
    
    /* Glassmorphism / Semi-transparent Service Cards */
    .service-card {
        background: rgba(15, 15, 15, 0.80);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        border: 1px solid rgba(184, 151, 104, 0.3);
        box-shadow: 0 8px 20px rgba(0,0,0,0.7);
    }
    
    .service-name {
        margin: 0; 
        color: #FFFFFF; 
        font-size: 1.4rem;
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    .service-desc {
        margin: 6px 0 0 0; 
        color: #A0A0A0; 
        font-size: 0.95rem;
        font-style: italic;
    }
    
    /* Category Headers */
    h2 {
        color: #B89768 !important;
        font-family: 'Didot', 'Bodoni MT', 'Times New Roman', serif;
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(184, 151, 104, 0.3);
        padding-bottom: 10px;
        margin-top: 30px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("<h1 class='shop-title'>SALON STEVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='shop-subtitle'>Premium Grooming & Style</p>", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 1. FETCH PROMOTIONS ---
active_promos = []
try:
    promo_res = requests.get(f"{API_URL}/promotions/")
    if promo_res.status_code == 200:
        active_promos = promo_res.json()
        if active_promos:
            banner_text = "  •  ".join([f"🔥 {p['title']}: GET {p['discount_percentage']}% OFF! 🔥" for p in active_promos])
            st.markdown(f"""
            <div style='background: rgba(184, 151, 104, 0.9); color: #000000; padding: 12px; 
                        text-align: center; font-size: 1.1rem; font-weight: bold; 
                        border-radius: 5px; margin-bottom: 30px; 
                        text-transform: uppercase; letter-spacing: 1px;'>
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

# --- 3. DISPLAY MENU BY CATEGORY ---
if services:
    categories = sorted(list(set([svc.get("category", "General") for svc in services])))
    
    for cat in categories:
        st.markdown(f"<h2>{cat}</h2>", unsafe_allow_html=True)
        cat_services = [s for s in services if s.get("category", "General") == cat and s['is_active']]
        
        for svc in cat_services:
            best_discount = 0.0
            for p in active_promos:
                if p['service_id'] is None or p['service_id'] == svc['id']:
                    if p['discount_percentage'] > best_discount:
                        best_discount = p['discount_percentage']
            
            original_price = svc['base_price']
            if best_discount > 0:
                discounted_price = original_price * (1 - (best_discount / 100))
                price_html = f"<span style='color: #888; text-decoration: line-through; font-size: 1.1rem; margin-right: 10px;'>${original_price:.2f}</span> <span style='color: #B89768;'>${discounted_price:.2f}</span>"
                display_price = discounted_price
            else:
                price_html = f"<span style='color: #B89768;'>${original_price:.2f}</span>"
                display_price = original_price

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="service-card">
                    <div class="service-name">{svc['name']} <span style="float: right;">{price_html}</span></div>
                    <div class="service-desc">{svc.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.write("")
                is_selected = st.checkbox("Select", key=f"chk_{svc['id']}")
                if is_selected:
                    st.session_state.cart[svc['name']] = display_price
                elif svc['name'] in st.session_state.cart:
                    del st.session_state.cart[svc['name']]

# --- GALLERY (STRUCTURED 2x2 GRID) ---
st.markdown("<h2>THE EXPERIENCE</h2>", unsafe_allow_html=True)
g_col1, g_col2 = st.columns(2)

img_pole = os.path.join(ASSETS_DIR, "pole.jpeg")
img_scissors = os.path.join(ASSETS_DIR, "scissors.jpeg")
img_clippers = os.path.join(ASSETS_DIR, "clippers.jpeg")
img_desk = os.path.join(ASSETS_DIR, "desk.jpeg")

with g_col1:
    if os.path.exists(img_pole): st.image(img_pole, use_column_width=True)
    if os.path.exists(img_clippers): st.image(img_clippers, use_column_width=True)
with g_col2:
    if os.path.exists(img_scissors): st.image(img_scissors, use_column_width=True)
    if os.path.exists(img_desk): st.image(img_desk, use_column_width=True)

# --- 4. CHECKOUT & WHATSAPP ---
st.markdown("<h2>🛒 CHECKOUT</h2>", unsafe_allow_html=True)

if st.session_state.cart:
    total_price = sum(st.session_state.cart.values())
    
    st.markdown("<div class='service-card'>", unsafe_allow_html=True)
    st.write("**Selected Services:**")
    for item, price in st.session_state.cart.items():
        st.write(f"- {item}: ${price:.2f}")
    st.markdown(f"<h3 style='color: #B89768; margin-top: 10px;'>Total: ${total_price:.2f}</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("Your Details")
    cust_name = st.text_input("Full Name")
    cust_phone = st.text_input("Phone Number")
    
    if st.button("Confirm Order & Send", use_container_width=True):
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
            
            st.success("Order saved! Click below to notify Salon Steve.")
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#B89768; color:black; padding:15px 32px; border:none; border-radius:5px; font-weight:bold; font-size:18px; cursor:pointer; width:100%; margin-top:10px; text-transform:uppercase; letter-spacing: 2px;">Send via WhatsApp</button></a>', unsafe_allow_html=True)
        else:
            st.error("Please enter your name and phone number.")
else:
    st.info("Your order is empty. Select a service above.")