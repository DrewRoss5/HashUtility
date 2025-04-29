import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from file_hash import hash_file

class MainWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Tk('Hash Utility')
        self.root.title('SHA256 Hash Tool')
        # create the widgets for the file entry
        self.file_label = tk.Label(self.root, text='File: ')
        self.file_entry = tk.Entry(self.root, state='readonly', width=64)
        self.file_select = tk.Button(self.root, text='Select', command=self.select_file)
        # create the widgets for the hash
        self.hash_label = tk.Label(self.root, text='Hash: ')
        self.hash_entry = tk.Entry(self.root, state='readonly', width=64)
        self.hash_button = tk.Button(self.root, text='Hash!', command=self.hash_file)
        # place the widgets
        self.file_label.grid(column=0, row=0)
        self.file_entry.grid(column=1, row=0)
        self.file_select.grid(column=2, row=0)
        self.hash_label.grid(column=0, row=1)
        self.hash_entry.grid(column=1, row=1)
        self.hash_button.grid(column=0, row=2, columnspan=2)

    # inserts text into a disabled entry widget
    def update_entry(self, entry: tk.Entry, data: str):
        entry.config(state=tk.NORMAL)
        entry.delete(0, len(entry.get()))
        entry.insert(0, data)
        entry.config(state='readonly')

    # opens a file selection dialog and stores the file to the appropriate entry
    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.update_entry(self.file_entry, file_path)

    # hashes the provided file
    def hash_file(self):
        # ensure a file has been selected, and that the file exists
        file_path = self.file_entry.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror('Error', 'Please provide a file to be hashed')
            return
        file_hash = hash_file(file_path)
        self.update_entry(self.hash_entry, file_hash)

    def run(self):
        self.root.mainloop()