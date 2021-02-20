import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import messagebox as msg
from tkinter import filedialog
class PdfSearchTool(tk.Tk):
  def __init__(self):
    super().__init__()

    self.path=tk.StringVar(self,value='')

    self.title("PdfSearch")
    self.geometry("800x600")
    self.resizable(False,False)

    self.menu=tk.Menu(self,bg="lightgrey",fg="black")

    self.file_menu=tk.Menu(self.menu,tearoff=0,bg="lightgrey",fg="black")
    self.file_menu.add_command(label="Open File...",command=self.open_file,accelerator="Ctrl+F")
    self.file_menu.add_command(label="Open Dir...",command=self.open_dir,accelerator="Ctrl+D")
    self.file_menu.add_command(label="Save Output",command=self.save_output,accelerator="Ctrl+S")

    self.help_menu=tk.Menu(self.menu,tearoff=0,bg="lightgrey",fg="black")
    self.help_menu.add_command(label="About...",command=self.about)

    self.menu.add_cascade(label="File",menu=self.file_menu)
    self.menu.add_cascade(label="Help",menu=self.help_menu)

    self.config(menu=self.menu)

    self.left_frame = tk.Frame(self, width=150, height=600, bg="lightgrey")
    self.left_frame.pack_propagate(0)

    self.right_frame = tk.Frame(self, width=650, height=600, bg="lightgrey")
    self.right_frame.pack_propagate(0)

    self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
    self.right_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

    self.bind("<Control-f>", self.open_file)
    self.bind("<Control-d>",self.open_dir)
    self.bind("<Control-s>", self.save_output)

  def open_file(self,event=None):
    temp_file=filedialog.askopenfilename()
    while temp_file and not temp_file.endswith(".pdf"):
      msg.showerror("Wrong Filetype","Please select a pdf file")
      temp_file=filedialog.askopenfilename()

    if(temp_file):
      self.path.set(temp_file)

  def open_dir(self,event=None):
    temp=filedialog.askdirectory(mustexist=True)
    self.path.set(temp)

  def save_output(self):
    pass
  def about(self):
    pass

if __name__=="__main__":
  pdfSearchTool = PdfSearchTool()
  pdfSearchTool.mainloop()