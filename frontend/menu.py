import streamlit as st
import requests
import urllib.parse

API_URL = "https://salon-steve.onrender.com"
# REPLACE WITH YOUR ACTUAL NUMBER (Include country code, no + or spaces. e.g., 96170123456)
BARBER_PHONE = "1234567890" 

st.set_page_config(page_title="Barber Menu & Booking", layout="centered")

st.markdown("<h1 style='text-align: center; color: #d4af37;'>PREMIUM CUTS</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Select your services below</h4>", unsafe_allow_html=True)

# Initialize shopping cart in session state
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- 1. FETCH SERVICES ---
try:
    response = requests.get(f"{API_URL}/services/")
    services = response.json() if response.status_code == 200 else []
except:
    services = []
    st.error("Cannot connect to server.")

# --- 2. DISPLAY MENU BY CATEGORY ---
if services:
    # Group services by their category
    categories = sorted(list(set([svc.get("category", "General") for svc in services])))
    
    for cat in categories:
        st.header(f"💈 {cat}")
        cat_services = [s for s in services if s.get("category", "General") == cat and s['is_active']]
        
        for svc in cat_services:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{svc['name']}** - ${svc['base_price']:.2f}")
                st.caption(svc['description'])
            with col2:
                # Checkbox acts as an "Add to Cart"
                is_selected = st.checkbox("Select", key=f"chk_{svc['id']}")
                if is_selected:
                    st.session_state.cart[svc['name']] = svc['base_price']
                elif svc['name'] in st.session_state.cart:
                    del st.session_state.cart[svc['name']]
        st.divider()

# --- 3. CHECKOUT & WHATSAPP ---
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
            # 1. Save to Database
            selected_items_str = ", ".join(st.session_state.cart.keys())
            payload = {
                "customer_name": cust_name,
                "customer_phone": cust_phone,
                "services_ordered": selected_items_str,
                "total_price": total_price
            }
            requests.post(f"{API_URL}/orders/", json=payload)
            
            # 2. Generate WhatsApp Link
            msg = f"New Order from {cust_name} ({cust_phone})!\n\nServices:\n"
            for item, price in st.session_state.cart.items():
                msg += f"- {item}\n"
            msg += f"\nTotal: ${total_price:.2f}"
            
            encoded_msg = urllib.parse.quote(msg)
            whatsapp_url = f"https://wa.me/{BARBER_PHONE}?text={encoded_msg}"
            
            st.success("Order saved! Click the button below to send it to the barber.")
            # Create a clickable button that opens WhatsApp
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:10px 24px; border:none; border-radius:8px; font-size:16px; cursor:pointer;">Send WhatsApp Message</button></a>', unsafe_allow_html=True)
        else:
            st.error("Please enter your name and phone number.")
else:
    st.info("Your cart is empty. Select a service above.")