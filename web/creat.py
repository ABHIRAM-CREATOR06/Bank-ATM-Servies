import customtkinter as ctk
from tkinter import messagebox
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
    result = cursor.fetchone()
    return result is not None

def create_account():
    acc_no = int(acc_no_entry.get())
    password = int(password_entry.get())
    name = name_entry.get()

    cursor = conn.cursor(buffered=True)
    if check_account_exists(cursor, acc_no):
        messagebox.showerror("Error", "Account number already exists")
        cursor.close()
        return

    query = "INSERT INTO records (acc_no, password, name, cr_amt, withdrawl) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (acc_no, password, name, 0, 0))
        conn.commit()
        messagebox.showinfo("Success", "Account successfully created")
        ask_deposit(acc_no)
    except a.Error as err:
        messagebox.showerror("Error", f"Error creating account: {err}")
    finally:
        cursor.close()

def ask_deposit(acc_no):
    response = messagebox.askyesno("Deposit", "Minimum balance is 1000 rupees. Do you want to deposit some amount?")
    if response:
        deposit_amount(acc_no)

def deposit_amount(acc_no):
    amount_str = deposit_entry.get()
    if not amount_str:
        messagebox.showerror("Error", "Please enter a deposit amount")
        return

    try:
        amount = int(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit amount. Please enter a valid number.")
        return

    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("UPDATE records SET cr_amt=cr_amt+%s WHERE acc_no=%s", (amount, acc_no))
        conn.commit()
        cursor.execute("UPDATE records SET balance=cr_amt-withdrawl WHERE acc_no=%s", (acc_no,))
        conn.commit()
        messagebox.showinfo("Success", "Amount deposited successfully")
    except a.Error as err:
        messagebox.showerror("Error", f"Error depositing amount: {err}")
    finally:
        cursor.close()

def update_font_size(value):
    new_size = int(value)
    for widget in all_widgets:
        widget.configure(font=("Arial", new_size))

# Initialize the main window
root = ctk.CTk()
root.title("Account Management")
root.geometry("600x400")

# Connect to the database
conn = connect_to_db()
if conn:
    cursor = conn.cursor(buffered=True)

# Welcome message
welcome_label = ctk.CTkLabel(root, text="Account Management", font=("Arial", 16))
welcome_label.pack(pady=10)

# Input fields for account number, password, and name
acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter account number")
acc_no_entry.pack(pady=5)

password_entry = ctk.CTkEntry(root, placeholder_text="Enter password", show="*")
password_entry.pack(pady=5)

name_entry = ctk.CTkEntry(root, placeholder_text="Enter name")
name_entry.pack(pady=5)

# Create account button
create_button = ctk.CTkButton(root, text="Create Account", command=create_account)
create_button.pack(pady=10)

# Input field for deposit amount
deposit_entry = ctk.CTkEntry(root, placeholder_text="Enter deposit amount")
deposit_entry.pack(pady=5)

# Font size slider
font_size_slider = ctk.CTkSlider(root, from_=10, to=30, command=update_font_size)
font_size_slider.set(16)  # Default font size
font_size_slider.pack(side="bottom", fill="x", padx=10, pady=10)

# Collect all widgets for font size adjustment
all_widgets = [welcome_label, acc_no_entry, password_entry, name_entry, create_button, deposit_entry]

# Run the main loop
root.mainloop()




