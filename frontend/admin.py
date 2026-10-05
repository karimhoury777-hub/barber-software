import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Barber Admin Panel", layout="centered")

# --- SECURITY LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Shop Login")
    pwd = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if pwd == st.secrets["shop_password"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect Password")
    st.stop()

API_URL = "https://salon-steve.onrender.com"

col1, col2 = st.columns([3, 1])
with col1:
    st.title("💈 Shop Control Panel")
with col2:
    st.write("")
    if st.button("🔄 Sync Orders"):
        st.rerun()

# --- SECTION 1: ADD A NEW SERVICE ---
st.header("Add a New Service")
with st.form("add_service_form", clear_on_submit=True):
    name = st.text_input("Service Name (e.g., Haircut + Beard)")
    category = st.selectbox("Category", ["Hair", "Beard", "Treatments", "Coloring", "Other"])
    description = st.text_input("Description")
    price = st.number_input("Base Price ($)", min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button("Save to Database")

    if submit_button:
        payload = {
            "name": name,
            "category": category,
            "description": description,
            "base_price": price,
            "is_active": True
        }
        response = requests.post(f"{API_URL}/services/", json=payload)
        if response.status_code == 200:
            st.success(f"'{name}' added successfully!")
            st.rerun()
        else:
            st.error("Failed to add service.")

st.divider()

# --- SECTION 2: MANAGE CURRENT MENU ---
st.header("Manage & Edit Menu")
try:
    response = requests.get(f"{API_URL}/services/")
    if response.status_code == 200:
        services = response.json()
        if services:
            for svc in services:
                with st.expander(f"💈 {svc['name']} - ${svc['base_price']:.2f}"):
                    with st.form(f"edit_form_{svc['id']}"):
                        new_name = st.text_input("Name", value=svc['name'])
                        
                        current_cat = svc.get('category', 'General')
                        cat_options = ["Hair", "Beard", "Treatments", "Coloring", "Other"]
                        if current_cat not in cat_options:
                            cat_options.append(current_cat)
                        
                        new_category = st.selectbox("Category", cat_options, index=cat_options.index(current_cat))
                        new_desc = st.text_input("Description", value=svc.get('description', ''))
                        new_price = st.number_input("Price ($)", value=svc['base_price'], format="%.2f")
                        is_active = st.checkbox("Show on Public Menu", value=svc['is_active'])
                        
                        update_button = st.form_submit_button("Update Service")
                        
                        if update_button:
                            update_payload = {
                                "name": new_name,
                                "category": new_category,
                                "description": new_desc,
                                "base_price": new_price,
                                "is_active": is_active
                            }
                            update_res = requests.put(f"{API_URL}/services/{svc['id']}", json=update_payload)
                            if update_res.status_code == 200:
                                st.success("Updated! Refreshing...")
                                st.rerun()
                            else:
                                st.error("Failed to update.")
        else:
            st.info("No services found. Add one above!")
except:
    st.error("Cannot connect to backend.")

st.divider()

# --- SECTION 3: MANAGE PROMOTIONS ---
st.header("📢 Promotions")

# 3A. Active Promotions List
st.subheader("Active Sales")
try:
    promo_res = requests.get(f"{API_URL}/promotions/")
    if promo_res.status_code == 200:
        promos = promo_res.json()
        if promos:
            for p in promos:
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{p['title']}** ({p['discount_percentage']}% OFF)")
                if c2.button("Remove", key=f"del_promo_{p['id']}"):
                    requests.delete(f"{API_URL}/promotions/{p['id']}")
                    st.rerun()
        else:
            st.info("No active promotions.")
except:
    st.error("Could not fetch promotions.")

# 3B. Launch New Promotion
with st.expander("Launch a New Promotion"):
    with st.form("add_promo_form", clear_on_submit=True):
        promo_title = st.text_input("Promotion Title (e.g., Holiday Special)")
        discount = st.number_input("Discount Percentage (%)", min_value=1.0, max_value=100.0, step=1.0)
        
        col1, col2 = st.columns(2)
        today = datetime.date.today()
        start_d = col1.date_input("Start Date", today)
        end_d = col2.date_input("End Date", today + datetime.timedelta(days=7))
        
        submit_promo = st.form_submit_button("Launch Promotion")
        
        if submit_promo:
            start_dt = datetime.datetime.combine(start_d, datetime.datetime.min.time()).isoformat()
            end_dt = datetime.datetime.combine(end_d, datetime.datetime.max.time()).isoformat()
            
            promo_payload = {
                "title": promo_title,
                "discount_percentage": discount,
                "start_date": start_dt,
                "end_date": end_dt,
                "service_id": None
            }
            promo_post = requests.post(f"{API_URL}/promotions/", json=promo_payload)
            if promo_post.status_code == 200:
                st.success("Promotion launched!")
                st.rerun()
            else:
                st.error("Failed to launch promotion.")

st.divider()

# --- SECTION 4: CLIENT DATABASE & ORDERS ---
st.header("📋 Client Database & Orders")
try:
    orders_res = requests.get(f"{API_URL}/orders/")
    if orders_res.status_code == 200:
        orders = orders_res.json()
        if orders:
            unique_clients = set([o['customer_phone'] for o in orders])
            today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            today_orders = [o for o in orders if o['created_at'].startswith(today_str)]
            
            col1, col2 = st.columns(2)
            col1.metric("All-Time Registered Clients", len(unique_clients))
            col2.metric("Orders Today", len(today_orders))
            
            tab1, tab2 = st.tabs(["Today's Orders", "All-Time History"])
            
            with tab1:
                if today_orders:
                    st.dataframe(today_orders, column_order=("customer_name", "customer_phone", "services_ordered", "total_price", "created_at"), hide_index=True, use_container_width=True)
                else:
                    st.info("No orders yet today.")
                    
            with tab2:
                st.dataframe(orders, column_order=("customer_name", "customer_phone", "services_ordered", "total_price", "created_at"), hide_index=True, use_container_width=True)
        else:
            st.info("No clients registered yet.")
except:
    st.error("Could not fetch orders.")