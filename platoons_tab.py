import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from platoon import Platoon


class PlatoonsTab:
    def __init__(self, parent_frame, company, colors):
        self.parent_frame = parent_frame
        self.company = company
        self.colors = colors
        self.platoons_tree = None

    def create_tab(self):
        """Create the platoons management tab"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.create_page_header("🎖️ Platoons", "Organize platoons and assign soldiers")

        # Action buttons
        actions_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        actions_frame.pack(fill='x', padx=40, pady=(0, 20))

        add_btn = tk.Button(actions_frame,
                            text="➕ Add New Platoon",
                            bg=self.colors["accent"],
                            fg=self.colors["text_light"],
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat',
                            padx=20,
                            pady=10,
                            border=0,
                            command=self.add_platoon_dialog)
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
                             command=self.edit_selected_platoon)
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
                               command=self.delete_selected_platoon)
        delete_btn.pack(side='left')

        # Platoons list
        list_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        list_frame.pack(fill='both', expand=True, padx=40, pady=(0, 20))

        # Create treeview for platoons
        columns = ('Soldier Count', 'Assigned Missions', 'Authorizations Available')
        self.platoons_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')

        # Configure columns
        self.platoons_tree.heading('#0', text='Platoon Name')
        self.platoons_tree.column('#0', width=150, minwidth=100)

        column_widths = {'Soldier Count': 120, 'Assigned Missions': 200, 'Authorizations Available': 300}
        for col in columns:
            self.platoons_tree.heading(col, text=col)
            self.platoons_tree.column(col, width=column_widths[col], minwidth=80)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.platoons_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.platoons_tree.xview)
        self.platoons_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.platoons_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Show empty state if no platoons
        if not self.company.platoons:
            self.show_empty_state()
        else:
            self.refresh_platoons_list()

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
        """Show empty state when no platoons exist"""
        empty_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        empty_frame.pack(expand=True, fill='both')

        # Center content
        center_frame = tk.Frame(empty_frame, bg=self.colors["content_bg"])
        center_frame.pack(expand=True)

        # Empty state icon and text
        icon_label = tk.Label(center_frame,
                              text="🎖️",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 48))
        icon_label.pack(pady=20)

        empty_label = tk.Label(center_frame,
                               text="No platoons created yet",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        empty_label.pack()

        desc_label = tk.Label(center_frame,
                              text="Create your first platoon to organize soldiers",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 12))
        desc_label.pack(pady=(5, 20))

        add_first_btn = tk.Button(center_frame,
                                  text="➕ Create First Platoon",
                                  bg=self.colors["accent"],
                                  fg=self.colors["text_light"],
                                  font=('Segoe UI', 12, 'bold'),
                                  relief='flat',
                                  padx=25,
                                  pady=12,
                                  border=0,
                                  command=self.add_platoon_dialog)
        add_first_btn.pack()

    def add_platoon_dialog(self):
        """Open dialog to add a new platoon"""
        dialog = PlatoonDialog(self.parent_frame, self.colors)
        if dialog.result:
            platoon_name = dialog.result['name']

            # Check if platoon already exists
            if self.company.get_platoon_by_name(platoon_name):
                messagebox.showerror("Error", "A platoon with this name already exists!")
                return

            # Create new platoon
            new_platoon = Platoon(platoon_name)
            self.company.add_platoon(new_platoon)

            messagebox.showinfo("Success", f"Platoon {platoon_name} created successfully!")
            self.create_tab()  # Refresh the tab

    def edit_selected_platoon(self):
        """Edit the selected platoon"""
        selection = self.platoons_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a platoon to edit!")
            return

        platoon_name = self.platoons_tree.item(selection[0])['text']
        platoon = self.company.get_platoon_by_name(platoon_name)

        if platoon:
            dialog = PlatoonDialog(self.parent_frame, self.colors, platoon)
            if dialog.result:
                new_name = dialog.result['name']

                # Check if new name conflicts with existing platoons
                if new_name != platoon_name and self.company.get_platoon_by_name(new_name):
                    messagebox.showerror("Error", "A platoon with this name already exists!")
                    return

                # Update platoon name
                platoon.name = new_name

                # Update soldier references
                for soldier in platoon.soldiers:
                    soldier.platoon = new_name

                self.refresh_platoons_list()
                messagebox.showinfo("Success", "Platoon updated successfully!")

    def delete_selected_platoon(self):
        """Delete the selected platoon"""
        selection = self.platoons_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a platoon to delete!")
            return

        platoon_name = self.platoons_tree.item(selection[0])['text']
        platoon = self.company.get_platoon_by_name(platoon_name)

        if platoon and platoon.soldiers:
            messagebox.showerror("Error", "Cannot delete platoon with soldiers! Please reassign soldiers first.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete platoon {platoon_name}?"):
            if platoon:
                self.company.remove_platoon(platoon)
                self.refresh_platoons_list()
                messagebox.showinfo("Success", "Platoon deleted successfully!")

    def refresh_platoons_list(self):
        """Refresh the platoons list display"""
        if not self.platoons_tree:
            return

        # Clear existing items
        for item in self.platoons_tree.get_children():
            self.platoons_tree.delete(item)

        # Use filtered platoons if search is active
        if hasattr(self, 'filtered_platoons') and self.filtered_platoons is not None:
            platoons_to_show = self.filtered_platoons
        else:
            platoons_to_show = self.company.platoons
            self.filtered_platoons = self.company.platoons  # Initialize if not set

        if not platoons_to_show:
            if not self.company.platoons:
                self.create_tab()  # Show empty state
            return

        for platoon in platoons_to_show:
            soldier_count = len(platoon.soldiers)
            missions_str = ", ".join([m.name for m in platoon.weekly_missions]) if platoon.weekly_missions else "None"

            # Get available authorizations from soldiers
            auth_summary = platoon.get_authorization_summary()
            auth_str = ", ".join(
                [f"{auth}: {count}" for auth, count in auth_summary.items()]) if auth_summary else "None"

            self.platoons_tree.insert('', 'end', text=platoon.name,
                                      values=(soldier_count, missions_str, auth_str))
        if not self.platoons_tree:
            return

        # Clear existing items
        for item in self.platoons_tree.get_children():
            self.platoons_tree.delete(item)

        # Add all platoons
        if not self.company.platoons:
            self.create_tab()  # Show empty state
            return

        for platoon in self.company.platoons:
            soldier_count = len(platoon.soldiers)
            missions_str = ", ".join([m.name for m in platoon.weekly_missions]) if platoon.weekly_missions else "None"

            # Get available authorizations from soldiers
            auth_summary = platoon.get_authorization_summary()
            auth_str = ", ".join([f"{auth}: {count}" for auth, count in auth_summary.items()]) if auth_summary else "None"

            self.platoons_tree.insert('', 'end', text=platoon.name,
                                    values=(soldier_count, missions_str, auth_str))


class PlatoonDialog:
    def __init__(self, parent, colors, platoon=None):
        self.result = None
        self.colors = colors

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Platoon" if platoon is None else "Edit Platoon")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=colors["content_bg"])

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 150))

        # Variables
        self.name_var = tk.StringVar(value=platoon.name if platoon else "")

        self.create_widgets(platoon)

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self, platoon):
        # Main frame with padding
        main_frame = tk.Frame(self.dialog, bg=self.colors["content_bg"])
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Title
        title_text = "Create New Platoon" if platoon is None else "Edit Platoon"
        title_label = tk.Label(main_frame,
                              text=title_text,
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_primary"],
                              font=('Segoe UI', 18, 'bold'))
        title_label.pack(anchor='w', pady=(0, 20))

        # Form fields
        fields_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        fields_frame.pack(fill='x', pady=(0, 20))

        # Platoon Name
        tk.Label(fields_frame, text="Platoon Name:", bg=self.colors["content_bg"],
                fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 5))

        name_entry = tk.Entry(fields_frame, textvariable=self.name_var, width=40, font=('Segoe UI', 11))
        name_entry.pack(anchor='w', pady=(0, 10))
        name_entry.focus()

        # Instructions
        instructions = tk.Label(fields_frame,
                               text="Enter a unique name for the platoon (e.g., Alpha, Bravo, Charlie)",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10),
                               wraplength=300,
                               justify='left')
        instructions.pack(anchor='w', pady=(0, 20))

        # Show current soldiers if editing
        if platoon and platoon.soldiers:
            soldiers_label = tk.Label(fields_frame,
                                     text=f"Current soldiers in this platoon:",
                                     bg=self.colors["content_bg"],
                                     fg=self.colors["text_primary"],
                                     font=('Segoe UI', 11, 'bold'))
            soldiers_label.pack(anchor='w', pady=(0, 5))

            soldiers_list = tk.Label(fields_frame,
                                    text=", ".join([s.name for s in platoon.soldiers]),
                                    bg=self.colors["content_bg"],
                                    fg=self.colors["text_secondary"],
                                    font=('Segoe UI', 10),
                                    wraplength=300,
                                    justify='left')
            soldiers_list.pack(anchor='w')

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        button_frame.pack(fill='x', pady=(20, 0))

        save_btn = tk.Button(button_frame,
                            text="Save Platoon",
                            bg=self.colors["accent"],
                            fg=self.colors["text_light"],
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat',
                            padx=20,
                            pady=10,
                            border=0,
                            command=self.save_platoon)
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

    def save_platoon(self):
        # Validate input
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Platoon name is required!")
            return

        # Store result
        self.result = {
            'name': name
        }

        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()