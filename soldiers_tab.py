import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from soldier import Soldier


class SoldiersTab:
    def __init__(self, parent_frame, company, colors, shifts, authorizations):
        self.parent_frame = parent_frame
        self.company = company
        self.colors = colors
        self.shifts = shifts
        self.authorizations = authorizations
        self.soldiers_tree = None

    def create_tab(self):
        """Create the soldiers management tab"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.create_page_header("👥 Soldiers", "Manage soldier information and authorizations")

        # Action buttons
        actions_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        actions_frame.pack(fill='x', padx=40, pady=(0, 20))

        add_btn = tk.Button(actions_frame,
                            text="➕ Add New Soldier",
                            bg=self.colors["accent"],
                            fg=self.colors["text_light"],
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat',
                            padx=20,
                            pady=10,
                            border=0,
                            command=self.add_soldier_dialog)
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
                             command=self.edit_selected_soldier)
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
                               command=self.delete_selected_soldier)
        delete_btn.pack(side='left')

        # Soldiers list
        list_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        list_frame.pack(fill='both', expand=True, padx=40, pady=(0, 20))

        # Create treeview for soldiers
        columns = ('Serial Number', 'Platoon', 'Preferred Shift', 'Authorizations')
        self.soldiers_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')

        # Configure columns
        self.soldiers_tree.heading('#0', text='Name')
        self.soldiers_tree.column('#0', width=150, minwidth=100)

        column_widths = {'Serial Number': 120, 'Platoon': 100, 'Preferred Shift': 120, 'Authorizations': 300}
        for col in columns:
            self.soldiers_tree.heading(col, text=col)
            self.soldiers_tree.column(col, width=column_widths[col], minwidth=80)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.soldiers_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.soldiers_tree.xview)
        self.soldiers_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.soldiers_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Show empty state if no soldiers
        if not self.company.get_all_soldiers():
            self.show_empty_state()
        else:
            self.refresh_soldiers_list()

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
        """Show empty state when no soldiers exist"""
        empty_frame = tk.Frame(self.parent_frame, bg=self.colors["content_bg"])
        empty_frame.pack(expand=True, fill='both')

        # Center content
        center_frame = tk.Frame(empty_frame, bg=self.colors["content_bg"])
        center_frame.pack(expand=True)

        # Empty state icon and text
        icon_label = tk.Label(center_frame,
                              text="👥",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 48))
        icon_label.pack(pady=20)

        empty_label = tk.Label(center_frame,
                               text="No soldiers added yet",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        empty_label.pack()

        desc_label = tk.Label(center_frame,
                              text="Start by adding your first soldier to the system",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 12))
        desc_label.pack(pady=(5, 20))

        add_first_btn = tk.Button(center_frame,
                                  text="➕ Add First Soldier",
                                  bg=self.colors["accent"],
                                  fg=self.colors["text_light"],
                                  font=('Segoe UI', 12, 'bold'),
                                  relief='flat',
                                  padx=25,
                                  pady=12,
                                  border=0,
                                  command=self.add_soldier_dialog)
        add_first_btn.pack()

    def add_soldier_dialog(self):
        """Open dialog to add a new soldier"""
        dialog = SoldierDialog(self.parent_frame, self.authorizations, self.shifts,
                               [p.name for p in self.company.platoons], self.colors)
        if dialog.result:
            soldier_data = dialog.result
            soldier = Soldier(
                soldier_data['name'],
                soldier_data['serial_number'],
                soldier_data['platoon'],
                soldier_data['preferred_shift'],
                soldier_data['authorizations']
            )

            # Add to appropriate platoon or create new one
            if soldier_data['platoon']:
                platoon = self.company.get_platoon_by_name(soldier_data['platoon'])
                if platoon:
                    platoon.add_soldier(soldier)
                else:
                    # Create new platoon if it doesn't exist
                    from platoon import Platoon
                    new_platoon = Platoon(soldier_data['platoon'])
                    new_platoon.add_soldier(soldier)
                    self.company.add_platoon(new_platoon)

                messagebox.showinfo("Success", f"Soldier {soldier.name} added successfully!")
                self.create_tab()  # Refresh the tab
            else:
                messagebox.showerror("Error", "Please select or enter a platoon name!")

    def edit_selected_soldier(self):
        """Edit the selected soldier"""
        selection = self.soldiers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a soldier to edit!")
            return

        # Get soldier name from selection
        soldier_name = self.soldiers_tree.item(selection[0])['text']
        soldier = None

        # Find the soldier
        for s in self.company.get_all_soldiers():
            if s.name == soldier_name:
                soldier = s
                break

        if soldier:
            dialog = SoldierDialog(self.parent_frame, self.authorizations, self.shifts,
                                   [p.name for p in self.company.platoons], self.colors, soldier)
            if dialog.result:
                # Update soldier data
                soldier_data = dialog.result
                old_platoon_name = soldier.platoon

                soldier.name = soldier_data['name']
                soldier.serial_number = soldier_data['serial_number']
                soldier.preferred_shift = soldier_data['preferred_shift']
                soldier.authorizations = soldier_data['authorizations']

                # Handle platoon change
                if old_platoon_name != soldier_data['platoon']:
                    old_platoon = self.company.get_platoon_by_name(old_platoon_name)
                    new_platoon = self.company.get_platoon_by_name(soldier_data['platoon'])

                    if old_platoon:
                        old_platoon.remove_soldier(soldier)

                    if new_platoon:
                        new_platoon.add_soldier(soldier)
                    else:
                        # Create new platoon if needed
                        from platoon import Platoon
                        new_platoon = Platoon(soldier_data['platoon'])
                        new_platoon.add_soldier(soldier)
                        self.company.add_platoon(new_platoon)

                self.refresh_soldiers_list()
                messagebox.showinfo("Success", "Soldier updated successfully!")

    def delete_selected_soldier(self):
        """Delete the selected soldier"""
        selection = self.soldiers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a soldier to delete!")
            return

        soldier_name = self.soldiers_tree.item(selection[0])['text']

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete soldier {soldier_name}?"):
            # Find and remove soldier
            for platoon in self.company.platoons:
                for soldier in platoon.soldiers:
                    if soldier.name == soldier_name:
                        platoon.remove_soldier(soldier)
                        self.filtered_soldiers = self.company.get_all_soldiers()
                        self.refresh_soldiers_list()
                        self.perform_search()  # Update search results
                        messagebox.showinfo("Success", "Soldier deleted successfully!")
                        return

    def refresh_soldiers_list(self):
        """Refresh the soldiers list display"""
        if not self.soldiers_tree:
            return

        # Clear existing items
        for item in self.soldiers_tree.get_children():
            self.soldiers_tree.delete(item)

        # Use filtered soldiers if search is active, otherwise all soldiers
        soldiers_to_show = self.filtered_soldiers if hasattr(self,
                                                             'filtered_soldiers') and self.filtered_soldiers is not None else self.company.get_all_soldiers()

        if not soldiers_to_show:
            if not self.company.get_all_soldiers():
                self.create_tab()  # Show empty state if no soldiers at all
            return

        for soldier in soldiers_to_show:
            authorizations_str = ", ".join(soldier.authorizations)
            self.soldiers_tree.insert('', 'end', text=soldier.name,
                                      values=(soldier.serial_number, soldier.platoon,
                                              soldier.preferred_shift, authorizations_str))


class AuthorizationSelectionDialog:
    def __init__(self, parent, authorizations, current_vars, colors):
        self.result = None
        self.colors = colors
        self.current_vars = current_vars

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Authorizations")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=colors["content_bg"])

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100))

        self.create_widgets(authorizations)

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self, authorizations):
        # Title
        title_label = tk.Label(self.dialog,
                               text="Select Required Authorizations",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=15)

        # Instructions
        instr_label = tk.Label(self.dialog,
                               text="Soldiers must have ALL selected authorizations:",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10))
        instr_label.pack(pady=(0, 15))

        # Scrollable frame for authorizations
        canvas = tk.Canvas(self.dialog, bg=self.colors["content_bg"], height=300)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["content_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add checkboxes for all authorizations
        for auth in authorizations:
            var = self.current_vars.get(auth, tk.BooleanVar())
            if auth not in self.current_vars:
                self.current_vars[auth] = var

            cb = tk.Checkbutton(scrollable_frame, text=auth, variable=var,
                                bg=self.colors["content_bg"], fg=self.colors["text_primary"],
                                font=('Segoe UI', 10), selectcolor=self.colors["content_bg"])
            cb.pack(anchor='w', padx=20, pady=2)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        button_frame = tk.Frame(self.dialog, bg=self.colors["content_bg"])
        button_frame.pack(fill='x', pady=15)

        close_btn = tk.Button(button_frame,
                              text="Done",
                              bg=self.colors["accent"],
                              fg=self.colors["text_light"],
                              font=('Segoe UI', 11, 'bold'),
                              relief='flat',
                              padx=20,
                              pady=8,
                              border=0,
                              command=self.dialog.destroy)
        close_btn.pack()

        clear_all_btn = tk.Button(button_frame,
                                  text="Clear All",
                                  bg=self.colors["text_secondary"],
                                  fg=self.colors["text_light"],
                                  font=('Segoe UI', 10),
                                  relief='flat',
                                  padx=15,
                                  pady=6,
                                  border=0,
                                  command=self.clear_all)
        clear_all_btn.pack(pady=(10, 0))

    def clear_all(self):
        """Clear all authorization selections"""
        for var in self.current_vars.values():
            var.set(False)


class SoldierDialog:
    def __init__(self, parent, authorizations, shifts, platoons, colors, soldier=None):
        self.result = None
        self.colors = colors

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Soldier" if soldier is None else "Edit Soldier")
        self.dialog.geometry("500x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=colors["content_bg"])

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))

        # Variables
        self.name_var = tk.StringVar(value=soldier.name if soldier else "")
        self.serial_var = tk.StringVar(value=soldier.serial_number if soldier else "")
        self.platoon_var = tk.StringVar(value=soldier.platoon if soldier else "")
        self.shift_var = tk.StringVar(value=soldier.preferred_shift if soldier else shifts[0])

        # Authorization variables
        self.auth_vars = {}
        for auth in authorizations:
            var = tk.BooleanVar()
            if soldier and auth in soldier.authorizations:
                var.set(True)
            self.auth_vars[auth] = var

        self.create_widgets(authorizations, shifts, platoons)

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self, authorizations, shifts, platoons):
        # Main frame with padding
        main_frame = tk.Frame(self.dialog, bg=self.colors["content_bg"])
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Title
        title_text = "Add New Soldier" if not hasattr(self, 'soldier') else "Edit Soldier"
        title_label = tk.Label(main_frame,
                               text=title_text,
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        title_label.pack(anchor='w', pady=(0, 20))

        # Form fields
        fields_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        fields_frame.pack(fill='x', pady=(0, 20))

        row = 0

        # Name
        tk.Label(fields_frame, text="Name:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                                                     pady=10)
        name_entry = tk.Entry(fields_frame, textvariable=self.name_var, width=30, font=('Segoe UI', 11))
        name_entry.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
        row += 1

        # Serial Number
        tk.Label(fields_frame, text="Serial Number:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                                                     pady=10)
        serial_entry = tk.Entry(fields_frame, textvariable=self.serial_var, width=30, font=('Segoe UI', 11))
        serial_entry.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
        row += 1

        # Platoon
        tk.Label(fields_frame, text="Platoon:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                                                     pady=10)
        platoon_entry = tk.Entry(fields_frame, textvariable=self.platoon_var, width=30, font=('Segoe UI', 11))
        platoon_entry.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))

        # Add existing platoons as suggestions
        if platoons:
            suggestions_text = "Existing: " + ", ".join(platoons)
            tk.Label(fields_frame, text=suggestions_text, bg=self.colors["content_bg"],
                     fg=self.colors["text_secondary"], font=('Segoe UI', 9)).grid(row=row, column=2, sticky='w',
                                                                                  padx=(10, 0))
        row += 1

        # Preferred Shift
        tk.Label(fields_frame, text="Preferred Shift:", bg=self.colors["content_bg"],
                 fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                                                     pady=10)

        shift_frame = tk.Frame(fields_frame, bg=self.colors["content_bg"])
        shift_frame.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))

        for i, shift in enumerate(shifts):
            rb = tk.Radiobutton(shift_frame, text=shift, variable=self.shift_var, value=shift,
                                bg=self.colors["content_bg"], fg=self.colors["text_primary"],
                                font=('Segoe UI', 10), selectcolor=self.colors["content_bg"])
            rb.pack(side='left', padx=(0, 15))
        row += 1

        # Authorizations
        auth_label = tk.Label(fields_frame, text="Authorizations:", bg=self.colors["content_bg"],
                              fg=self.colors["text_primary"], font=('Segoe UI', 11, 'bold'))
        auth_label.grid(row=row, column=0, sticky='nw', pady=10)

        # Create scrollable frame for authorizations
        auth_canvas = tk.Canvas(fields_frame, height=200, width=300, bg=self.colors["content_bg"])
        auth_scrollbar = ttk.Scrollbar(fields_frame, orient="vertical", command=auth_canvas.yview)
        auth_scrollable_frame = tk.Frame(auth_canvas, bg=self.colors["content_bg"])

        auth_scrollable_frame.bind(
            "<Configure>",
            lambda e: auth_canvas.configure(scrollregion=auth_canvas.bbox("all"))
        )

        auth_canvas.create_window((0, 0), window=auth_scrollable_frame, anchor="nw")
        auth_canvas.configure(yscrollcommand=auth_scrollbar.set)

        # Add checkboxes for authorizations
        for auth in authorizations:
            cb = tk.Checkbutton(auth_scrollable_frame, text=auth, variable=self.auth_vars[auth],
                                bg=self.colors["content_bg"], fg=self.colors["text_primary"],
                                font=('Segoe UI', 10), selectcolor=self.colors["content_bg"])
            cb.pack(anchor='w', pady=2)

        auth_canvas.grid(row=row, column=1, sticky='w', pady=10, padx=(10, 0))
        auth_scrollbar.grid(row=row, column=2, sticky='ns', pady=10)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        button_frame.pack(fill='x', pady=(20, 0))

        save_btn = tk.Button(button_frame,
                             text="Save Soldier",
                             bg=self.colors["accent"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 11, 'bold'),
                             relief='flat',
                             padx=20,
                             pady=10,
                             border=0,
                             command=self.save_soldier)
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

    def save_soldier(self):
        # Validate input
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required!")
            return

        if not self.serial_var.get().strip():
            messagebox.showerror("Error", "Serial number is required!")
            return

        if not self.platoon_var.get().strip():
            messagebox.showerror("Error", "Platoon is required!")
            return

        # Get selected authorizations
        selected_auths = [auth for auth, var in self.auth_vars.items() if var.get()]

        if not selected_auths:
            messagebox.showerror("Error", "At least one authorization is required!")
            return

        # Store result
        self.result = {
            'name': self.name_var.get().strip(),
            'serial_number': self.serial_var.get().strip(),
            'platoon': self.platoon_var.get().strip(),
            'preferred_shift': self.shift_var.get(),
            'authorizations': selected_auths
        }

        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()