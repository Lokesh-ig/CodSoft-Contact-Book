"""
Database module for Contact Book application.
Handles SQLite connection, schema creation, and CRUD operations.
"""

import sqlite3
import os
from typing import List, Dict, Optional, Any


class ContactDatabase:
    """Manages persistent SQLite storage for contact records."""

    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a connection to the SQLite database with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Creates the contacts table if it does not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT DEFAULT '',
                    address TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_contact(self, name: str, phone: str, email: str = "", address: str = "") -> int:
        """
        Adds a new contact to the database.
        Returns the ID of the created contact.
        """
        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()

        if not name:
            raise ValueError("Contact name cannot be empty.")
        if not phone:
            raise ValueError("Phone number cannot be empty.")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contacts (name, phone, email, address)
                VALUES (?, ?, ?, ?)
            """, (name, phone, email, address))
            conn.commit()
            return cursor.lastrowid

    def get_all_contacts(self) -> List[Dict[str, Any]]:
        """Retrieves all contacts sorted alphabetically by name."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, phone, email, address, created_at
                FROM contacts
                ORDER BY LOWER(name) ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_contact_by_id(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single contact by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, phone, email, address, created_at
                FROM contacts
                WHERE id = ?
            """, (contact_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def search_contacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches contacts by name or phone number.
        Returns matching records sorted alphabetically by name.
        """
        query = query.strip()
        if not query:
            return self.get_all_contacts()

        pattern = f"%{query}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, phone, email, address, created_at
                FROM contacts
                WHERE name LIKE ? OR phone LIKE ?
                ORDER BY LOWER(name) ASC
            """, (pattern, pattern))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_contact(self, contact_id: int, name: str, phone: str, email: str = "", address: str = "") -> bool:
        """
        Updates details for an existing contact.
        Returns True if successful, False if contact was not found.
        """
        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()

        if not name:
            raise ValueError("Contact name cannot be empty.")
        if not phone:
            raise ValueError("Phone number cannot be empty.")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE contacts
                SET name = ?, phone = ?, email = ?, address = ?
                WHERE id = ?
            """, (name, phone, email, address, contact_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_contact(self, contact_id: int) -> bool:
        """
        Deletes a contact by ID.
        Returns True if deleted, False if contact was not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            return cursor.rowcount > 0

    def seed_sample_data_if_empty(self) -> None:
        """Seeds initial sample contacts if database is empty."""
        contacts = self.get_all_contacts()
        if not contacts:
            sample_contacts = [
                ("Alice Smith", "+1 555-0192", "alice.smith@example.com", "123 Maple Street, Springfield"),
                ("Bob Johnson", "+1 555-0143", "bob.j@example.com", "456 Oak Avenue, Metropolis"),
                ("Charlie Brown", "+1 555-0188", "charlie@example.com", "789 Pine Road, Gotham"),
                ("Diana Prince", "+1 555-0177", "diana.prince@example.com", "101 Amazon Way, Themyscira")
            ]
            for name, phone, email, address in sample_contacts:
                self.add_contact(name, phone, email, address)
