"""
Command Line Interface (CLI) for Contact Book application.
"""

import sys
from database import ContactDatabase


class ContactBookCLI:
    def __init__(self):
        self.db = ContactDatabase()
        self.db.seed_sample_data_if_empty()

    def run(self):
        print("=" * 50)
        print("        📇 CONTACT BOOK - CLI INTERFACE")
        print("=" * 50)

        while True:
            self._print_menu()
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.view_contacts()
            elif choice == "3":
                self.search_contacts()
            elif choice == "4":
                self.update_contact()
            elif choice == "5":
                self.delete_contact()
            elif choice == "6":
                print("\nThank you for using Contact Book! Goodbye.")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please enter a number from 1 to 6.")

    def _print_menu(self):
        print("\n--- MENU ---")
        print("1. ➕ Add Contact")
        print("2. 📋 View Contact List")
        print("3. 🔍 Search Contact")
        print("4. ✏️ Update Contact")
        print("5. 🗑️ Delete Contact")
        print("6. 🚪 Exit")

    def add_contact(self):
        print("\n--- ADD NEW CONTACT ---")
        name = input("Enter Name*: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return

        phone = input("Enter Phone Number*: ").strip()
        if not phone:
            print("❌ Phone number cannot be empty!")
            return

        email = input("Enter Email Address: ").strip()
        address = input("Enter Physical Address: ").strip()

        try:
            cid = self.db.add_contact(name, phone, email, address)
            print(f"✅ Contact '{name}' added successfully! (ID: {cid})")
        except Exception as e:
            print(f"❌ Error adding contact: {str(e)}")

    def view_contacts(self):
        print("\n--- CONTACT LIST ---")
        contacts = self.db.get_all_contacts()
        if not contacts:
            print("No contacts found.")
            return

        print(f"{'ID':<5} | {'NAME':<25} | {'PHONE NUMBER':<18}")
        print("-" * 55)
        for c in contacts:
            print(f"{c['id']:<5} | {c['name']:<25} | {c['phone']:<18}")
        print("-" * 55)
        print(f"Total: {len(contacts)} contact(s)")

    def search_contacts(self):
        print("\n--- SEARCH CONTACTS ---")
        query = input("Enter Name or Phone Number to search: ").strip()
        if not query:
            print("❌ Search query cannot be empty!")
            return

        results = self.db.search_contacts(query)
        if not results:
            print(f"No contacts found matching '{query}'.")
            return

        print(f"\nFound {len(results)} matching contact(s):")
        print(f"{'ID':<5} | {'NAME':<20} | {'PHONE':<15} | {'EMAIL':<25} | {'ADDRESS'}")
        print("-" * 80)
        for c in results:
            print(f"{c['id']:<5} | {c['name']:<20} | {c['phone']:<15} | {c['email']:<25} | {c['address']}")

    def update_contact(self):
        print("\n--- UPDATE CONTACT ---")
        self.view_contacts()
        try:
            cid = int(input("\nEnter the ID of the contact to update: ").strip())
        except ValueError:
            print("❌ Invalid ID format!")
            return

        contact = self.db.get_contact_by_id(cid)
        if not contact:
            print(f"❌ Contact with ID {cid} not found.")
            return

        print(f"\nUpdating contact '{contact['name']}'. (Press Enter to keep current value)")
        new_name = input(f"Name [{contact['name']}]: ").strip() or contact["name"]
        new_phone = input(f"Phone [{contact['phone']}]: ").strip() or contact["phone"]
        new_email = input(f"Email [{contact['email']}]: ").strip() or contact["email"]
        new_address = input(f"Address [{contact['address']}]: ").strip() or contact["address"]

        updated = self.db.update_contact(cid, new_name, new_phone, new_email, new_address)
        if updated:
            print(f"✅ Contact '{new_name}' updated successfully!")
        else:
            print("❌ Failed to update contact.")

    def delete_contact(self):
        print("\n--- DELETE CONTACT ---")
        self.view_contacts()
        try:
            cid = int(input("\nEnter the ID of the contact to delete: ").strip())
        except ValueError:
            print("❌ Invalid ID format!")
            return

        contact = self.db.get_contact_by_id(cid)
        if not contact:
            print(f"❌ Contact with ID {cid} not found.")
            return

        confirm = input(f"Are you sure you want to delete '{contact['name']}'? (y/N): ").strip().lower()
        if confirm == "y":
            deleted = self.db.delete_contact(cid)
            if deleted:
                print(f"✅ Contact '{contact['name']}' deleted.")
            else:
                print("❌ Could not delete contact.")
        else:
            print("Deletion canceled.")


if __name__ == "__main__":
    app = ContactBookCLI()
    app.run()
