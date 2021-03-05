from Gui.model_tab import ModelTab
import tkinter as tk


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

        temp_central = {
            "": 80
        }
        self.set_central_frame(temp_central)
