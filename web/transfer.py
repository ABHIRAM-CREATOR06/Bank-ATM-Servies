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

def transfer_amount():
    sender_acct = sender_acc_no_entry.get()
    receiver_acct = receiver_acc_no_entry.get()
    amt = amount_entry.get()
    if not sender_acct.isdigit() or not receiver_acct.isdigit() or not amt.isdigit():
        messagebox.showerror("Error", "Please enter valid numbers for account numbers and amount.")
        return

    sender_acct = int(sender_acct)
    receiver_acct = int(receiver_acct)
    amt = int(amt)
    try:
        cursor.execute("SELECT balance FROM records WHERE acc_no=%s", (sender_acct,))
        sender_balance = cursor.fetchone()
        if sender_balance and sender_balance[0] >= amt:
            cursor.execute('UPDATE records SET withdrawl=withdrawl+%s WHERE acc_no=%s', (amt, sender_acct))
            cursor.execute('UPDATE records SET cr_amt=cr_amt+%s WHERE acc_no=%s', (amt, receiver_acct))
            conn.commit()
            cursor.execute('UPDATE records SET balance=cr_amt-withdrawl WHERE acc_no=%s', (sender_acct,))
            cursor.execute('UPDATE records SET balance=cr_amt-withdrawl WHERE acc_no=%s', (receiver_acct,))
            conn.commit()
            messagebox.showinfo("Success", "Amount transferred successfully")
        else:
            messagebox.showerror("Error", "Insufficient balance or sender account not found")
    except a.Error as err:
        messagebox.showerror("Error", f"Error transferring amount: {err}")

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

# Input fields for sender and receiver account numbers and amount
sender_acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter sender account number")
sender_acc_no_entry.pack(pady=5)

receiver_acc_no_entry = ctk.CTkEntry(root, placeholder_text="Enter receiver account number")
receiver_acc_no_entry.pack(pady=5)

amount_entry = ctk.CTkEntry(root, placeholder_text="Enter amount to transfer")
amount_entry.pack(pady=5)

# Transfer button
transfer_button = ctk.CTkButton(root, text="Transfer Amount", command=transfer_amount)
transfer_button.pack(pady=10)

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
all_widgets = [welcome_label, sender_acc_no_entry, receiver_acc_no_entry, amount_entry, transfer_button]

# Ensure the database connection is closed when the application exits
def on_closing():
    if conn:
        conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()
