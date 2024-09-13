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

def deposit_amount():
    acct = acc_no_entry.get()
    amt = amount_entry.get()
    if not acct.isdigit() or not amt.isdigit():
        messagebox.showerror("Error", "Please enter valid numbers for account and amount.")
        return

    acct = int(acct)
    amt = int(amt)
    try:
        cursor.execute('UPDATE records SET cr_amt=cr_amt+%s WHERE acc_no=%s', (amt, acct))
        conn.commit()
        cursor.execute('UPDATE records SET balance=cr_amt-withdrawl WHERE acc_no=%s', (acct,))
        conn.commit()
        messagebox.showinfo("Success", "Amount deposited successfully")
    except a.Error as err:
        messagebox.showerror("Error", f"Error depositing amount: {err}")

def withdraw_amount():
    acct = acc_no_entry.get()
    amt = amount_entry.get()
    if not acct.isdigit() or not amt.isdigit():
        messagebox.showerror("Error", "Please enter valid numbers for account and amount.")
        return

    acct = int(acct)
    amt = int(amt)
    try:
        cursor.execute("SELECT balance FROM records WHERE acc_no=%s", (acct,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amt:
            cursor.execute('UPDATE records SET withdrawl=withdrawl+%s WHERE acc_no=%s', (amt, acct))
            conn.commit()
            cursor.execute('UPDATE records SET balance=cr_amt-withdrawl WHERE acc_no=%s', (acct,))
            conn.commit()
            messagebox.showinfo("Success", "Amount withdrawn successfully")
        else:
            messagebox.showerror("Error", "Insufficient balance or account not found")
    except a.Error as err:
        messagebox.showerror("Error", f"Error withdrawing amount: {err}")

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
    cursor = conn.cursor()

# Welcome message
welcome_label = ctk.CTkLabel(root, text="Account Management", font=("Arial", 16))
welcome_label.pack(pady=10)

# Input fields for account number and amount
acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter account number")
acc_no_entry.pack(pady=5)

amount_entry = ctk.CTkEntry(root, placeholder_text="Enter amount")
amount_entry.pack(pady=5)

# Deposit button
deposit_button = ctk.CTkButton(root, text="Deposit Amount", command=deposit_amount)
deposit_button.pack(pady=10)

# Withdraw button
withdraw_button = ctk.CTkButton(root, text="Withdraw Amount", command=withdraw_amount)
withdraw_button.pack(pady=10)

# Font size slider with scrollbar
font_size_frame = ctk.CTkFrame(root)
font_size_frame.pack(side="bottom", fill="x", padx=10, pady=10)

font_size_slider = ctk.CTkSlider(font_size_frame, from_=10, to=30, command=update_font_size)
font_size_slider.set(16)  # Default font size
font_size_slider.pack(side="left", fill="x", expand=True)

font_size_scrollbar = ttk.Scrollbar(font_size_frame, orient="horizontal", command=font_size_slider.set)
font_size_scrollbar.pack(side="bottom", fill="x")
font_size_slider.configure(command=font_size_scrollbar.set)

# Toggle mode button
toggle_button = ctk.CTkButton(root, text="Toggle Dark/Light Mode", command=toggle_mode)
toggle_button.pack(pady=10)

# Collect all widgets for font size adjustment
all_widgets = [welcome_label, acc_no_entry, amount_entry, deposit_button, withdraw_button]

# Ensure the database connection is closed when the application exits
def on_closing():
    if conn:
        conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()

