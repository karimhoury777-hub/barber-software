# 💈 Salon Steve - Developer Guide & Cheat Sheet

## 1. Core Tech Stack
* **Python**: Core programming language.
* **FastAPI**: Backend framework handling data and APIs.
* **Streamlit**: Frontend framework powering both the Admin Panel and Customer Menu.
* **PostgreSQL (Neon)**: Cloud database storing services, promotions, and orders.
* **GitHub**: Version control system holding the cloud codebase.
* **Render**: Cloud server hosting the FastAPI backend 24/7.
* **Streamlit Community Cloud**: Cloud server hosting the frontend apps.

---

## 2. Cloud Control Centers (Dashboards)
* **Code Repository**: [GitHub](https://github.com) (`barber-software` repository)
* **Database Management**: [Neon Tech](https://neon.tech)
* **Backend Server**: [Render](https://render.com) (`Salon-Steve` web service)
* **Frontend Servers**: [Streamlit Cloud](https://share.streamlit.io) (Managed apps & `shop_password` secrets)

---

## 3. Deployment Workflow (Updating Live Apps)
Because your apps pull directly from GitHub, you never need to manually upload files. To make updates:
1. Open your project folder (`C:\Users\karim\barber-software`) in your code editor.
2. Edit your files and save them.
3. Open PowerShell, navigate to the project folder, and push the updates:
   ```powershell
   git add .
   git commit -m "Description of updates"
   git push




4. Local Testing (Offline Mode)
If you want to test changes locally before pushing to the internet:

Run Backend Locally:

PowerShell
cd backend
uvicorn main:app --reload
(API runs at http://127.0.0.1:8000)

Run Admin Panel Locally:

PowerShell
cd frontend
streamlit run admin.py
(Runs at localhost:8501)

Run Client Menu Locally:

PowerShell
cd frontend
streamlit run menu.py
(Runs at localhost:8502)