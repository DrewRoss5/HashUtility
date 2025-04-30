import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from file_hash import hash_file

def update_entry(entry: tk.Entry, data: str):
    entry.config(state='normal')
    entry.delete(0, len(entry.get()))
    entry.insert(0, data)
    entry.config(state='readonly')

# a generic widget for a file selection
class FileEntry:
    def __init__(self, parent: tk.Tk, label: str):
        self.parent = parent
        self.label = tk.Label(self.parent, text=label)
        self.entry = tk.Entry(self.parent, state='readonly', width=64)
        self.button = tk.Button(self.parent, text='Select', command=self.select_file)

    # calls the file select dialog
    def select_file(self):
        file_path = filedialog.askopenfilename()
        update_entry(self.entry, file_path)

    # returns the file
    def get(self):
        return self.entry.get()

    # places the file entry in a given row
    def grid(self, row: int):
        self.label.grid(column=0, row=row)
        self.entry.grid(column=1, row=row)
        self.button.grid(column=2, row=row)

class MainWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title('SHA256 Hash Tool')
        # create the file selection
        self.file_select = FileEntry(self.root, 'File:')
        # create the widgets for the hash
        self.hash_label = tk.Label(self.root, text='Hash: ')
        self.hash_entry = tk.Entry(self.root, state='readonly', width=64)
        self.hash_button = tk.Button(self.root, text='Hash!', command=self.hash_file)
        # create the button to switch mode
        self.comp_button = tk.Button(self.root, text='Compare files', command=self.open_comp)
        # place the widgets
        self.file_select.grid(row = 0)
        self.hash_label.grid(column=0, row=1)
        self.hash_entry.grid(column=1, row=1)
        self.hash_button.grid(column=0, row=2, columnspan=2)
        self.comp_button.grid(column=0, row=3, columnspan=2)

    # hashes the provided file
    def hash_file(self):
        # ensure a file has been selected, and that the file exists
        file_path = self.file_select.get()
        if not os.path.exists(file_path):
            messagebox.showerror('Error', 'Please provide a file to be hashed')
            return
        file_hash = hash_file(file_path)
        update_entry(self.hash_entry, file_hash)

    # opens a file comparison window, and closes this window
    def open_comp(self):
        self.root.destroy()
        window = FileCompWindow()
        window.run()

    def run(self):
        self.root.mainloop()

class FileCompWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title('SHA256 Hash Tool')
        # create the entries
        self.file_entries = []
        self.file_entries.append(FileEntry(self.root, 'First File:'))
        self.file_entries.append(FileEntry(self.root, 'Second File:'))
        # create the buttons
        self.comp_button = tk.Button(self.root, text='Compare!', command=self.compare)
        self.main_window_b  = tk.Button(self.root, text='Return', command=self.open_main_win)
        # place the widgets
        self.file_entries[0].grid(row=0)
        self.file_entries[1].grid(row=1)
        self.comp_button.grid(column=0, row=2, columnspan=2)
        self.main_window_b.grid(column=0, row=3, columnspan=2)

    def compare(self):
        file_1 = self.file_entries[0].get()
        file_2 = self.file_entries[1].get()
        # ensure both files are valid paths
        for i in (file_1, file_2):
            if not os.path.exists(i):
                messagebox.showerror('Error', 'Please provide two files to be read')
                return
        # compare the hashes
        if hash_file(file_1) == hash_file(file_2):
            messagebox.showinfo('Files Match', 'The hashes of these files match')
        else:
            messagebox.showinfo('No Match', 'The hashes of these files do not match')

    def open_main_win(self):
        self.root.destroy()
        window = MainWindow()
        window.run()


    def run(self):
        self.root.mainloop()