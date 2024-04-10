# File Manager Controller

import os
import shutil


# ---------------------------- Logic ------------------------------- #

class FileManagerController:

    def __init__(self):
        # defining current path to navigate through application
        self.current_path = ""
        self.source_path = ""
        self.copy_or_move = True

    # Listing all directories in current directory
    # Navigate through files
    @staticmethod
    def list_dir_in_path(path):
        return os.listdir(path)

    def get_absolute_path(self):
        return os.path.dirname(self.current_path)

    # Navigation Properties

# ---------------------------- Create and Delete ------------------- #
    # Create new directory
    def create_new_dir(self, values):
        try:
            os.chdir(self.current_path + values[1])

            os.makedirs(values[0])
            return f"Directory '{values[0]}' created successfully."
        except OSError as e:
            return f"Error: {values[0]} : {e.strerror}"

    # Delete new directory
    @staticmethod
    def remove_old_dir(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"File '{path}' deleted successfully."
            elif os.path.isdir(path):
                os.rmdir(path)
                return f"Directory '{path}' deleted successfully."
            else:
                return f"Directory '{path}' deleted successfully."
        except OSError as e:
            return f"Error: {path} : {e.strerror}"

    # Copy current file path
    def copy_current_file_path(self, selected_value):
        self.source_path = self.current_path + selected_value
        self.copy_or_move = True

    # Copy current file path to move the file
    def copy_current_file_path_for_move(self, selected_value):
        self.source_path = self.current_path + selected_value
        self.copy_or_move = False

    # paste file in the selected directory
    def paste_file(self, selected_file_path):
        if self.source_path == "":
            return "Please select a file to be pasted first."
        if self.copy_or_move:
            try:
                shutil.copy(self.source_path, self.current_path + selected_file_path)
                return "The file have been copied successfully."
            except IOError as e:
                return e
        else:
            try:
                shutil.move(self.source_path, self.current_path + selected_file_path)
                return "The file have been moved successfully."
            except IOError as e:
                return e

    def list_dir_in_path_by_created_date(self, path):
        # Get a list of all entries in the directory
        files = os.listdir(path)
        # Create a list of tuples containing entry name and its creation time
        file_info = [(file_name, os.path.getctime(os.path.join(path, file_name))) for file_name in files]
        # Sort the list of tuples based on creation time
        sorted_file_info = sorted(file_info, key=lambda x: x[1])
        # Extract entry names from sorted list of tuples
        sorted_files = [entry[0] for entry in sorted_file_info]
        return sorted_files

    def list_dir_in_path_by_modified_date(self, path):
        files = os.listdir(path)
        file_info = [(file_name, os.path.getmtime(os.path.join(path, file_name))) for file_name in files]
        sorted_file_info = sorted(file_info, key=lambda x: x[1], reverse=True)
        sorted_files = [file_name[0] for file_name in sorted_file_info]
        return sorted_files

    def list_dir_in_path_by_file_size(self, path):
        files = os.listdir(path)
        file_info = [(file_name, os.path.getsize(os.path.join(path, file_name))) for file_name in files]
        sorted_file_info = sorted(file_info, key=lambda x: x[1])
        sorted_files = [file_name[0] for file_name in sorted_file_info]
        return sorted_files
