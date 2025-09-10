import tkinter as tk
from tkinter import ttk, messagebox
from authorization_manager import show_authorization_manager


class SettingsTab:
    def __init__(self, parent_frame, company, colors, authorizations):
        self.parent_frame = parent_frame
        self.company = company
        self.colors = colors
        self.authorizations = authorizations

    def create_tab(self):
        """Create the settings management tab"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.create_page_header("⚙️ Settings", "Manage system settings and configurations")

        # Create main content frame with scrolling
        main_canvas = tk.Canvas(self.parent_frame, bg=self.colors["content_bg"])
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.colors["content_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True, padx=40)
        scrollbar.pack(side="right", fill="y")

        # Create content sections
        self.create_authorization_section(scrollable_frame)
        self.create_system_info_section(scrollable_frame)
        self.create_data_management_section(scrollable_frame)
        self.create_appearance_section(scrollable_frame)

    def create_page_header(self, title, subtitle):
        """Create a consistent page header"""
        header_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
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

    def create_authorization_section(self, parent):
        """Create authorization management section"""
        section_frame = self.create_section_frame(parent, "🔐 Authorization Management",
                                                  "Manage authorization types for soldiers and missions")

        # Description
        desc_label = tk.Label(section_frame,
                              text="Add, edit, or remove authorization types that soldiers can have for different missions.",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 11),
                              wraplength=600,
                              justify='left')
        desc_label.pack(anchor='w', pady=(0, 15))

        # Manage button
        manage_btn = tk.Button(section_frame,
                               text="🔐 Manage Authorizations",
                               bg=self.colors["accent"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 12, 'bold'),
                               relief='raised',
                               bd=2,
                               padx=25,
                               pady=12,
                               cursor='hand2',
                               command=self.manage_authorizations)
        manage_btn.pack(anchor='w', pady=(0, 15))

        # Add hover effects
        self.add_button_hover_effects(manage_btn)

        # Current authorizations display
        self.create_current_authorizations_display(section_frame)

    def create_current_authorizations_display(self, parent):
        """Display current authorizations"""
        current_label = tk.Label(parent,
                                 text="Current Authorizations:",
                                 bg=self.colors["content_bg"],
                                 fg=self.colors["text_primary"],
                                 font=('Segoe UI', 11, 'bold'))
        current_label.pack(anchor='w', pady=(0, 8))

        # Display frame
        display_frame = tk.Frame(parent, bg=self.colors["card_shadow"], relief='solid', bd=1)
        display_frame.pack(fill='x', pady=(0, 10))

        content_frame = tk.Frame(display_frame, bg=self.colors["card_shadow"])
        content_frame.pack(fill='x', padx=15, pady=12)

        # Create authorization tags
        tags_frame = tk.Frame(content_frame, bg=self.colors["card_shadow"])
        tags_frame.pack(fill='x')

        for i, auth in enumerate(self.authorizations):
            tag = tk.Label(tags_frame,
                           text=auth,
                           bg=self.colors["accent"],
                           fg=self.colors["text_light"],
                           font=('Segoe UI', 9),
                           padx=8,
                           pady=4,
                           relief='flat')

            # Calculate position for grid layout
            row = i // 3
            col = i % 3
            tag.grid(row=row, column=col, padx=3, pady=3, sticky='w')

        # Configure grid weights
        for i in range(3):
            tags_frame.grid_columnconfigure(i, weight=1)

        # Count label
        count_label = tk.Label(content_frame,
                               text=f"Total: {len(self.authorizations)} authorizations",
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10))
        count_label.pack(anchor='w', pady=(10, 0))

    def create_system_info_section(self, parent):
        """Create system information section"""
        section_frame = self.create_section_frame(parent, "ℹ️ System Information",
                                                  "Current system status and company statistics")

        # Create info cards
        info_grid = tk.Frame(section_frame, bg=self.colors["content_bg"])
        info_grid.pack(fill='x', pady=(0, 15))

        # Company info card
        self.create_info_card(info_grid, "Company",
                              self.company.name if self.company else 'None',
                              "🏢", 0, 0)

        # Soldiers info card
        soldier_count = len(self.company.get_all_soldiers()) if self.company else 0
        self.create_info_card(info_grid, "Soldiers",
                              str(soldier_count),
                              "👥", 0, 1)

        # Platoons info card
        platoon_count = len(self.company.platoons) if self.company else 0
        self.create_info_card(info_grid, "Platoons",
                              str(platoon_count),
                              "🎖️", 0, 2)

        # Missions info card
        mission_count = len(self.company.missions) if self.company else 0
        self.create_info_card(info_grid, "Missions",
                              str(mission_count),
                              "🎯", 1, 0)

        # Authorizations info card
        self.create_info_card(info_grid, "Authorizations",
                              str(len(self.authorizations)),
                              "🔐", 1, 1)

        # File status info card
        file_status = "Saved" if hasattr(self, 'current_file') and self.current_file else "Unsaved"
        self.create_info_card(info_grid, "File Status",
                              file_status,
                              "💾", 1, 2)

    def create_data_management_section(self, parent):
        """Create data management section"""
        section_frame = self.create_section_frame(parent, "💾 Data Management",
                                                  "Import, export, and backup your company data")

        # Description
        desc_label = tk.Label(section_frame,
                              text="Manage your company data files and create backups for safety.",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 11))
        desc_label.pack(anchor='w', pady=(0, 15))

        # Buttons frame
        buttons_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
        buttons_frame.pack(fill='x')

        # Export button
        export_btn = tk.Button(buttons_frame,
                               text="📤 Export Data",
                               bg=self.colors["sidebar_hover"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=10,
                               cursor='hand2',
                               command=self.export_data)
        export_btn.pack(side='left', padx=(0, 15))

        # Backup button
        backup_btn = tk.Button(buttons_frame,
                               text="🗄️ Create Backup",
                               bg="#059669",  # Green
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=10,
                               cursor='hand2',
                               command=self.create_backup)
        backup_btn.pack(side='left')

        # Add hover effects
        self.add_button_hover_effects(export_btn)
        self.add_button_hover_effects(backup_btn)

    def create_appearance_section(self, parent):
        """Create appearance and preferences section"""
        section_frame = self.create_section_frame(parent, "🎨 Appearance & Preferences",
                                                  "Customize the application appearance and behavior")

        # Description
        desc_label = tk.Label(section_frame,
                              text="Customize how the application looks and behaves to suit your preferences.",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 11))
        desc_label.pack(anchor='w', pady=(0, 15))

        # Preferences frame
        prefs_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
        prefs_frame.pack(fill='x')

        # Theme selection (placeholder for future)
        theme_label = tk.Label(prefs_frame,
                               text="Theme:",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 11, 'bold'))
        theme_label.pack(anchor='w', pady=(0, 5))

        theme_info = tk.Label(prefs_frame,
                              text="• Blue Theme (Current)",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 10))
        theme_info.pack(anchor='w', pady=(0, 15))

        # Future settings placeholder
        future_label = tk.Label(prefs_frame,
                                text="More customization options coming soon...",
                                bg=self.colors["content_bg"],
                                fg=self.colors["text_secondary"],
                                font=('Segoe UI', 10, 'italic'))
        future_label.pack(anchor='w')

    def create_section_frame(self, parent, title, subtitle):
        """Create a section frame with title and subtitle"""
        # Section container
        container = tk.Frame(parent, bg=self.colors["content_bg"])
        container.pack(fill='x', pady=(0, 30))

        # Section title
        title_label = tk.Label(container,
                               text=title,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w', pady=(0, 5))

        # Section subtitle
        subtitle_label = tk.Label(container,
                                  text=subtitle,
                                  bg=self.colors["content_bg"],
                                  fg=self.colors["text_secondary"],
                                  font=('Segoe UI', 12))
        subtitle_label.pack(anchor='w', pady=(0, 15))

        # Section content frame
        content_frame = tk.Frame(container, bg=self.colors["content_bg"])
        content_frame.pack(fill='x')

        return content_frame

    def create_info_card(self, parent, title, value, icon, row, col):
        """Create an information card"""
        card = tk.Frame(parent, bg=self.colors["card_shadow"], relief='solid', bd=1,
                        width=180, height=80)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        card.grid_propagate(False)

        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)

        # Card content
        content = tk.Frame(card, bg=self.colors["card_shadow"])
        content.pack(expand=True, fill='both', padx=10, pady=8)

        # Icon and value row
        top_row = tk.Frame(content, bg=self.colors["card_shadow"])
        top_row.pack(fill='x')

        icon_label = tk.Label(top_row,
                              text=icon,
                              bg=self.colors["card_shadow"],
                              fg=self.colors["accent"],
                              font=('Segoe UI', 16))
        icon_label.pack(side='left')

        value_label = tk.Label(top_row,
                               text=value,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 14, 'bold'))
        value_label.pack(side='right')

        # Title
        title_label = tk.Label(content,
                               text=title,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10))
        title_label.pack(anchor='w')

    def add_button_hover_effects(self, button):
        """Add hover effects to a button"""
        original_bg = button['bg']

        def on_enter(event):
            if original_bg == self.colors["accent"]:
                button.configure(bg=self.colors["sidebar_hover"], bd=3)
            elif original_bg == self.colors["sidebar_hover"]:
                button.configure(bg="#1e40af", bd=3)  # Darker blue
            elif original_bg == "#059669":  # Green
                button.configure(bg="#047857", bd=3)  # Darker green

        def on_leave(event):
            button.configure(bg=original_bg, bd=2)

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def manage_authorizations(self):
        """Open the authorization manager"""
        updated_authorizations = show_authorization_manager(
            self.parent_frame,
            self.colors,
            self.authorizations
        )

        if updated_authorizations is not None:
            # Update the local authorizations list
            self.authorizations[:] = updated_authorizations

            # Update the main GUI's authorizations list if we have a reference
            if hasattr(self, 'main_gui') and self.main_gui:
                self.main_gui.authorizations[:] = updated_authorizations

            messagebox.showinfo("Success",
                                f"Authorization list updated!\n"
                                f"New list contains {len(self.authorizations)} authorizations.\n"
                                f"Click 'Save' to save these changes to file!")

            # Refresh the current tab to show updated authorizations
            self.create_tab()

    def export_data(self):
        """Export company data"""
        # Placeholder for future implementation
        messagebox.showinfo("Export Data", "Data export feature coming soon!")

    def create_backup(self):
        """Create a backup of current data"""
        # Placeholder for future implementation
        messagebox.showinfo("Create Backup", "Backup feature coming soon!")