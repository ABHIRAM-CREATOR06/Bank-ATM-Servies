import customtkinter as ctk
from tkinter import messagebox
import mysql.connector as a

def connect_to_db():
    try:
        conn = a.connect(host="localhost", user="root", password="1234", database="services")
        return conn
    except a.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None

def delete_record():
    acc_no = int(acc_no_entry.get())
    password = int(password_entry.get())
    try:
        query = "DELETE FROM records WHERE acc_no=%s AND password=%s"
        cursor.execute(query, (acc_no, password))
        conn.commit()
        messagebox.showinfo("Success", "Values successfully deleted\nRecords are completely deleted")
    except a.Error as err:
        messagebox.showerror("Error", f"DATA INPUT ERROR\nPLEASE TRY AGAIN WITH CORRECT DATA\n{err}")

def update_font_size(value):
    new_size = int(value)
    for widget in all_widgets:
        widget.configure(font=("Arial", new_size))

# Initialize the main window
root = ctk.CTk()
root.title("Admin Portal")
root.geometry("600x400")

# Connect to the database
conn = connect_to_db()
if conn:
    cursor = conn.cursor()

# Welcome message
welcome_label = ctk.CTkLabel(root, text="Welcome Admin", font=("Arial", 16))
welcome_label.pack(pady=10)

# Input fields for account number and password
acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter account number")
acc_no_entry.pack(pady=5)

password_entry = ctk.CTkEntry(root, placeholder_text="Enter password", show="*")
password_entry.pack(pady=5)

# Delete button
delete_button = ctk.CTkButton(root, text="Delete Record", command=delete_record)
delete_button.pack(pady=10)

# Font size slider
font_size_slider = ctk.CTkSlider(root, from_=10, to=30, command=update_font_size)
font_size_slider.set(16)  # Default font size
font_size_slider.pack(side="bottom", fill="x", padx=10, pady=10)

# Collect all widgets for font size adjustment
all_widgets = [welcome_label, acc_no_entry, password_entry, delete_button]

# Run the main loop
root.mainloop()

