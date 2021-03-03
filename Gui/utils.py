import tkinter as tk


class CentralWindow(tk.Toplevel):
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



