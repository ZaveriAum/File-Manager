# Logs
import sqlite3
import traceback


class Logs:
    def __init__(self):
        # Establish a connection to the SQLite database 'Logs.db' when the object is instantiated
        self.conn = sqlite3.connect('Logs.db')
        self.cursor = self.conn.cursor()

    # Get all Traversal Logs
    def get_traversal_logs(self):
        # SQL query to select all records from the Traversal_Logs table
        query = '''SELECT * FROM Traversal_Logs'''
        self.cursor.execute(query)
        # Fetch all records
        traversal_logs = self.cursor.fetchall()
        # Initialize a list to store the logs
        logs = ["User Logs For Directory Traversal"]

        # Iterate through each record and format the log message
        for log in traversal_logs:
            appending_string = f"{log[0]}: User traversed from {log[1]} to {log[2]} at {log[3]}"
            # Append the log message to the logs list
            logs.append(appending_string)

        return logs

    # Log a traversal action
    def log_traversal(self, source_file_path, destination_file_path, timestamp):
        # SQL query to insert a record into the Traversal_Logs table
        query = '''INSERT INTO Traversal_Logs (SourceFilePath, DestinationFilePath, Timestamp) 
                           VALUES (?, ?, ?)'''
        data = (source_file_path, destination_file_path, timestamp)
        # Execute the query
        self.cursor.execute(query, data)
        # Commit the transaction
        self.conn.commit()

    # Get all Creation Logs
    def get_creation_logs(self):
        query = '''SELECT * FROM Creation_Logs'''
        self.cursor.execute(query)
        logs = []
        creation_logs = self.cursor.fetchall()
        title = "User Logs For Directory Creation"
        logs.append(title)
        for log in creation_logs:
            appending_string = f"{log[0]}: User created new directory at {log[1]} at {log[2]}"
            logs.append(appending_string)

        return logs

    # Log a creation action
    def log_creation(self, creation_file_path, timestamp):
        query = '''INSERT INTO Creation_Logs (CreationFilePath, Timestamp) Values (?, ?)'''
        data = (creation_file_path, timestamp)
        self.cursor.execute(query, data)
        self.conn.commit()

    # Get all Deletion Logs
    def get_deletion_logs(self):
        query = '''SELECT * FROM Deletion_Logs'''
        self.cursor.execute(query)
        deletion_logs = self.cursor.fetchall()
        logs = ["User Logs For Directory Deletion"]
        for log in deletion_logs:
            appending_string = f"{log[0]}: User deleted a directory at {log[1]} at {log[2]}"
            logs.append(appending_string)
        return logs

    # Log a deletion action
    def log_deletion(self, deletion_file_path, timestamp):
        query = '''INSERT INTO Deletion_Logs (DeletionFilePath, Timestamp) Values (?, ?)'''
        data = (deletion_file_path, timestamp)
        self.cursor.execute(query, data)
        self.conn.commit()

    # Get all Copy/Move Logs
    def get_copy_or_move_logs(self):
        query = '''SELECT * FROM Copy_Or_Move_Logs'''
        self.cursor.execute(query)
        copy_or_move_logs = self.cursor.fetchall()
        logs = ["User Logs For Directory Copy(C) or Move(M)"]
        for log in copy_or_move_logs:
            appending_string = f"{log[0]}: Action Type {log[5]} at {log[4]} "
            appending_string_1 = f"     File: {log[1]} from {log[2]} to {log[3]} "
            logs.append(appending_string)
            logs.append(appending_string_1)
        return logs

    # Log a copy or move action
    def log_copy_or_move(self, file_path, source_file_path, destination_file_path, timestamp, action_type):
        query = '''INSERT INTO Copy_Or_Move_Logs (FilePath, SourceFilePath, DestinationFilePath, Timestamp, ActionType)
         Values(?, ?, ?, ?, ?)'''
        data = (file_path, source_file_path, destination_file_path, timestamp, action_type)
        self.cursor.execute(query, data)
        self.conn.commit()

    # Get all Error Logs
    def get_error_logs(self):
        query = '''SELECT * FROM Error_Logs'''
        self.cursor.execute(query)
        error_logs = self.cursor.fetchall()
        logs = ["User Logs For Error"]
        for log in error_logs:
            appending_string_1 = f"{log[0]}: Error at: {log[1]} {log[2]}: {log[3]}\nTraceback: {log[4]} at {log[5]}"
            appending_string_2 = f"    {log[2]}: {log[3]} at {log[5]}"
            appending_string_3 = f"    Traceback: {log[4]}"
            logs.append(appending_string_1)
            logs.append(appending_string_2)
            logs.append(appending_string_3)
        return logs

    # Log an error
    def log_error(self, error_data):
        query = '''INSERT INTO Error_Logs (SourceFilePath, ErrorType, ErrorMessage, Traceback, Timestamp)
         Values(?, ?, ?, ?, ?)'''
        self.cursor.execute(query, error_data)
        self.conn.commit()

    # Get error information
    def get_error_info(self, source_file_path, e, timestamp):
        error_type = type(e).__name__
        error_message = str(e)
        traceback_details = traceback.format_exc()
        return source_file_path, error_type, error_message, traceback_details, timestamp

    # Close connection
    def close_connection(self):
        self.cursor.close()
        self.conn.close()
