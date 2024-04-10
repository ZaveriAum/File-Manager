# File Manager Interface

from tkinter import *
from tkinter import ttk, simpledialog, Menu, messagebox
from file_manager_controller import FileManagerController
from Logging import Logs
from datetime import datetime


class FileManagerInterface:
    # ---------------------------- UI SETUP ------------------------------- #
    # Tk inter window setup

    def __init__(self, drivers):

        try:
            self.insert_driver_call = 0
            self.drivers = drivers
            self.file_man = FileManagerController()
            try:
                self.logs = Logs()
            except ConnectionError as e:
                print(f"Error: {e}")
            self.window = Tk()
            self.window.title("N0T C0D3R5 File Manager")
            self.window_width = 700
            self.window_height = 700
            self.window.geometry(f"{self.window_width}x{self.window_height}")
            self.window.config(pady=40, padx=20)

            # Frames for all three rows

            self.frame1 = Frame(self.window, width=60)
            self.frame2 = Frame(self.window, width=60)
            self.frame3 = Frame(self.window, width=60)

            # All buttons and text field

            # Frame 1 items
            # Previous_directory
            self.previous_directory = Button(self.frame1, text="<-", command=self.navigate_backward)

            # Directory Path text field
            self.directory_path = Entry(self.frame1, width=100)
            # Go to directory button
            self.next_directory = Button(self.frame1, text="->", command=self.navigate_forward_absolute_path)

            # Frame 2 items
            # Sort directories drop down.
            # label for Sort dropdown
            self.sort_label = StringVar()
            self.sort_label.set("Sort")

            self.sort_directories = Button(self.frame2, text="Sort")
            self.sort_directories.bind("<Button-1>", self.sort_selection)
            # Logs button
            self.logs_button = Button(self.frame2, text="Logs")
            self.logs_button.bind("<Button-1>", self.show_options_for_logs)

            # Frame 3 items
            # List box for listing Directories

            # Create a scrollbar
            self.ver_scrollbar = Scrollbar(self.frame3, orient=VERTICAL)
            self.hor_scrollbar = Scrollbar(self.frame3, orient=HORIZONTAL)

            self.directory_list_box = Listbox(self.frame3, yscrollcommand=self.ver_scrollbar.set,
                                              xscrollcommand=self.hor_scrollbar.set, height=33, width=110)

            # Attach scrollbar to listbox
            self.ver_scrollbar.config(command=self.directory_list_box.yview)
            self.hor_scrollbar.config(command=self.directory_list_box.xview)
            if self.insert_driver_call == 0:
                self.insert_drivers()
                self.insert_driver_call += 1

            self.directory_list_box.bind("<Double-1>", self.navigate_forward)
            self.directory_list_box.bind("<Button-3>", self.on_right_click)
            self.directory_list_box.bind("<Button-2>", self.on_right_click)

            # ---------------------------- Laying the components ------------------------------- #

            # Laying out Frames
            self.frame1.pack()
            self.frame2.pack()
            self.frame3.pack()

            # Laying out components inside the Frame
            # Component arrangement in Frame 1
            # First row elements
            self.previous_directory.pack(side=LEFT, pady=5, padx=10)
            self.directory_path.pack(side=LEFT, pady=5, padx=10)
            self.next_directory.pack(side=LEFT, pady=5, padx=10)

            # Component arrangement in Frame 2
            # Second row elements
            self.sort_directories.pack(side=LEFT, padx=10)
            self.logs_button.pack(side=LEFT, padx=10)

            # Component arrangement in Frame 3
            # Third row elements
            self.ver_scrollbar.pack(side=RIGHT, fill=Y, pady=10)
            self.directory_list_box.pack(fill=BOTH, expand=True, pady=10)
            self.hor_scrollbar.pack(side=BOTTOM, fill=X, pady=10)

            # Bind the destroy event to the on_close function
            self.window.bind("<Destroy>", self.logs.close_connection)
            self.window.state('zoomed')

            self.window.mainloop()
        except Exception as e:
            self.logs.log_error(self.logs.get_error_info("This PC", e, datetime.now()))

# ------------------------------------------- Navigation [ Forward and backward ] --------------------------------------
    # Menu when right click
    def on_right_click(self, event):
        try:
            menu = Menu(self.window, tearoff=0)
            menu.add_command(label="Create", command=lambda: self.create_new_directory(event))
            menu.add_command(label="Copy", command=lambda: self.copy_file(event))
            menu.add_command(label="Move", command=lambda: self.move_file(event))
            menu.add_command(label="Paste", command=lambda: self.paste_file(event))
            menu.add_command(label="Delete", command=lambda: self.delete_new_directory(event))

            menu.post(event.x_root, event.y_root)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # it will get the selection from the list box if the item is selected
    def get_selected_listbox_item(self):
        try:
            if self.directory_list_box.curselection():
                index = self.directory_list_box.curselection()[0]
                return self.directory_list_box.get(index)
            return ""
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # it will populate list box from teh list of files given
    def populate_listbox(self, name_list):
        try:
            self.directory_list_box.config(state="normal")
            self.directory_list_box.delete(0, END)
            for dir_name in name_list:
                self.directory_list_box.insert(END, dir_name)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # It will insert the drivers which are inserted by the user in the first screen
    def insert_drivers(self):
        try:
            self.file_man.current_path = ""
            self.directory_list_box.delete(0, END)
            for i in range(0, len(self.drivers)):
                self.directory_list_box.insert(i, self.drivers[i])
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Navigate forward by double-click on the names
    def navigate_forward(self, event):
        try:
            source_file_path = self.file_man.current_path
            selected_value = self.get_selected_listbox_item()
            self.file_man.current_path += selected_value
            file_names = self.file_man.list_dir_in_path(self.file_man.current_path)

            self.populate_listbox(file_names)
            self.show_current_directory()
            if self.file_man.current_path != "/":
                self.file_man.current_path += "/"
            destination_file_path = self.file_man.current_path
            self.logs.log_traversal(source_file_path, destination_file_path, datetime.now())
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Navigate forward by writing absolute path to the entry
    def navigate_forward_absolute_path(self):
        try:
            source_file_path = self.file_man.current_path
            timestamp = datetime.now()
            self.file_man.current_path = self.directory_path.get()
            file_names = self.file_man.list_dir_in_path(self.file_man.current_path)
            self.populate_listbox(file_names)
            if self.file_man.current_path != "/":
                self.file_man.current_path += "/"
            destination_file_path = self.file_man.current_path
            self.logs.log_traversal(source_file_path, destination_file_path, timestamp)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Go to the Parent directory
    def navigate_backward(self):
        try:
            if (self.file_man.current_path == "/" or self.file_man.current_path == "D:"
                    or self.file_man.current_path == "//" or self.file_man.current_path == "D://"):
                self.insert_drivers()
                self.file_man.current_path = ""
                return
            self.file_man.current_path = self.file_man.current_path[:-1]
            self.file_man.current_path = self.file_man.get_absolute_path()
            file_names = self.file_man.list_dir_in_path(self.file_man.current_path)
            self.populate_listbox(file_names)
            self.file_man.current_path += "/"
            if self.file_man.current_path == "//":
                self.file_man.current_path = "/"
            elif self.file_man.current_path == "D:/":
                self.file_man.current_path = "D:"
            self.show_current_directory()
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    def show_current_directory(self):
        try:
            self.directory_path.delete(0, 'end')
            self.directory_path.insert(0, self.file_man.current_path)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # ---------------------------------------- Create Delete New Files or Directories ----------------------------------
    def create_new_directory(self, event):
        # Get the selected item from the listbox
        try:
            selected_value = self.get_selected_listbox_item()
            if selected_value == "":
                selected_value = self.file_man.current_path
            new_dir_name = simpledialog.askstring("New Directory", f"Enter name for new directory: ",
                                                  parent=self.window)
            creation_file_path = self.file_man.current_path + selected_value + "\\" + new_dir_name
            timestamp = datetime.now()
            self.logs.log_creation(creation_file_path, timestamp)
            messagebox.showinfo("Status", self.file_man.create_new_dir([new_dir_name, selected_value]))
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    def delete_new_directory(self, event):
        try:
            selected_value = self.get_selected_listbox_item()
            path = self.file_man.current_path + selected_value
            messagebox.showinfo("Status", FileManagerController.remove_old_dir(path))
            file_names = self.file_man.list_dir_in_path(self.file_man.current_path)
            self.populate_listbox(file_names)
            deletion_file_path = path
            timestamp = datetime.now()
            self.logs.log_deletion(deletion_file_path, timestamp)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # ---------------------------------------- Copy Move New Files ----------------------------------------
    def copy_file(self, event):
        try:
            selected_value = self.get_selected_listbox_item()
            self.file_man.copy_current_file_path(selected_value)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    def move_file(self, event):
        try:
            selected_value = self.get_selected_listbox_item()
            self.file_man.copy_current_file_path_for_move(selected_value)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    def paste_file(self, event):
        try:
            selected_file_path = self.get_selected_listbox_item()
            messagebox.showinfo("Status", self.file_man.paste_file(selected_file_path))
            file_path = self.file_man.source_path
            source_file_path = self.file_man.source_path
            destination_file_path = self.file_man.current_path + selected_file_path
            timestamp = datetime.now()
            action_type = "M"
            if self.file_man.copy_or_move:
                action_type = "C"
            self.file_man.source_path = ""
            file_names = self.file_man.list_dir_in_path(self.file_man.current_path)
            self.populate_listbox(file_names)
            self.logs.log_copy_or_move(file_path, source_file_path, destination_file_path, timestamp, action_type)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))
    # ---------------------------------------- Logs ----------------------------------------

    def show_options_for_logs(self, event):
        try:
            menu = Menu(self.window, tearoff=0)
            menu.add_command(label="Traversal", command=self.show_traversal_logs)
            menu.add_command(label="Creation", command=self.show_creation_logs)
            menu.add_command(label="Deletion", command=self.show_deletion_logs)
            menu.add_command(label="Copy/Move", command=self.show_copy_or_move_logs)
            menu.add_command(label="Error", command=self.show_error_logs)

            menu.post(event.x_root, event.y_root)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # show traversal logs in the directory list box
    def show_traversal_logs(self):
        try:
            traversal_logs = self.logs.get_traversal_logs()
            self.populate_listbox(traversal_logs)
            self.directory_list_box.config(state="disabled")
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # show creation logs
    def show_creation_logs(self):
        try:
            creation_logs = self.logs.get_creation_logs()
            self.populate_listbox(creation_logs)
            self.directory_list_box.config(state="disabled")
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # list deletion logs in the directory logs
    def show_deletion_logs(self):
        try:
            deletion_logs = self.logs.get_deletion_logs()
            self.populate_listbox(deletion_logs)
            self.directory_list_box.config(state="disabled")
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # List copy or move logs in the directory box
    def show_copy_or_move_logs(self):
        try:
            copy_or_move_logs = self.logs.get_copy_or_move_logs()
            self.populate_listbox(copy_or_move_logs)
            self.directory_list_box.config(state="disabled")
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # List error logs in the directory box
    def show_error_logs(self):
        try:
            error_logs = self.logs.get_error_logs()
            self.populate_listbox(error_logs)
            self.directory_list_box.config(state="disabled")
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # ---------------------------------------- Sort the Directories and Files ----------------------------------------
    def sort_selection(self, event):
        try:
            menu = Menu(self.frame2, tearoff=0)
            menu.add_command(label="Date-Created", command=self.sort_by_creation_date)
            menu.add_command(label="Date-Modified", command=self.sort_by_modified_date)
            menu.add_command(label="A-Z", command=self.sort_by_alphabet)
            menu.add_command(label="Size", command=self.sort_by_file_size)

            menu.post(event.x_root, event.y_root)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Sort the dir list based on alphabets
    def sort_by_alphabet(self):
        try:
            file_names = sorted(self.file_man.list_dir_in_path(self.file_man.current_path))
            self.populate_listbox(file_names)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Sort the dir list based on Creation Date
    def sort_by_creation_date(self):
        try:
            file_names = self.file_man.list_dir_in_path_by_created_date(self.file_man.current_path)
            self.populate_listbox(file_names)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Sort the dir list based on Modified Date
    def sort_by_modified_date(self):
        try:
            file_names = self.file_man.list_dir_in_path_by_modified_date(self.file_man.current_path)
            self.populate_listbox(file_names)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))

    # Sort the dir list based on File Size
    def sort_by_file_size(self):
        try:
            file_names = self.file_man.list_dir_in_path_by_file_size(self.file_man.current_path)
            self.populate_listbox(file_names)
        except Exception as e:
            source_file_path = "Drivers" if self.file_man.current_path == "" else self.file_man.current_path
            self.logs.log_error(self.logs.get_error_info(source_file_path, e, datetime.now()))