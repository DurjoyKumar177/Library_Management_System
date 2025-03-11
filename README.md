# Library Management System

## 📚 Project Overview
This is a **Django-based Library Management System** where users can **borrow, review, and manage books**. The system supports **account creation, deposit/withdrawal transactions, book listings with categories, and email notifications**. It also provides features like **profile management, borrowing history, and dynamic transaction filtering**.

## 🚀 Features
- **User Authentication:** Sign up, log in, password reset, and profile management.
- **Book Listings:** Categorized book display with search and filter functionality.
- **Book Borrowing:** Users can borrow books based on available balance.
- **Deposit/Withdraw Transactions:** Users can manage their funds for book borrowing.
- **Reviews & Ratings:** Users can leave reviews and ratings on books.
- **Borrowing History:** Track previously borrowed books.
- **Transaction Filtering:** View and filter past transactions dynamically.
- **Email Notifications:** Users receive emails for major actions like borrowing and returning books.

## 🛠️ Technologies Used
- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.x installed
- Virtual environment setup (optional but recommended)

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/yourusername/library-management-system.git
 cd library-management-system
```

### 2️⃣ Create & Activate a Virtual Environment
```bash
 python -m venv venv  # Create a virtual environment
 source venv/bin/activate  # Activate (Mac/Linux)
 venv\Scripts\activate  # Activate (Windows)
```

### 3️⃣ Install Dependencies
```bash
 pip install -r requirements.txt
```

### 4️⃣ Apply Migrations & Create Superuser
```bash
 python manage.py makemigrations
 python manage.py migrate
 python manage.py createsuperuser  # Follow the prompts to create an admin user
```

### 5️⃣ Run the Development Server
```bash
 python manage.py runserver
```
Then open **http://127.0.0.1:8000/** in your browser.

## 📌 Usage Instructions
1. **Admin Panel:** Access at `/admin/` to manage books, users, and transactions.
2. **Register/Login:** Users must register and log in to borrow books.
3. **Deposit Money:** Users must deposit funds before borrowing books.
4. **Borrow Books:** Borrow available books if balance is sufficient.
5. **Review & Rate:** Users can leave feedback on books.

## 🎯 Future Enhancements
- Implement API endpoints for external integrations.
- Add support for more databases like PostgreSQL.
- Introduce a fine system for overdue books.
- Improve UI with React for a dynamic frontend.

## 🤝 Contribution Guidelines
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a Pull Request.

## 📩 Contact & Support
For any queries, feel free to reach out to me at **durjoykumar177@gmail.com**.

---
🚀 Happy Coding!

