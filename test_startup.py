import tkinter as tk
from tkinter import messagebox
import time


def test_window_hiding():
    """Test window hiding and showing"""
    print("Creating main window...")

    # Create main window
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("800x600")
    root.configure(bg="lightblue")

    # Hide it immediately
    print("Hiding main window...")
    root.withdraw()

    # Add some content to main window
    label = tk.Label(root, text="This is the main application!",
                     font=("Arial", 24), bg="lightblue")
    label.pack(expand=True)

    # Create startup dialog
    print("Creating startup dialog...")

    startup = tk.Toplevel(root)  # Use Toplevel instead of separate Tk()
    startup.title("Startup Dialog")
    startup.geometry("400x300")
    startup.configure(bg="white")
    startup.transient(root)
    startup.grab_set()

    # Center startup dialog
    startup.update_idletasks()
    x = (startup.winfo_screenwidth() // 2) - 200
    y = (startup.winfo_screenheight() // 2) - 150
    startup.geometry(f"400x300+{x}+{y}")

    result = {'choice': None}

    # Startup dialog content
    title = tk.Label(startup, text="Choose an option:",
                     font=("Arial", 16), bg="white")
    title.pack(pady=20)

    def option1():
        print("Option 1 selected")
        result['choice'] = 'option1'
        startup.destroy()

    def option2():
        print("Option 2 selected")
        result['choice'] = 'option2'
        startup.destroy()

    def cancel():
        print("Cancelled")
        result['choice'] = 'cancel'
        startup.destroy()

    btn1 = tk.Button(startup, text="Option 1", command=option1,
                     font=("Arial", 12), bg="lightgreen", pady=10)
    btn1.pack(pady=10)

    btn2 = tk.Button(startup, text="Option 2", command=option2,
                     font=("Arial", 12), bg="lightcoral", pady=10)
    btn2.pack(pady=10)

    cancel_btn = tk.Button(startup, text="Cancel", command=cancel,
                           font=("Arial", 12), bg="gray", pady=10)
    cancel_btn.pack(pady=10)

    # Handle startup close
    def startup_close():
        result['choice'] = 'cancel'
        startup.destroy()

    startup.protocol("WM_DELETE_WINDOW", startup_close)

    print("Waiting for startup dialog...")
    startup.wait_window()  # Wait for startup to close

    print(f"Startup dialog closed. Result: {result}")

    # Now decide what to do with main window
    if result['choice'] in ['option1', 'option2']:
        print("Showing main window...")
        root.deiconify()  # Show main window
        root.lift()
        root.focus_force()

        # Update main window content based on choice
        label.config(text=f"You selected: {result['choice']}")

        print("Main window should now be visible")
        root.mainloop()
    else:
        print("User cancelled, destroying main window...")
        root.destroy()


if __name__ == "__main__":
    test_window_hiding()