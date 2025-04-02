# Auction Project
![image](https://github.com/user-attachments/assets/b093f35c-cbf2-4168-9c90-0df6cf51ab57)

## 📖 Overview
Auction Project is a simple web-based platform that allows users to create auction listings, place bids on items, and manage their watchlists. Users can participate in bidding wars and track their winning bids in real-time.

## ⭐ Features
- User authentication and authorization
- Create, edit, and delete auction listings
- Place bids on active listings
- Add items to a personal watchlist
- Track winning bids
- Admin dashboard for managing listings and users

## ⚙️ Requirements
- Python 3.8+
- Django 4.0+
- SQLite (default) or PostgreSQL/MySQL for production
- Bootstrap (for styling)

## 🛠️ Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Peeralis/CS50-Commerce.git auction
   ```
2. Navigate to the project directory:
   ```sh
   cd auction
   ```
3. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## 📂 Project Structure
```plaintext
DjangoAuction/
│-- auctions/         # Main app for auction functionalities
│   ├── migrations/   # Database migrations
│   ├── static/       # Static files (CSS, JS, images)
│   ├── templates/    # HTML templates
│   ├── views.py      # View functions
│   ├── models.py     # Database models
│   ├── urls.py       # Paths
│-- users/            # User authentication and profiles
│-- manage.py         # Django management script
│-- db.sqlite3        # SQLite database (or configure PostgreSQL/MySQL)
```

## ▶️ How to Run
1. Ensure you have activated your virtual environment.
2. Run the development server:
   ```sh
   python manage.py runserver
   ```
3. Open your browser and go to `http://127.0.0.1:8000/`.

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for more details.

## 👤 Author
Developed by [Peeralis](https://github.com/Peeralis).

