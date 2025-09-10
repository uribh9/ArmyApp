import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class CompanyTab:
    def __init__(self, parent_frame, company, colors):
        self.parent_frame = parent_frame
        self.company = company
        self.colors = colors

        # Company information variables
        self.company_name_var = tk.StringVar()
        self.commander_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.contact_phone_var = tk.StringVar()
        self.contact_email_var = tk.StringVar()
        self.established_date_var = tk.StringVar()
        self.unit_type_var = tk.StringVar()
        self.description_var = tk.StringVar()

        # Initialize with existing company data
        self.load_company_data()

    def load_company_data(self):
        """Load existing company data into form variables"""
        self.company_name_var.set(self.company.name)

        # Load additional info from company policies if it exists
        policies = getattr(self.company, 'company_policies', {})
        self.commander_var.set(policies.get('commander', ''))
        self.location_var.set(policies.get('location', ''))
        self.contact_phone_var.set(policies.get('contact_phone', ''))
        self.contact_email_var.set(policies.get('contact_email', ''))
        self.established_date_var.set(policies.get('established_date', ''))
        self.unit_type_var.set(policies.get('unit_type', 'Infantry'))
        self.description_var.set(policies.get('description', ''))

    def create_tab(self):
        """Create the company management tab"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.create_page_header("🏢 Company Information", "Manage company details and organizational information")

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
        self.create_basic_info_section(scrollable_frame)
        self.create_contact_info_section(scrollable_frame)
        self.create_organizational_info_section(scrollable_frame)
        self.create_statistics_section(scrollable_frame)
        self.create_action_buttons(scrollable_frame)

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

    def create_basic_info_section(self, parent):
        """Create basic company information section"""
        section_frame = self.create_section_frame(parent, "📋 Basic Information")

        # Company Name
        self.create_form_field(section_frame, "Company Name:", self.company_name_var, 0, required=True)

        # Commander
        self.create_form_field(section_frame, "Commanding Officer:", self.commander_var, 1)

        # Unit Type
        unit_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
        unit_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(unit_frame, text="Unit Type:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')

        unit_types = ["Infantry", "Armor", "Artillery", "Engineers", "Signal", "Medical", "Logistics", "Special Forces",
                      "Other"]
        unit_combo = ttk.Combobox(unit_frame, textvariable=self.unit_type_var, values=unit_types,
                                  width=30, font=('Segoe UI', 11), state="readonly")
        unit_combo.pack(anchor='w', pady=(5, 0))

        # Established Date
        date_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
        date_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(date_frame, text="Established Date:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')

        date_entry_frame = tk.Frame(date_frame, bg=self.colors["content_bg"])
        date_entry_frame.pack(anchor='w', pady=(5, 0))

        date_entry = tk.Entry(date_entry_frame, textvariable=self.established_date_var,
                              width=15, font=('Segoe UI', 11))
        date_entry.pack(side='left')

        tk.Label(date_entry_frame, text="(YYYY-MM-DD)", bg=self.colors["content_bg"],
                 fg=self.colors["text_secondary"], font=('Segoe UI', 9)).pack(side='left', padx=(10, 0))

        today_btn = tk.Button(date_entry_frame,
                              text="Today",
                              bg=self.colors["accent"],
                              fg=self.colors["text_light"],
                              font=('Segoe UI', 9),
                              relief='flat',
                              padx=10,
                              pady=2,
                              border=0,
                              command=lambda: self.established_date_var.set(datetime.now().strftime("%Y-%m-%d")))
        today_btn.pack(side='left', padx=(10, 0))

        # Description
        desc_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
        desc_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(desc_frame, text="Description:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')

        self.description_text = tk.Text(desc_frame, width=50, height=4, font=('Segoe UI', 10))
        self.description_text.pack(anchor='w', pady=(5, 0))

        # Set initial description text
        if self.description_var.get():
            self.description_text.insert('1.0', self.description_var.get())

    def create_contact_info_section(self, parent):
        """Create contact information section"""
        section_frame = self.create_section_frame(parent, "📞 Contact Information")

        # Location
        self.create_form_field(section_frame, "Base Location:", self.location_var, 0)

        # Phone
        self.create_form_field(section_frame, "Contact Phone:", self.contact_phone_var, 1)

        # Email
        self.create_form_field(section_frame, "Contact Email:", self.contact_email_var, 2)

    def create_organizational_info_section(self, parent):
        """Create organizational structure section"""
        section_frame = self.create_section_frame(parent, "🎖️ Organizational Structure")

        # Current structure info (read-only)
        structure_info = self.get_organizational_structure()

        info_text = tk.Text(section_frame, width=60, height=8, font=('Segoe UI', 10),
                            state='disabled', bg=self.colors["card_shadow"])
        info_text.grid(row=0, column=0, columnspan=2, sticky='ew', pady=10)

        info_text.config(state='normal')
        info_text.insert('1.0', structure_info)
        info_text.config(state='disabled')

    def create_statistics_section(self, parent):
        """Create company statistics section"""
        section_frame = self.create_section_frame(parent, "📊 Company Statistics")

        stats = self.company.get_company_statistics()

        # Create stats grid
        stats_grid = tk.Frame(section_frame, bg=self.colors["content_bg"])
        stats_grid.grid(row=0, column=0, columnspan=2, sticky='ew', pady=10)

        # Stat cards
        self.create_stat_card(stats_grid, "👥", "Total Personnel", str(stats['total_soldiers']), 0, 0)
        self.create_stat_card(stats_grid, "🎖️", "Platoons", str(stats['total_platoons']), 0, 1)
        self.create_stat_card(stats_grid, "🎯", "Active Missions", str(stats['total_missions']), 0, 2)

        # Authorization breakdown
        if stats['authorization_distribution']:
            auth_frame = tk.Frame(section_frame, bg=self.colors["content_bg"])
            auth_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(20, 0))

            tk.Label(auth_frame, text="Authorization Distribution:", bg=self.colors["content_bg"],
                     fg=self.colors["text_primary"], font=('Segoe UI', 12, 'bold')).pack(anchor='w')

            auth_text = ""
            for auth, count in stats['authorization_distribution'].items():
                auth_text += f"• {auth}: {count} personnel\n"

            auth_label = tk.Label(auth_frame, text=auth_text, bg=self.colors["content_bg"],
                                  fg=self.colors["text_secondary"], font=('Segoe UI', 10),
                                  justify='left', anchor='nw')
            auth_label.pack(anchor='w', padx=(20, 0), pady=(5, 0))

        # Refresh button
        refresh_btn = tk.Button(section_frame,
                                text="🔄 Refresh Statistics",
                                bg=self.colors["sidebar_hover"],
                                fg=self.colors["text_light"],
                                font=('Segoe UI', 10),
                                relief='flat',
                                padx=15,
                                pady=8,
                                border=0,
                                command=self.refresh_statistics)
        refresh_btn.grid(row=2, column=0, sticky='w', pady=(20, 0))

    def create_action_buttons(self, parent):
        """Create action buttons section"""
        button_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        button_frame.pack(fill='x', pady=(30, 20))

        # Save button
        save_btn = tk.Button(button_frame,
                             text="💾 Save Company Information",
                             bg=self.colors["accent"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 12, 'bold'),
                             relief='flat',
                             padx=25,
                             pady=12,
                             border=0,
                             command=self.save_company_info)
        save_btn.pack(side='left', padx=(0, 15))

        # Reset button
        reset_btn = tk.Button(button_frame,
                              text="🔄 Reset to Saved",
                              bg=self.colors["text_secondary"],
                              fg=self.colors["text_light"],
                              font=('Segoe UI', 11),
                              relief='flat',
                              padx=20,
                              pady=12,
                              border=0,
                              command=self.reset_form)
        reset_btn.pack(side='left')

        # Export button
        export_btn = tk.Button(button_frame,
                               text="📄 Export Company Report",
                               bg=self.colors["sidebar_hover"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='flat',
                               padx=20,
                               pady=12,
                               border=0,
                               command=self.export_company_report)
        export_btn.pack(side='right')

    def create_section_frame(self, parent, title):
        """Create a section frame with title"""
        # Section container
        container = tk.Frame(parent, bg=self.colors["content_bg"])
        container.pack(fill='x', pady=(0, 30))

        # Section title
        title_label = tk.Label(container,
                               text=title,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w', pady=(0, 15))

        # Section content frame
        content_frame = tk.Frame(container, bg=self.colors["content_bg"], relief='solid', bd=1)
        content_frame.pack(fill='x', padx=(0, 20))

        # Inner padding frame
        inner_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
        inner_frame.pack(fill='x', padx=20, pady=20)

        # Configure grid weights
        inner_frame.grid_columnconfigure(1, weight=1)

        return inner_frame

    def create_form_field(self, parent, label_text, text_var, row, required=False):
        """Create a form field with label and entry"""
        label_text_display = label_text + " *" if required else label_text

        tk.Label(parent, text=label_text_display, bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).grid(
            row=row, column=0, sticky='w', pady=10, padx=(0, 20))

        entry = tk.Entry(parent, textvariable=text_var, width=40, font=('Segoe UI', 11))
        entry.grid(row=row, column=1, sticky='w', pady=10)

        return entry

    def create_stat_card(self, parent, icon, title, value, row, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=self.colors["card_shadow"], relief='solid', bd=1,
                        width=120, height=80)
        card.grid(row=row, column=column, padx=5, pady=5, sticky='ew')
        card.grid_propagate(False)

        # Configure grid weights
        parent.grid_columnconfigure(column, weight=1)

        # Card content
        content = tk.Frame(card, bg=self.colors["card_shadow"])
        content.pack(expand=True, fill='both', padx=10, pady=10)

        # Icon
        icon_label = tk.Label(content,
                              text=icon,
                              bg=self.colors["card_shadow"],
                              fg=self.colors["accent"],
                              font=('Segoe UI', 16))
        icon_label.pack()

        # Value
        value_label = tk.Label(content,
                               text=value,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 14, 'bold'))
        value_label.pack()

        # Title
        title_label = tk.Label(content,
                               text=title,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 8))
        title_label.pack()

    def get_organizational_structure(self):
        """Get formatted organizational structure information"""
        structure = f"Company: {self.company.name}\n"
        structure += f"Total Personnel: {len(self.company.get_all_soldiers())}\n"
        structure += f"Number of Platoons: {len(self.company.platoons)}\n"
        structure += f"Active Missions: {len(self.company.missions)}\n\n"

        if self.company.platoons:
            structure += "Platoon Structure:\n"
            for platoon in self.company.platoons:
                structure += f"  • {platoon.name}: {len(platoon.soldiers)} soldiers\n"
                if platoon.soldiers:
                    for soldier in platoon.soldiers[:3]:  # Show first 3 soldiers
                        structure += f"    - {soldier.name} ({soldier.serial_number})\n"
                    if len(platoon.soldiers) > 3:
                        structure += f"    - ... and {len(platoon.soldiers) - 3} more\n"
        else:
            structure += "No platoons created yet.\n"

        return structure

    def save_company_info(self):
        """Save company information"""
        try:
            # Validate required fields
            if not self.company_name_var.get().strip():
                messagebox.showerror("Error", "Company name is required!")
                return

            # Validate date format if provided
            if self.established_date_var.get().strip():
                try:
                    datetime.strptime(self.established_date_var.get(), "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return

            # Update company name
            self.company.name = self.company_name_var.get().strip()

            # Update company policies with additional info
            self.company.company_policies.update({
                'commander': self.commander_var.get().strip(),
                'location': self.location_var.get().strip(),
                'contact_phone': self.contact_phone_var.get().strip(),
                'contact_email': self.contact_email_var.get().strip(),
                'established_date': self.established_date_var.get().strip(),
                'unit_type': self.unit_type_var.get(),
                'description': self.description_text.get('1.0', 'end-1c').strip(),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            messagebox.showinfo("Success", "Company information saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save company information: {str(e)}")

    def reset_form(self):
        """Reset form to saved values"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all changes?"):
            self.load_company_data()
            self.description_text.delete('1.0', 'end')
            if self.description_var.get():
                self.description_text.insert('1.0', self.description_var.get())

    def refresh_statistics(self):
        """Refresh the statistics section"""
        self.create_tab()  # Refresh the entire tab

    def export_company_report(self):
        """Export comprehensive company report"""
        try:
            filename = f"{self.company.name.replace(' ', '_')}_company_report.txt"

            with open(filename, 'w') as f:
                # Company header
                f.write("=" * 60 + "\n")
                f.write(f"COMPANY REPORT - {self.company.name.upper()}\n")
                f.write("=" * 60 + "\n\n")

                # Basic information
                f.write("BASIC INFORMATION:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Company Name: {self.company_name_var.get()}\n")
                f.write(f"Commanding Officer: {self.commander_var.get() or 'Not specified'}\n")
                f.write(f"Unit Type: {self.unit_type_var.get()}\n")
                f.write(f"Established: {self.established_date_var.get() or 'Not specified'}\n")
                f.write(f"Location: {self.location_var.get() or 'Not specified'}\n")
                f.write(f"Contact Phone: {self.contact_phone_var.get() or 'Not specified'}\n")
                f.write(f"Contact Email: {self.contact_email_var.get() or 'Not specified'}\n")

                description = self.description_text.get('1.0', 'end-1c').strip()
                if description:
                    f.write(f"Description: {description}\n")

                f.write(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # Organizational structure
                f.write("ORGANIZATIONAL STRUCTURE:\n")
                f.write("-" * 30 + "\n")
                f.write(self.get_organizational_structure())
                f.write("\n")

                # Statistics
                stats = self.company.get_company_statistics()
                f.write("COMPANY STATISTICS:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Total Personnel: {stats['total_soldiers']}\n")
                f.write(f"Total Platoons: {stats['total_platoons']}\n")
                f.write(f"Total Missions: {stats['total_missions']}\n\n")

                if stats['authorization_distribution']:
                    f.write("AUTHORIZATION DISTRIBUTION:\n")
                    f.write("-" * 30 + "\n")
                    for auth, count in stats['authorization_distribution'].items():
                        f.write(f"  {auth}: {count} personnel\n")
                    f.write("\n")

                # Platoon details
                if stats['platoon_details']:
                    f.write("PLATOON BREAKDOWN:\n")
                    f.write("-" * 20 + "\n")
                    for platoon_name, details in stats['platoon_details'].items():
                        f.write(f"  {platoon_name}:\n")
                        f.write(f"    Soldiers: {details['soldier_count']}\n")
                        f.write(f"    Assigned Missions: {details['assigned_missions']}\n")
                        if details['authorizations']:
                            f.write("    Available Authorizations:\n")
                            for auth, count in details['authorizations'].items():
                                f.write(f"      - {auth}: {count}\n")
                        f.write("\n")

                # Mission coverage
                f.write("MISSION COVERAGE ANALYSIS:\n")
                f.write("-" * 30 + "\n")
                for mission_name, coverage in stats['mission_coverage'].items():
                    f.write(f"  {mission_name}:\n")
                    f.write(f"    Personnel Required: {coverage['personnel_required']}\n")
                    f.write(f"    Required Authorizations: {', '.join(coverage['required_authorizations'])}\n")
                    f.write(
                        f"    Capable Platoons: {', '.join(coverage['capable_platoons']) if coverage['capable_platoons'] else 'None'}\n")
                    f.write("\n")

            messagebox.showinfo("Success", f"Company report exported to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")