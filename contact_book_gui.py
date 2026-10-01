"""
Ultra-Modern Desktop GUI for Contact Book Application featuring sleek Dark & Light modes,
glowing accent borders, interactive hover effects, and instant theme toggling using Tkinter and SQLite.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox
from database import ContactDatabase


class GlowButton(tk.Frame):
    """Custom Tkinter button widget featuring modern rounded styling, hover transitions, and a vibrant glow border ring."""

    def __init__(
        self,
        parent,
        text="",
        command=None,
        bg_color="#6366F1",
        hover_color="#4F46E5",
        glow_color="#818CF8",
        fg_color="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=9,
        fixed_width=None,
        fixed_height=None,
        disabled_bg="#1E293B",
        disabled_fg="#64748B",
        **kwargs,
    ):
        self.normal_bg = bg_color
        self.hover_bg = hover_color
        self.glow_bg = glow_color
        self.fg_color = fg_color
        self.disabled_bg = disabled_bg
        self.disabled_fg = disabled_fg
        self.command = command
        self.is_disabled = False
        self.use_canvas = bool(fixed_width and fixed_height)

        super().__init__(parent, bg=self.normal_bg, bd=0, highlightthickness=0, **kwargs)

        if self.use_canvas:
            self.config(width=fixed_width, height=fixed_height)
            self.pack_propagate(False)
            self.grid_propagate(False)

        self.inner = tk.Frame(self, bg=self.normal_bg, bd=0, highlightthickness=0)
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)

        if self.use_canvas:
            self.inner.pack_propagate(False)
            self.inner.grid_propagate(False)

            self.canvas = tk.Canvas(
                self.inner,
                bg=self.normal_bg,
                bd=0,
                highlightthickness=0,
                cursor="hand2",
            )
            self.canvas.pack(fill="both", expand=True)

            cx = (fixed_width - 2) / 2
            cy = (fixed_height - 2) / 2
            self.text_id = self.canvas.create_text(
                cx, cy, text=text, fill=self.fg_color, font=font, anchor="center"
            )
            active_widgets = (self, self.inner, self.canvas)
        else:
            self.label = tk.Label(
                self.inner,
                text=text,
                bg=self.normal_bg,
                fg=self.fg_color,
                font=font,
                anchor="center",
                justify="center",
                cursor="hand2",
                padx=padx,
                pady=pady,
            )
            self.label.pack(fill="both", expand=True)
            active_widgets = (self, self.inner, self.label)

        for widget in active_widgets:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, event=None):
        if not self.is_disabled:
            self.config(bg=self.glow_bg)
            self.inner.config(bg=self.hover_bg)
            if self.use_canvas:
                self.canvas.config(bg=self.hover_bg)
            else:
                self.label.config(bg=self.hover_bg)

    def _on_leave(self, event=None):
        if not self.is_disabled:
            self.config(bg=self.normal_bg)
            self.inner.config(bg=self.normal_bg)
            if self.use_canvas:
                self.canvas.config(bg=self.normal_bg)
            else:
                self.label.config(bg=self.normal_bg)

    def _on_click(self, event=None):
        if not self.is_disabled and self.command:
            self.command()

    def set_text(self, text: str):
        if self.use_canvas:
            self.canvas.itemconfig(self.text_id, text=text)
        else:
            self.label.config(text=text)

    def set_state(self, state: str, disabled_bg: str = None, disabled_fg: str = None):
        if disabled_bg:
            self.disabled_bg = disabled_bg
        if disabled_fg:
            self.disabled_fg = disabled_fg

        dbg = getattr(self, "disabled_bg", "#1E293B")
        dfg = getattr(self, "disabled_fg", "#64748B")

        if state == "disabled":
            self.is_disabled = True
            self.config(bg=dbg)
            self.inner.config(bg=dbg)
            if self.use_canvas:
                self.canvas.config(bg=dbg, cursor="")
                self.canvas.itemconfig(self.text_id, fill=dfg)
            else:
                self.label.config(bg=dbg, fg=dfg, cursor="")
        else:
            self.is_disabled = False
            self.config(bg=self.normal_bg)
            self.inner.config(bg=self.normal_bg)
            if self.use_canvas:
                self.canvas.config(bg=self.normal_bg, cursor="hand2")
                self.canvas.itemconfig(self.text_id, fill=self.fg_color)
            else:
                self.label.config(bg=self.normal_bg, fg=self.fg_color, cursor="hand2")

    def update_theme(
        self,
        bg_color: str,
        hover_color: str,
        glow_color: str,
        fg_color: str = "#FFFFFF",
        disabled_bg: str = None,
        disabled_fg: str = None,
    ):
        self.normal_bg = bg_color
        self.hover_bg = hover_color
        self.glow_bg = glow_color
        self.fg_color = fg_color
        if disabled_bg:
            self.disabled_bg = disabled_bg
        if disabled_fg:
            self.disabled_fg = disabled_fg

        if self.is_disabled:
            self.set_state("disabled")
        else:
            self.set_state("normal")


class GlowInput(tk.Frame):
    """Custom input frame wrapper that lights up with an active glowing border ring on hover or focus."""

    def __init__(
        self,
        parent,
        textvariable=None,
        normal_border="#334155",
        glow_border="#6366F1",
        hover_border="#475569",
        bg="#1E293B",
        fg="#F8FAFC",
        font=("Segoe UI", 10),
        **kwargs,
    ):
        self.normal_border = normal_border
        self.glow_border = glow_border
        self.hover_border = hover_border
        self.is_focused = False
        self.bg = bg
        self.fg = fg

        super().__init__(parent, bg=self.normal_border, bd=0, highlightthickness=0, **kwargs)

        self.inner = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.entry = tk.Entry(
            self.inner,
            textvariable=textvariable,
            bg=bg,
            fg=fg,
            insertbackground=fg,
            font=font,
            bd=0,
            relief="flat",
        )
        self.entry.pack(fill="x", expand=True, padx=10, ipady=7)

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Enter>", self._on_enter)
        self.entry.bind("<Leave>", self._on_leave)

    def _on_focus_in(self, event=None):
        self.is_focused = True
        self.config(bg=self.glow_border)

    def _on_focus_out(self, event=None):
        self.is_focused = False
        self.config(bg=self.normal_border)

    def _on_enter(self, event=None):
        if not self.is_focused:
            self.config(bg=self.hover_border)

    def _on_leave(self, event=None):
        if not self.is_focused:
            self.config(bg=self.normal_border)

    def update_theme(self, bg: str, fg: str, normal_border: str, hover_border: str):
        self.bg = bg
        self.fg = fg
        self.normal_border = normal_border
        self.hover_border = hover_border
        self.config(bg=self.normal_border if not self.is_focused else self.glow_border)
        self.inner.config(bg=bg)
        self.entry.config(bg=bg, fg=fg, insertbackground=fg)

    def get(self):
        return self.entry.get()

    def set(self, val: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)


class GlowText(tk.Frame):
    """Custom textarea wrapper featuring glowing active border rings on hover and focus."""

    def __init__(
        self,
        parent,
        height=3,
        normal_border="#334155",
        glow_border="#6366F1",
        hover_border="#475569",
        bg="#1E293B",
        fg="#F8FAFC",
        font=("Segoe UI", 10),
        **kwargs,
    ):
        self.normal_border = normal_border
        self.glow_border = glow_border
        self.hover_border = hover_border
        self.is_focused = False
        self.bg = bg
        self.fg = fg

        super().__init__(parent, bg=self.normal_border, bd=0, highlightthickness=0, **kwargs)

        self.inner = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.text = tk.Text(
            self.inner,
            height=height,
            bg=bg,
            fg=fg,
            insertbackground=fg,
            font=font,
            bd=0,
            relief="flat",
            wrap="word",
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=8)

        self.text.bind("<FocusIn>", self._on_focus_in)
        self.text.bind("<FocusOut>", self._on_focus_out)
        self.text.bind("<Enter>", self._on_enter)
        self.text.bind("<Leave>", self._on_leave)

    def _on_focus_in(self, event=None):
        self.is_focused = True
        self.config(bg=self.glow_border)

    def _on_focus_out(self, event=None):
        self.is_focused = False
        self.config(bg=self.normal_border)

    def _on_enter(self, event=None):
        if not self.is_focused:
            self.config(bg=self.hover_border)

    def _on_leave(self, event=None):
        if not self.is_focused:
            self.config(bg=self.normal_border)

    def update_theme(self, bg: str, fg: str, normal_border: str, hover_border: str):
        self.bg = bg
        self.fg = fg
        self.normal_border = normal_border
        self.hover_border = hover_border
        self.config(bg=self.normal_border if not self.is_focused else self.glow_border)
        self.inner.config(bg=bg)
        self.text.config(bg=bg, fg=fg, insertbackground=fg)

    def get(self, start="1.0", end=tk.END):
        return self.text.get(start, end)

    def delete(self, start="1.0", end=tk.END):
        self.text.delete(start, end)

    def insert(self, index, chars: str):
        self.text.insert(index, chars)


class ContactBookGUI:
    """Tkinter Desktop Graphical User Interface with Dark & Light theme switching."""

    # Theme Palettes
    THEMES = {
        "dark": {
            "BG_MAIN": "#0B0F19",
            "BG_CARD": "#151C2C",
            "BG_HEADER": "#0D1527",
            "BORDER_CARD": "#1E293B",
            "TEXT_PRIMARY": "#F8FAFC",
            "TEXT_MUTED": "#94A3B8",
            "INPUT_BG": "#1E293B",
            "INPUT_BORDER": "#334155",
            "INPUT_HOVER": "#475569",
            "TREE_BG": "#151C2C",
            "TREE_FG": "#F8FAFC",
            "TREE_HEADING_BG": "#1E293B",
            "TREE_HEADING_FG": "#94A3B8",
            "TREE_SELECT_BG": "#312E81",
            "TREE_SELECT_FG": "#F8FAFC",
            "STATUS_BG": "#0D1527",
            "ICON_BG": "#1E1B4B",
            "ICON_FG": "#A5B4FC",
            "TOGGLE_BTN_TXT": "☀",
            "TOGGLE_BG": "#312E81",
            "TOGGLE_HOVER": "#4338CA",
            "TOGGLE_GLOW": "#818CF8",
            "DISABLED_BG": "#1E293B",
            "DISABLED_FG": "#64748B",
        },
        "light": {
            "BG_MAIN": "#F1F5F9",
            "BG_CARD": "#FFFFFF",
            "BG_HEADER": "#1E293B",
            "BORDER_CARD": "#CBD5E1",
            "TEXT_PRIMARY": "#0F172A",
            "TEXT_MUTED": "#64748B",
            "INPUT_BG": "#F8FAFC",
            "INPUT_BORDER": "#CBD5E1",
            "INPUT_HOVER": "#94A3B8",
            "TREE_BG": "#FFFFFF",
            "TREE_FG": "#0F172A",
            "TREE_HEADING_BG": "#F1F5F9",
            "TREE_HEADING_FG": "#475569",
            "TREE_SELECT_BG": "#DBEAFE",
            "TREE_SELECT_FG": "#1E40AF",
            "STATUS_BG": "#E2E8F0",
            "ICON_BG": "#334155",
            "ICON_FG": "#60A5FA",
            "TOGGLE_BTN_TXT": "🌙",
            "TOGGLE_BG": "#0284C7",
            "TOGGLE_HOVER": "#0369A1",
            "TOGGLE_GLOW": "#38BDF8",
            "DISABLED_BG": "#E2E8F0",
            "DISABLED_FG": "#94A3B8",
        },
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Contact Book Pro")
        self.root.geometry("960x650")
        self.root.minsize(850, 540)

        # Initialize Database Manager
        self.db = ContactDatabase()
        self.db.seed_sample_data_if_empty()

        # State Variables
        self.selected_contact_id = None
        self.contacts_data = []
        self.current_theme = "dark"

        # Brand Accent Colors
        self.COLOR_INDIGO = "#6366F1"
        self.COLOR_CYAN = "#0EA5E9"
        self.COLOR_EMERALD = "#10B981"
        self.COLOR_ROSE = "#F43F5E"

        self.root.configure(bg=self.THEMES["dark"]["BG_MAIN"])

        # Configure Styles
        self._setup_styles()

        # Build UI Components
        self._build_header()
        self._build_main_layout()
        self._build_statusbar()

        # Initial Load
        self.refresh_contact_list()

    def _setup_styles(self):
        """Applies custom styling to ttk widgets."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        t = self.THEMES[self.current_theme]
        self._apply_treeview_style(t)

        self.style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#1E293B",
            darkcolor="#1E293B",
            lightcolor="#1E293B",
            troughcolor=t["BG_CARD"],
            bordercolor=t["BG_CARD"],
            arrowcolor="#94A3B8",
        )

    def _apply_treeview_style(self, t: dict):
        """Updates Treeview colors dynamically for active theme."""
        self.style.configure(
            "Treeview",
            background=t["TREE_BG"],
            foreground=t["TREE_FG"],
            fieldbackground=t["TREE_BG"],
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0,
            relief="flat",
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background=t["TREE_HEADING_BG"],
            foreground=t["TREE_HEADING_FG"],
            relief="flat",
            padding=8,
        )
        self.style.map(
            "Treeview",
            background=[("selected", t["TREE_SELECT_BG"])],
            foreground=[("selected", t["TREE_SELECT_FG"])],
        )

    def _build_header(self):
        """Creates the header frame with title, status badges, and Theme Toggle button."""
        t = self.THEMES[self.current_theme]

        self.header_frame = tk.Frame(self.root, bg=t["BG_HEADER"], height=75, bd=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.header_glow = tk.Frame(self.root, bg=self.COLOR_INDIGO, height=2)
        self.header_glow.pack(fill="x", side="top")

        # Left Branding Container
        self.brand_frame = tk.Frame(self.header_frame, bg=t["BG_HEADER"])
        self.brand_frame.pack(side="left", fill="y", padx=20)

        self.icon_badge = tk.Frame(self.brand_frame, bg=self.COLOR_INDIGO, padx=1, pady=1)
        self.icon_badge.pack(side="left", pady=15, padx=(0, 12))

        self.icon_inner = tk.Frame(self.icon_badge, bg=t["ICON_BG"], padx=10, pady=6)
        self.icon_inner.pack(fill="both", expand=True)

        self.icon_lbl = tk.Label(self.icon_inner, text="👥", font=("Segoe UI", 14), bg=t["ICON_BG"], fg=t["ICON_FG"])
        self.icon_lbl.pack()

        self.title_box = tk.Frame(self.brand_frame, bg=t["BG_HEADER"])
        self.title_box.pack(side="left", fill="y", pady=16)

        self.title_label = tk.Label(
            self.title_box,
            text="CONTACT BOOK",
            font=("Segoe UI", 14, "bold"),
            bg=t["BG_HEADER"],
            fg=t["TEXT_PRIMARY"],
            anchor="w",
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.title_box,
            text="Smart Contact Directory",
            font=("Segoe UI", 9),
            bg=t["BG_HEADER"],
            fg=t["TEXT_MUTED"],
            anchor="w",
        )
        self.subtitle_label.pack(anchor="w")

        # Right Side Badges & Theme Toggle Button
        self.badges_frame = tk.Frame(self.header_frame, bg=t["BG_HEADER"])
        self.badges_frame.pack(side="right", fill="y", padx=20, pady=16)

        # Theme Toggle Button (Fixed 34x34 compact square icon button)
        self.theme_toggle_btn = GlowButton(
            self.badges_frame,
            text=t["TOGGLE_BTN_TXT"],
            command=self.toggle_theme,
            bg_color=t["TOGGLE_BG"],
            hover_color=t["TOGGLE_HOVER"],
            glow_color=t["TOGGLE_GLOW"],
            font=("Segoe UI", 11, "bold"),
            fixed_width=34,
            fixed_height=34,
        )
        self.theme_toggle_btn.pack(side="right", padx=(10, 0))

        self.db_status_badge = tk.Label(
            self.badges_frame,
            text="⚡ DB Active",
            font=("Segoe UI", 9, "bold"),
            bg="#064E3B",
            fg="#6EE7B7",
            padx=10,
            pady=4,
        )
        self.db_status_badge.pack(side="right", padx=(8, 0))

        self.badge_count = tk.Label(
            self.badges_frame,
            text="👥 0 Contacts",
            font=("Segoe UI", 9, "bold"),
            bg="#312E81",
            fg="#C7D2FE",
            padx=10,
            pady=4,
        )
        self.badge_count.pack(side="right")

    def _build_main_layout(self):
        """Builds split panels for list and form."""
        t = self.THEMES[self.current_theme]

        self.main_container = tk.Frame(self.root, bg=t["BG_MAIN"], padx=18, pady=18)
        self.main_container.pack(fill="both", expand=True)

        # --- LEFT PANEL: Search & Contact List ---
        self.left_card_glow = tk.Frame(self.main_container, bg=t["BORDER_CARD"], bd=0, highlightthickness=0)
        self.left_card_glow.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.left_panel = tk.Frame(self.left_card_glow, bg=t["BG_CARD"], bd=0, highlightthickness=0)
        self.left_panel.pack(fill="both", expand=True, padx=1, pady=1)

        # Search Frame
        self.search_frame = tk.Frame(self.left_panel, bg=t["BG_CARD"], padx=16, pady=16)
        self.search_frame.pack(fill="x")

        self.search_header = tk.Frame(self.search_frame, bg=t["BG_CARD"])
        self.search_header.pack(fill="x", pady=(0, 10))

        self.search_title = tk.Label(
            self.search_header, text="SAVED CONTACTS", font=("Segoe UI", 11, "bold"), bg=t["BG_CARD"], fg=t["TEXT_PRIMARY"]
        )
        self.search_title.pack(side="left")

        self.count_label = tk.Label(
            self.search_header, text="Showing 0 items", font=("Segoe UI", 9), bg=t["BG_CARD"], fg=t["TEXT_MUTED"]
        )
        self.count_label.pack(side="right")

        # Search Box Frame
        self.search_box = tk.Frame(self.search_frame, bg=t["INPUT_BG"], bd=0)
        self.search_box.pack(fill="x")

        self.search_glow_wrapper = tk.Frame(self.search_box, bg=t["INPUT_BORDER"], bd=0)
        self.search_glow_wrapper.pack(fill="x", padx=0, pady=0)

        self.search_inner = tk.Frame(self.search_glow_wrapper, bg=t["INPUT_BG"], bd=0)
        self.search_inner.pack(fill="x", padx=1, pady=1)

        self.search_icon = tk.Label(self.search_inner, text="🔍", bg=t["INPUT_BG"], fg=self.COLOR_CYAN, font=("Segoe UI", 10))
        self.search_icon.pack(side="left", padx=(10, 4))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        self.search_entry = tk.Entry(
            self.search_inner,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg=t["INPUT_BG"],
            fg=t["TEXT_PRIMARY"],
            insertbackground=t["TEXT_PRIMARY"],
            bd=0,
            relief="flat",
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=7)

        self.search_entry.bind("<FocusIn>", lambda e: self.search_glow_wrapper.config(bg=self.COLOR_CYAN))
        self.search_entry.bind("<FocusOut>", lambda e: self.search_glow_wrapper.config(bg=self.THEMES[self.current_theme]["INPUT_BORDER"]))
        self.search_entry.bind("<Enter>", lambda e: self._hover_search(True))
        self.search_entry.bind("<Leave>", lambda e: self._hover_search(False))

        self.clear_search_btn = tk.Label(
            self.search_inner,
            text=" ✕ ",
            bg=t["INPUT_BG"],
            fg=t["TEXT_MUTED"],
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.clear_search_btn.pack(side="right", padx=8)
        self.clear_search_btn.bind("<Button-1>", lambda e: self._clear_search())
        self.clear_search_btn.bind("<Enter>", lambda e: self.clear_search_btn.config(fg=self.COLOR_ROSE))
        self.clear_search_btn.bind("<Leave>", lambda e: self.clear_search_btn.config(fg=self.THEMES[self.current_theme]["TEXT_MUTED"]))

        # Treeview Contact List
        self.list_frame = tk.Frame(self.left_panel, bg=t["BG_CARD"], padx=16, pady=0)
        self.list_frame.pack(fill="both", expand=True, pady=(0, 16))

        columns = ("name", "phone")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("name", text="FULL NAME", anchor="w")
        self.tree.heading("phone", text="PHONE NUMBER", anchor="w")
        self.tree.column("name", width=220, minwidth=130, stretch=True)
        self.tree.column("phone", width=170, minwidth=110, stretch=True)

        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_contact_selected)

        # --- RIGHT PANEL: Contact Details & Form ---
        self.right_card_glow = tk.Frame(self.main_container, bg=t["BORDER_CARD"], bd=0, highlightthickness=0)
        self.right_card_glow.pack(side="right", fill="both", expand=False, padx=(10, 0))
        self.right_card_glow.config(width=430)

        self.right_panel = tk.Frame(self.right_card_glow, bg=t["BG_CARD"], bd=0, highlightthickness=0)
        self.right_panel.pack(fill="both", expand=True, padx=1, pady=1)

        self.form_container = tk.Frame(self.right_panel, bg=t["BG_CARD"], padx=24, pady=18)
        self.form_container.pack(fill="both", expand=True)

        self.form_header_label = tk.Label(
            self.form_container,
            text="✨ Add New Contact",
            font=("Segoe UI", 13, "bold"),
            bg=t["BG_CARD"],
            fg=t["TEXT_PRIMARY"],
        )
        self.form_header_label.pack(anchor="w", pady=(0, 16))

        # Form Inputs
        self.lbl_name, self.name_input = self._create_glow_field(self.form_container, "👤  Full Name *", "#6366F1")
        self.lbl_phone, self.phone_input = self._create_glow_field(self.form_container, "📞  Phone Number *", "#6366F1")
        self.lbl_email, self.email_input = self._create_glow_field(self.form_container, "✉️  Email Address", "#0EA5E9")

        # Address Text Field
        self.lbl_addr = tk.Label(
            self.form_container, text="📍  Physical Address", font=("Segoe UI", 9, "bold"), bg=t["BG_CARD"], fg=t["TEXT_MUTED"]
        )
        self.lbl_addr.pack(anchor="w", pady=(10, 4))

        self.address_input = GlowText(
            self.form_container,
            height=3,
            normal_border=t["INPUT_BORDER"],
            glow_border=self.COLOR_INDIGO,
            hover_border=t["INPUT_HOVER"],
            bg=t["INPUT_BG"],
            fg=t["TEXT_PRIMARY"],
        )
        self.address_input.pack(fill="x", pady=(0, 18))

        # Action Buttons
        self.btn_frame = tk.Frame(self.form_container, bg=t["BG_CARD"])
        self.btn_frame.pack(fill="x", pady=(8, 0))

        self.save_btn = GlowButton(
            self.btn_frame,
            text="➕ Save Contact",
            command=self.save_contact,
            bg_color=self.COLOR_INDIGO,
            hover_color="#4F46E5",
            glow_color="#818CF8",
            disabled_bg=t["DISABLED_BG"],
            disabled_fg=t["DISABLED_FG"],
        )
        self.save_btn.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.delete_btn = GlowButton(
            self.btn_frame,
            text="🗑️ Delete",
            command=self.delete_contact,
            bg_color=self.COLOR_ROSE,
            hover_color="#E11D48",
            glow_color="#FDA4AF",
            disabled_bg=t["DISABLED_BG"],
            disabled_fg=t["DISABLED_FG"],
        )
        self.delete_btn.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.delete_btn.set_state("disabled", disabled_bg=t["DISABLED_BG"], disabled_fg=t["DISABLED_FG"])

        self.clear_btn = GlowButton(
            self.btn_frame,
            text="🔄 Clear / New",
            command=self.reset_form,
            bg_color=self.COLOR_CYAN,
            hover_color="#0284C7",
            glow_color="#7DD3FC",
            disabled_bg=t["DISABLED_BG"],
            disabled_fg=t["DISABLED_FG"],
        )
        self.clear_btn.grid(row=1, column=1, sticky="ew", padx=(5, 0))

        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)

    def _create_glow_field(self, parent: tk.Widget, label_text: str, glow_color: str):
        """Helper to create labeled glowing input fields."""
        t = self.THEMES[self.current_theme]
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 9, "bold"), bg=t["BG_CARD"], fg=t["TEXT_MUTED"])
        lbl.pack(anchor="w", pady=(10, 4))

        input_widget = GlowInput(
            parent,
            normal_border=t["INPUT_BORDER"],
            glow_border=glow_color,
            hover_border=t["INPUT_HOVER"],
            bg=t["INPUT_BG"],
            fg=t["TEXT_PRIMARY"],
        )
        input_widget.pack(fill="x")
        return lbl, input_widget

    def _hover_search(self, is_entering: bool):
        t = self.THEMES[self.current_theme]
        if not self.search_entry.focus_get() == self.search_entry:
            self.search_glow_wrapper.config(bg=self.COLOR_CYAN if is_entering else t["INPUT_BORDER"])

    def _build_statusbar(self):
        """Bottom status bar."""
        t = self.THEMES[self.current_theme]
        self.statusbar_frame = tk.Frame(self.root, bg=t["STATUS_BG"], height=30)
        self.statusbar_frame.pack(fill="x", side="bottom")

        self.status_icon = tk.Label(
            self.statusbar_frame, text="🟢", font=("Segoe UI", 8), bg=t["STATUS_BG"], fg=self.COLOR_EMERALD
        )
        self.status_icon.pack(side="left", padx=(15, 4))

        self.statusbar = tk.Label(
            self.statusbar_frame,
            text="System Ready",
            font=("Segoe UI", 9),
            bg=t["STATUS_BG"],
            fg=t["TEXT_MUTED"],
            anchor="w",
        )
        self.statusbar.pack(side="left", fill="x", expand=True)

    def toggle_theme(self):
        """Switches between Dark Mode and Light Mode instantly."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        t = self.THEMES[self.current_theme]

        # 1. Root window
        self.root.configure(bg=t["BG_MAIN"])

        # 2. Header
        self.header_frame.config(bg=t["BG_HEADER"])
        self.brand_frame.config(bg=t["BG_HEADER"])
        self.icon_inner.config(bg=t["ICON_BG"])
        self.icon_lbl.config(bg=t["ICON_BG"], fg=t["ICON_FG"])
        self.title_box.config(bg=t["BG_HEADER"])
        self.title_label.config(bg=t["BG_HEADER"], fg=t["TEXT_PRIMARY"])
        self.subtitle_label.config(bg=t["BG_HEADER"], fg=t["TEXT_MUTED"])
        self.badges_frame.config(bg=t["BG_HEADER"])

        # Update Theme Toggle Button
        self.theme_toggle_btn.set_text(t["TOGGLE_BTN_TXT"])
        self.theme_toggle_btn.update_theme(t["TOGGLE_BG"], t["TOGGLE_HOVER"], t["TOGGLE_GLOW"])

        # 3. Main container & cards
        self.main_container.config(bg=t["BG_MAIN"])
        self.left_card_glow.config(bg=t["BORDER_CARD"])
        self.left_panel.config(bg=t["BG_CARD"])
        self.right_card_glow.config(bg=t["BORDER_CARD"])
        self.right_panel.config(bg=t["BG_CARD"])
        self.form_container.config(bg=t["BG_CARD"])

        # 4. Search Section
        self.search_frame.config(bg=t["BG_CARD"])
        self.search_header.config(bg=t["BG_CARD"])
        self.search_title.config(bg=t["BG_CARD"], fg=t["TEXT_PRIMARY"])
        self.count_label.config(bg=t["BG_CARD"], fg=t["TEXT_MUTED"])
        self.search_box.config(bg=t["INPUT_BG"])
        self.search_glow_wrapper.config(bg=t["INPUT_BORDER"])
        self.search_inner.config(bg=t["INPUT_BG"])
        self.search_icon.config(bg=t["INPUT_BG"])
        self.search_entry.config(bg=t["INPUT_BG"], fg=t["TEXT_PRIMARY"], insertbackground=t["TEXT_PRIMARY"])
        self.clear_search_btn.config(bg=t["INPUT_BG"], fg=t["TEXT_MUTED"])

        # 5. Treeview List
        self.list_frame.config(bg=t["BG_CARD"])
        self._apply_treeview_style(t)

        # 6. Form Section
        header_fg = self.COLOR_CYAN if self.selected_contact_id else t["TEXT_PRIMARY"]
        self.form_header_label.config(bg=t["BG_CARD"], fg=header_fg)

        self.lbl_name.config(bg=t["BG_CARD"], fg=t["TEXT_MUTED"])
        self.lbl_phone.config(bg=t["BG_CARD"], fg=t["TEXT_MUTED"])
        self.lbl_email.config(bg=t["BG_CARD"], fg=t["TEXT_MUTED"])
        self.lbl_addr.config(bg=t["BG_CARD"], fg=t["TEXT_MUTED"])

        self.name_input.update_theme(t["INPUT_BG"], t["TEXT_PRIMARY"], t["INPUT_BORDER"], t["INPUT_HOVER"])
        self.phone_input.update_theme(t["INPUT_BG"], t["TEXT_PRIMARY"], t["INPUT_BORDER"], t["INPUT_HOVER"])
        self.email_input.update_theme(t["INPUT_BG"], t["TEXT_PRIMARY"], t["INPUT_BORDER"], t["INPUT_HOVER"])
        self.address_input.update_theme(t["INPUT_BG"], t["TEXT_PRIMARY"], t["INPUT_BORDER"], t["INPUT_HOVER"])

        # 6b. Action Buttons & Button Frame
        self.btn_frame.config(bg=t["BG_CARD"])
        self.save_btn.update_theme(self.COLOR_INDIGO, "#4F46E5", "#818CF8", "#FFFFFF", t["DISABLED_BG"], t["DISABLED_FG"])
        self.delete_btn.update_theme(self.COLOR_ROSE, "#E11D48", "#FDA4AF", "#FFFFFF", t["DISABLED_BG"], t["DISABLED_FG"])
        self.clear_btn.update_theme(self.COLOR_CYAN, "#0284C7", "#7DD3FC", "#FFFFFF", t["DISABLED_BG"], t["DISABLED_FG"])

        # 7. Status bar
        self.statusbar_frame.config(bg=t["STATUS_BG"])
        self.status_icon.config(bg=t["STATUS_BG"])
        self.statusbar.config(bg=t["STATUS_BG"], fg=t["TEXT_MUTED"])

        self.set_status(f"Switched to {self.current_theme.capitalize()} Mode")

    def set_status(self, message: str, is_error: bool = False):
        """Updates status text with dynamic glow state indicator."""
        t = self.THEMES[self.current_theme]
        if is_error:
            self.status_icon.config(text="🔴", fg=self.COLOR_ROSE)
            self.statusbar.config(text=message, fg=self.COLOR_ROSE)
        else:
            self.status_icon.config(text="🟢", fg=self.COLOR_EMERALD)
            self.statusbar.config(text=message, fg=t["TEXT_PRIMARY"])

    def refresh_contact_list(self, query: str = ""):
        """Fetches contacts from SQLite and updates Treeview with glow highlights."""
        self.tree.delete(*self.tree.get_children())
        if query:
            self.contacts_data = self.db.search_contacts(query)
        else:
            self.contacts_data = self.db.get_all_contacts()

        for c in self.contacts_data:
            self.tree.insert("", "end", iid=str(c["id"]), values=(c["name"], c["phone"]))

        total = len(self.contacts_data)
        self.badge_count.config(text=f"👥 {total} Contact(s)")

        if query:
            self.count_label.config(text=f"Found {total} item(s)")
            self.set_status(f"Search results: {total} matching contact(s) found.")
        else:
            self.count_label.config(text=f"Total: {total} item(s)")
            self.set_status("System Ready")

    def _on_search_change(self, *args):
        query = self.search_var.get()
        self.refresh_contact_list(query)

    def _clear_search(self):
        self.search_var.set("")

    def _on_contact_selected(self, event):
        """Populates fields when a contact item is selected."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item_id = int(selected_items[0])
        contact = self.db.get_contact_by_id(item_id)
        if not contact:
            return

        self.selected_contact_id = item_id
        self.name_input.set(contact["name"])
        self.phone_input.set(contact["phone"])
        self.email_input.set(contact["email"])
        self.address_input.delete("1.0", tk.END)
        self.address_input.insert("1.0", contact["address"])

        self.form_header_label.config(text="✏️ Edit Contact", fg=self.COLOR_CYAN)
        self.save_btn.set_text("💾 Save Changes")
        self.delete_btn.set_state("normal")
        self.set_status(f"Selected contact: '{contact['name']}'")

    def reset_form(self):
        """Resets inputs to prepare for creating a new contact."""
        t = self.THEMES[self.current_theme]
        self.selected_contact_id = None
        self.tree.selection_remove(self.tree.selection())
        self.name_input.set("")
        self.phone_input.set("")
        self.email_input.set("")
        self.address_input.delete("1.0", tk.END)

        self.form_header_label.config(text="✨ Add New Contact", fg=t["TEXT_PRIMARY"])
        self.save_btn.set_text("➕ Save Contact")
        self.delete_btn.set_state("disabled")
        self.set_status("Form cleared. Ready for new contact entry.")

    def _validate_inputs(self) -> bool:
        """Validates entry values."""
        name = self.name_input.get().strip()
        phone = self.phone_input.get().strip()
        email = self.email_input.get().strip()

        if not name:
            messagebox.showwarning("Validation Warning", "Contact Full Name is required.")
            return False

        if not phone:
            messagebox.showwarning("Validation Warning", "Phone Number is required.")
            return False

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validation Warning", "Please enter a valid email address.")
            return False

        return True

    def save_contact(self):
        """Handles adding or updating contact entries in database."""
        if not self._validate_inputs():
            return

        name = self.name_input.get().strip()
        phone = self.phone_input.get().strip()
        email = self.email_input.get().strip()
        address = self.address_input.get("1.0", tk.END).strip()

        try:
            if self.selected_contact_id is None:
                cid = self.db.add_contact(name, phone, email, address)
                self.refresh_contact_list(self.search_var.get())
                self.reset_form()
                self.set_status(f"✅ Contact '{name}' added successfully!")
                messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            else:
                updated = self.db.update_contact(self.selected_contact_id, name, phone, email, address)
                if updated:
                    self.refresh_contact_list(self.search_var.get())
                    self.tree.selection_set(str(self.selected_contact_id))
                    self.set_status(f"✅ Contact '{name}' updated successfully!")
                    messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
                else:
                    messagebox.showerror("Error", "Failed to update contact record.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_contact(self):
        """Deletes selected contact after user confirmation."""
        if self.selected_contact_id is None:
            return

        name = self.name_input.get().strip()
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete contact '{name}'?", icon="warning"
        )
        if confirm:
            deleted = self.db.delete_contact(self.selected_contact_id)
            if deleted:
                self.refresh_contact_list(self.search_var.get())
                self.reset_form()
                self.set_status(f"🗑️ Contact '{name}' deleted.", is_error=True)
                messagebox.showinfo("Deleted", f"Contact '{name}' has been deleted.")
            else:
                messagebox.showerror("Error", "Could not delete contact.")


def main():
    root = tk.Tk()
    app = ContactBookGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
