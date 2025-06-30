# e‑Library – UAS OOP Semester 3 📚

**A virtual library built in Python for Object‑Oriented Programming (UAS, Semester 3)**

## 🚀 Table of Contents

- [About](#about)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  

---

## About

This project implements a simple e‑Library system using Python and OOP principles as part of the Semester 3 final assignment (UAS). It allows users to:

- Log in with accounts
- Search books via Google Books API
- Borrow and return books
- View book catalog and user account details  
:contentReference[oaicite:1]{index=1}

---

## Features

- **Authentication system** (`account.py`) for user login
- **Google Books API integration** (`google_books_api.py`) for fetching book data
- **Main app** logic in `main.py` covering borrowing, returning, searching
- **Persistent storage** using SQLite DB under `database/`
- **Requirements** managed via `requirements.txt`
- Modular design separating concerns into distinct Python modules

---

## Tech Stack

- Python 3.x
- Object‑Oriented Programming patterns
- SQLite (via `sqlite3` module)
- Requests library for HTTP integration
- Google Books API

---

## Project Structure

```bash
e-Library-UAS-OOP-SEMESTER-3/
├── account.py # User account & authentication
├── google_books_api.py # Google Books API wrapper
├── main.py # Main application flow
├── database/ # SQLite database files and schema
├── requirements.txt # Project dependencies
├── logo.ico # App icon
└── pycache/ # Python caches
```


---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/RaffiAkhdilputra/e-Library-UAS-OOP-SEMESTER-3.git
   cd e-Library-UAS-OOP-SEMESTER-3
   ```
2. **Install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   pip install -r requirements.txt
   ```

---

## Usage

Run the main script:
```bash
python main.py
```
You'll be prompted to log in or register, then you'll have options to:
- Search the book catalog (via Google Books API)
- Borrow or return books
- View your borrowed books
- Exit the program

## Team

Built by me **Raffi Akhdilputra**, **Hilma Zahra** and **Rivaldi Cahya** as part of our final exam for Object-Oriented Programing, semester 3
