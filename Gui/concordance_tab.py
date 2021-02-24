import tkinter as tk

from Gui.model_tab import ModelTab


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
