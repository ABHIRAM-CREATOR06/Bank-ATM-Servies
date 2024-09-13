import customtkinter as ctk
from tkinter import messagebox
import random as r

def generate_otp():
    otp = "".join([str(r.randint(0, 9)) for _ in range(4)])
    otp_label.configure(text=f"Your one-time password is: {otp}")
    return otp

def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == otp:
        messagebox.showinfo("Verification", "Verified")
        show_options()
    else:
        messagebox.showerror("Verification", "Error")

def show_options():
    options_frame.pack(pady=10)

def perform_action():
    choice = int(choice_var.get())
    if choice == 1:
        import web.setup
    elif choice == 2:
        import web.creat
    elif choice == 3:
        import web.change
    elif choice == 4:
        import web.delet
    else:
        messagebox.showerror("Error", "Invalid option")

# Initialize the main window
root = ctk.CTk()
root.title("Admin Portal")
root.geometry("400x400")

# Welcome message
welcome_label = ctk.CTkLabel(root, text="Welcome Admin", font=("Arial", 32))
welcome_label.pack(pady=10)

# OTP label (defined before generating OTP)
otp_label = ctk.CTkLabel(root, text="", font=("Arial", 22))
otp_label.pack(pady=10)

# Generate OTP
otp = generate_otp()

otp_entry = ctk.CTkEntry(root, placeholder_text="Enter OTP")
otp_entry.pack(pady=5)

verify_button = ctk.CTkButton(root, text="Verify OTP", command=verify_otp)
verify_button.pack(pady=10)

# Options frame (initially hidden)
options_frame = ctk.CTkFrame(root)

options_label = ctk.CTkLabel(options_frame, text="Enter options:\n1: Setup\n2: Account Creation\n3: Account Modification\n4: Account Deletion", font=("Arial", 12))
options_label.pack(pady=10)

choice_var = ctk.CTkEntry(options_frame, placeholder_text="Enter choice")
choice_var.pack(pady=5)

action_button = ctk.CTkButton(options_frame, text="Submit", command=perform_action)
action_button.pack(pady=10)

# Run the main loop
root.mainloop()

