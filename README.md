# 🍽️ FoodRescue

FoodRescue is a **web application** built to tackle the problem of **food waste** by connecting people who have surplus food with those in need.  
The idea is simple: instead of throwing away extra food, donors can list it on the platform, and receivers (such as NGOs, shelters, or individuals) can request it.  

This creates a **community-driven system** to reduce food waste, help underprivileged people, and build awareness about sustainable living.  

---

## 🌍 Why FoodRescue?
Every day, a huge amount of food is wasted while millions of people go hungry.  
FoodRescue solves this problem by:
- ♻️ **Reducing food waste** at the household and community level.  
- 🤝 **Connecting donors & receivers** in real time.  
- ❤️ **Supporting NGOs and shelters** that rely on food donations.  
- 📊 **Encouraging sustainable practices** for a better environment.  

---

## 🚀 Features
- 👤 **User Authentication** – Register, log in, and manage your account securely.  
- 📦 **Food Listings** – Donors can add available food items with details (type, quantity, etc.).  
- 🔒 **Secure Passwords** – Passwords are hashed before being stored in the database.  
- 🗂️ **Database Support** – Uses SQLite for fast and lightweight storage.  
- 🎨 **Frontend UI** – Clean and responsive pages built with HTML, CSS, and Jinja2 templates.  

---

## 🛠️ Tech Stack
- **Backend:** Python (Flask)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, Jinja2  
- **Other Tools:** Werkzeug (security), Git for version control  

---

## ⚙️ Installation & Setup

### 1. Clone the reposit


### 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows


### 3. nstall dependencies
pip install -r requirements.txt

📂 Project Structure
FoodRescue/
│── app.py              # Main Flask application
│── foodrescue.db       # SQLite database (auto-generated)
│── static/             # CSS, images, JS files
│── templates/          # HTML templates
│── venv/               # Virtual environment (ignored in git)
│── README.md           # Project documentation

📌 Future Enhancements

📷 Add image upload for food items.

📍 Location-based search (find food near you).

📱 Mobile-friendly UI or Android/iOS app.

🛡️ Role-based access (Donors, Receivers, NGOs, Admin).

☁️ Deployment on cloud (Heroku / Google Cloud / AWS).

🙌 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to improve.

Thank You!!

