import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from company import Company


class StartupDialog:
    def __init__(self, colors, parent_root=None):
        self.result = None
        self.colors = colors
        self.parent_root = parent_root
        self.selected_file = None

        # Create the startup window
        self.root = tk.Tk()
        self.root.title("Military Scheduling System - Startup")
        self.root.geometry("750x700")
        self.root.configure(bg=colors["content_bg"])

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 750) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"750x700+{x}+{y}")

        # Make it non-resizable and bring to front
        self.root.resizable(False, False)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()

        # If we have a parent root, hide it
        if self.parent_root:
            self.parent_root.withdraw()

        # Find existing company files
        self.company_files = self.find_company_files()

        self.create_widgets()

        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        print(f"Found {len(self.company_files)} company files")  # Debug

        # Run the dialog
        self.root.mainloop()

    def find_company_files(self):
        """Find all JSON files in the current directory that might be company files"""
        company_files = []
        current_dir = os.getcwd()

        try:
            for file in os.listdir(current_dir):
                if file.endswith('.json'):
                    try:
                        # Try to load the file and check if it's a valid company file
                        with open(file, 'r') as f:
                            data = json.load(f)
                            # Check if it has company-like structure
                            if 'name' in data and ('platoons' in data or 'missions' in data):
                                # Get file modification time
                                mod_time = os.path.getmtime(file)
                                company_files.append({
                                    'filename': file,
                                    'name': data.get('name', 'Unknown Company'),
                                    'platoons': len(data.get('platoons', [])),
                                    'soldiers': len(
                                        [s for p in data.get('platoons', []) for s in p.get('soldiers', [])]),
                                    'missions': len(data.get('missions', [])),
                                    'modified': datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M"),
                                    'data': data
                                })
                    except (json.JSONDecodeError, KeyError, FileNotFoundError):
                        # Skip invalid JSON files or files without proper structure
                        continue
        except Exception as e:
            print(f"Error scanning directory: {e}")

        # Sort by modification time (newest first)
        company_files.sort(key=lambda x: x['modified'], reverse=True)
        return company_files

    def on_closing(self):
        """Handle window closing"""
        print("Dialog closed by user")
        self.result = None

        # Show parent root if it exists
        if self.parent_root:
            self.parent_root.deiconify()

        self.root.quit()
        self.root.destroy()

    def create_widgets(self):
        """Create the startup dialog widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["content_bg"])
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Header
        self.create_header(main_frame)

        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))

        if self.company_files:
            self.create_existing_companies_section(content_frame)
        else:
            self.create_no_companies_section(content_frame)

        # Always show the "Create New Company" option
        self.create_new_company_section(content_frame)

        # Footer with app info
        self.create_footer(main_frame)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        header_frame.pack(fill='x', pady=(0, 10))

        # App title
        title_label = tk.Label(header_frame,
                               text="🎖️ Military Scheduling System",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 24, 'bold'))
        title_label.pack()

        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                  text="Choose an existing company or create a new one",
                                  bg=self.colors["content_bg"],
                                  fg=self.colors["text_secondary"],
                                  font=('Segoe UI', 12))
        subtitle_label.pack(pady=(5, 0))

        # Separator
        separator = tk.Frame(header_frame, bg=self.colors["border"], height=2)
        separator.pack(fill='x', pady=(15, 0))

    def create_existing_companies_section(self, parent):
        """Create section for existing companies"""
        existing_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        existing_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Section title
        title_label = tk.Label(existing_frame,
                               text="📂 Existing Companies",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w', pady=(0, 10))

        # Companies list frame with scrollbar
        list_container = tk.Frame(existing_frame, bg=self.colors["content_bg"])
        list_container.pack(fill='both', expand=True)

        # Create canvas for scrolling
        canvas = tk.Canvas(list_container, bg=self.colors["content_bg"], height=200)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["content_bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add company cards
        for i, company in enumerate(self.company_files):
            self.create_company_card(scrollable_frame, company, i)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_company_card(self, parent, company, index):
        """Create a card for each company"""
        print(f"Creating card for company: {company['name']}")  # Debug

        # Card frame
        card_frame = tk.Frame(parent, bg=self.colors["card_shadow"], relief='solid', bd=1)
        card_frame.pack(fill='x', pady=5, padx=10)

        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors["card_shadow"])
        content_frame.pack(fill='x', padx=15, pady=10)

        # Company name and select button
        header_frame = tk.Frame(content_frame, bg=self.colors["card_shadow"])
        header_frame.pack(fill='x')

        name_label = tk.Label(header_frame,
                              text=company['name'],
                              bg=self.colors["card_shadow"],
                              fg=self.colors["text_primary"],
                              font=('Segoe UI', 14, 'bold'))
        name_label.pack(side='left')

        # Create a working select button with proper styling
        def select_this_company():
            print(f"Button clicked for company: {company['name']}")
            self.select_company(company)

        select_btn = tk.Button(header_frame,
                               text="SELECT",
                               bg=self.colors["accent"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 10, 'bold'),
                               relief='raised',
                               bd=2,
                               padx=15,
                               pady=8,
                               cursor='hand2',
                               activebackground=self.colors["sidebar_hover"],
                               activeforeground=self.colors["text_light"],
                               command=select_this_company)
        select_btn.pack(side='right')

        # Add button hover effects
        def btn_on_enter(event):
            select_btn.configure(bg=self.colors["sidebar_hover"], relief='raised', bd=3)

        def btn_on_leave(event):
            select_btn.configure(bg=self.colors["accent"], relief='raised', bd=2)

        select_btn.bind('<Enter>', btn_on_enter)
        select_btn.bind('<Leave>', btn_on_leave)

        # Company details
        details_frame = tk.Frame(content_frame, bg=self.colors["card_shadow"])
        details_frame.pack(fill='x', pady=(8, 0))

        # Statistics
        stats_text = f"👥 {company['soldiers']} soldiers  •  🎖️ {company['platoons']} platoons  •  🎯 {company['missions']} missions"
        stats_label = tk.Label(details_frame,
                               text=stats_text,
                               bg=self.colors["card_shadow"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 10))
        stats_label.pack(side='left')

        # File info
        file_info = f"📄 {company['filename']}  •  📅 {company['modified']}"
        file_label = tk.Label(details_frame,
                              text=file_info,
                              bg=self.colors["card_shadow"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 9))
        file_label.pack(anchor='w', pady=(2, 0))

        # Hover effects
        def on_enter(e):
            card_frame.configure(bg=self.colors["accent"], bd=2)
            content_frame.configure(bg=self.colors["accent"])
            header_frame.configure(bg=self.colors["accent"])
            details_frame.configure(bg=self.colors["accent"])
            for widget in [name_label, stats_label, file_label]:
                widget.configure(bg=self.colors["accent"])

        def on_leave(e):
            card_frame.configure(bg=self.colors["card_shadow"], bd=1)
            content_frame.configure(bg=self.colors["card_shadow"])
            header_frame.configure(bg=self.colors["card_shadow"])
            details_frame.configure(bg=self.colors["card_shadow"])
            for widget in [name_label, stats_label, file_label]:
                widget.configure(bg=self.colors["card_shadow"])

        # Bind hover effects and click to card
        for widget in [card_frame, content_frame, header_frame, details_frame, name_label, stats_label, file_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e: select_this_company())

    def create_no_companies_section(self, parent):
        """Create section when no companies exist"""
        no_companies_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        no_companies_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Center content
        center_frame = tk.Frame(no_companies_frame, bg=self.colors["content_bg"])
        center_frame.pack(expand=True)

        # Icon
        icon_label = tk.Label(center_frame,
                              text="📂",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 48))
        icon_label.pack(pady=20)

        # Message
        message_label = tk.Label(center_frame,
                                 text="No existing company files found",
                                 bg=self.colors["content_bg"],
                                 fg=self.colors["text_primary"],
                                 font=('Segoe UI', 16, 'bold'))
        message_label.pack()

        desc_label = tk.Label(center_frame,
                              text="Get started by creating your first military company",
                              bg=self.colors["content_bg"],
                              fg=self.colors["text_secondary"],
                              font=('Segoe UI', 12))
        desc_label.pack(pady=(5, 0))

    def create_new_company_section(self, parent):
        """Create section for creating new company"""
        new_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        new_frame.pack(fill='x', pady=(10, 0))

        # Separator
        separator = tk.Frame(new_frame, bg=self.colors["border"], height=1)
        separator.pack(fill='x', pady=(0, 15))

        # Section title
        title_label = tk.Label(new_frame,
                               text="✨ Create New Company",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w', pady=(0, 10))

        # New company card
        card_frame = tk.Frame(new_frame, bg=self.colors["card_shadow"], relief='solid', bd=1)
        card_frame.pack(fill='x', pady=5)

        content_frame = tk.Frame(card_frame, bg=self.colors["card_shadow"])
        content_frame.pack(fill='x', padx=15, pady=15)

        # Description
        desc_label = tk.Label(content_frame,
                              text="Start fresh with a new military company",
                              bg=self.colors["card_shadow"],
                              fg=self.colors["text_primary"],
                              font=('Segoe UI', 12))
        desc_label.pack(anchor='w')

        sub_desc_label = tk.Label(content_frame,
                                  text="Set up soldiers, platoons, missions, and scheduling from scratch",
                                  bg=self.colors["card_shadow"],
                                  fg=self.colors["text_secondary"],
                                  font=('Segoe UI', 10))
        sub_desc_label.pack(anchor='w', pady=(2, 10))

        # Create button with hover effects
        def create_new_company_wrapper():
            try:
                self.create_new_company()
            except Exception as e:
                messagebox.showerror("Error", f"Error creating company: {e}")

        create_btn = tk.Button(content_frame,
                               text="🚀 Create New Company",
                               bg=self.colors["accent"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 12, 'bold'),
                               relief='raised',
                               bd=3,
                               padx=25,
                               pady=15,
                               cursor='hand2',
                               activebackground=self.colors["sidebar_hover"],
                               activeforeground=self.colors["text_light"],
                               command=create_new_company_wrapper)
        create_btn.pack(pady=10)

        # Add hover effects
        def on_enter(event):
            create_btn.configure(
                bg=self.colors["sidebar_hover"],
                relief='raised',
                bd=4
            )

        def on_leave(event):
            create_btn.configure(
                bg=self.colors["accent"],
                relief='raised',
                bd=3
            )

        def on_button_press(event):
            create_btn.configure(
                relief='sunken',
                bd=2
            )

        def on_button_release(event):
            create_btn.configure(
                relief='raised',
                bd=4
            )

        create_btn.bind('<Enter>', on_enter)
        create_btn.bind('<Leave>', on_leave)
        create_btn.bind('<ButtonPress-1>', on_button_press)
        create_btn.bind('<ButtonRelease-1>', on_button_release)

    def create_footer(self, parent):
        """Create footer with app info"""
        footer_frame = tk.Frame(parent, bg=self.colors["content_bg"])
        footer_frame.pack(fill='x', pady=(20, 0))

        # Separator
        separator = tk.Frame(footer_frame, bg=self.colors["border"], height=1)
        separator.pack(fill='x', pady=(0, 10))

        # Footer text
        footer_label = tk.Label(footer_frame,
                                text="Military Scheduling Management System v1.0",
                                bg=self.colors["content_bg"],
                                fg=self.colors["text_secondary"],
                                font=('Segoe UI', 9))
        footer_label.pack()

    def select_company(self, company):
        """Select an existing company"""
        print(f"SELECT COMPANY CALLED: {company['name']}")  # Debug
        try:
            # Load the company data
            loaded_company = Company.from_dict(company['data'])
            self.result = {
                'action': 'load',
                'company': loaded_company,
                'filename': company['filename']
            }
            print(f"Company loaded successfully: {loaded_company.name}")  # Debug

            # Show parent root if it exists
            if self.parent_root:
                self.parent_root.deiconify()

            # Close the dialog properly
            self.root.quit()
            self.root.destroy()

        except Exception as e:
            print(f"Error loading company: {str(e)}")  # Debug
            messagebox.showerror("Error", f"Failed to load company: {str(e)}")

    def create_new_company(self):
        """Create a new company"""
        print("DEBUG: CREATE NEW COMPANY CALLED!")  # Debug

        try:
            # Create a custom dialog instead of simpledialog
            self.create_name_input_dialog()
        except Exception as e:
            print(f"DEBUG: Error in create_new_company: {str(e)}")
            import traceback
            traceback.print_exc()

    def create_name_input_dialog(self):
        """Create a custom dialog for company name input"""
        print("DEBUG: Creating name input dialog")

        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("New Company Name")
        dialog.geometry("400x250")
        dialog.configure(bg=self.colors["content_bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        x = self.root.winfo_rootx() + 100
        y = self.root.winfo_rooty() + 100
        dialog.geometry(f"400x250+{x}+{y}")

        # Variables
        name_var = tk.StringVar(value="New Military Company")
        dialog_result = {'cancelled': True}

        # Main frame
        main_frame = tk.Frame(dialog, bg=self.colors["content_bg"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame,
                               text="Create New Company",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_primary"],
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Instructions
        instr_label = tk.Label(main_frame,
                               text="Enter the name for your new military company:",
                               bg=self.colors["content_bg"],
                               fg=self.colors["text_secondary"],
                               font=('Segoe UI', 11))
        instr_label.pack(pady=(0, 10))

        # Name entry
        name_entry = tk.Entry(main_frame,
                              textvariable=name_var,
                              font=('Segoe UI', 12),
                              width=30)
        name_entry.pack(pady=(0, 20))
        name_entry.focus()
        name_entry.select_range(0, tk.END)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors["content_bg"])
        button_frame.pack()

        def create_company():
            print("DEBUG: Create company function called")
            name = name_var.get().strip()
            if name:
                dialog_result['cancelled'] = False
                dialog_result['name'] = name
                print(f"DEBUG: Company name set to: {name}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Company name cannot be empty!")

        def cancel():
            print("DEBUG: Create company cancelled")
            dialog_result['cancelled'] = True
            dialog.destroy()

        create_btn = tk.Button(button_frame,
                               text="Create",
                               bg=self.colors["accent"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11, 'bold'),
                               relief='raised',
                               padx=20,
                               pady=8,
                               borderwidth=2,
                               command=create_company)
        create_btn.pack(side='left', padx=(0, 10))

        cancel_btn = tk.Button(button_frame,
                               text="Cancel",
                               bg=self.colors["text_secondary"],
                               fg=self.colors["text_light"],
                               font=('Segoe UI', 11),
                               relief='raised',
                               padx=20,
                               pady=8,
                               borderwidth=2,
                               command=cancel)
        cancel_btn.pack(side='left')

        # Handle Enter key
        name_entry.bind('<Return>', lambda e: create_company())

        # Wait for dialog
        print("DEBUG: Waiting for dialog...")
        dialog.wait_window()

        # Process result
        print(f"DEBUG: Dialog result: {dialog_result}")
        if not dialog_result['cancelled']:
            company_name = dialog_result['name']
            print(f"DEBUG: Creating company: {company_name}")

            try:
                # Create new company
                new_company = Company(company_name)
                self.result = {
                    'action': 'new',
                    'company': new_company,
                    'filename': None
                }
                print(f"DEBUG: New company created: {new_company.name}")

                # Show parent root if it exists
                if self.parent_root:
                    self.parent_root.deiconify()

                # Close the main dialog
                self.root.quit()
                self.root.destroy()

            except Exception as e:
                print(f"DEBUG: Error creating company: {str(e)}")
                messagebox.showerror("Error", f"Failed to create company: {str(e)}")


def show_startup_dialog(colors, parent_root=None):
    """Show the startup dialog and return the result"""
    dialog = StartupDialog(colors, parent_root)
    return dialog.result