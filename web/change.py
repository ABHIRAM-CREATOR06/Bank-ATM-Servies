import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector as a

def connect_to_db():
    try:
        conn = a.connect(host='localhost', user='root', passwd='1234', database='services')
        return conn
    except a.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None

def check_account_exists(cursor, acc_no):
    query = "SELECT * FROM records WHERE acc_no=%s"
    cursor.execute(query, (acc_no,))
    result = cursor.fetchone()  # Fetch one result to clear the cursor
    return result is not None

def update_account_number():
    acc_no = acc_no_entry.get()
    if not acc_no.isdigit():
        messagebox.showerror("Error", "Please enter a valid account number.")
        return

    acc_no = int(acc_no)
    cursor = conn.cursor(buffered=True)  # Use buffered cursor
    if check_account_exists(cursor, acc_no):
        messagebox.showerror("Error", "This account number already exists. Try again.")
        cursor.close()  # Close the cursor
        return

    name = name_entry.get()
    password = password_entry.get()
    if not password.isdigit():
        messagebox.showerror("Error", "Please enter a valid password.")
        cursor.close()  # Close the cursor
        return

    password = int(password)
    query = "UPDATE records SET acc_no=%s WHERE name=%s AND password=%s"
    try:
        cursor.execute(query, (acc_no, name, password))
        conn.commit()
        messagebox.showinfo("Success", f"Account number updated to {acc_no}")
    except a.Error as err:
        messagebox.showerror("Error", f"Error updating account number: {err}")
    finally:
        cursor.close()  # Ensure cursor is closed

def update_password():
    new_password = new_password_entry.get()
    if not new_password.isdigit():
        messagebox.showerror("Error", "Please enter a valid password.")
        return

    new_password = int(new_password)
    cursor = conn.cursor(buffered=True)  # Use buffered cursor
    name = name_entry.get()
    old_password = password_entry.get()
    if not old_password.isdigit():
        messagebox.showerror("Error", "Please enter a valid current password.")
        cursor.close()  # Close the cursor
        return

    old_password = int(old_password)
    query = "UPDATE records SET password=%s WHERE name=%s AND password=%s"
    try:
        cursor.execute(query, (new_password, name, old_password))
        conn.commit()
        messagebox.showinfo("Success", f"Password updated to {new_password}")
    except a.Error as err:
        messagebox.showerror("Error", f"Error updating password: {err}")
    finally:
        cursor.close()  # Ensure cursor is closed

def update_font_size(value):
    new_size = int(value)
    for widget in all_widgets:
        widget.configure(font=("Arial", new_size))

def toggle_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

# Initialize the main window
root = ctk.CTk()
root.title("Account Management")
root.geometry("600x400")

# Connect to the database
conn = connect_to_db()
if conn:
    cursor = conn.cursor(buffered=True)  # Use buffered cursor

# Welcome message
welcome_label = ctk.CTkLabel(root, text="Account Management", font=("Arial", 16))
welcome_label.pack(pady=10)

# Input fields for account number, password, and name
acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter new account number")
acc_no_entry.pack(pady=5)

password_entry = ctk.CTkEntry(root, placeholder_text="Enter current password", show="*")
password_entry.pack(pady=5)

new_password_entry = ctk.CTkEntry(root, placeholder_text="Enter new password", show="*")
new_password_entry.pack(pady=5)

name_entry = ctk.CTkEntry(root, placeholder_text="Enter name")
name_entry.pack(pady=5)

# Update account number button
update_acc_no_button = ctk.CTkButton(root, text="Update Account Number", command=update_account_number)
update_acc_no_button.pack(pady=10)

# Update password button
update_password_button = ctk.CTkButton(root, text="Update Password", command=update_password)
update_password_button.pack(pady=10)

# Font size slider with scrollbar
font_size_frame = ctk.CTkFrame(root)
font_size_frame.pack(side="bottom", fill="x", padx=10, pady=10)

font_size_slider = ctk.CTkSlider(font_size_frame, from_=10, to=30, command=update_font_size)
font_size_slider.set(16)  # Default font size
font_size_slider.pack(side="left", fill="x", expand=True)

font_size_scrollbar = ttk.Scrollbar(font_size_frame, orient="horizontal", command=font_size_slider.set)
font_size_scrollbar.pack(side="bottom", fill="x")
font_size_slider.configure(command=font_size_scrollbar.set)

# List of all widgets for font size update
all_widgets = [welcome_label, acc_no_entry, password_entry, new_password_entry, name_entry, update_acc_no_button, update_password_button]

# Toggle mode button
toggle_mode_button = ctk.CTkButton(root, text="Toggle Mode", command=toggle_mode)
toggle_mode_button.pack(pady=10)

# Ensure the database connection is closed when the application exits
def on_closing():
    if conn:
        conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()


