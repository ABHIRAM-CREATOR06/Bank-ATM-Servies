import customtkinter as ctk
from tkinter import messagebox

def toggle_theme():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def check_admin():
    if admin_entry.get() == "admin":
        messagebox.showinfo("Admin", "Admin access granted.")
        import web.admin
    else:
        messagebox.showerror("Admin", "Access denied.")

def perform_action():
    option = int(option_var.get())
    if option == 1:
        import web.deposit
        messagebox.showinfo("Service", "Cash Deposit selected.")
    elif option == 2:
        import web.withdrawal
        messagebox.showinfo("Service", "Cash Withdrawal selected.")
    elif option == 3:
        import web.transfer
        messagebox.showinfo("Service", "Money Transfer selected.")
    elif option == 4:
        messagebox.showinfo("Service", "Logout")
        root.quit()
    else:
        messagebox.showerror("Service", "Invalid option")

def update_font_size(value):
    new_size = int(value)
    welcome_label.configure(font=("Arial", new_size))
    services_label.configure(font=("Arial", new_size))
    for label in option_labels:
        label.configure(font=("Arial", new_size))

# Initialize the main window
root = ctk.CTk()
root.title("Service Portal")
root.geometry("800x600")

# Top right section for theme, fullscreen, and admin options
top_right_frame = ctk.CTkFrame(root)
top_right_frame.pack(side="top", anchor="ne", padx=10, pady=10)

theme_button = ctk.CTkButton(top_right_frame, text="Toggle Theme", command=toggle_theme)
theme_button.pack(side="left", padx=5)

fullscreen_button = ctk.CTkButton(top_right_frame, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.pack(side="left", padx=5)

admin_label = ctk.CTkLabel(top_right_frame, text="Admin:")
admin_label.pack(side="left", padx=5)

admin_entry = ctk.CTkEntry(top_right_frame, width=100)
admin_entry.pack(side="left", padx=5)

admin_button = ctk.CTkButton(top_right_frame, text="Check", command=check_admin)
admin_button.pack(side="left", padx=5)

# Welcome message
welcome_label = ctk.CTkLabel(root, text="WELCOME TO OUR SERVICES", font=("Arial", 16))
welcome_label.pack(pady=10)

# Available services
services_label = ctk.CTkLabel(root, text="OPTION: AVAILABLE SERVICES", font=("Arial", 14))
services_label.pack(pady=10)

options = ["1 = CASH DEPOSIT", "2 = CASH WITHDRAWAL", "3 = MONEY TRANSFER", "4 = Logout"]
option_labels = []
for option in options:
    option_label = ctk.CTkLabel(root, text=option, font=("Arial", 14))
    option_label.pack(pady=2)
    option_labels.append(option_label)

option_var = ctk.CTkEntry(root)
option_var.pack(pady=5)

action_button = ctk.CTkButton(root, text="Perform Action", command=perform_action)
action_button.pack(pady=10)

# Font size slider
font_size_slider = ctk.CTkSlider(root, from_=10, to=30, command=update_font_size)
font_size_slider.set(16)  # Default font size
font_size_slider.pack(side="bottom", fill="x", padx=10, pady=10)

# Run the main loop
root.mainloop()


