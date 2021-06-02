import tkinter as tk

class AddDiagnosticFrame:

    def __init__(self, master, num):
        self.master = master
        self.diag_num = num
        self.subframe = tk.Frame(master=self.master, relief='groove', borderwidth=2)
        self.subframe.rowconfigure(list(i for i in range(8)), minsize=1, weight=1)
        self.subframe.columnconfigure(list(i for i in range(8)), minsize=1, weight=1)
        self.subframe.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')
        self.dlist = [i+1 for i in range(num)]
        self.selected_diagnostic = tk.IntVar()
        self.selected_diagnostic.set(1)
        self.dropdown = tk.OptionMenu(self.subframe, self.selected_diagnostic, *self.dlist)
        self.dlabel = tk.Label(master=self.subframe, text='Diagnostic:')
        self.dlabel.grid(row=0, column=0, sticky='e')
        self.dropdown.grid(row=0, column=1, sticky='w')
