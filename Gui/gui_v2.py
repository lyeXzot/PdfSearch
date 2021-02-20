import tkinter as tk
from tkinter.ttk import Notebook, Label,Style,Progressbar
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter.font import BOLD, Font


class PdfSearchTool(tk.Tk):
  def __init__(self):
    super().__init__()

    self.path = tk.StringVar(self, value='')
    self.total_file_num_var=tk.StringVar(self,value='0')

    self.style=Style()
    self.style.configure('Bold10.TLabel',background="lightgrey",foreground="black",font="Helvetica 8 bold")
    self.style.configure('TProgressbar',troughcolor="green",background="gray")


    self.title("PdfSearch")
    self.geometry("800x600")
    self.resizable(False, False)

    # top menubar
    self.menu = tk.Menu(self, bg="lightgrey", fg="black")

    self.file_menu = tk.Menu(self.menu, tearoff=0,
                             bg="lightgrey", fg="black")
    self.file_menu.add_command(
        label="Open File...", command=self.open_file, accelerator="Ctrl+F")
    self.file_menu.add_command(
        label="Open Dir...", command=self.open_dir, accelerator="Ctrl+D")
    self.file_menu.add_command(
        label="Save Output", command=self.save_output, accelerator="Ctrl+S")

    self.help_menu = tk.Menu(self.menu, tearoff=0,
                             bg="lightgrey", fg="black")
    self.help_menu.add_command(label="About...", command=self.about)

    self.menu.add_cascade(label="File", menu=self.file_menu)
    self.menu.add_cascade(label="Help", menu=self.help_menu)

    self.config(menu=self.menu)

    self.left_frame = tk.Frame(self, width=150, height=600, bg="lightgrey")
    self.left_frame.pack_propagate(0)

    self.right_frame = tk.Frame(
        self, width=650, height=600, bg="lightgrey")
    self.right_frame.pack_propagate(0)

    self.corpus_label = Label(
        self.left_frame, text="Corpus Files", style="Bold10.TLabel")
    self.corpus_label.pack(side=tk.TOP)

    self.section_select = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
    self.section_select.configure(exportselection=False)
    self.section_select.pack(fill=tk.Y,expand=0.8)
    self.section_select.bind("<<ListboxSelect>>", self.view_file)

    self.total_num_label=Label(self.left_frame,text="Total No.",style="Bold10.TLabel")
    self.total_num_value_label=Label(self.left_frame,textvar=self.total_file_num_var,background="white")
    self.file_processed_label=Label(self.left_frame,text="File Processed",style="Bold10.TLabel")
    self.file_processed_progressbar=Progressbar(self.left_frame,orient=tk.HORIZONTAL,style="TProgressbar")
    self.file_processed_progressbar.pack(side=tk.BOTTOM,fill=tk.X)
    self.file_processed_label.pack(side=tk.BOTTOM,fill=tk.X)
    self.total_num_value_label.pack(side=tk.BOTTOM,fill=tk.X)
    self.total_num_label.pack(side=tk.BOTTOM,fill=tk.X)

    self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    self.right_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

    self.bind("<Control-f>", self.open_file)
    self.bind("<Control-d>", self.open_dir)
    self.bind("<Control-s>", self.save_output)

  def open_file(self, event=None):
    temp_file = filedialog.askopenfilename()
    while temp_file and not temp_file.endswith(".pdf"):
      msg.showerror("Wrong Filetype", "Please select a pdf file")
      temp_file = filedialog.askopenfilename()

    if(temp_file):
      self.path.set(temp_file)

  def open_dir(self, event=None):
    temp = filedialog.askdirectory(mustexist=True)
    self.path.set(temp)

  def save_output(self):
    pass

  def about(self):
    pass

  def view_file(self, event=None):
    pass


if __name__ == "__main__":
  pdfSearchTool = PdfSearchTool()
  pdfSearchTool.mainloop()
