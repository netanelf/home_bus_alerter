from tkinter import *


class BusGui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


if __name__ == '__main__':
    root = Tk()
    app = BusGui(root)
    root.mainloop()