import streamlit as st
import requests
import urllib.parse
import time

API_URL = "https://salon-steve.onrender.com"
BARBER_PHONE = "96181750142" 

st.set_page_config(page_title="Barber Menu & Booking", layout="centered")

# --- CUSTOM CSS FOR PREMIUM DESIGN ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .shop-title {
        text-align: center; 
        font-size: 4rem; 
        font-weight: 900; 
        color: #d4af37;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .service-card {
        background-color: #1a1c23;
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 15px; 
        border-left: 5px solid #d4af37;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .service-name {
        margin: 0; 
        color: #FFFFFF; 
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .service-desc {
        margin: 5px 0 0 0; 
        color: #a0aab5; 
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='shop-title'>PREMIUM CUTS</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Select your services below</h4>", unsafe_allow_html=True)

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
            <div style='background-color: #d32f2f; color: white; padding: 15px; 
                        text-align: center; font-size: 1.2rem; font-weight: bold; 
                        border-radius: 10px; margin-bottom: 30px; 
                        text-transform: uppercase;'>
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
        st.header(f"💈 {cat}")
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
                price_html = f"<span style='color: #d32f2f; text-decoration: line-through; font-size: 1.2rem; margin-right: 10px;'>${original_price:.2f}</span> <span style='color: #4CAF50;'>${discounted_price:.2f}</span>"
                display_price = discounted_price
            else:
                price_html = f"<span style='color: #4CAF50;'>${original_price:.2f}</span>"
                display_price = original_price

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="service-card">
                    <div class="service-name">{svc['name']} <span style="float: right;">{price_html}</span></div>
                    <div class="service-desc">{svc.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.write("") 
                st.write("") 
                is_selected = st.checkbox("Add to Order", key=f"chk_{svc['id']}")
                if is_selected:
                    st.session_state.cart[svc['name']] = display_price
                elif svc['name'] in st.session_state.cart:
                    del st.session_state.cart[svc['name']]
        st.divider()

# --- 4. CHECKOUT & WHATSAPP ---
st.header("🛒 Checkout")

if st.session_state.cart:
    total_price = sum(st.session_state.cart.values())
    st.write("**Selected Services:**")
    for item, price in st.session_state.cart.items():
        st.write(f"- {item}: ${price:.2f}")
    st.markdown(f"### **Total: ${total_price:.2f}**")
    
    st.divider()
    st.subheader("Your Details")
    cust_name = st.text_input("Full Name")
    cust_phone = st.text_input("Phone Number")
    
    if st.button("Confirm Order & Send to Barber"):
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
            
            st.success("Order saved to the barber's database!")
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:15px 32px; border:none; border-radius:8px; font-weight:bold; font-size:18px; cursor:pointer; width:100%; margin-top:10px;">Send Order via WhatsApp</button></a>', unsafe_allow_html=True)
        else:
            st.error("Please enter your name and phone number so the barber knows who you are.")
else:
    st.info("Your order is empty. Select a service above.")