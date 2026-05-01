SoulSync is a full-stack real-time chat application built using Django and WebSockets. It allows users to connect, send friend requests, and chat instantly with a modern UI.

---

## 🚀 Features

- 🔐 User Authentication (Login/Register/Logout)
- 👥 Friend Request System (Send, Accept, Notes)
- 💬 Real-Time One-to-One Chat (WebSockets)
- 📂 Persistent Chat History (Database)
- 🔍 User Search Functionality
- 🧑‍🤝‍🧑 Dynamic Friend List
- 🎨 Clean and Responsive UI

---

## 🛠 Tech Stack

- **Backend:** Django, Django Channels, WebSockets  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite  
- **Tools:** Git, GitHub  

---

## 📸 Screenshots

### 🏠 Chat Interface
![Chat UI](screenshots/home_pag.png)

### 👥 Friend Requests
![Requests](screenshots/freind_requests.png)

### ➕ Add Friend Popup
![Popup](screenshots/sending_freind_request.png)

### Authentication Page
![Popup](screenshots/authentication_page.png)

### Contact Page
![Popup](screenshots/contact_page.png)

### About Page
![Popup](screenshots/about_page.png)

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/soulsync.git
cd soulsync
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
