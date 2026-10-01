"""
Unit tests for Contact Book Database Manager.
"""

import os
import unittest
from database import ContactDatabase


class TestContactDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_contacts.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = ContactDatabase(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_contact(self):
        cid = self.db.add_contact("John Doe", "+123456789", "john@example.com", "123 Main St")
        self.assertIsInstance(cid, int)
        contact = self.db.get_contact_by_id(cid)
        self.assertIsNotNone(contact)
        self.assertEqual(contact["name"], "John Doe")
        self.assertEqual(contact["phone"], "+123456789")
        self.assertEqual(contact["email"], "john@example.com")
        self.assertEqual(contact["address"], "123 Main St")

    def test_add_contact_validation(self):
        with self.assertRaises(ValueError):
            self.db.add_contact("", "+123456789")
        with self.assertRaises(ValueError):
            self.db.add_contact("John Doe", "")

    def test_get_all_contacts(self):
        self.db.add_contact("Zack", "111")
        self.db.add_contact("Adam", "222")
        contacts = self.db.get_all_contacts()
        self.assertEqual(len(contacts), 2)
        # Should be sorted by name alphabetically
        self.assertEqual(contacts[0]["name"], "Adam")
        self.assertEqual(contacts[1]["name"], "Zack")

    def test_search_contacts_by_name(self):
        self.db.add_contact("Alice Smith", "12345")
        self.db.add_contact("Bob Jones", "67890")
        results = self.db.search_contacts("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice Smith")

    def test_search_contacts_by_phone(self):
        self.db.add_contact("Alice Smith", "987654321")
        self.db.add_contact("Bob Jones", "123456789")
        results = self.db.search_contacts("9876")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice Smith")

    def test_update_contact(self):
        cid = self.db.add_contact("Old Name", "111", "old@example.com", "Old Addr")
        updated = self.db.update_contact(cid, "New Name", "999", "new@example.com", "New Addr")
        self.assertTrue(updated)
        contact = self.db.get_contact_by_id(cid)
        self.assertEqual(contact["name"], "New Name")
        self.assertEqual(contact["phone"], "999")
        self.assertEqual(contact["email"], "new@example.com")
        self.assertEqual(contact["address"], "New Addr")

    def test_delete_contact(self):
        cid = self.db.add_contact("To Delete", "000")
        deleted = self.db.delete_contact(cid)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_contact_by_id(cid))


if __name__ == "__main__":
    unittest.main()
