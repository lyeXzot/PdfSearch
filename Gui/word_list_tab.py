import model_tab
from model_tab import ModelTab
import tkinter as tk

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
