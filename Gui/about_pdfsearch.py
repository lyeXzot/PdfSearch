import tkinter as tk
from tkinter.ttk import Button

from Gui.utils import CentralWindow


class AboutPdfSearch(CentralWindow):
    def __init__(self, master):
        my_height = 300
        super().__init__(master, my_height)

        self.master = master

        self.title("About PdfSearch")
        self.resizable = False

        self.ok_button = Button(self, text="OK", command=self.destroy)
        self.ok_button.pack(side=tk.BOTTOM, pady=(0, 20))

        self.bind("<Return>", lambda event=None: self.ok_button.invoke())
        self.bind("<Escape>", lambda event=None: self.ok_button.invoke())

        self.content_text = tk.Text(self, bg="white", fg="black")
        self.content_text.insert(tk.END, "Developed by ...\nStudents of HUST")
        self.content_text.pack(side=tk.TOP, fill=tk.X,
                               expand=1, padx=10, pady=5)
        self.content_text.insert("1.0", "PdfSearch 1.0\n")
        self.content_text.tag_add("title", "1.0", "1.13")
        self.content_text.tag_config(
            "title", font=("Times New Roman", 12, "bold"))
        self.content_text.configure(state='disabled')

        self.focus_force()
