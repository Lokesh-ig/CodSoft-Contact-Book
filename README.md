# 📇 Contact Book Application (CodSoft Task 3)

A feature-rich **Contact Book Application** built using Python, Tkinter (Modern Desktop GUI), Flask (Web App), and SQLite (Persistent Database).

🌐 **Live Web Demo**: [https://contact-book-joew.onrender.com](https://contact-book-joew.onrender.com)

---

## 🌟 Task Requirements & Features

| Requirement | Implementation Details | Status |
|---|---|:---:|
| **Contact Information** | Stores Name, Phone Number, Email Address, and Physical Address for each contact. | ✅ Complete |
| **Add Contact** | User-friendly form to add new contacts with input validation (Email & Phone format). | ✅ Complete |
| **View Contact List** | List view displaying all saved contacts showing Names and Phone Numbers. | ✅ Complete |
| **Search Contact** | Dynamic real-time search bar to filter contacts instantly by Name or Phone Number. | ✅ Complete |
| **Update Contact** | Click any contact to view details and edit existing information easily. | ✅ Complete |
| **Delete Contact** | Delete option with confirmation modal dialog to prevent accidental deletion. | ✅ Complete |
| **User Interface** | Modern Desktop GUI (Tkinter) + Option for CLI mode. | ✅ Complete |

---

## 📁 Project Structure

```
codsoft_taskno3_contact-book/
├── database.py          # SQLite database manager (CRUD operations & search)
├── contact_book_gui.py  # Modern Tkinter Graphical User Interface
├── cli_contact_book.py  # Command Line Interface (CLI mode)
├── main.py              # Application entry point (GUI / CLI)
├── test_contact_book.py # Unit tests for database & validation logic
├── requirements.txt     # Standard library dependencies documentation
└── README.md            # Project documentation
```

---

## 🚀 How to Run

### 1. Modern Desktop GUI (Default)
Run the following command to launch the Desktop GUI:
```bash
python main.py
```
*Or run directly:*
```bash
python contact_book_gui.py
```

### 2. Command Line Interface (CLI Mode)
If you prefer managing contacts from your terminal:
```bash
python main.py --cli
```
*Or run directly:*
```bash
python cli_contact_book.py
```

---

## 🧪 Running Unit Tests

To run the automated unit test suite:
```bash
python -m unittest discover
```

---

## 🗄️ Database Schema (`contacts.db`)

Contacts are stored persistently in a local SQLite database table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT DEFAULT '',
    address TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 GUI Highlights
- **Real-time Live Search**: Results update automatically as you type in the search bar.
- **Form Reset / Quick Actions**: Easily switch between adding new contacts and editing existing ones.
- **Status Bar Feedback**: Displays real-time status notifications for additions, updates, and deletions.
- **Safety First**: Confirms with a popup dialog before deleting any record.
