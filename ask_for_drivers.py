# Ask for Drivers

from tkinter import *
from file_manager_interface import FileManagerInterface


class AskForDrivers:

    def __init__(self):
        # Initialize the Tkinter window
        self.driver_window = Tk()
        # List to store entered drivers
        self.drivers = []
        self.driver_window.title("N0T C0D3R5")  # Title of the window

        # Center the window on the screen
        self.driver_window.geometry("+%d+%d" % ((self.driver_window.winfo_screenwidth() - 700) // 2,
                                                (self.driver_window.winfo_screenheight() - 700) // 2))

        # Create a frame to contain the content
        frame = Frame(self.driver_window)
        frame.pack(expand=True)

        # Label to prompt user to insert driver
        self.insert_driver_label = Label(frame, text="Insert Driver", font=("Helvetica", 20, "bold"))
        self.insert_driver_label.pack(pady=5)

        # Label and Entry widget to enter driver details
        self.driver_name = Label(frame, text="Driver: ", font=("Arial", 12, "normal"))
        self.driver_name.pack(pady=5)

        self.driver_entry = Entry(frame)
        self.driver_entry.pack(pady=5)

        # Create a frame to contain the buttons
        button_frame = Frame(frame)
        button_frame.pack(pady=5)

        # Button to add driver
        self.driver_entry_button = Button(button_frame, text="Add", command=self.add_driver)
        self.driver_entry_button.pack(side="left", padx=15, pady=5)

        # Button to submit drivers
        self.driver_submit_button = Button(button_frame, text="Submit", command=self.submit_driver)
        self.driver_submit_button.pack(side="left", padx=15, pady=5)

        # Center the window on the screen
        self.driver_window.state('zoomed')  # Maximizes the window
        self.driver_window.mainloop()

    # Method to add driver to the list
    def add_driver(self):
        user_driver_entry = self.driver_entry.get()
        if not user_driver_entry.isnumeric():  # Ensure entry is not numeric
            self.drivers.append(user_driver_entry)
            self.driver_entry.delete(0, END)  # Clear the entry box after adding
        return

    # Method to submit drivers and close the window
    def submit_driver(self):
        self.driver_window.destroy()  # Close the window
        # Create an instance of FileManagerInterface with the entered drivers
        file_man_int = FileManagerInterface(self.drivers)
