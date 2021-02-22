import tkinter as tk
from tkinter.ttk import Notebook, Label, Style, Progressbar, Button
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter.font import BOLD, Font


class CentralForm(tk.Toplevel):

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

    self.content_text = tk.Text(self,  bg="white", fg="black")
    self.content_text.insert(tk.END, "Developed by ...\nStudents of HUST")
    self.content_text.pack(side=tk.TOP, fill=tk.X,
                           expand=1, padx=10, pady=5)
    self.content_text.insert("1.0", "PdfSearch 1.0\n")
    self.content_text.tag_add("title", "1.0", "1.13")
    self.content_text.tag_config(
        "title", font=("Times New Roman", 12, "bold"))
    self.content_text.configure(state='disabled')


class PdfSearch(tk.Tk):
  def __init__(self):
    super().__init__()

    self.path = tk.StringVar(self, value='')
    self.total_file_num_var = tk.StringVar(self, value='0')

    self.style = Style()
    self.style.configure('Bold10.TLabel', background="lightgrey",
                         foreground="black", font="Helvetica 8 bold")
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

    self.left_frame = tk.Frame(self, width=150, height=600, bg="lightgrey")
    self.left_frame.pack_propagate(0)

    self.right_frame = tk.Frame(
        self, width=650, height=600, bg="lightgrey")
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

    # word_list_tab
    word_list_tab = tk.Frame(self.notebook, bg="lightgrey")
    self.word_list_word_types = tk.IntVar(self, value=0)
    self.word_list_word_tokens = tk.IntVar(self, value=0)
    self.word_list_search_hits = tk.IntVar(self, value=0)
    # word_list_top_frame
    self.word_list_top_frame = tk.Frame(
        word_list_tab, background="lightgrey")
    self.word_list_word_types_label = Label(
        self.word_list_top_frame, text="Word Types: ", style="Bold10.TLabel")
    self.word_list_word_tokens_label = Label(
        self.word_list_top_frame, text="Word Tokens: ", style="Bold10.TLabel")
    self.word_list_search_hits_label = Label(
        self.word_list_top_frame, text="Search Hits: ", style="Bold10.TLabel")
    self.word_list_word_types_value_label = Label(
        self.word_list_top_frame, textvar=str(self.word_list_word_types), background="lightgrey")
    self.word_list_word_tokens_value_label = Label(
        self.word_list_top_frame, textvar=str(self.word_list_word_tokens), background="lightgrey")
    self.word_list_search_hits_value_label = Label(
        self.word_list_top_frame, textvar=str(self.word_list_search_hits), background="lightgrey")
    self.word_list_word_types_label.pack(side=tk.LEFT)
    self.word_list_word_types_value_label.pack(side=tk.LEFT, padx=(5, 20))
    self.word_list_word_tokens_label.pack(side=tk.LEFT)
    self.word_list_word_tokens_value_label.pack(side=tk.LEFT, padx=(5, 20))
    self.word_list_search_hits_label.pack(side=tk.LEFT)
    self.word_list_search_hits_value_label.pack(side=tk.LEFT, padx=(5, 0))

    self.word_list_top_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

    # word_list_bottom_frame
    self.word_list_bottom_frame = tk.Frame(
        word_list_tab, background="lightgrey")




    self.search_by_case = tk.IntVar(self, value=0)
    self.search_by_words = tk.IntVar(self, value=0)
    self.search_by_regex = tk.IntVar(self, value=0)
    self.search_term = tk.StringVar(self, value="")

    self.search_term_text = Label(
        self.word_list_bottom_frame, text="Search Term", style="Bold10.TLabel")
    self.search_by_words_cb = tk.Checkbutton(
        self.word_list_bottom_frame, variable=self.search_by_words, text="Words")
    self.search_by_case_cb = tk.Checkbutton(
        self.word_list_bottom_frame, variable=self.search_by_case, text="Case")
    self.search_by_regex_cb = tk.Checkbutton(
        self.word_list_bottom_frame, variable=self.search_by_regex, text="Regex")

    self.search_term_text.grid(row=1,column=1)
    self.search_by_words_cb.grid(row=1,column=2)
    self.search_by_case_cb.grid(row=1,column=3)
    self.search_by_regex_cb.grid(row=1,column=4)

    self.search_term_entry = tk.Entry(
        self.word_list_bottom_frame, textvariable=self.search_term)
    self.search_term_entry.grid(row=2, columnspan=4)

    self.search_start = Button(
        self.word_list_bottom_frame, text="Start", command=self.start_search)
    self.search_stop = Button(
        self.word_list_bottom_frame, text="Stop", command=self.stop_search)
    self.search_sort = Button(
        self.word_list_bottom_frame, text="Sort", command=self.sort_search)

    self.search_start.grid(row=3,column=1)
    self.search_stop.grid(row=3,column=2)
    self.search_sort.grid(row=3,column=3)

    self.word_list_bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

    # word_list_central_frame
    self.word_list_central_frame = tk.Frame(
        word_list_tab, background="lightgrey")

    self.word_list_vertical_scrollbar = tk.Scrollbar(
        self.word_list_central_frame, orient="vertical", command=self.scroll_rank_and_freq_and_word)

    self.word_list_rank_text = tk.Text(
        self.word_list_central_frame, width=10)
    self.word_list_rank_text.configure(state="disabled")

    self.word_list_freq_text = tk.Text(
        self.word_list_central_frame, width=10)
    self.word_list_freq_text.configure(state="disabled")

    self.word_list_word_text = tk.Text(
        self.word_list_central_frame, width=80)
    self.word_list_word_text.configure(state="disabled")

    self.word_list_freq_text.configure(
        yscrollcommand=self.word_list_vertical_scrollbar.set)
    self.word_list_rank_text.configure(
        yscrollcommand=self.word_list_vertical_scrollbar.set)
    self.word_list_word_text.configure(
        yscrollcommand=self.word_list_vertical_scrollbar.set)

    self.word_list_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.word_list_rank_text.pack(side=tk.LEFT, fill=tk.Y, padx=10)
    self.word_list_freq_text.pack(side=tk.LEFT, fill=tk.Y, padx=10)
    self.word_list_word_text.pack(side=tk.LEFT, fill=tk.Y, padx=10)

    self.word_list_central_frame.pack(side=tk.TOP, fill=tk.BOTH)

    self.notebook.add(word_list_tab, text="Word List")

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

  def scroll_rank_and_freq_and_word(self, *args):
    try:  # from scrollbar
      self.main_text.yview_moveto(args[1])
      self.line_numbers.yview_moveto(args[1])
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

      self.main_text.yview_scroll(int(move), "units")
      self.line_numbers.yview_scroll(int(move), "units")

    return "break"


if __name__ == "__main__":
  pdfSearch = PdfSearch()
  pdfSearch.mainloop()
