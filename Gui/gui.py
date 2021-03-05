import tkinter as tk
from tkinter import messagebox as msg, filedialog, Frame
from tkinter.ttk import Notebook, Label, Style, Progressbar

from Gui.about_pdfsearch import AboutPdfSearch
from Gui.concordance_tab import ConcordanceTab
from Gui.file_view_tab import FileViewTab
from Gui.word_list_tab import WordListTab

from Pdf.util import get_all_PdfPath
from pdfminer.high_level import extract_text

from Statistics.statistics import statistics
import ntpath
from Search.search import search
from Gui.model_tab import ModelTab


class PdfSearch(tk.Tk):
    def __init__(self):
        super().__init__()

        self.path = tk.StringVar(self, value='')
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

        self.total_num_label = Label(
            self.left_frame, text="Total No.", style="Bold10.TLabel")
        self.total_num_value_label = Label(
            self.left_frame, textvar=self.total_file_num_var,
            background="white")
        self.file_processed_label = Label(
            self.left_frame, text="File Processed", style="Bold10.TLabel")
        self.file_processed_progressbar = Progressbar(
            self.left_frame, orient=tk.HORIZONTAL, style="TProgressbar",
            mode='determinate')
        self.file_processed_progressbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_processed_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.total_num_value_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.total_num_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.section_select_frame = Frame(self.left_frame)
        self.section_select_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1,
                                       padx=10, pady=10)

        self.section_select_horizontal_scrollbar = tk.Scrollbar(
            self.section_select_frame, orient="horizontal")
        self.section_select_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.section_select_vertical_scrollbar = tk.Scrollbar(
            self.section_select_frame, orient="vertical"
        )
        self.section_select_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.section_select = tk.Listbox(self.section_select_frame,
                                         selectmode=tk.SINGLE,
                                         xscrollcommand=self.section_select_horizontal_scrollbar.set,
                                         yscrollcommand=self.section_select_vertical_scrollbar.set)
        self.section_select.configure(exportselection=False)
        self.section_select.pack(fill=tk.Y, expand=0.8, padx=5)
        self.section_select.bind("<<ListboxSelect>>", self.view_file)

        self.section_select_horizontal_scrollbar[
            'command'] = self.section_select.xview
        self.section_select_vertical_scrollbar[
            'command'] = self.section_select.yview

        # inside right_frame
        self.notebook = Notebook(self.right_frame)

        self.concordance_tab = ConcordanceTab(self)
        self.file_view_tab = FileViewTab(self)
        self.word_list_tab = WordListTab(self)

        self.notebook.add(self.concordance_tab, text="Concordance")
        self.notebook.add(self.file_view_tab, text="File View")
        self.notebook.add(self.word_list_tab, text="Word List")

        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=5)
        self.right_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.bind("<Control-f>", self.open_file)
        self.bind("<Control-d>", self.open_dir)
        self.bind("<Control-s>", self.save_output)

    def update_word_list(self):
        # 词频
        temp_list = []
        # for i in range(100):
        #    temp_list.append(str(i))
        # self.tab.central_texts['Rank'].insert(tk.END ,'\n'.join(temp_list))

        freq_result = statistics(self.path.get())
        freq = ''
        word = ''
        line_number = 0
        for i, j in freq_result:
            word += (str(i) + '\n')
            freq += (str(j) + '\n')
            line_number += 1
        line_number_string = "\n".join(str(no + 1) for no in range(line_number))
        self.enable_text_in_modelTab(self.word_list_tab)
        self.word_list_tab.central_texts['Freq'].insert(tk.END, freq)
        self.word_list_tab.central_texts['Word'].insert(tk.END, word)
        self.word_list_tab.central_texts['Rank'].insert(tk.END,
                                                        line_number_string)
        self.disable_text_in_modelTab(self.word_list_tab)
        self.word_list_tab.word_types.set(line_number)

    def open_file(self, event=None):
        temp_file = filedialog.askopenfilename()
        while temp_file and not temp_file.endswith(".pdf"):
            msg.showerror("Wrong Filetype", "Please select a pdf file")
            temp_file = filedialog.askopenfilename()

        if temp_file:
            self.path.set(temp_file)
            self.total_file_num_var.set("1")
            self.clear_listbox()
            self.update_word_list()  # TODO:not dir

    def open_dir(self, event=None):
        temp = filedialog.askdirectory(mustexist=True)
        self.path.set(temp)

        result = get_all_PdfPath(temp)
        self.clear_listbox()
        for i in result:
            self.section_select.insert("end", i)
        self.total_file_num_var.set(str(len(result)))
        self.update_word_list()

    def clear_listbox(self):
        self.section_select.delete(0, 'end')

    def save_output(self):
        pass

    def start_search(self, event=None):
        if self.concordance_tab.search_by_words.get():
            result = search(self.path.get(),
                            self.concordance_tab.search_term_entry.get(),
                            "term")
            print(result)
        elif self.concordance_tab.search_by_case.get():
            result = search(self.path.get(),
                            self.concordance_tab.search_term_entry.get(),
                            "match")
        elif self.concordance_tab.search_by_regex.get():
            result = search(self.path.get(),
                            self.concordance_tab.search_term_entry.get(),
                            "wildcard")
        else:
            return

        line_num = 0
        # num = result['hits']['total']['value']
        temp = ''
        highlight = ''
        path = ''
        to_add_tag_list = []
        for i in result['hits']['hits']:
            for hits in i['highlight']['content']:
                line_num += 1
                self.add_index_to_tag(hits, to_add_tag_list, line_num)
                hits = hits.replace("<em>", "")
                hits = hits.replace("</em>", "")
                highlight += hits + '\n'
                # tt = '||'.join(i['highlight']['content'])
                # highlight += (tt + '\n')
                path += (i['_source']['path'] + '\n')
        for i in range(line_num):
            temp += (str(i + 1) + '\n')
        self.concordance_tab.concordance_hits.set(line_num)
        self.enable_text_in_modelTab(self.concordance_tab)
        self.clear_text_in_modelTab(self.concordance_tab)
        self.concordance_tab.central_texts['Hit'].insert(tk.END, temp)
        self.concordance_tab.central_texts['KWIC'].insert(tk.END, highlight)
        self.add_tags(to_add_tag_list,
                      self.concordance_tab.central_texts['KWIC'], "hits")
        self.concordance_tab.central_texts['File'].insert(tk.END, path)
        self.disable_text_in_modelTab(self.concordance_tab)

    def add_index_to_tag(self, str_hits, to_add_tag_list, line_number):
        em_end = 0
        em_found = 0

        while 1:
            em_start = str_hits.find("<em>", em_end)
            em_end = str_hits.find("</em>", em_start)
            if em_start == -1:
                return
            real_start = em_start - em_found * 9
            real_end = real_start + em_end - em_start - 4
            to_add_tag_list.append(str(line_number) + "." + str(real_start))
            to_add_tag_list.append(str(line_number) + "." + str(real_end))
            em_found += 1

    def add_tags(self, to_add_tags_list, text, title):
        for i in range(len(to_add_tags_list) // 2):
            text.tag_add(title, to_add_tags_list[2 * i],
                         to_add_tags_list[2 * i + 1])

    def stop_search(self, event=None):
        pass

    def enable_text_in_modelTab(self, modelTab):
        if isinstance(modelTab, ModelTab):
            for text in modelTab.central_texts.values():
                text.configure(state="normal")

    def disable_text_in_modelTab(self, modelTab):
        if isinstance(modelTab, ModelTab):
            for text in modelTab.central_texts.values():
                text.configure(state='disabled')

    def clear_text_in_modelTab(self, modelTab):
        if isinstance(modelTab, ModelTab):
            for text in modelTab.central_texts.values():
                text.delete(1.0, tk.END)

    def sort_search(self, event=None):
        pass

    def about(self):
        AboutPdfSearch(self)

    def view_file(self, event=None):
        # 内容
        self.notebook.select(self.file_view_tab)
        self.file_view_tab.file_view_hits.set(1)
        path = self.section_select.get(self.section_select.curselection())
        content = extract_text(path)
        self.file_view_tab.file_str.set(path)
        self.enable_text_in_modelTab(self.file_view_tab)
        self.file_view_tab.central_texts[''].delete(1.0, tk.END)
        self.file_view_tab.central_texts[''].insert(tk.END, content)
        self.disable_text_in_modelTab(self.file_view_tab)


if __name__ == "__main__":
    pdfSearch = PdfSearch()
    pdfSearch.mainloop()
