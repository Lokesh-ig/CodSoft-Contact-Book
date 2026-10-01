"""
Flask Web Application for Render.com Deployment.
Serves a responsive modern Web UI for Contact Book using database.py.
"""

from flask import Flask, render_template_string, request, jsonify
from database import ContactDatabase

app = Flask(__name__)
db = ContactDatabase()
db.seed_sample_data_if_empty()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Book Web</title>
    <style>
        :root {
            --bg-main: #0B0F19;
            --bg-card: #151C2C;
            --bg-header: #0D1527;
            --border-card: #1E293B;
            --text-primary: #F8FAFC;
            --text-muted: #94A3B8;
            --input-bg: #1E293B;
            --input-border: #334155;
            --indigo: #6366F1;
            --cyan: #0EA5E9;
            --emerald: #10B981;
            --rose: #F43F5E;
        }

        [data-theme="light"] {
            --bg-main: #F1F5F9;
            --bg-card: #FFFFFF;
            --bg-header: #1E293B;
            --border-card: #CBD5E1;
            --text-primary: #0F172A;
            --text-muted: #64748B;
            --input-bg: #F8FAFC;
            --input-border: #CBD5E1;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-primary); transition: all 0.3s ease; min-height: 100vh; }
        
        header { background-color: var(--bg-header); padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--indigo); }
        .brand { display: flex; align-items: center; gap: 12px; }
        .logo { background: #1E1B4B; color: #A5B4FC; font-size: 20px; padding: 6px 12px; border-radius: 8px; border: 1px solid var(--indigo); }
        .titles h1 { font-size: 18px; font-weight: 700; color: #F8FAFC; }
        .titles p { font-size: 12px; color: #94A3B8; }

        .theme-toggle { background: var(--indigo); color: white; border: none; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: 0.2s; }
        .theme-toggle:hover { opacity: 0.9; transform: scale(1.03); }

        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 25px; max-width: 1100px; margin: 0 auto; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }

        .card { background-color: var(--bg-card); border: 1px solid var(--border-card); border-radius: 10px; padding: 20px; }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .card-title { font-size: 14px; font-weight: bold; letter-spacing: 0.5px; }

        .search-box { display: flex; align-items: center; background: var(--input-bg); border: 1px solid var(--input-border); border-radius: 6px; padding: 8px 12px; margin-bottom: 15px; }
        .search-box input { background: transparent; border: none; color: var(--text-primary); outline: none; width: 100%; margin-left: 8px; font-size: 14px; }

        .contact-list { max-height: 400px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
        .contact-item { background: var(--input-bg); border: 1px solid var(--border-card); padding: 12px; border-radius: 6px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: 0.2s; }
        .contact-item:hover, .contact-item.active { border-color: var(--indigo); background: #1E1B4B; }
        .contact-item h4 { font-size: 14px; margin-bottom: 2px; }
        .contact-item p { font-size: 12px; color: var(--text-muted); }

        .form-group { margin-bottom: 14px; }
        .form-group label { display: block; font-size: 12px; font-weight: bold; color: var(--text-muted); margin-bottom: 5px; }
        .form-group input, .form-group textarea { width: 100%; background: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary); padding: 9px 12px; border-radius: 6px; outline: none; font-size: 14px; }
        .form-group input:focus, .form-group textarea:focus { border-color: var(--indigo); }

        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        .btn { flex: 1; padding: 10px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; color: white; transition: 0.2s; }
        .btn-primary { background: var(--indigo); }
        .btn-danger { background: var(--rose); }
        .btn-secondary { background: var(--cyan); }
        .btn:hover { opacity: 0.9; }

        .status-bar { background: var(--bg-header); padding: 10px 25px; font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 8px; border-top: 1px solid var(--border-card); position: fixed; bottom: 0; width: 100%; }
        .dot { width: 8px; height: 8px; background: var(--emerald); border-radius: 50%; display: inline-block; }
    </style>
</head>
<body data-theme="dark">

<header>
    <div class="brand">
        <div class="logo">👥</div>
        <div class="titles">
            <h1>CONTACT BOOK</h1>
            <p>Smart Contact Directory</p>
        </div>
    </div>
    <button class="theme-toggle" onclick="toggleTheme()" id="themeBtn">☀</button>
</header>

<div class="container">
    <div class="card">
        <div class="card-header">
            <span class="card-title">SAVED CONTACTS</span>
            <span style="font-size: 12px; color: var(--text-muted);" id="contactCount">Total: 0</span>
        </div>
        <div class="search-box">
            <span>🔍</span>
            <input type="text" id="searchInput" placeholder="Search by name or phone..." oninput="fetchContacts()">
        </div>
        <div class="contact-list" id="contactList"></div>
    </div>

    <div class="card">
        <div class="card-header">
            <span class="card-title" id="formHeader">✨ Add New Contact</span>
        </div>
        <input type="hidden" id="contactId">
        <div class="form-group">
            <label>👤 Full Name *</label>
            <input type="text" id="nameInput" placeholder="John Doe">
        </div>
        <div class="form-group">
            <label>📞 Phone Number *</label>
            <input type="text" id="phoneInput" placeholder="+1 555-0192">
        </div>
        <div class="form-group">
            <label>✉️ Email Address</label>
            <input type="email" id="emailInput" placeholder="john@example.com">
        </div>
        <div class="form-group">
            <label>📍 Physical Address</label>
            <textarea id="addressInput" rows="3" placeholder="123 Main Street"></textarea>
        </div>
        <div class="btn-group">
            <button class="btn btn-primary" onclick="saveContact()" id="saveBtn">➕ Save Contact</button>
            <button class="btn btn-secondary" onclick="resetForm()">🔄 Clear / New</button>
            <button class="btn btn-danger" onclick="deleteContact()" id="deleteBtn" style="display:none;">🗑️ Delete</button>
        </div>
    </div>
</div>

<div class="status-bar">
    <span class="dot"></span>
    <span id="statusText">System Ready</span>
</div>

<script>
    let currentTheme = 'dark';

    function toggleTheme() {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', currentTheme);
        document.getElementById('themeBtn').innerText = currentTheme === 'dark' ? '☀' : '🌙';
    }

    async function fetchContacts() {
        const query = document.getElementById('searchInput').value;
        const res = await fetch(`/api/contacts?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        
        const listEl = document.getElementById('contactList');
        document.getElementById('contactCount').innerText = `Total: ${data.length}`;
        listEl.innerHTML = '';

        data.forEach(c => {
            const div = document.createElement('div');
            div.className = 'contact-item';
            div.onclick = () => selectContact(c);
            div.innerHTML = `<div><h4>${escapeHtml(c.name)}</h4><p>📞 ${escapeHtml(c.phone)}</p></div><span>➔</span>`;
            listEl.appendChild(div);
        });
    }

    function selectContact(c) {
        document.getElementById('contactId').value = c.id;
        document.getElementById('nameInput').value = c.name;
        document.getElementById('phoneInput').value = c.phone;
        document.getElementById('emailInput').value = c.email || '';
        document.getElementById('addressInput').value = c.address || '';

        document.getElementById('formHeader').innerText = '✏️ Edit Contact';
        document.getElementById('saveBtn').innerText = '💾 Save Changes';
        document.getElementById('deleteBtn').style.display = 'block';
    }

    function resetForm() {
        document.getElementById('contactId').value = '';
        document.getElementById('nameInput').value = '';
        document.getElementById('phoneInput').value = '';
        document.getElementById('emailInput').value = '';
        document.getElementById('addressInput').value = '';

        document.getElementById('formHeader').innerText = '✨ Add New Contact';
        document.getElementById('saveBtn').innerText = '➕ Save Contact';
        document.getElementById('deleteBtn').style.display = 'none';
    }

    async function saveContact() {
        const id = document.getElementById('contactId').value;
        const name = document.getElementById('nameInput').value.trim();
        const phone = document.getElementById('phoneInput').value.trim();
        const email = document.getElementById('emailInput').value.trim();
        const address = document.getElementById('addressInput').value.trim();

        if (!name || !phone) {
            alert('Name and Phone Number are required!');
            return;
        }

        const payload = { name, phone, email, address };
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/contacts/${id}` : '/api/contacts';

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            resetForm();
            fetchContacts();
            document.getElementById('statusText').innerText = 'Contact saved successfully!';
        } else {
            alert('Failed to save contact');
        }
    }

    async function deleteContact() {
        const id = document.getElementById('contactId').value;
        if (!id) return;

        if (confirm('Are you sure you want to delete this contact?')) {
            const res = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
            if (res.ok) {
                resetForm();
                fetchContacts();
                document.getElementById('statusText').innerText = 'Contact deleted!';
            }
        }
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    fetchContacts();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    query = request.args.get("q", "").strip()
    if query:
        contacts = db.search_contacts(query)
    else:
        contacts = db.get_all_contacts()
    return jsonify(contacts)

@app.route("/api/contacts", methods=["POST"])
def add_contact():
    data = request.json or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    address = data.get("address", "").strip()

    if not name or not phone:
        return jsonify({"error": "Name and Phone required"}), 400

    cid = db.add_contact(name, phone, email, address)
    return jsonify({"id": cid, "status": "created"}), 201

@app.route("/api/contacts/<int:cid>", methods=["PUT"])
def update_contact(cid):
    data = request.json or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    address = data.get("address", "").strip()

    updated = db.update_contact(cid, name, phone, email, address)
    if updated:
        return jsonify({"status": "updated"})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/contacts/<int:cid>", methods=["DELETE"])
def delete_contact(cid):
    deleted = db.delete_contact(cid)
    if deleted:
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
