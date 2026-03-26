from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable

from .db import Database, User
from .reports import build_student_report, export_report_to_pdf, mark_to_grade


def _setup_theme(root: tk.Misc) -> None:
    """Configure a modern web-app style system theme."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Modern Web-App Palette (Slate/Indigo)
    bg_main = "#f1f5f9"       # Slate 100
    bg_card = "#ffffff"       # White
    sidebar_bg = "#0f172a"    # Slate 900 (Deeper for web feel)
    accent = "#4f46e5"        # Indigo 600
    accent_hover = "#4338ca"  # Indigo 700
    text_primary = "#0f172a"  # Slate 900
    text_secondary = "#475569" # Slate 600
    border_color = "#e2e8f0"  # Slate 200

    root.configure(bg=bg_main)

    # General Frame Styles
    style.configure("App.TFrame", background=bg_main)
    style.configure("Card.TFrame", background=bg_card, borderwidth=2, relief="solid")
    style.configure("Sidebar.TFrame", background=sidebar_bg)
    style.configure("Header.TFrame", background=bg_card, borderwidth=2, relief="solid")

    # Label Styles
    style.configure("TLabel", background=bg_main, foreground=text_primary, font=("Inter", 10))
    style.configure("Card.TLabel", background=bg_card, foreground=text_primary, font=("Inter", 10))
    style.configure("Header.TLabel", background=bg_card, foreground=text_primary, font=("Inter", 12, "bold"))
    style.configure("Sidebar.TLabel", background=sidebar_bg, foreground="white", font=("Inter", 12, "bold"))
    style.configure("Muted.TLabel", background=bg_main, foreground=text_secondary, font=("Inter", 9))
    style.configure("CardMuted.TLabel", background=bg_card, foreground=text_secondary, font=("Inter", 9))

    # Button Styles (Modern Flat Web Buttons)
    style.configure(
        "Primary.TButton",
        background=accent,
        foreground="white",
        font=("Inter", 10, "bold"),
        padding=(12, 6),
        borderwidth=0,
    )
    style.map("Primary.TButton", background=[("active", accent_hover)])

    style.configure(
        "Secondary.TButton",
        background="#ffffff",
        foreground=text_primary,
        font=("Inter", 10),
        padding=(12, 6),
        borderwidth=1,
        relief="solid",
    )
    style.map("Secondary.TButton", background=[("active", "#f8fafc")])

    style.configure(
        "Danger.TButton",
        background="#fee2e2",
        foreground="#dc2626",
        font=("Inter", 10, "bold"),
        padding=(12, 6),
        borderwidth=0,
    )
    style.map("Danger.TButton", background=[("active", "#fecaca")])

    style.configure(
        "Nav.TButton",
        background=sidebar_bg,
        foreground="#94a3b8",
        font=("Inter", 10),
        padding=(20, 10),
        borderwidth=0,
        anchor="w",
    )
    style.map(
        "Nav.TButton",
        background=[("active", "#1e293b")],
        foreground=[("active", "white")],
    )
    style.configure(
        "NavActive.TButton",
        background="#1e293b",
        foreground="white",
        font=("Inter", 10, "bold"),
        padding=(20, 10),
        borderwidth=0,
        anchor="w",
    )

    # Modern Data Table Styling
    style.configure(
        "Treeview",
        background=bg_card,
        foreground=text_primary,
        fieldbackground=bg_card,
        rowheight=30,
        font=("Inter", 10),
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background="#f8fafc",
        foreground=text_secondary,
        font=("Inter", 9, "bold"),
        relief="flat",
        padding=12,
    )
    style.map("Treeview", background=[("selected", "#eef2ff")], foreground=[("selected", accent)])

    # Modern Entry Styles
    style.configure("TEntry", padding=8, relief="flat")
    style.configure("TCombobox", padding=8)

    # Dashboard/Widgets
    style.configure("StatCard.TFrame", background=bg_card, borderwidth=2, relief="solid", padding=3)
    style.configure("StatTitle.TLabel", background=bg_card, foreground=text_secondary, font=("Inter", 9, "bold"))
    style.configure("StatValue.TLabel", background=bg_card, foreground=accent, font=("Inter", 24, "bold"))
    style.configure("StatLabel.TLabel", background=bg_card, foreground=text_primary, font=("Inter", 11, "bold"))
    style.configure("Welcome.TLabel", background=bg_main, foreground=text_primary, font=("Inter", 18, "bold"))
    style.configure("Subtitle.TLabel", background=bg_main, foreground=text_secondary, font=("Inter", 10))
    
    # Dashboard section styles
    style.configure("DashboardSection.TFrame", background=bg_main, borderwidth=0, relief="flat")
    style.configure("DashboardCard.TFrame", background=bg_card, borderwidth=2, relief="solid", padding=20)


    # Login Screen Refinement
    style.configure("Login.TFrame", background=bg_card)
    style.configure("Login.Title.TLabel", background=bg_card, foreground=text_primary, font=("Inter", 24, "bold"))




class LoginWindow(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.user: User | None = None

        _setup_theme(self)

        self.title("SMS - Modern Login")
        self.geometry("450x600")
        self.resizable(False, False)

        # Center window
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - 450) // 2
        y = (sh - 600) // 2
        self.geometry(f"450x600+{x}+{y}")

        # Glass-like effect simulation
        outer = ttk.Frame(self, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        container = ttk.Frame(outer, style="Login.TFrame", padding=50)
        container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=500)

        ttk.Label(container, text="Welcome", style="Login.Title.TLabel").pack(pady=(0, 5))
        ttk.Label(container, text="Sign in to continue", style="CardMuted.TLabel").pack(pady=(0, 40))

        # Form
        ttk.Label(container, text="USERNAME", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        self.username = ttk.Entry(container)
        self.username.pack(fill="x", pady=(0, 25))

        ttk.Label(container, text="PASSWORD", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        self.password = ttk.Entry(container, show="•")
        self.password.pack(fill="x", pady=(0, 40))

        ttk.Button(container, text="Sign In", style="Primary.TButton", command=self._login).pack(fill="x", pady=(0, 25))

        # Register link
        reg_frame = ttk.Frame(container, style="Login.TFrame")
        reg_frame.pack(fill="x")
        ttk.Label(reg_frame, text="New here?", style="CardMuted.TLabel").pack(side="left")
        reg_btn = tk.Label(reg_frame, text="Create Account", fg="#6366f1", bg="white", font=("Segoe UI", 9, "bold"), cursor="hand2")
        reg_btn.pack(side="left", padx=8)
        reg_btn.bind("<Button-1>", lambda e: self._open_register_dialog())

        self.bind("<Return>", lambda e: self._login())
        self.username.focus_set()

    def _open_register_dialog(self) -> None:
        win = tk.Toplevel(self)
        win.title("Create Account")
        win.geometry("450x600")
        win.resizable(False, False)
        _setup_theme(win)

        outer = ttk.Frame(win, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        container = ttk.Frame(outer, style="Login.TFrame", padding=40)
        container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=520)

        ttk.Label(container, text="Join Us", style="Login.Title.TLabel").pack(pady=(0, 5))
        ttk.Label(container, text="Create a new account", style="CardMuted.TLabel").pack(pady=(0, 30))

        ttk.Label(container, text="USERNAME", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        uname = ttk.Entry(container)
        uname.pack(fill="x", pady=(0, 15))

        ttk.Label(container, text="PASSWORD", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        pw1 = ttk.Entry(container, show="•")
        pw1.pack(fill="x", pady=(0, 15))

        ttk.Label(container, text="CONFIRM PASSWORD", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        pw2 = ttk.Entry(container, show="•")
        pw2.pack(fill="x", pady=(0, 30))

        def submit():
            username = uname.get().strip()
            p1, p2 = pw1.get(), pw2.get()
            if not username or not p1:
                messagebox.showwarning("Missing", "Please fill all fields.")
                return
            if p1 != p2:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return
            try:
                self.db.create_user(username, p1, "staff")
                messagebox.showinfo("Success", "Account created successfully!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Create Account", style="Primary.TButton", command=submit).pack(fill="x")
        ttk.Button(container, text="Back to Login", style="Secondary.TButton", command=win.destroy).pack(fill="x", pady=(15, 0))


    def _login(self) -> None:
        u = self.username.get().strip()
        p = self.password.get()
        if not u or not p:
            messagebox.showwarning("Missing", "Enter username and password.")
            return
        user = self.db.authenticate(u, p)
        if not user:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return
        self.user = user
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self, db: Database, user: User):
        super().__init__()
        self.db = db
        self.user = user
        _setup_theme(self)

        self.title(f"SMS - {user.username} ({user.role})")
        self.geometry("1200x750")

        self._build_ui()
        self._refresh_all()

    def _build_ui(self) -> None:
        # Sidebar (Web Sidebar style)
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Logo Section
        brand_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding=(25, 40))
        brand_frame.pack(fill="x")
        ttk.Label(brand_frame, text="SMS", style="Sidebar.TLabel", foreground="#6366f1").pack(side="left")
        ttk.Label(brand_frame, text="PRO", style="Sidebar.TLabel").pack(side="left")

        self.nav_buttons: dict[str, ttk.Button] = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("students", "👥  Students"),
            ("marks", "📝  Marks & Grades"),
            ("graphs", "📊  Analytics"),
            ("reports", "📄  Reports"),
        ]
        if self.user.role == "admin":
            nav_items.append(("users", "⚙️  User Management"))

        for key, label in nav_items:
            btn = ttk.Button(
                self.sidebar,
                text=label,
                style="Nav.TButton",
                command=lambda k=key: self._show_page(k),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = btn

        # Logout at bottom
        logout_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding=10)
        logout_frame.pack(side="bottom", fill="x")
        ttk.Button(
            logout_frame,
            text="🚪  Logout",
            style="Nav.TButton",
            command=self._logout
        ).pack(fill="x", pady=20)

        # Main Content Area
        self.main_content = ttk.Frame(self, style="App.TFrame")
        self.main_content.pack(side="right", fill="both", expand=True)

        # Sticky Web Header
        self.header = ttk.Frame(self.main_content, style="Header.TFrame", padding=(30, 20))
        self.header.pack(fill="x")
        
        # Breadcrumb-style title
        title_frame = ttk.Frame(self.header, style="Header.TFrame")
        title_frame.pack(side="left")
        ttk.Label(title_frame, text="Pages", style="Muted.TLabel").pack(side="left")
        ttk.Label(title_frame, text=" / ", style="Muted.TLabel").pack(side="left")
        self.header_title = ttk.Label(title_frame, text="Dashboard", style="Header.TLabel")
        self.header_title.pack(side="left")

        user_info_frame = ttk.Frame(self.header, style="Header.TFrame")
        user_info_frame.pack(side="right")
        
        # User Avatar placeholder (initials)
        initials = self.user.username[:2].upper()
        avatar = tk.Label(user_info_frame, text=initials, bg="#6366f1", fg="white", 
                         font=("Inter", 9, "bold"), width=4, height=2)
        avatar.pack(side="right", padx=(10, 0))
        
        ttk.Label(user_info_frame, text=self.user.username, style="Card.TLabel", font=("Inter", 10, "bold")).pack(side="right")

        # Page Container
        self.pages_container = ttk.Frame(self.main_content, style="App.TFrame", padding=30)
        self.pages_container.pack(fill="both", expand=True)
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, ttk.Frame] = {}
        for key, _ in nav_items:
            page = ttk.Frame(self.pages_container, style="App.TFrame")
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[key] = page

        self._build_dashboard_tab()
        self._build_students_tab()
        self._build_marks_tab()
        self._build_graphs_tab()
        self._build_reports_tab()
        if self.user.role == "admin":
            self._build_users_tab()

        self._show_page("dashboard")

    def _show_page(self, key: str) -> None:
        page = self.pages.get(key)
        if not page: return

        # Update title
        titles = {
            "dashboard": "System Overview",
            "students": "Student Directory",
            "marks": "Academic Records",
            "graphs": "Performance Analytics",
            "reports": "Generate Reports",
            "users": "System Users"
        }
        self.header_title.configure(text=titles.get(key, "Dashboard"))

        # Update nav buttons
        for k, btn in self.nav_buttons.items():
            btn.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

        if key == "dashboard":
            self._refresh_dashboard()

        page.tkraise()

    def _logout(self) -> None:
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy()
            # The run() function will handle re-opening login if needed or just exiting.
            # In this current implementation, it just exits.


    # ---------------- Dashboard Tab ----------------
    def _build_dashboard_tab(self) -> None:
        f = self.pages["dashboard"]
        
        # Outer container with padding
        outer_container = ttk.Frame(f, style="App.TFrame")
        outer_container.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== WELCOME SECTION =====
        welcome_container = ttk.Frame(outer_container, style="DashboardCard.TFrame")
        welcome_container.pack(fill="x", pady=(0, 30))
        
        ttk.Label(welcome_container, text=f"Welcome back, {self.user.username}!", style="Welcome.TLabel").pack(anchor="w")
        ttk.Label(welcome_container, text="Here's your management system overview.", style="Subtitle.TLabel").pack(anchor="w", pady=(8, 0))

        # ===== MAIN GRID: STATS + QUICK ACTIONS =====
        main_grid = ttk.Frame(outer_container, style="App.TFrame")
        main_grid.pack(fill="both", expand=True)
        
        # Configure columns: 70% stats, 30% actions
        main_grid.columnconfigure(0, weight=7)
        main_grid.columnconfigure(1, weight=3)
        main_grid.rowconfigure(0, weight=1)

        # ===== LEFT: STATS CARDS =====
        stats_container = ttk.Frame(main_grid, style="App.TFrame")
        stats_container.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Stats heading
        ttk.Label(stats_container, text="KEY METRICS", style="Muted.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Stats frame
        stats_frame = ttk.Frame(stats_container, style="App.TFrame")
        stats_frame.pack(fill="both", expand=True)
        
        self.stat_cards = {}
        metrics = [
            ("total_students", "Total Students", "👥", "#4f46e5"),
            ("total_classes", "Total Classes", "🏫", "#06b6d4"),
            ("total_subjects", "Total Subjects", "📚", "#10b981"),
            ("avg_mark", "Average Mark", "📊", "#f59e0b")
        ]
        
        if self.user.role == "admin":
            metrics.append(("total_users", "System Users", "🔐", "#8b5cf6"))

        # Create grid of cards (2 per row)
        for i, (key, label, icon, color) in enumerate(metrics):
            row, col = divmod(i, 2)
            stats_frame.columnconfigure(col, weight=1)
            
            # Card container
            card = ttk.Frame(stats_frame, style="StatCard.TFrame")
            card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            
            # Card content frame
            content = ttk.Frame(card, style="Card.TFrame")
            content.pack(fill="both", expand=True)
            
            # Icon header
            header = ttk.Frame(content, style="Card.TFrame")
            header.pack(fill="x", pady=(0, 15))
            tk.Label(header, text=icon, bg="#ffffff", font=("Inter", 16), fg=color).pack(side="left")
            
            # Metric label
            ttk.Label(header, text=label, style="StatLabel.TLabel").pack(side="left", padx=12)
            
            # Value display - Large and prominent
            val_label = ttk.Label(content, text="0", style="StatValue.TLabel")
            val_label.pack(anchor="w", pady=(10, 5))
            
            # Separator line
            sep = tk.Frame(content, bg="#e2e8f0", height=1)
            sep.pack(fill="x", pady=(10, 0))
            
            self.stat_cards[key] = val_label

        # ===== RIGHT: QUICK ACTIONS =====
        actions_card = ttk.Frame(main_grid, style="DashboardCard.TFrame")
        actions_card.grid(row=0, column=1, sticky="nsew")
        
        ttk.Label(actions_card, text="QUICK ACTIONS", style="Muted.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Scrollable actions frame
        actions_scroll = ttk.Frame(actions_card, style="Card.TFrame")
        actions_scroll.pack(fill="both", expand=True)
        
        def add_action(text, cmd, color="#4f46e5"):
            btn = tk.Button(
                actions_scroll, 
                text=text, 
                command=cmd, 
                bg="white", 
                fg=color,
                relief="flat", 
                font=("Inter", 9, "bold"), 
                anchor="w", 
                padx=10, 
                pady=8,
                cursor="hand2",
                border=1
            )
            btn.pack(fill="x", pady=6)
            # Hover effect
            def on_enter(e):
                btn.config(bg="#f0f4ff") if color == "#4f46e5" else (
                    btn.config(bg="#ecfdf5") if color == "#10b981" else (
                        btn.config(bg="#fdf2e9") if color == "#f59e0b" else 
                        btn.config(bg="#f3f1ff")
                    )
                )
            def on_leave(e):
                btn.config(bg="white")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        add_action("➕  Add Student", self._add_student_dialog, "#4f46e5")
        add_action("📝  Record Mark", self._add_mark_dialog, "#06b6d4")
        add_action("📊  View Analytics", lambda: self._show_page("graphs"), "#f59e0b")
        add_action("📄  Export Report", lambda: self._show_page("reports"), "#10b981")
        
        if self.user.role == "admin":
            add_action("🔐  Manage Users", lambda: self._show_page("users"), "#8b5cf6")
            add_action("⚙️  Settings", self._show_settings, "#6b7280")

    def _show_settings(self) -> None:
        """Placeholder for settings dialog"""
        messagebox.showinfo("Settings", "System settings coming soon!")


    def _refresh_dashboard(self) -> None:
        stats = self.db.get_dashboard_stats()
        
        self.stat_cards["total_students"].configure(text=str(stats["total_students"]))
        self.stat_cards["total_classes"].configure(text=str(stats["total_classes"]))
        self.stat_cards["total_subjects"].configure(text=str(stats["total_subjects"]))
        
        avg = stats["avg_mark"]
        self.stat_cards["avg_mark"].configure(text=f"{avg}%")
        
        if "total_users" in self.stat_cards:
            self.stat_cards["total_users"].configure(text=str(stats["total_users"]))

    # ---------------- Students Tab ----------------
    def _build_students_tab(self) -> None:
        f = self.pages["students"]

        # Action bar (Web-style)
        actions = ttk.Frame(f, style="App.TFrame")
        actions.pack(fill="x", pady=(0, 25))

        btn_frame = ttk.Frame(actions, style="App.TFrame")
        btn_frame.pack(side="left")
        ttk.Button(btn_frame, text="+  Add Student", style="Primary.TButton", command=self._add_student_dialog).pack(side="left")
        ttk.Button(btn_frame, text="Edit", style="Secondary.TButton", command=self._edit_student_dialog).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Delete", style="Danger.TButton", command=self._delete_selected_student).pack(side="left")

        # Search bar
        search_frame = ttk.Frame(actions, style="App.TFrame")
        search_frame.pack(side="right")
        
        search_inner = ttk.Frame(search_frame, style="Card.TFrame", padding=2)
        search_inner.pack(side="left")
        
        self.s_search = ttk.Entry(search_inner, width=35, font=("Inter", 10))
        self.s_search.pack(side="left", padx=10)
        
        ttk.Button(search_frame, text="Search", style="Primary.TButton", command=self._refresh_students).pack(side="left", padx=(10, 0))
        ttk.Button(search_frame, text="Clear", style="Secondary.TButton", command=self._clear_search).pack(side="left", padx=5)

        # Table Container
        card = ttk.Frame(f, style="Card.TFrame", padding=1)
        card.pack(fill="both", expand=True)

        cols = ("student_id", "name", "class_name", "program")
        self.students_tree = ttk.Treeview(card, columns=cols, show="headings", style="Treeview")
        
        for c, w in (("student_id", 180), ("name", 320), ("class_name", 220), ("program", 320)):
            self.students_tree.heading(c, text=c.replace("_", " ").upper())
            self.students_tree.column(c, width=w, anchor="w")
        
        self.students_tree.pack(fill="both", expand=True)
        
        # Tag for alternating rows
        self.students_tree.tag_configure("oddrow", background="#f8fafc")
        self.students_tree.tag_configure("evenrow", background="white")

    def _add_student_dialog(self) -> None:
        self._student_form_dialog(None)

    def _edit_student_dialog(self) -> None:
        item = self._selected_student_item()
        if not item:
            messagebox.showinfo("Selection", "Please select a student to edit.")
            return
        sid = self.students_tree.item(item, "values")[0]
        student = self.db.get_student(sid)
        self._student_form_dialog(student)

    def _student_form_dialog(self, student: dict | None) -> None:
        win = tk.Toplevel(self)
        win.title("Student Details" if student else "New Student")
        win.geometry("500x650")
        win.resizable(False, False)
        _setup_theme(win)

        outer = ttk.Frame(win, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        container = ttk.Frame(outer, style="Login.TFrame", padding=40)
        container.place(relx=0.5, rely=0.5, anchor="center", width=420, height=580)

        ttk.Label(container, text="STUDENT PROFILE", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(container, text="Manage student registration details.", style="CardMuted.TLabel").pack(pady=(0, 30))

        # Fields
        ttk.Label(container, text="STUDENT ID", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        sid_entry = ttk.Entry(container)
        sid_entry.pack(fill="x", pady=(0, 15))
        if student:
            sid_entry.insert(0, student["student_id"])
            sid_entry.configure(state="disabled")

        ttk.Label(container, text="FULL NAME", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        name_entry = ttk.Entry(container)
        name_entry.pack(fill="x", pady=(0, 15))
        if student: name_entry.insert(0, student["name"])

        ttk.Label(container, text="PROGRAM / COURSE", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        prog_entry = ttk.Entry(container)
        prog_entry.pack(fill="x", pady=(0, 15))
        if student: prog_entry.insert(0, student["program"] or "")

        ttk.Label(container, text="ASSIGNED CLASS", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        class_frame = ttk.Frame(container, style="Login.TFrame")
        class_frame.pack(fill="x", pady=(0, 30))
        
        class_cb = ttk.Combobox(class_frame, state="readonly")
        class_cb.pack(side="left", fill="x", expand=True)
        
        classes = self.db.list_classes()
        class_cb["values"] = [c["name"] for c in classes]
        if student and student["class_name"]:
            class_cb.set(student["class_name"])

        def refresh_classes():
            class_cb["values"] = [c["name"] for c in self.db.list_classes()]

        ttk.Button(class_frame, text="+", width=3, command=lambda: self._add_class_dialog(refresh_classes)).pack(side="right", padx=(10, 0))

        def save():
            sid, name = sid_entry.get().strip(), name_entry.get().strip()
            if not sid or not name:
                messagebox.showwarning("Required", "ID and Name are mandatory.")
                return
            
            cls_name = class_cb.get()
            cls_id = next((c["id"] for c in self.db.list_classes() if c["name"] == cls_name), None)

            try:
                if student:
                    self.db.update_student(sid, name=name, program=prog_entry.get().strip(), class_id=cls_id)
                else:
                    self.db.add_student(sid, name, prog_entry.get().strip(), cls_id)
                
                messagebox.showinfo("Success", "Record updated.")
                win.destroy()
                self._refresh_students()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Save Profile", style="Primary.TButton", command=save).pack(fill="x")
        ttk.Button(container, text="Discard", style="Secondary.TButton", command=win.destroy).pack(fill="x", pady=(10, 0))


    def _clear_search(self) -> None:
        self.s_search.delete(0, "end")
        self._refresh_students()

    def _add_class_dialog(self, callback: Callable | None = None) -> None:
        win = tk.Toplevel(self)
        win.title("Add Class")
        win.geometry("400x300")
        win.resizable(False, False)
        _setup_theme(win)

        container = ttk.Frame(win, style="Login.TFrame", padding=40)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="NEW CLASS", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(container, text="Create a new academic class.", style="CardMuted.TLabel").pack(pady=(0, 30))

        ttk.Label(container, text="CLASS NAME", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        entry = ttk.Entry(container)
        entry.pack(fill="x", pady=(0, 30))

        def save() -> None:
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("Missing", "Enter class name.")
                return
            try:
                self.db.upsert_class(name)
                messagebox.showinfo("Success", f"Class '{name}' created.")
                win.destroy()
                self._refresh_classes()
                if callback: callback()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Create Class", style="Primary.TButton", command=save).pack(fill="x")
        entry.focus_set()

    def _save_student(self) -> None:
        sid = self.s_id.get().strip()
        name = self.s_name.get().strip()
        program = self.s_program.get().strip()
        class_id = self._selected_class_id()

        if not sid or not name:
            messagebox.showwarning("Missing", "Student ID and Name are required.")
            return

        existing = self.db.get_student(sid)
        try:
            if existing:
                self.db.update_student(sid, name=name, program=program, class_id=class_id)
            else:
                self.db.add_student(sid, name, program, class_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self._refresh_students()
        self._refresh_student_picklists()

    def _delete_selected_student(self) -> None:
        item = self._selected_student_item()
        if not item:
            messagebox.showinfo("Select", "Select a student from the list first.")
            return
        sid = self.students_tree.item(item, "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete student {sid}?"):
            return
        try:
            self.db.delete_student(sid)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self._refresh_all()

    def _selected_student_item(self):
        sel = self.students_tree.selection()
        return sel[0] if sel else None

    def _on_student_selected(self, _e) -> None:
        item = self._selected_student_item()
        if not item:
            return
        sid, name, class_name, program = self.students_tree.item(item, "values")
        self.s_id.delete(0, "end")
        self.s_id.insert(0, sid)
        self.s_name.delete(0, "end")
        self.s_name.insert(0, name)
        self.s_program.delete(0, "end")
        self.s_program.insert(0, program)
        if class_name:
            self.s_class.set(class_name)
        else:
            self.s_class.set("")

    # ---------------- Marks Tab ----------------
    def _build_marks_tab(self) -> None:
        f = self.pages["marks"]

        # Action bar
        actions = ttk.Frame(f, style="App.TFrame")
        actions.pack(fill="x", pady=(0, 25))

        ttk.Button(actions, text="+  Record New Mark", style="Primary.TButton", command=self._add_mark_dialog).pack(side="left")

        # Filters
        filters = ttk.Frame(actions, style="App.TFrame")
        filters.pack(side="right")
        
        ttk.Label(filters, text="STUDENT", style="Muted.TLabel").pack(side="left", padx=5)
        self.m_view_student = ttk.Combobox(filters, state="readonly", width=35)
        self.m_view_student.pack(side="left", padx=5)
        
        ttk.Label(filters, text="TERM", style="Muted.TLabel").pack(side="left", padx=15)
        self.m_view_term = ttk.Entry(filters, width=15)
        self.m_view_term.pack(side="left", padx=5)
        
        ttk.Button(filters, text="Filter Results", style="Primary.TButton", command=self._refresh_marks_view).pack(side="left", padx=(15, 0))

        # Table Container
        card = ttk.Frame(f, style="Card.TFrame", padding=1)
        card.pack(fill="both", expand=True)

        cols = ("term", "subject", "mark", "grade")
        self.marks_tree = ttk.Treeview(card, columns=cols, show="headings", style="Treeview")
        
        for c, w in (("term", 200), ("subject", 300), ("mark", 150), ("grade", 150)):
            self.marks_tree.heading(c, text=c.upper())
            self.marks_tree.column(c, width=w, anchor="w")
        
        self.marks_tree.pack(fill="both", expand=True)
        
        # Tags for alternating rows
        self.marks_tree.tag_configure("oddrow", background="#f8fafc")
        self.marks_tree.tag_configure("evenrow", background="white")

    def _add_mark_dialog(self) -> None:
        win = tk.Toplevel(self)
        win.title("Record Mark")
        win.geometry("500x650")
        win.resizable(False, False)
        _setup_theme(win)

        outer = ttk.Frame(win, style="App.TFrame")
        outer.pack(fill="both", expand=True)

        container = ttk.Frame(outer, style="Login.TFrame", padding=40)
        container.place(relx=0.5, rely=0.5, anchor="center", width=420, height=580)

        ttk.Label(container, text="ACADEMIC RECORD", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(container, text="Log new student marks and grades.", style="CardMuted.TLabel").pack(pady=(0, 30))

        ttk.Label(container, text="SELECT STUDENT", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        student_cb = ttk.Combobox(container, state="readonly")
        student_cb.pack(fill="x", pady=(0, 15))
        
        students = self.db.list_students()
        student_cb["values"] = [f"{s['student_id']} - {s['name']}" for s in students]

        ttk.Label(container, text="SUBJECT", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        sub_frame = ttk.Frame(container, style="Login.TFrame")
        sub_frame.pack(fill="x", pady=(0, 15))
        
        subject_cb = ttk.Combobox(sub_frame, state="readonly")
        subject_cb.pack(side="left", fill="x", expand=True)
        subject_cb["values"] = [s["name"] for s in self.db.list_subjects()]

        def refresh_subjects():
            subject_cb["values"] = [s["name"] for s in self.db.list_subjects()]

        ttk.Button(sub_frame, text="+", width=3, command=lambda: self._add_subject_dialog(refresh_subjects)).pack(side="right", padx=(10, 0))

        ttk.Label(container, text="ACADEMIC TERM", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        term_entry = ttk.Entry(container)
        term_entry.pack(fill="x", pady=(0, 15))
        term_entry.insert(0, "Term 1")

        ttk.Label(container, text="NUMERIC MARK (0-100)", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        mark_entry = ttk.Entry(container)
        mark_entry.pack(fill="x", pady=(0, 30))

        def save():
            s_label, sub_name = student_cb.get(), subject_cb.get()
            term, mark_str = term_entry.get().strip(), mark_entry.get().strip()

            if not s_label or not sub_name or not term or not mark_str:
                messagebox.showwarning("Incomplete", "Please complete all fields.")
                return

            sid = s_label.split(" - ")[0]
            sub_id = next((s["id"] for s in self.db.list_subjects() if s["name"] == sub_name), None)
            
            try:
                mark = int(mark_str)
                if not (0 <= mark <= 100): raise ValueError()
            except ValueError:
                messagebox.showerror("Invalid", "Mark must be a number between 0 and 100.")
                return

            try:
                self.db.set_mark(sid, sub_id, term, mark)
                messagebox.showinfo("Success", "Record saved.")
                win.destroy()
                self._refresh_marks_view()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Record Mark", style="Primary.TButton", command=save).pack(fill="x")
        ttk.Button(container, text="Cancel", style="Secondary.TButton", command=win.destroy).pack(fill="x", pady=(10, 0))


    def _add_subject_dialog(self, callback: Callable | None = None) -> None:
        win = tk.Toplevel(self)
        win.title("Add Subject")
        win.geometry("400x300")
        win.resizable(False, False)
        _setup_theme(win)

        container = ttk.Frame(win, style="Login.TFrame", padding=40)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="NEW SUBJECT", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(container, text="Add a new subject to the curriculum.", style="CardMuted.TLabel").pack(pady=(0, 30))

        ttk.Label(container, text="SUBJECT NAME", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        entry = ttk.Entry(container)
        entry.pack(fill="x", pady=(0, 30))

        def save() -> None:
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("Missing", "Enter subject name.")
                return
            try:
                self.db.upsert_subject(name)
                messagebox.showinfo("Success", f"Subject '{name}' added.")
                win.destroy()
                self._refresh_subjects()
                if callback: callback()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Add Subject", style="Primary.TButton", command=save).pack(fill="x")
        entry.focus_set()

    def _save_mark(self) -> None:
        sid = self._selected_mark_student_id()
        subject_id = self._selected_subject_id()
        term = self.m_term.get().strip()
        try:
            mark = int(self.m_mark.get().strip())
        except Exception:
            messagebox.showwarning("Invalid", "Mark must be a number 0-100.")
            return
        if not sid or subject_id is None or not term:
            messagebox.showwarning("Missing", "Select Student, Subject and enter Term.")
            return
        if mark < 0 or mark > 100:
            messagebox.showwarning("Invalid", "Mark must be between 0 and 100.")
            return
        try:
            self.db.set_mark(sid, subject_id, term, mark)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self._refresh_marks_view()

    def _refresh_marks_view(self) -> None:
        self.marks_tree.delete(*self.marks_tree.get_children())
        sid = self._selected_view_student_id()
        if not sid:
            return
        term = self.m_view_term.get().strip() or None
        rows = self.db.get_student_marks(sid, term)
        for r in rows:
            grade = mark_to_grade(r["mark"])
            self.marks_tree.insert("", "end", values=(r["term"], r["subject"], r["mark"], grade))

    # ---------------- Graphs Tab ----------------
    def _build_graphs_tab(self) -> None:
        f = self.pages["graphs"]

        # Action bar
        actions = ttk.Frame(f, style="App.TFrame")
        actions.pack(fill="x", pady=(0, 25))

        filters = ttk.Frame(actions, style="App.TFrame")
        filters.pack(side="left")

        ttk.Label(filters, text="CLASS", style="Muted.TLabel").pack(side="left", padx=5)
        self.g_class = ttk.Combobox(filters, state="readonly", width=25)
        self.g_class.pack(side="left", padx=5)

        ttk.Label(filters, text="TERM", style="Muted.TLabel").pack(side="left", padx=15)
        self.g_term = ttk.Entry(filters, width=15)
        self.g_term.pack(side="left", padx=5)
        self.g_term.insert(0, "Term 1")

        ttk.Button(actions, text="Generate Analytics View", style="Primary.TButton", command=self._plot_class_performance).pack(side="right")

        # Graph Container Card
        self.graph_host = ttk.Frame(f, style="Card.TFrame", padding=40)
        self.graph_host.pack(fill="both", expand=True)

        self.graph_note = ttk.Label(self.graph_host, text="Select a class and term to visualize performance data.", style="CardMuted.TLabel")
        self.graph_note.pack(anchor="center", pady=150)


    def _plot_class_performance(self) -> None:
        for w in self.graph_host.winfo_children():
            w.destroy()

        class_name = self.g_class.get()
        term = self.g_term.get().strip()
        
        if not class_name or not term:
            ttk.Label(self.graph_host, text="Select a class and term first.", foreground="#ef4444", style="Muted.TLabel").pack(pady=20)
            return

        class_id = next((c["id"] for c in self.db.list_classes() if c["name"] == class_name), None)
        
        rows = self.db.class_averages(class_id, term)
        if not rows:
            ttk.Label(self.graph_host, text="No data found for this class and term.", style="Muted.TLabel").pack(pady=20)
            return

        names = [r["name"] for r in rows]
        avgs = [float(r["avg_mark"]) for r in rows]

        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            
            fig = Figure(figsize=(10, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.bar(names, avgs, color="#3b82f6")
            ax.set_title(f"Class Average Performance - {term}", pad=20)
            ax.set_ylabel("Average Mark")
            ax.set_ylim(0, 100)
            ax.tick_params(axis="x", labelrotation=15)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_host)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception:
            # Fallback to table
            tv = ttk.Treeview(self.graph_host, columns=("name", "avg"), show="headings", style="Treeview")
            tv.heading("name", text="STUDENT")
            tv.heading("avg", text="AVERAGE")
            tv.pack(fill="both", expand=True)
            for n, a in zip(names, avgs):
                tv.insert("", "end", values=(n, f"{a:.2f}"))
            ttk.Label(self.graph_host, text="Note: Install matplotlib for visual charts.", style="Muted.TLabel").pack(pady=10)


    # ---------------- Reports Tab ----------------
    def _build_reports_tab(self) -> None:
        f = self.pages["reports"]

        # Center the content like a web portal
        container = ttk.Frame(f, style="App.TFrame")
        container.place(relx=0.5, rely=0.4, anchor="center", width=500)

        card = ttk.Frame(container, style="Card.TFrame", padding=50)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="GENERATE REPORT", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(card, text="Export official student performance records.", style="CardMuted.TLabel").pack(pady=(0, 40))

        ttk.Label(card, text="SELECT STUDENT", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        self.r_student = ttk.Combobox(card, state="readonly")
        self.r_student.pack(fill="x", pady=(0, 25))

        ttk.Label(card, text="ACADEMIC TERM (OPTIONAL)", style="CardMuted.TLabel").pack(anchor="w", pady=(0, 5))
        self.r_term = ttk.Entry(card)
        self.r_term.pack(fill="x", pady=(0, 40))

        ttk.Button(card, text="Generate PDF Report", style="Primary.TButton", command=self._export_pdf).pack(fill="x")

        self.r_status = ttk.Label(card, text="Requires 'reportlab' for PDF generation.", style="CardMuted.TLabel")
        self.r_status.pack(pady=(20, 0))


    def _export_pdf(self) -> None:
        s_label = self.r_student.get()
        if not s_label:
            messagebox.showwarning("Missing", "Select a student.")
            return
        
        sid = s_label.split(" - ")[0]
        term = self.r_term.get().strip() or None
        s = self.db.get_student(sid)
        if not s:
            messagebox.showerror("Error", "Student not found.")
            return

        marks_rows = self.db.get_student_marks(sid, term)
        marks = [(r["subject"], r["term"], int(r["mark"])) for r in marks_rows]
        report = build_student_report(
            student_id=s["student_id"],
            name=s["name"],
            program=s["program"],
            class_name=s["class_name"],
            marks=marks,
        )

        out = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")],
            initialfile=f"Report_{sid}.pdf",
        )
        if not out:
            return
        try:
            export_report_to_pdf(report, out)
            messagebox.showinfo("Report Exported", f"Successfully saved to:\n{out}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))


    # ---------------- Users Tab (Admin) ----------------
    def _build_users_tab(self) -> None:
        f = self.pages["users"]

        # Action bar
        actions = ttk.Frame(f, style="App.TFrame")
        actions.pack(fill="x", pady=(0, 25))

        ttk.Button(actions, text="+  Register New System User", style="Primary.TButton", command=self._add_user_dialog).pack(side="left")

        # Table Container
        card = ttk.Frame(f, style="Card.TFrame", padding=1)
        card.pack(fill="both", expand=True)

        cols = ("username", "role")
        self.users_tree = ttk.Treeview(card, columns=cols, show="headings", style="Treeview")
        
        for c, w in (("username", 500), ("role", 300)):
            self.users_tree.heading(c, text=c.upper())
            self.users_tree.column(c, width=w, anchor="w")
        
        self.users_tree.pack(fill="both", expand=True)
        
        # Tags for alternating rows
        self.users_tree.tag_configure("oddrow", background="#f8fafc")
        self.users_tree.tag_configure("evenrow", background="white")

    def _add_user_dialog(self) -> None:
        win = tk.Toplevel(self)
        win.title("New User")
        win.geometry("400x450")
        win.resizable(False, False)
        _setup_theme(win)

        container = ttk.Frame(win, style="Login.TFrame", padding=30)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="CREATE NEW USER", style="Header.TLabel").pack(pady=(0, 20))

        ttk.Label(container, text="Username", style="Card.TLabel").pack(anchor="w")
        uname = ttk.Entry(container)
        uname.pack(fill="x", pady=(5, 15))

        ttk.Label(container, text="Password", style="Card.TLabel").pack(anchor="w")
        upass = ttk.Entry(container, show="•")
        upass.pack(fill="x", pady=(5, 15))

        ttk.Label(container, text="System Role", style="Card.TLabel").pack(anchor="w")
        urole = ttk.Combobox(container, state="readonly", values=["admin", "staff"])
        urole.pack(fill="x", pady=(5, 25))
        urole.set("staff")

        def save():
            name = uname.get().strip()
            pw = upass.get()
            role = urole.get()
            if not name or not pw:
                messagebox.showwarning("Missing Info", "Username and password required.")
                return
            try:
                self.db.create_user(name, pw, role)
                messagebox.showinfo("Success", "User created.")
                win.destroy()
                self._refresh_users()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(container, text="Create User", style="Primary.TButton", command=save).pack(fill="x")
        ttk.Button(container, text="Cancel", style="Secondary.TButton", command=win.destroy).pack(fill="x", pady=(10, 0))


    # ---------------- Refresh helpers ----------------
    def _refresh_all(self) -> None:
        self._refresh_dashboard()
        self._refresh_classes()
        self._refresh_students()
        self._refresh_subjects()
        self._refresh_student_picklists()
        self._refresh_marks_view()
        if self.user.role == "admin":
            self._refresh_users()

    def _refresh_classes(self) -> None:
        classes = self.db.list_classes()
        names = [c["name"] for c in classes]
        self.g_class["values"] = names

    def _refresh_subjects(self) -> None:
        # Subjects are refreshed in the dialog directly now
        pass

    def _refresh_students(self) -> None:
        q = self.s_search.get().strip() or None
        rows = self.db.list_students(q=q)
        self.students_tree.delete(*self.students_tree.get_children())
        for i, r in enumerate(rows):
            tag = "evenrow" if i % 2 else "oddrow"
            self.students_tree.insert("", "end", values=(r["student_id"], r["name"], r["class_name"] or "", r["program"] or ""), tags=(tag,))
        self._refresh_student_picklists()

    def _refresh_student_picklists(self) -> None:
        rows = self.db.list_students()
        items = [f'{r["student_id"]} - {r["name"]}' for r in rows]
        self.m_view_student["values"] = items
        self.r_student["values"] = items

    def _refresh_users(self) -> None:
        if not hasattr(self, 'users_tree'): return
        self.users_tree.delete(*self.users_tree.get_children())
        for i, r in enumerate(self.db.list_users()):
            tag = "evenrow" if i % 2 else "oddrow"
            self.users_tree.insert("", "end", values=(r["username"], r["role"]), tags=(tag,))

    def _refresh_marks_view(self) -> None:
        self.marks_tree.delete(*self.marks_tree.get_children())
        s_label = self.m_view_student.get()
        if not s_label: return
        
        sid = s_label.split(" - ")[0]
        term = self.m_view_term.get().strip() or None
        rows = self.db.get_student_marks(sid, term)
        for i, r in enumerate(rows):
            tag = "evenrow" if i % 2 else "oddrow"
            grade = mark_to_grade(r["mark"])
            self.marks_tree.insert("", "end", values=(r["term"], r["subject"], r["mark"], grade), tags=(tag,))

    def _selected_student_item(self):
        sel = self.students_tree.selection()
        return sel[0] if sel else None



def run() -> None:
    def show_err(msg: str) -> None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup error", msg)
        root.destroy()

    primary_path = "students.db"
    fallback_path = "students_gui.db"

    db = Database(primary_path)
    try:
        db.migrate()
    except Exception as e:
        # If the legacy DB is locked by another process, start using a fresh DB
        # so the GUI can still run.
        if "locked" in str(e).lower():
            try:
                db.close()
            except Exception:
                pass
            db = Database(fallback_path)
            try:
                db.migrate()
            except Exception as e2:
                show_err(str(e2))
                try:
                    db.close()
                except Exception:
                    pass
                return
            show_err(
                f"'{primary_path}' is locked by another app.\n\n"
                f"The program started using '{fallback_path}' instead.\n\n"
                f"Close whatever is using '{primary_path}' to use your old data."
            )
        else:
            show_err(str(e))
            db.close()
            return

    login = LoginWindow(db)
    login.mainloop()
    if not login.user:
        db.close()
        return

    app = MainWindow(db, login.user)
    app.protocol("WM_DELETE_WINDOW", lambda: (db.close(), app.destroy()))
    app.mainloop()

