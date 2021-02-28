import tkinter as tk
from tkinter import Frame
from tkinter.ttk import Label, Button


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
        self.bottom_frame.pack_propagate(0)

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

        self.bottom_frame.pack(side=tk.BOTTOM, pady=(0, 20))

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
            self.central_frame, orient="vertical",
            command=self.scroll_all_text_vertical)

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
        # new_text.configure(state="disabled")
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
                move = -1 * (event.delta / 120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            for text in self.central_texts:
                text.yview_scroll(int(move), "units")

        return "break"
