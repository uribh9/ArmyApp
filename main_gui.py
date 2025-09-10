import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
from typing import List, Dict, Optional

# Import our custom classes
from soldier import Soldier
from mission import Mission
from platoon import Platoon
from company import Company

# Import tab modules
from soldiers_tab import SoldiersTab
from platoons_tab import PlatoonsTab
from missions_tab import MissionsTab
from company_tab import CompanyTab
from settings_tab import SettingsTab

# Import startup dialog
from startup_dialog import show_startup_dialog


class ModernMilitaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Scheduling Management System")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximize window

        # Available options
        self.shifts = ["Morning", "Noon", "Night"]

        # DEFAULT authorizations (only used if no saved data exists)
        self.default_authorizations = [
            "Guard Duty", "Patrol", "Communications",
            "Equipment Maintenance", "Medical Support",
            "Driver", "Weapons Specialist", "Logistics"
        ]

        # Initialize authorizations as empty - will be set by startup dialog or defaults
        self.authorizations = []

        # Modern color scheme - Blueish theme
        self.colors = {
            "primary_bg": "#f8fafc",  # Light blue-gray background
            "sidebar_bg": "#1e40af",  # Deep blue sidebar
            "sidebar_hover": "#2563eb",  # Lighter blue hover
            "sidebar_active": "#3b82f6",  # Active blue
            "content_bg": "#ffffff",  # White content area
            "accent": "#3b82f6",  # Blue accent
            "text_primary": "#1f2937",  # Dark gray text
            "text_secondary": "#6b7280",  # Medium gray text
            "text_light": "#ffffff",  # White text
            "border": "#e5e7eb",  # Light border
            "card_shadow": "#f3f4f6"  # Card shadow
        }

        # Initialize company and current file
        self.company = None
        self.current_file = None
        self.current_page = "welcome"

        # Show startup dialog to select/create company
        self.initialize_company()

        # Set authorizations to defaults if still empty (new company case)
        if not self.authorizations:
            self.authorizations = self.default_authorizations.copy()

        # Initialize tab objects
        self.soldiers_tab = None
        self.platoons_tab = None
        self.missions_tab = None
        self.company_tab = None
        self.settings_tab = None

        # Setup the interface
        self.setup_styles()
        self.create_main_interface()
        self.show_welcome_page()

    def initialize_company(self):
        """Initialize company through startup dialog and load authorizations"""
        try:
            # Show startup dialog as a child of main window
            startup_result = show_startup_dialog(self.colors, self.root)

            if startup_result and startup_result.get('company'):
                self.company = startup_result['company']
                self.current_file = startup_result.get('filename')

                # IMPORTANT: Load authorizations from the company file if it was loaded
                if startup_result.get('action') == 'load' and self.current_file:
                    self.load_authorizations_from_current_file()

                # Update window title
                if self.current_file:
                    title = f"Military Scheduling Management System - {self.company.name} ({self.current_file})"
                else:
                    title = f"Military Scheduling Management System - {self.company.name}"

                self.root.title(title)

            else:
                # User cancelled - create a default company to prevent crashes
                self.company = Company("Default Company")
                self.current_file = None

                # Update window title
                self.root.title("Military Scheduling Management System - Default Company")

        except Exception as e:
            import traceback
            traceback.print_exc()

            # Create fallback company to prevent crashes
            messagebox.showerror("Startup Error",
                                 f"There was an error during startup: {str(e)}\nCreating a default company.")
            self.company = Company("Default Company")
            self.current_file = None

    def setup_styles(self):
        """Configure modern styling"""
        self.root.configure(bg=self.colors["primary_bg"])

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure modern styles
        self.style.configure('Sidebar.TFrame', background=self.colors["sidebar_bg"])
        self.style.configure('Content.TFrame', background=self.colors["content_bg"])
        self.style.configure('Card.TFrame', background=self.colors["content_bg"], relief='solid', borderwidth=1)

        # Button styles
        self.style.configure('SidebarButton.TButton',
                             background=self.colors["sidebar_bg"],
                             foreground=self.colors["text_light"],
                             borderwidth=0,
                             focuscolor='none',
                             font=('Segoe UI', 10))

        self.style.map('SidebarButton.TButton',
                       background=[('active', self.colors["sidebar_hover"]),
                                   ('pressed', self.colors["sidebar_active"])])

        self.style.configure('Accent.TButton',
                             background=self.colors["accent"],
                             foreground=self.colors["text_light"],
                             borderwidth=0,
                             focuscolor='none',
                             font=('Segoe UI', 10, 'bold'))

        # Configure other elements
        self.style.configure('Modern.TLabel',
                             background=self.colors["content_bg"],
                             foreground=self.colors["text_primary"],
                             font=('Segoe UI', 10))

        self.style.configure('Title.TLabel',
                             background=self.colors["content_bg"],
                             foreground=self.colors["text_primary"],
                             font=('Segoe UI', 24, 'bold'))

        self.style.configure('Subtitle.TLabel',
                             background=self.colors["content_bg"],
                             foreground=self.colors["text_secondary"],
                             font=('Segoe UI', 12))

        self.style.configure('Modern.Treeview',
                             background=self.colors["content_bg"],
                             foreground=self.colors["text_primary"],
                             fieldbackground=self.colors["content_bg"],
                             borderwidth=1,
                             relief='solid')

        self.style.configure('Modern.TEntry',
                             fieldbackground=self.colors["content_bg"],
                             borderwidth=1,
                             relief='solid')

    def create_main_interface(self):
        """Create the main interface with toolbar, sidebar and content area"""
        # Create main container
        self.main_container = tk.Frame(self.root, bg=self.colors["primary_bg"])
        self.main_container.pack(fill='both', expand=True)

        # Create toolbar at the top
        self.create_toolbar()

        # Create bottom container for sidebar and content
        bottom_container = tk.Frame(self.main_container, bg=self.colors["primary_bg"])
        bottom_container.pack(fill='both', expand=True)

        # Create sidebar
        self.create_sidebar_in_container(bottom_container)

        # Create content area
        self.content_frame = tk.Frame(bottom_container, bg=self.colors["content_bg"])
        self.content_frame.pack(side='right', fill='both', expand=True)

    def create_toolbar(self):
        """Create a toolbar with quick access buttons"""
        self.toolbar = tk.Frame(self.main_container, bg=self.colors["card_shadow"], height=50, relief='solid', bd=1)
        self.toolbar.pack(fill='x', side='top')
        self.toolbar.pack_propagate(False)

        # Toolbar content frame
        toolbar_content = tk.Frame(self.toolbar, bg=self.colors["card_shadow"])
        toolbar_content.pack(fill='both', expand=True, padx=15, pady=8)

        # Left side - File operations
        left_frame = tk.Frame(toolbar_content, bg=self.colors["card_shadow"])
        left_frame.pack(side='left')

        # Quick Save button (most prominent)
        self.save_btn = tk.Button(left_frame,
                                  text="💾 Save",
                                  bg="#059669",  # Green
                                  fg="white",
                                  font=('Segoe UI', 10, 'bold'),
                                  relief='raised',
                                  bd=2,
                                  padx=15,
                                  pady=6,
                                  cursor='hand2',
                                  command=self.save_company_data)
        self.save_btn.pack(side='left', padx=(0, 8))

        # Load button
        load_btn = tk.Button(left_frame,
                             text="📂 Load",
                             bg=self.colors["sidebar_hover"],
                             fg="white",
                             font=('Segoe UI', 10),
                             relief='raised',
                             bd=2,
                             padx=12,
                             pady=6,
                             cursor='hand2',
                             command=self.load_company_data)
        load_btn.pack(side='left', padx=(0, 8))

        # New button
        new_btn = tk.Button(left_frame,
                            text="✨ New",
                            bg=self.colors["accent"],
                            fg="white",
                            font=('Segoe UI', 10),
                            relief='raised',
                            bd=2,
                            padx=12,
                            pady=6,
                            cursor='hand2',
                            command=self.new_company)
        new_btn.pack(side='left', padx=(0, 15))

        # Separator
        separator = tk.Frame(left_frame, bg=self.colors["border"], width=1, height=25)
        separator.pack(side='left', padx=(0, 15))

        # Quick navigation buttons
        nav_btn = tk.Button(left_frame,
                            text="👥 Soldiers",
                            bg=self.colors["card_shadow"],
                            fg=self.colors["text_primary"],
                            font=('Segoe UI', 9),
                            relief='flat',
                            bd=0,
                            padx=10,
                            pady=6,
                            cursor='hand2',
                            command=lambda: self.show_page("soldiers"))
        nav_btn.pack(side='left', padx=(0, 5))

        platoon_btn = tk.Button(left_frame,
                                text="🎖️ Platoons",
                                bg=self.colors["card_shadow"],
                                fg=self.colors["text_primary"],
                                font=('Segoe UI', 9),
                                relief='flat',
                                bd=0,
                                padx=10,
                                pady=6,
                                cursor='hand2',
                                command=lambda: self.show_page("platoons"))
        platoon_btn.pack(side='left', padx=(0, 5))

        mission_btn = tk.Button(left_frame,
                                text="🎯 Missions",
                                bg=self.colors["card_shadow"],
                                fg=self.colors["text_primary"],
                                font=('Segoe UI', 9),
                                relief='flat',
                                bd=0,
                                padx=10,
                                pady=6,
                                cursor='hand2',
                                command=lambda: self.show_page("missions"))
        mission_btn.pack(side='left')

        # Right side - Company info and settings
        right_frame = tk.Frame(toolbar_content, bg=self.colors["card_shadow"])
        right_frame.pack(side='right')

        # Settings button
        settings_btn = tk.Button(right_frame,
                                 text="⚙️",
                                 bg=self.colors["card_shadow"],
                                 fg=self.colors["text_primary"],
                                 font=('Segoe UI', 12),
                                 relief='flat',
                                 bd=0,
                                 padx=8,
                                 pady=6,
                                 cursor='hand2',
                                 command=lambda: self.show_page("settings"))
        settings_btn.pack(side='right', padx=(10, 0))

        # Current file status
        self.file_status_label = tk.Label(right_frame,
                                          text=self.get_file_status(),
                                          bg=self.colors["card_shadow"],
                                          fg=self.colors["text_secondary"],
                                          font=('Segoe UI', 9))
        self.file_status_label.pack(side='right', padx=(0, 10))

        # Add hover effects to all buttons
        self.add_toolbar_hover_effects()

    def create_sidebar_in_container(self, container):
        """Create sidebar in the specified container"""
        self.sidebar = tk.Frame(container, bg=self.colors["sidebar_bg"], width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        # App title in sidebar
        title_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], height=80)
        title_frame.pack(fill='x', pady=(20, 30))
        title_frame.pack_propagate(False)

        app_title = tk.Label(title_frame,
                             text="Military\nScheduling",
                             bg=self.colors["sidebar_bg"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 16, 'bold'),
                             justify='center')
        app_title.pack(expand=True)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠", "Welcome", "welcome"),
            ("👥", "Soldiers", "soldiers"),
            ("🎖️", "Platoons", "platoons"),
            ("🎯", "Missions", "missions"),
            ("🏢", "Company", "company"),
            ("📊", "Overview", "overview"),
            ("⚙️", "Settings", "settings")
        ]

        for icon, text, page_id in nav_items:
            self.create_nav_button(icon, text, page_id)

        # Bottom section with company info
        bottom_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"])
        bottom_frame.pack(side='bottom', fill='x', pady=20)

        # Company name display
        company_name = self.company.name if self.company else "No Company"
        self.company_label = tk.Label(bottom_frame,
                                      text=f"📋 {company_name}",
                                      bg=self.colors["sidebar_bg"],
                                      fg=self.colors["text_light"],
                                      font=('Segoe UI', 9),
                                      wraplength=200)
        self.company_label.pack(pady=10)

    def add_toolbar_hover_effects(self):
        """Add hover effects to toolbar buttons"""
        # Get all buttons in the toolbar
        for widget in self.toolbar.winfo_children():
            for child in widget.winfo_children():
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Button):
                        self.add_button_hover_effect(grandchild)

    def add_button_hover_effect(self, button):
        """Add hover effect to a specific button"""
        original_bg = button['bg']

        def on_enter(event):
            if original_bg == "#059669":  # Green save button
                button.configure(bg="#047857", bd=3)
            elif original_bg == self.colors["sidebar_hover"]:
                button.configure(bg="#1e40af", bd=3)
            elif original_bg == self.colors["accent"]:
                button.configure(bg="#2563eb", bd=3)
            elif original_bg == self.colors["card_shadow"]:
                button.configure(bg=self.colors["border"], relief='raised', bd=1)

        def on_leave(event):
            if original_bg == self.colors["card_shadow"]:
                button.configure(bg=original_bg, relief='flat', bd=0)
            else:
                button.configure(bg=original_bg, bd=2)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def get_file_status(self):
        """Get current file status for toolbar"""
        if self.current_file:
            return f"📄 {self.current_file}"
        else:
            return "📄 Unsaved"

    def update_file_status(self):
        """Update the file status in toolbar"""
        if hasattr(self, 'file_status_label'):
            self.file_status_label.configure(text=self.get_file_status())


    def create_sidebar(self):
        """Create modern vertical sidebar"""
        self.sidebar = tk.Frame(self.main_container, bg=self.colors["sidebar_bg"], width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        # App title in sidebar
        title_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], height=80)
        title_frame.pack(fill='x', pady=(20, 30))
        title_frame.pack_propagate(False)

        app_title = tk.Label(title_frame,
                             text="Military\nScheduling",
                             bg=self.colors["sidebar_bg"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 16, 'bold'),
                             justify='center')
        app_title.pack(expand=True)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠", "Welcome", "welcome"),
            ("👥", "Soldiers", "soldiers"),
            ("🎖️", "Platoons", "platoons"),
            ("🎯", "Missions", "missions"),
            ("🏢", "Company", "company"),
            ("📊", "Overview", "overview"),
            ("⚙️", "Settings", "settings")
        ]

        for icon, text, page_id in nav_items:
            self.create_nav_button(icon, text, page_id)

        # Bottom section with company info
        bottom_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"])
        bottom_frame.pack(side='bottom', fill='x', pady=20)

        # Company name display
        company_name = self.company.name if self.company else "No Company"
        self.company_label = tk.Label(bottom_frame,
                                      text=f"📋 {company_name}",
                                      bg=self.colors["sidebar_bg"],
                                      fg=self.colors["text_light"],
                                      font=('Segoe UI', 9),
                                      wraplength=200)
        self.company_label.pack(pady=10)

    def create_nav_button(self, icon, text, page_id):
        """Create a navigation button"""
        button_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"])
        button_frame.pack(fill='x', padx=15, pady=2)

        button = tk.Button(button_frame,
                           text=f"{icon}  {text}",
                           bg=self.colors["sidebar_bg"],
                           fg=self.colors["text_light"],
                           font=('Segoe UI', 11),
                           relief='flat',
                           anchor='w',
                           padx=20,
                           pady=12,
                           border=0,
                           command=lambda: self.show_page(page_id))

        button.pack(fill='x')

        # Hover effects
        def on_enter(e):
            if self.current_page != page_id:
                button.configure(bg=self.colors["sidebar_hover"])

        def on_leave(e):
            if self.current_page != page_id:
                button.configure(bg=self.colors["sidebar_bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        self.nav_buttons[page_id] = button

    def update_nav_active(self, active_page):
        """Update active navigation button"""
        for page_id, button in self.nav_buttons.items():
            if page_id == active_page:
                button.configure(bg=self.colors["sidebar_active"])
            else:
                button.configure(bg=self.colors["sidebar_bg"])

    def show_page(self, page_id):
        """Show the selected page"""
        self.current_page = page_id
        self.update_nav_active(page_id)

        # Show appropriate page
        if page_id == "welcome":
            self.show_welcome_page()
        elif page_id == "soldiers":
            self.show_soldiers_page()
        elif page_id == "platoons":
            self.show_platoons_page()
        elif page_id == "missions":
            self.show_missions_page()
        elif page_id == "company":
            self.show_company_page()
        elif page_id == "overview":
            self.show_overview_page()
        elif page_id == "settings":
            self.show_settings_page()

    def show_welcome_page(self):
        """Show the welcome page with visible save buttons"""
        self.update_nav_active("welcome")

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create welcome content with proper scrolling
        main_canvas = tk.Canvas(self.content_frame, bg=self.colors["content_bg"])
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.colors["content_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create welcome content inside scrollable frame
        welcome_frame = tk.Frame(scrollable_frame, bg=self.colors["content_bg"])
        welcome_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Welcome header
        header_frame = tk.Frame(welcome_frame, bg=self.colors["content_bg"])
        header_frame.pack(fill='x', pady=(0, 30))

        welcome_title = tk.Label(header_frame,
                                 text="Welcome to Military Scheduling System",
                                 bg=self.colors["content_bg"],
                                 fg=self.colors["text_primary"],
                                 font=('Segoe UI', 28, 'bold'))
        welcome_title.pack(anchor='w')

        subtitle = tk.Label(header_frame,
                            text="Manage soldiers, platoons, missions, and scheduling efficiently",
                            bg=self.colors["content_bg"],
                            fg=self.colors["text_secondary"],
                            font=('Segoe UI', 14))
        subtitle.pack(anchor='w', pady=(5, 0))

        # Feature cards
        cards_frame = tk.Frame(welcome_frame, bg=self.colors["content_bg"])
        cards_frame.pack(fill='x', pady=(0, 30))

        # Create feature cards
        features = [
            ("👥", "Manage Soldiers", "Add and organize soldier information, authorizations, and preferences"),
            ("🎖️", "Organize Platoons", "Create platoons and assign soldiers with mission capabilities"),
            ("🎯", "Define Missions", "Set up missions with shift requirements and personnel needs"),
            ("📊", "View Overview", "Get comprehensive insights into your military operations")
        ]

        for i, (icon, title, desc) in enumerate(features):
            self.create_feature_card(cards_frame, icon, title, desc, i)

        # Quick actions section - THIS WAS MISSING!
        actions_frame = tk.Frame(welcome_frame, bg=self.colors["content_bg"])
        actions_frame.pack(fill='x', pady=(20, 0))

        # Actions title
        actions_title = tk.Label(actions_frame,
                                 text="Quick Actions",
                                 bg=self.colors["content_bg"],
                                 fg=self.colors["text_primary"],
                                 font=('Segoe UI', 18, 'bold'))
        actions_title.pack(anchor='w', pady=(0, 20))

        # Navigation actions
        nav_frame = tk.Frame(actions_frame, bg=self.colors["content_bg"])
        nav_frame.pack(fill='x', pady=(0, 15))

        nav_title = tk.Label(nav_frame,
                             text="Navigation:",
                             bg=self.colors["content_bg"],
                             fg=self.colors["text_secondary"],
                             font=('Segoe UI', 12, 'bold'))
        nav_title.pack(anchor='w', pady=(0, 10))

        nav_buttons_frame = tk.Frame(nav_frame, bg=self.colors["content_bg"])
        nav_buttons_frame.pack(anchor='w')

        # Navigation buttons
        nav_actions = [
            ("👥 Add Soldiers", lambda: self.show_page("soldiers")),
            ("🎖️ Create Platoons", lambda: self.show_page("platoons")),
            ("🎯 Define Missions", lambda: self.show_page("missions")),
            ("🏢 Company Info", lambda: self.show_page("company"))
        ]

        for text, command in nav_actions:
            btn = self.create_action_button(nav_buttons_frame, text, command, self.colors["accent"])
            btn.pack(side='left', padx=(0, 15))

        # File operations - PROMINENTLY DISPLAYED
        file_frame = tk.Frame(actions_frame, bg=self.colors["content_bg"])
        file_frame.pack(fill='x', pady=(15, 0))

        file_title = tk.Label(file_frame,
                              text="File Operations:",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 12, 'bold'))
        file_title.pack(anchor='w', pady=(0, 10))

        file_buttons_frame = tk.Frame(file_frame, bg=self.colors["content_bg"])
        file_buttons_frame.pack(anchor='w')

        # File operation buttons - MADE MORE PROMINENT
        file_actions = [
            ("💾 Save Company", self.save_company_data, "#059669"),  # Green for save
            ("📂 Load Company", self.load_company_data, self.colors["sidebar_hover"]),
            ("✨ New Company", self.new_company, self.colors["accent"]),
            ("⚙️ Settings", lambda: self.show_page("settings"), "#7c3aed")  # Purple for settings
        ]

        for text, command, color in file_actions:
            btn = self.create_action_button(file_buttons_frame, text, command, color)
            btn.pack(side='left', padx=(0, 15))

        # Force the canvas to update
        scrollable_frame.update_idletasks()
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    def create_action_button(self, parent, text, command, bg_color):
        """Create a styled action button"""
        btn = tk.Button(parent,
                        text=text,
                        bg=bg_color,
                        fg=self.colors["text_light"],
                        font=('Segoe UI', 11, 'bold'),
                        relief='raised',
                        bd=2,
                        padx=20,
                        pady=12,
                        cursor='hand2',
                        command=command)

        # Add hover effects
        def on_enter(e):
            # Darken the color on hover
            if bg_color == "#059669":  # Green
                btn.configure(bg="#047857", bd=3)
            elif bg_color == "#7c3aed":  # Purple
                btn.configure(bg="#6d28d9", bd=3)
            else:
                btn.configure(bg="#1e40af", bd=3)  # Darker blue

        def on_leave(e):
            btn.configure(bg=bg_color, bd=2)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn

    def create_feature_card(self, parent, icon, title, description, index):
        """Create a feature card with simple color hover effect"""
        # Determine which page to navigate to based on title
        page_mapping = {
            "Manage Soldiers": "soldiers",
            "Organize Platoons": "platoons",
            "Define Missions": "missions",
            "View Overview": "overview"
        }

        target_page = page_mapping.get(title, "welcome")

        # Create the card frame
        card = tk.Frame(parent, bg=self.colors["content_bg"], relief='solid', bd=1, cursor='hand2')
        card.pack(fill='x', pady=10)

        # Card content
        content = tk.Frame(card, bg=self.colors["content_bg"])
        content.pack(fill='both', expand=True, padx=25, pady=20)

        # Icon and title
        header = tk.Frame(content, bg=self.colors["content_bg"])
        header.pack(fill='x', pady=(0, 10))

        icon_label = tk.Label(header,
                              text=icon,
                              bg=self.colors["content_bg"],
                              fg=self.colors["accent"],
                              font=('Segoe UI', 24))
        icon_label.pack(side='left')

        title_label = tk.Label(header,
                               text=title,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side='left', padx=(15, 0))

        # Description
        desc_label = tk.Label(content,
                              text=description,
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 11),
                              wraplength=800,
                              justify='left')
        desc_label.pack(anchor='w')

        # Make it clickable
        def card_clicked(event=None):
            self.show_page(target_page)

        # Simple hover effect - ONLY background color change
        def on_enter(event):
            card.configure(bg=self.colors["card_shadow"])
            content.configure(bg=self.colors["card_shadow"])
            header.configure(bg=self.colors["card_shadow"])
            icon_label.configure(bg=self.colors["card_shadow"])
            title_label.configure(bg=self.colors["card_shadow"])
            desc_label.configure(bg=self.colors["card_shadow"])

        def on_leave(event):
            card.configure(bg=self.colors["content_bg"])
            content.configure(bg=self.colors["content_bg"])
            header.configure(bg=self.colors["content_bg"])
            icon_label.configure(bg=self.colors["content_bg"])
            title_label.configure(bg=self.colors["content_bg"])
            desc_label.configure(bg=self.colors["content_bg"])

        # Set hand cursor and bind events to all parts
        widgets_to_bind = [card, content, header, icon_label, title_label, desc_label]

        for widget in widgets_to_bind:
            widget.bind("<Button-1>", card_clicked)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.configure(cursor='hand2')

    def show_soldiers_page(self):
        """Show soldiers management page using SoldiersTab"""
        if not self.soldiers_tab:
            self.soldiers_tab = SoldiersTab(self.content_frame, self.company, self.colors,
                                            self.shifts, self.authorizations)
        self.soldiers_tab.create_tab()

    def show_platoons_page(self):
        """Show platoons management page using PlatoonsTab"""
        if not self.platoons_tab:
            self.platoons_tab = PlatoonsTab(self.content_frame, self.company, self.colors)
        self.platoons_tab.create_tab()

    def show_missions_page(self):
        """Show missions management page using MissionsTab"""
        if not self.missions_tab:
            self.missions_tab = MissionsTab(self.content_frame, self.company, self.colors,
                                            self.shifts, self.authorizations)
        self.missions_tab.create_tab()

    def show_company_page(self):
        """Show company settings page using CompanyTab"""
        if not self.company_tab:
            self.company_tab = CompanyTab(self.content_frame, self.company, self.colors)
        self.company_tab.create_tab()

    def show_settings_page(self):
        """Show settings management page using SettingsTab"""
        if not self.settings_tab:
            self.settings_tab = SettingsTab(self.content_frame, self.company, self.colors, self.authorizations)
            # Pass a reference to the main GUI so settings can update authorizations
            self.settings_tab.main_gui = self
        else:
            # Update the authorizations reference in case it changed
            self.settings_tab.authorizations = self.authorizations
            self.settings_tab.company = self.company
            self.settings_tab.main_gui = self
        self.settings_tab.create_tab()

    def show_overview_page(self):
        """Show overview page"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_page_header("📊 Overview", "Company statistics and insights")

        # Overview content
        overview_frame = tk.Frame(self.content_frame, bg=self.colors["content_bg"])
        overview_frame.pack(fill='both', expand=True, padx=40, pady=20)

        # Quick stats cards
        stats_grid = tk.Frame(overview_frame, bg=self.colors["content_bg"])
        stats_grid.pack(fill='x', pady=(0, 20))

        stats = self.company.get_company_statistics()

        # Create stat cards
        self.create_stat_card(stats_grid, "👥", "Total Soldiers", str(stats['total_soldiers']), 0)
        self.create_stat_card(stats_grid, "🎖️", "Platoons", str(stats['total_platoons']), 1)
        self.create_stat_card(stats_grid, "🎯", "Missions", str(stats['total_missions']), 2)

        # Detailed information
        if stats['total_soldiers'] > 0:
            details_frame = tk.Frame(overview_frame, bg=self.colors["content_bg"])
            details_frame.pack(fill='both', expand=True)

            # Platoon breakdown
            platoon_label = tk.Label(details_frame,
                                     text="Platoon Breakdown:",
                                     bg=self.colors["content_bg"],
                                     fg=self.colors["text_primary"],
                                     font=('Segoe UI', 14, 'bold'))
            platoon_label.pack(anchor='w', pady=(10, 5))

            for platoon_name, details in stats['platoon_details'].items():
                platoon_info = f"• {platoon_name}: {details['soldier_count']} soldiers, {details['assigned_missions']} missions"
                tk.Label(details_frame,
                         text=platoon_info,
                         bg=self.colors["content_bg"],
                         fg=self.colors["text_secondary"],
                         font=('Segoe UI', 11)).pack(anchor='w', padx=(20, 0))
        else:
            # Empty state
            empty_label = tk.Label(overview_frame,
                                   text="No data to display yet. Start by adding soldiers, platoons, and missions.",
                                   bg=self.colors["content_bg"],
                                   fg=self.colors["text_secondary"],
                                   font=('Segoe UI', 14))
            empty_label.pack(expand=True)

    def create_stat_card(self, parent, icon, title, value, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=self.colors["card_shadow"], relief='solid', bd=1, width=150, height=100)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='ew')
        card.grid_propagate(False)

        # Configure grid weights
        parent.grid_columnconfigure(column, weight=1)

        # Card content
        content = tk.Frame(card, bg=self.colors["card_shadow"])
        content.pack(expand=True, fill='both', padx=15, pady=15)

        # Icon
        icon_label = tk.Label(content,
                              text=icon,
                              bg=self.colors["card_shadow"],
                              fg=self.colors["accent"],
                              font=('Segoe UI', 20))
        icon_label.pack()

        # Value
        value_label = tk.Label(content,
                               text=value,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        value_label.pack()

        # Title
        title_label = tk.Label(content,
                               text=title,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10))
        title_label.pack()

    def create_page_header(self, title, subtitle):
        """Create a consistent page header"""
        header_frame = tk.Frame(self.content_frame, bg=self.colors["content_bg"])
        header_frame.pack(fill='x', padx=40, pady=(30, 20))

        title_label = tk.Label(header_frame,
                               text=title,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 24, 'bold'))
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(header_frame,
                                  text=subtitle,
                                  bg=self.colors["content_bg"],
                                  fg=self.colors["text_secondary"],
                                  font=('Segoe UI', 12))
        subtitle_label.pack(anchor='w', pady=(5, 0))

        # Separator line
        separator = tk.Frame(header_frame, bg=self.colors["border"], height=1)
        separator.pack(fill='x', pady=(15, 0))

    def save_company_data(self):
        """Save company data to JSON file - Enhanced to include authorizations"""
        try:
            # Use current filename or generate new one
            if self.current_file:
                filename = self.current_file
            else:
                filename = f"{self.company.name.replace(' ', '_')}_data.json"
                self.current_file = filename

            # Create the data dictionary with authorizations
            company_data = self.company.to_dict()

            # Add the current authorizations to the company data
            company_data['system_authorizations'] = self.authorizations

            with open(filename, 'w') as f:
                json.dump(company_data, f, indent=2)

            # Update window title to reflect saved state
            self.root.title(f"Military Scheduling Management System - {self.company.name} ({filename})")

            # Update toolbar file status if it exists
            if hasattr(self, 'file_status_label'):
                self.update_file_status()

            # Visual feedback in save button if it exists
            if hasattr(self, 'save_btn'):
                original_text = self.save_btn['text']
                self.save_btn.configure(text="✅ Saved", bg="#10b981")
                self.root.after(1500, lambda: self.save_btn.configure(text=original_text, bg="#059669"))

            messagebox.showinfo("Success", f"Company data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def load_authorizations_from_current_file(self):
        """Load authorizations from the current file"""
        try:
            if self.current_file:
                with open(self.current_file, 'r') as f:
                    data = json.load(f)

                if 'system_authorizations' in data:
                    self.authorizations = data['system_authorizations']
                    print(f"DEBUG: Loaded authorizations from file: {self.authorizations}")
                else:
                    print("DEBUG: No system_authorizations in file, using defaults")
                    self.authorizations = self.default_authorizations.copy()
            else:
                print("DEBUG: No current file, using defaults")
                self.authorizations = self.default_authorizations.copy()

        except Exception as e:
            print(f"DEBUG: Error loading authorizations: {e}")
            self.authorizations = self.default_authorizations.copy()

    def load_company_data(self):
        """Load company data from JSON file - Enhanced to load authorizations"""
        try:
            # Show file dialog to select JSON file
            filename = filedialog.askopenfilename(
                title="Load Company Data",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                defaultextension=".json"
            )

            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)

                self.company = Company.from_dict(data)
                self.current_file = os.path.basename(filename)

                # IMPORTANT: Load authorizations if they exist in the file
                if 'system_authorizations' in data:
                    self.authorizations = data['system_authorizations']
                    print(f"DEBUG: Loaded authorizations: {self.authorizations}")
                else:
                    # Use defaults if not in file (backward compatibility)
                    self.authorizations = self.default_authorizations.copy()
                    print("DEBUG: No system_authorizations found, using defaults")

                # Update UI
                self.company_label.configure(text=f"📋 {self.company.name}")
                self.root.title(f"Military Scheduling Management System - {self.company.name} ({self.current_file})")

                # Update toolbar file status if it exists
                if hasattr(self, 'file_status_label'):
                    self.update_file_status()

                # Reset tab objects so they reload with new data and new authorizations
                self.soldiers_tab = None
                self.platoons_tab = None
                self.missions_tab = None
                self.company_tab = None
                self.settings_tab = None

                # Refresh current page
                current_page = self.current_page
                self.show_page(current_page)

                messagebox.showinfo("Success",
                                    f"Company data loaded successfully!\nAuthorizations: {len(self.authorizations)} items")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def new_company(self):
        """Create a new company"""
        if messagebox.askyesno("New Company", "Are you sure? This will close the current company."):
            company_name = simpledialog.askstring(
                "New Company",
                "Enter the name for your new company:",
                initialvalue="New Military Company"
            )

            if company_name:
                company_name = company_name.strip()
                if company_name:
                    # Create new company
                    self.company = Company(company_name)
                    self.current_file = None

                    # Update UI
                    self.company_label.configure(text=f"📋 {self.company.name}")
                    self.root.title(f"Military Scheduling Management System - {self.company.name}")

                    # Reset tab objects
                    self.soldiers_tab = None
                    self.platoons_tab = None
                    self.missions_tab = None
                    self.company_tab = None
                    self.settings_tab = None

                    # Go to welcome page
                    self.show_page("welcome")

                    messagebox.showinfo("Success", f"New company '{company_name}' created!")

    def update_company_name(self):
        """Update company name from company tab"""
        if hasattr(self, 'company_tab') and self.company_tab:
            new_name = self.company.name
            self.company_label.configure(text=f"📋 {new_name}")
            if self.current_file:
                self.root.title(f"Military Scheduling Management System - {new_name} ({self.current_file})")
            else:
                self.root.title(f"Military Scheduling Management System - {new_name}")


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMilitaryGUI(root)
    root.mainloop()