import tkinter as tk # Import the tkinter module

# Function to exit full-screen mode and resize the window at ESC key press
def exit_fullscreen(event=None): # Function to exit full-screen mode
    root.attributes("-fullscreen", False)

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate half size
    half_width = screen_width // 2
    half_height = screen_height // 2

    # Calculate position to center the window
    x = (screen_width - half_width) // 2
    y = (screen_height - half_height) // 2

    # Set new window geometry (WxH+X+Y)
    root.geometry(f"{half_width}x{half_height}+{x}+{y}")

# Function to handle button click event
def on_button_click():
    print("Button clicked!")

# Create the main window
root = tk.Tk() # Initialize the Tkinter root window
root.title("Sonerie Inteligenta") # Set the title of the window
root.configure(bg="#1e1e2f")  # A dark, modern background color
# Make the window full-screen
root.attributes("-fullscreen", True)
# Bind ESC key to exit full-screen
root.bind("<Escape>", exit_fullscreen)

# START-STOP button creation
button = tk.Button(
    root,
    text="Start / Stop Sistem",  # the title of the button
    command=on_button_click,
    font=("Helvetica", 20, "bold"),
    bg="#3e8ed0",       # Background color
    fg="white",         # Text color
    activebackground="#5596e6",
    activeforeground="white",
    relief="flat",      # Flat modern look
    padx=20,
    pady=10,
    cursor="hand2"
)
button.pack(pady=50)

# LIST of time intervals creation
alarm_list_frame = tk.Frame(root, bg="#1e1e2f")  # Match background
alarm_list_frame.pack(pady=20)

# Sample alarms
alarms = ["07:00 - 07:15", "10:00 - 10:15", "18:00 - 18:30"]

# Add each alarm as a custom-styled label
for alarm in alarms:
    alarm_label = tk.Label(
        alarm_list_frame,
        text=alarm,
        font=("Helvetica", 16),
        bg="#2a2a3d",
        fg="white",
        padx=10,
        pady=5,
        width=30,
        anchor="w",  # left-align text
        relief="ridge",
        bd=1
    )
    alarm_label.pack(pady=5)


# Start the Tkinter event loop
root.mainloop()
