import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import datetime

class CodePad:
    def __init__(self, root):
        self.root = root
        self.root.title("DevPad: A Developer's Notepad")
        self.dark_theme = False

        # Create a text field for code editing
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Function to open a file
        open_button = tk.Button(self.root, text="Open File", command=self.open_file)
        open_button.pack()

        # Function to toggle dark theme
        theme_button = tk.Button(self.root, text="Toggle Dark Theme", command=self.toggle_theme)
        theme_button.pack()

        # Function to save the file
        save_button = tk.Button(self.root, text="Save File", command=self.save_file)
        save_button.pack()

        # Automatic saving function
        self.root.after(60000, self.auto_save)  # Autosave every minute (60000 milliseconds)

        # Function for finding and replacing text
        find_replace_button = tk.Button(self.root, text="Find and Replace", command=self.find_and_replace)
        find_replace_button.pack()

        # Function to change font
        font_button = tk.Button(self.root, text="Change Font", command=self.change_font)
        font_button.pack()

        # Function to clear the text area
        clear_button = tk.Button(self.root, text="Clear Text", command=self.clear_text)
        clear_button.pack()

        # Function to count lines and words
        stats_button = tk.Button(self.root, text="Count Lines and Words", command=self.count_lines_words)
        stats_button.pack()

        # Function to insert current date and time
        insert_datetime_button = tk.Button(self.root, text="Insert Date/Time", command=self.insert_datetime)
        insert_datetime_button.pack()

        # Function to select all text
        select_all_button = tk.Button(self.root, text="Select All", command=self.select_all)
        select_all_button.pack()

        # Function to copy selected text
        copy_button = tk.Button(self.root, text="Copy", command=self.copy_text)
        copy_button.pack()

        # Function to cut selected text
        cut_button = tk.Button(self.root, text="Cut", command=self.cut_text)
        cut_button.pack()

        # Function to paste copied or cut text
        paste_button = tk.Button(self.root, text="Paste", command=self.paste_text)
        paste_button.pack()

        # Function to delete selected text
        delete_button = tk.Button(self.root, text="Delete", command=self.delete_text)
        delete_button.pack()

        # Function to duplicate selected text
        duplicate_button = tk.Button(self.root, text="Duplicate", command=self.duplicate_text)
        duplicate_button.pack()

        # Bind keyboard shortcuts
        self.text_area.bind("<Control-c>", self.copy_text)
        self.text_area.bind("<Control-x>", self.cut_text)
        self.text_area.bind("<Control-v>", self.paste_text)
        self.text_area.bind("<Control-a>", self.select_all)
        self.text_area.bind("<Delete>", self.delete_text)
        self.text_area.bind("<Control-d>", self.duplicate_text)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.root.configure(bg="#272727" if self.dark_theme else "white")
        self.text_area.configure(bg="#272727" if self.dark_theme else "white", fg="white" if self.dark_theme else "#272727")

    def save_file(self):
        content = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)

    def auto_save(self):
        content = self.text_area.get("1.0", tk.END)
        with open("autosave.txt", "w") as file:
            file.write(content)
        self.root.after(60000, self.auto_save)

    def find_and_replace(self):
        find_text = simpledialog.askstring("Find", "Find:")
        if find_text:
            replace_text = simpledialog.askstring("Replace", f"Replace '{find_text}' with:")
            if replace_text:
                content = self.text_area.get("1.0", tk.END)
                content = content.replace(find_text, replace_text)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)

    def change_font(self):
        font_name = simpledialog.askstring("Font Name", "Enter font name:")
        if font_name:
            font_size = simpledialog.askinteger("Font Size", "Enter font size:")
            if font_size:
                self.text_area.configure(font=(font_name, font_size))

    def clear_text(self):
        response = messagebox.askyesno("Clear Text", "Do you want to clear the text area?")
        if response:
            self.text_area.delete("1.0", tk.END)

    def count_lines_words(self):
        content = self.text_area.get("1.0", tk.END)
        lines = len(content.splitlines())
        words = len(content.split())
        messagebox.showinfo("Statistics", f"Lines: {lines}\nWords: {words}")

    def insert_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, current_datetime)

    def select_all(self, event=None):
        self.text_area.tag_add("sel", "1.0", "end")

    def copy_text(self, event=None):
        self.text_area.event_generate("<<Copy>>")

    def cut_text(self, event=None):
        self.text_area.event_generate("<<Cut>>")

    def paste_text(self, event=None):
        self.text_area.event_generate("<<Paste>>")

    def delete_text(self, event=None):
        self.text_area.delete("sel.first", "sel.last")

    def duplicate_text(self, event=None):
        selected_text = self.text_area.get("sel.first", "sel.last")
        self.text_area.insert("sel.first", selected_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodePad(root)
    root.mainloop()
