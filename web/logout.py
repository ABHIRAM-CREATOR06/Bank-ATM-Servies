import customtkinter as ctk
from tkinter import messagebox

def logout():
    root.destroy()
    messagebox.showinfo("Logout", "You have been logged out successfully.")

def main_screen():
    global root

    root = ctk.CTk()
    root.title("Main Screen")
    root.geometry("400x300")

    # Welcome message
    welcome_label = ctk.CTkLabel(root, text="Welcome to the Main Screen", font=("Arial", 16))
    welcome_label.pack(pady=20)

    # Logout button
    logout_button = ctk.CTkButton(root, text="Logout", command=logout)
    logout_button.pack(pady=20)

    # Run the main loop
    root.mainloop()

# Start the application with the main screen
if __name__ == "__main__":
    main_screen()
