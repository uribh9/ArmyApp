import tkinter as tk
from tkinter import ttk, messagebox
from mission import Mission


class MissionsTab:
    def __init__(self, parent_frame, company, colors, shifts, authorizations):
        self.parent_frame = parent_frame
        self.company = company
        self.colors = colors
        self.shifts = shifts
        self.authorizations = authorizations
        self.missions_tree = None

    def create_tab(self):
        """Create the missions management tab"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.create_page_header("🎯 Missions", "Define missions and requirements")

        # Action buttons
        actions_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        actions_frame.pack(fill='x', padx=40, pady=(0, 20))

        add_btn = tk.Button(actions_frame,
                            text="➕ Add New Mission",
                            bg=self.colors["accent"],
                            fg=self.colors["text_light"],
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat',
                            padx=20,
                            pady=10,
                            border=0,
                            command=self.add_mission_dialog)
        add_btn.pack(side='left', padx=(0, 15))

        edit_btn = tk.Button(actions_frame,
                             text="✏️ Edit Selected",
                             bg=self.colors["sidebar_hover"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 11),
                             relief='flat',
                             padx=20,
                             pady=10,
                             border=0,
                             command=self.edit_selected_mission)
        edit_btn.pack(side='left', padx=(0, 15))

        delete_btn = tk.Button(actions_frame,
                               text="🗑️ Delete Selected",
                               bg="#dc2626",
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='flat',
                               padx=20,
                               pady=10,
                               border=0,
                               command=self.delete_selected_mission)
        delete_btn.pack(side='left')

        # Missions list
        list_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        list_frame.pack(fill='both', expand=True, padx=40, pady=(0, 20))

        # Create treeview for missions
        columns = ('Daily Personnel', 'Shift Hours', 'Required Authorizations')
        self.missions_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')

        # Configure columns
        self.missions_tree.heading('#0', text='Mission Name')
        self.missions_tree.column('#0', width=150, minwidth=100)

        column_widths = {'Daily Personnel': 120, 'Shift Hours': 250, 'Required Authorizations': 300}
        for col in columns:
            self.missions_tree.heading(col, text=col)
            self.missions_tree.column(col, width=column_widths[col], minwidth=80)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.missions_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.missions_tree.xview)
        self.missions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.missions_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Show empty state if no missions
        if not self.company.missions:
            self.show_empty_state()
        else:
            self.refresh_missions_list()

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

    def show_empty_state(self):
        """Show empty state when no missions exist"""
        empty_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        empty_frame.pack(expand=True, fill='both')

        # Center content
        center_frame = tk.Frame(empty_frame, bg=self.colors["content_bg"])
        center_frame.pack(expand=True)

        # Empty state icon and text
        icon_label = tk.Label(center_frame,
                              text="🎯",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 48))
        icon_label.pack(pady=20)

        empty_label = tk.Label(center_frame,
                               text="No missions defined yet",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        empty_label.pack()

        desc_label = tk.Label(center_frame,
                              text="Define your first mission with shift requirements",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 12))
        desc_label.pack(pady=(5, 20))

        add_first_btn = tk.Button(center_frame,
                                  text="➕ Create First Mission",
                                  bg=self.colors["accent"],
                                  fg=self.colors["text_light"],
                                  font=('Segoe UI', 12, 'bold'),
                                  relief='flat',
                                  padx=25,
                                  pady=12,
                                  border=0,
                                  command=self.add_mission_dialog)
        add_first_btn.pack()

    def add_mission_dialog(self):
        """Open dialog to add a new mission"""
        dialog = MissionDialog(self.parent_frame, self.colors, self.shifts, self.authorizations)
        if dialog.result:
            mission_data = dialog.result

            # Check if mission already exists
            if self.company.get_mission_by_name(mission_data['name']):
                messagebox.showerror("Error", "A mission with this name already exists!")
                return

            # Create new mission
            new_mission = Mission(
                mission_data['name'],
                mission_data['shift_hours'],
                mission_data['required_authorizations'],
                mission_data['daily_personnel']
            )

            self.company.add_mission(new_mission)
            messagebox.showinfo("Success", f"Mission {mission_data['name']} created successfully!")
            self.create_tab()  # Refresh the tab

    def edit_selected_mission(self):
        """Edit the selected mission"""
        selection = self.missions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mission to edit!")
            return

        mission_name = self.missions_tree.item(selection[0])['text']
        mission = self.company.get_mission_by_name(mission_name)

        if mission:
            dialog = MissionDialog(self.parent_frame, self.colors, self.shifts, self.authorizations, mission)
            if dialog.result:
                mission_data = dialog.result

                # Check if new name conflicts with existing missions
                if mission_data['name'] != mission_name and self.company.get_mission_by_name(mission_data['name']):
                    messagebox.showerror("Error", "A mission with this name already exists!")
                    return

                # Update mission data
                mission.name = mission_data['name']
                mission.shift_hours = mission_data['shift_hours']
                mission.required_authorizations = mission_data['required_authorizations']
                mission.daily_personnel = mission_data['daily_personnel']
                mission._calculate_shift_distribution()

                self.refresh_missions_list()
                messagebox.showinfo("Success", "Mission updated successfully!")

    def delete_selected_mission(self):
        """Delete the selected mission"""
        selection = self.missions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mission to delete!")
            return

        mission_name = self.missions_tree.item(selection[0])['text']

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete mission {mission_name}?"):
            mission = self.company.get_mission_by_name(mission_name)
            if mission:
                self.company.remove_mission(mission)
                self.filtered_missions = self.company.missions
                self.refresh_missions_list()
                self.perform_search()  # Update search results
                messagebox.showinfo("Success", "Mission deleted successfully!")

    def refresh_missions_list(self):
        """Refresh the missions list display"""
        if not self.missions_tree:
            return

        # Clear existing items
        for item in self.missions_tree.get_children():
            self.missions_tree.delete(item)

        # Use filtered missions if search is active
        missions_to_show = self.filtered_missions if hasattr(self,
                                                             'filtered_missions') and self.filtered_missions is not None else self.company.missions

        if not missions_to_show:
            if not self.company.missions:
                self.create_tab()  # Show empty state
            return

        for mission in missions_to_show:
            shift_hours_str = " | ".join([f"{k}: {v}" for k, v in mission.shift_hours.items()])
            auth_str = ", ".join(mission.required_authorizations)

            self.missions_tree.insert('', 'end', text=mission.name,
                                      values=(mission.daily_personnel, shift_hours_str, auth_str))


class MissionDialog:
    def __init__(self, parent, colors, shifts, authorizations, mission=None):
        self.result = None
        self.colors = colors
        self.shifts = shifts
        self.authorizations = authorizations

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Mission" if mission is None else "Edit Mission")
        self.dialog.geometry("600x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=colors["content_bg"])

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))

        # Variables
        self.name_var = tk.StringVar(value=mission.name if mission else "")
        self.personnel_var = tk.StringVar(value=str(mission.daily_personnel) if mission else "1")

        # Shift hours variables
        self.shift_vars = {}
        for shift in shifts:
            var = tk.StringVar()
            if mission and shift in mission.shift_hours:
                var.set(mission.shift_hours[shift])
            else:
                # Default shift times
                defaults = {
                    "Morning": "06:00-14:00",
                    "Noon": "14:00-22:00",
                    "Night": "22:00-06:00"
                }
                var.set(defaults.get(shift, "08:00-16:00"))
            self.shift_vars[shift] = var

        # Authorization variables
        self.auth_vars = {}
        for auth in authorizations:
            var = tk.BooleanVar()
            if mission and auth in mission.required_authorizations:
                var.set(True)
            self.auth_vars[auth] = var

        self.create_widgets(mission)

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self, mission):
        # Create main canvas and scrollbar
        main_canvas = tk.Canvas(self.dialog, bg=self.colors["content_bg"])
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.colors["content_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Content frame
        content_frame = tk.Frame(scrollable_frame, bg=self.colors["content_bg"])
        content_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Title
        title_text = "Create New Mission" if mission is None else "Edit Mission"
        title_label = tk.Label(content_frame,
                               text=title_text,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        title_label.pack(anchor='w', pady=(0, 20))

        # Mission Name
        name_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
        name_frame.pack(fill='x', pady=10)

        tk.Label(name_frame, text="Mission Name:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        name_entry = tk.Entry(name_frame, textvariable=self.name_var, width=40, font=('Segoe UI', 11))
        name_entry.pack(anchor='w', pady=(5, 0))

        # Daily Personnel
        personnel_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
        personnel_frame.pack(fill='x', pady=10)

        tk.Label(personnel_frame, text="Daily Personnel Required:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        personnel_entry = tk.Entry(personnel_frame, textvariable=self.personnel_var, width=10, font=('Segoe UI', 11))
        personnel_entry.pack(anchor='w', pady=(5, 0))

        # Shift Hours Section
        shifts_label = tk.Label(content_frame, text="Shift Hours:", bg=self.colors["content_bg"],
                                fg=self.colors["text_primary"], font=('Segoe UI', 14, 'bold'))
        shifts_label.pack(anchor='w', pady=(20, 10))

        for shift in self.shifts:
            shift_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
            shift_frame.pack(fill='x', pady=5)

            tk.Label(shift_frame, text=f"{shift} Shift:", bg=self.colors["content_bg"],
                     fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            time_frame = tk.Frame(shift_frame, bg=self.colors["content_bg"])
            time_frame.pack(anchor='w', pady=(2, 0))

            tk.Entry(time_frame, textvariable=self.shift_vars[shift], width=20, font=('Segoe UI', 11)).pack(side='left')
            tk.Label(time_frame, text="(Format: HH:MM-HH:MM)", bg=self.colors["content_bg"],
                     fg=self.colors["text_secondary"], font=('Segoe UI', 9)).pack(side='left', padx=(10, 0))

        # Required Authorizations Section
        auth_label = tk.Label(content_frame, text="Required Authorizations:", bg=self.colors["content_bg"],
                              fg=self.colors["text_primary"], font=('Segoe UI', 14, 'bold'))
        auth_label.pack(anchor='w', pady=(20, 10))

        # Create authorization checkboxes in a grid
        auth_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
        auth_frame.pack(fill='x', pady=5)

        row = 0
        col = 0
        for auth in self.authorizations:
            cb = tk.Checkbutton(auth_frame, text=auth, variable=self.auth_vars[auth],
                                bg=self.colors["content_bg"], fg=self.colors["text_primary"],
                                font=('Segoe UI', 10), selectcolor=self.colors["content_bg"])
            cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)

            col += 1
            if col >= 2:  # 2 columns
                col = 0
                row += 1

        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors["content_bg"])
        button_frame.pack(fill='x', pady=(30, 0))

        save_btn = tk.Button(button_frame,
                             text="Save Mission",
                             bg=self.colors["accent"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 11, 'bold'),
                             relief='flat',
                             padx=20,
                             pady=10,
                             border=0,
                             command=self.save_mission)
        save_btn.pack(side='right', padx=(10, 0))

        cancel_btn = tk.Button(button_frame,
                               text="Cancel",
                               bg=self.colors["text_secondary"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='flat',
                               padx=20,
                               pady=10,
                               border=0,
                               command=self.cancel)
        cancel_btn.pack(side='right')

        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def save_mission(self):
        # Validate input
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Mission name is required!")
            return

        try:
            daily_personnel = int(self.personnel_var.get())
            if daily_personnel <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Daily personnel must be a positive number!")
            return

        # Validate shift hours format
        shift_hours = {}
        for shift, var in self.shift_vars.items():
            hours = var.get().strip()
            if hours:
                if not self.validate_time_format(hours):
                    messagebox.showerror("Error", f"Invalid time format for {shift} shift!\nUse format: HH:MM-HH:MM")
                    return
                shift_hours[shift] = hours

        if not shift_hours:
            messagebox.showerror("Error", "At least one shift time is required!")
            return

        # Get selected authorizations
        selected_auths = [auth for auth, var in self.auth_vars.items() if var.get()]

        if not selected_auths:
            messagebox.showerror("Error", "At least one authorization is required!")
            return

        # Store result
        self.result = {
            'name': self.name_var.get().strip(),
            'daily_personnel': daily_personnel,
            'shift_hours': shift_hours,
            'required_authorizations': selected_auths
        }

        self.dialog.destroy()

    def validate_time_format(self, time_str):
        """Validate time format HH:MM-HH:MM"""
        try:
            if '-' not in time_str:
                return False

            start_time, end_time = time_str.split('-')

            # Validate start time
            start_parts = start_time.split(':')
            if len(start_parts) != 2:
                return False
            start_hour, start_min = int(start_parts[0]), int(start_parts[1])
            if not (0 <= start_hour <= 23 and 0 <= start_min <= 59):
                return False

            # Validate end time
            end_parts = end_time.split(':')
            if len(end_parts) != 2:
                return False
            end_hour, end_min = int(end_parts[0]), int(end_parts[1])
            if not (0 <= end_hour <= 23 and 0 <= end_min <= 59):
                return False

            return True
        except (ValueError, IndexError):
            return False

    def cancel(self):
        self.dialog.destroy()