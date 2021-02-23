import tkinter as tk
from tkinter.ttk import Notebook, Label, Style, Progressbar, Button
from tkinter import messagebox as msg
from tkinter import filedialog, Frame
from tkinter.font import BOLD, Font


class ModelTab(Frame):
  """
  所有Tab的模型
  """
  def __init__(self, master):
    super().__init__(master)
    self.set_bottom_frame()

  def set_bottom_frame(self):
    """
    底部框架，包含搜索框、搜索选项
    """

    self.bottom_frame = Frame(self)

    self.search_by_case = tk.IntVar(self, value=0)
    self.search_by_words = tk.IntVar(self, value=0)
    self.search_by_regex = tk.IntVar(self, value=0)
    self.search_term = tk.StringVar(self, value="")

    self.search_term_text = Label(
        self.bottom_frame, text="Search Term", style="Bold10.TLabel")
    self.search_by_words_cb = tk.Checkbutton(
        self.bottom_frame, variable=self.search_by_words, text="Words")
    self.search_by_case_cb = tk.Checkbutton(
        self.bottom_frame, variable=self.search_by_case, text="Case")
    self.search_by_regex_cb = tk.Checkbutton(
        self.bottom_frame, variable=self.search_by_regex, text="Regex")

    self.bottom_frame.pack(side=tk.BOTTOM)

    self.search_term_text.grid(row=0, column=0)
    self.search_by_words_cb.grid(row=0, column=1)
    self.search_by_case_cb.grid(row=0, column=2)
    self.search_by_regex_cb.grid(row=0, column=3)

    self.search_term_entry = tk.Entry(
        self.bottom_frame, textvariable=self.search_term, width=60)
    self.search_term_entry.grid(row=1, column=0, columnspan=4)

    self.search_start = Button(
        self.bottom_frame, text="Start", command=self.master.start_search)
    self.search_stop = Button(
        self.bottom_frame, text="Stop", command=self.master.stop_search)
    self.search_sort = Button(
        self.bottom_frame, text="Sort", command=self.master.sort_search)

    self.search_start.grid(row=2, column=0)
    self.search_stop.grid(row=2, column=1)
    self.search_sort.grid(row=2, column=2)

  def set_top_frame(self, top_item_dict):
    """
    顶部信息框架
    top_item_dict:
        key: 信息名称
        value: tk.StringVar/tk.IntVar...实例
    """
    self.top_frame = Frame(self)

    for name, variable in top_item_dict.items():
      name_label = Label(self.top_frame, text=name,
                         style="Bold10.TLabel")
      if isinstance(variable, tk.StringVar):
        value_label = Label(
            self.top_frame, textvar=variable)
      else:
        value_label = Label(self.top_frame, textvar=str(
            variable))
      name_label.pack(side=tk.LEFT)
      value_label.pack(side=tk.LEFT, padx=(5, 20))

    self.top_frame.pack(side=tk.TOP, fill=tk.X, ipady=10, ipadx=10)

  def set_central_frame(self, central_title_to_width_dict):
    """
    中间框架，包含文本框，滑动条
    """
    self.central_texts = {}  # key:title     value:instance of tk.Text

    self.central_frame = Frame(self)

    self.vertical_scrollbar = tk.Scrollbar(
        self.central_frame, orient="vertical", command=self.scroll_all_text_vertical)

    self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for title, width in central_title_to_width_dict.items():
      new_text = self.set_central_title_and_text(title, width)
      self.central_texts[title] = new_text

    self.central_frame.pack(side=tk.TOP, fill=tk.BOTH)

  def set_central_title_and_text(self, title, width):
    """
    中间框架内部的纵向小单元，包含名称、文本框、横向滑动条
    """
    new_frame = Frame(self.central_frame, width=width)

    new_label = Label(new_frame, text=title,
                      style="blue.TLabel", width=width)
    new_text = tk.Text(new_frame, width=width)
    new_text.configure(state="disabled")
    new_text.configure(yscrollcommand=self.vertical_scrollbar.set)
    new_horizontal_scrollbar = tk.Scrollbar(
        new_frame, orient="horizontal", command=self.scroll_text_horizontal)

    new_label.pack(side=tk.TOP, fill=tk.X)
    new_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    new_text.pack(side=tk.TOP, fill=tk.BOTH)
    new_frame.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=5)

    return new_text

  def scroll_text_horizontal(self, *args):  # TODO
    pass

  def scroll_all_text_vertical(self, *args):
    try:  # from scrollbar
      for text in self.central_texts:
        text.yview_moveto(args[1])
    except IndexError:
      # from mouse MouseWheel
      event = args[0]
      if event.delta:
        move = -1*(event.delta/120)
      else:
        if event.num == 5:
          move = 1
        else:
          move = -1

      for text in self.central_texts:
        text.yview_scroll(int(move), "units")

    return "break"


class ConcordanceTab(ModelTab):
  def __init__(self, master):
    super().__init__(master)

    self.concordance_hits = tk.IntVar(self, value=0)
    temp_top = {
      "Concordance Hits": self.concordance_hits
    }
    self.set_top_frame(temp_top)
    temp_central = {
      "Hit": 10,
      "KWIC": 60,
      "File": 30
    }
    self.set_central_frame(temp_central)


class FileViewTab(ModelTab):
  def __init__(self, master):
    super().__init__(master)

    self.file_view_hits = tk.IntVar(self, value=0)
    self.file_str = tk.StringVar(self, value="")

    temp_top = {
      "File View Hits": self.file_view_hits,
      "File": self.file_str
    }
    self.set_top_frame(temp_top)

    temp_central={
      "":80
    }
    self.set_central_frame(temp_central)


class WordListTab(ModelTab):
  def __init__(self, master):
    super().__init__(master)

    self.word_types = tk.IntVar(self, value=0)
    self.word_tokens = tk.IntVar(self, value=0)
    self.search_hits = tk.IntVar(self, value=0)

    temp_top = {
      "Word Types": self.word_types,
      "Word Tokens": self.word_tokens, "Search Hits": self.search_hits
    }
    self.set_top_frame(temp_top)
    temp_central = {
      "Rank": 10,
      "Freq": 10,
      "Word": 80
    }
    self.set_central_frame(temp_central)


class CentralForm(tk.Toplevel):
  """
  让弹出窗口居中显示
  """
  def __init__(self, master, my_height=80):
    super().__init__()
    self.master = master

    master_pos_x = self.master.winfo_x()
    master_pos_y = self.master.winfo_y()

    master_width = self.master.winfo_width()
    master_height = self.master.winfo_height()

    my_width = 300

    pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
    pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)

    geometry = "{}x{}+{}+{}".format(my_width, my_height, pos_x, pos_y)
    self.geometry(geometry)


class AboutPdfSearch(CentralForm):
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

    self.content_text = tk.Text(self,  bg="white", fg="black")
    self.content_text.insert(tk.END, "Developed by ...\nStudents of HUST")
    self.content_text.pack(side=tk.TOP, fill=tk.X,
                           expand=1, padx=10, pady=5)
    self.content_text.insert("1.0", "PdfSearch 1.0\n")
    self.content_text.tag_add("title", "1.0", "1.13")
    self.content_text.tag_config(
        "title", font=("Times New Roman", 12, "bold"))
    self.content_text.configure(state='disabled')

    self.focus_force()


class PdfSearch(tk.Tk):
  def __init__(self):
    super().__init__()

    self.path = tk.StringVar(self, value='')
    self.total_file_num_var = tk.StringVar(self, value='0')

    self.style = Style()
    self.style.configure('Bold10.TLabel',
                         foreground="black", font="Helvetica 8 bold")
    self.style.configure('blue.TLabel', foreground="blue")
    self.style.configure(
        'TProgressbar', troughcolor="green", background="gray")

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

    self.left_frame = Frame(self, width=150, height=600)
    self.left_frame.pack_propagate(0)

    self.right_frame = Frame(
        self, width=650, height=600)
    self.right_frame.pack_propagate(0)

    # inside left_frame
    self.corpus_label = Label(
        self.left_frame, text="Corpus Files", style="Bold10.TLabel")
    self.corpus_label.pack(side=tk.TOP)

    self.section_select = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
    self.section_select.configure(exportselection=False)
    self.section_select.pack(fill=tk.Y, expand=0.8)
    self.section_select.bind("<<ListboxSelect>>", self.view_file)

    self.total_num_label = Label(
        self.left_frame, text="Total No.", style="Bold10.TLabel")
    self.total_num_value_label = Label(
        self.left_frame, textvar=self.total_file_num_var, background="white")
    self.file_processed_label = Label(
        self.left_frame, text="File Processed", style="Bold10.TLabel")
    self.file_processed_progressbar = Progressbar(
        self.left_frame, orient=tk.HORIZONTAL, style="TProgressbar")
    self.file_processed_progressbar.pack(side=tk.BOTTOM, fill=tk.X)
    self.file_processed_label.pack(side=tk.BOTTOM, fill=tk.X)
    self.total_num_value_label.pack(side=tk.BOTTOM, fill=tk.X)
    self.total_num_label.pack(side=tk.BOTTOM, fill=tk.X)

    # inside right_frame
    self.notebook = Notebook(self.right_frame)

    self.concordance_tab = ConcordanceTab(self)
    self.file_view_tab = FileViewTab(self)
    self.tab = WordListTab(self)

    self.notebook.add(self.concordance_tab, text="Concordance")
    self.notebook.add(self.file_view_tab, text="File View")
    self.notebook.add(self.tab, text="Word List")

    self.notebook.pack(fill=tk.BOTH, expand=1)

    self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=5)
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

  def start_search(self, event=None):
    pass

  def stop_search(self, event=None):
    pass

  def sort_search(self, event=None):
    pass

  def about(self):
    AboutPdfSearch(self)

  def view_file(self, event=None):
    pass


if __name__ == "__main__":
  pdfSearch = PdfSearch()
  pdfSearch.mainloop()
