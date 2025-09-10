import tkinter as tk
from tkinter import ttk, messagebox


class AuthorizationManager:
    def __init__(self, parent, colors, authorizations_list):
        self.result = None
        self.colors = colors
        self.authorizations = authorizations_list.copy()  # Work with a copy

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Manage Authorizations")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=colors["content_bg"])

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))

        self.create_widgets()

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.dialog, bg=self.colors["content_bg"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame,
                               text="🔐 Manage Authorizations",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 18, 'bold'))
        title_label.pack(pady=(0, 20))

        # Instructions
        instructions = tk.Label(main_frame,
                                text="Add, edit, or remove authorization types for your military personnel:",
                                bg=self.colors["content_bg"],
                                fg=self.colors["text_secondary"],
                                font=('Segoe UI', 11))
        instructions.pack(pady=(0, 15))

        # List frame
        list_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        list_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Authorization listbox with scrollbar
        list_container = tk.Frame(list_frame, bg=self.colors["content_bg"])
        list_container.pack(fill='both', expand=True)

        self.auth_listbox = tk.Listbox(list_container,
                                       font=('Segoe UI', 11),
                                       bg=self.colors["content_bg"],
                                       fg=self.colors["text_primary"],
                                       selectbackground=self.colors["accent"],
                                       selectforeground=self.colors["text_light"],
                                       height=15)

        scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.auth_listbox.yview)
        self.auth_listbox.configure(yscrollcommand=scrollbar.set)

        self.auth_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Populate listbox
        self.refresh_list()

        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        buttons_frame.pack(fill='x', pady=(0, 20))

        # Add button
        add_btn = tk.Button(buttons_frame,
                            text="➕ Add New",
                            bg=self.colors["accent"],
                            fg=self.colors["text_light"],
                            font=('Segoe UI', 11, 'bold'),
                            relief='raised',
                            bd=2,
                            padx=15,
                            pady=8,
                            cursor='hand2',
                            command=self.add_authorization)
        add_btn.pack(side='left', padx=(0, 10))

        # Edit button
        edit_btn = tk.Button(buttons_frame,
                             text="✏️ Edit Selected",
                             bg=self.colors["sidebar_hover"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 11),
                             relief='raised',
                             bd=2,
                             padx=15,
                             pady=8,
                             cursor='hand2',
                             command=self.edit_authorization)
        edit_btn.pack(side='left', padx=(0, 10))

        # Delete button
        delete_btn = tk.Button(buttons_frame,
                               text="🗑️ Delete Selected",
                               bg="#dc2626",
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='raised',
                               bd=2,
                               padx=15,
                               pady=8,
                               cursor='hand2',
                               command=self.delete_authorization)
        delete_btn.pack(side='left')

        # Bottom buttons frame
        bottom_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        bottom_frame.pack(fill='x')

        # Reset to defaults button
        reset_btn = tk.Button(bottom_frame,
                              text="🔄 Reset to Defaults",
                              bg=self.colors["text_secondary"],
                              fg=self.colors["text_light"],
                              font=('Segoe UI', 10),
                              relief='raised',
                              bd=2,
                              padx=15,
                              pady=6,
                              cursor='hand2',
                              command=self.reset_to_defaults)
        reset_btn.pack(side='left')

        # Save and Cancel buttons
        save_btn = tk.Button(bottom_frame,
                             text="💾 Save Changes",
                             bg=self.colors["accent"],
                             fg=self.colors["text_light"],
                             font=('Segoe UI', 12, 'bold'),
                             relief='raised',
                             bd=2,
                             padx=20,
                             pady=10,
                             cursor='hand2',
                             command=self.save_changes)
        save_btn.pack(side='right', padx=(10, 0))

        cancel_btn = tk.Button(bottom_frame,
                               text="Cancel",
                               bg=self.colors["text_secondary"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=10,
                               cursor='hand2',
                               command=self.cancel)
        cancel_btn.pack(side='right')

    def refresh_list(self):
        """Refresh the authorization listbox"""
        self.auth_listbox.delete(0, tk.END)
        for auth in sorted(self.authorizations):
            self.auth_listbox.insert(tk.END, auth)

    def add_authorization(self):
        """Add a new authorization"""
        new_auth = tk.simpledialog.askstring(
            "Add Authorization",
            "Enter the name of the new authorization:",
            parent=self.dialog
        )

        if new_auth and new_auth.strip():
            new_auth = new_auth.strip()
            if new_auth not in self.authorizations:
                self.authorizations.append(new_auth)
                self.refresh_list()
                # Select the newly added item
                sorted_auths = sorted(self.authorizations)
                index = sorted_auths.index(new_auth)
                self.auth_listbox.selection_set(index)
                self.auth_listbox.see(index)
            else:
                messagebox.showwarning("Duplicate", "This authorization already exists!")

    def edit_authorization(self):
        """Edit the selected authorization"""
        selection = self.auth_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an authorization to edit!")
            return

        current_auth = self.auth_listbox.get(selection[0])
        new_auth = tk.simpledialog.askstring(
            "Edit Authorization",
            "Edit the authorization name:",
            initialvalue=current_auth,
            parent=self.dialog
        )

        if new_auth and new_auth.strip():
            new_auth = new_auth.strip()
            if new_auth != current_auth:
                if new_auth not in self.authorizations:
                    # Replace the old authorization
                    index = self.authorizations.index(current_auth)
                    self.authorizations[index] = new_auth
                    self.refresh_list()
                    # Select the edited item
                    sorted_auths = sorted(self.authorizations)
                    new_index = sorted_auths.index(new_auth)
                    self.auth_listbox.selection_set(new_index)
                    self.auth_listbox.see(new_index)
                else:
                    messagebox.showwarning("Duplicate", "This authorization already exists!")

    def delete_authorization(self):
        """Delete the selected authorization"""
        selection = self.auth_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an authorization to delete!")
            return

        auth_to_delete = self.auth_listbox.get(selection[0])

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete '{auth_to_delete}'?\n\n"
                               "Warning: This may affect soldiers who currently have this authorization."):
            self.authorizations.remove(auth_to_delete)
            self.refresh_list()

    def reset_to_defaults(self):
        """Reset to default authorizations"""
        if messagebox.askyesno("Reset to Defaults",
                               "Are you sure you want to reset to the default authorization list?\n\n"
                               "This will remove all custom authorizations you've added."):
            self.authorizations = [
                "Guard Duty", "Patrol", "Communications",
                "Equipment Maintenance", "Medical Support",
                "Driver", "Weapons Specialist", "Logistics"
            ]
            self.refresh_list()

    def save_changes(self):
        """Save the changes"""
        if not self.authorizations:
            messagebox.showerror("Error", "You must have at least one authorization!")
            return

        self.result = self.authorizations.copy()
        self.dialog.destroy()

    def cancel(self):
        """Cancel without saving"""
        self.dialog.destroy()


def show_authorization_manager(parent, colors, current_authorizations):
    """Show the authorization manager dialog and return the updated list"""
    manager = AuthorizationManager(parent, colors, current_authorizations)
    return manager.result