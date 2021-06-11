import tkinter as tk


class cameraConfig:
    def __init__(self):
        self.window = tk.Tk(className='Test')
        self.window.geometry(
            '%dx%d+%d+%d' % (int(self.window.winfo_screenwidth() * 0.25), int(self.window.winfo_screenheight() * 0.55),
                             self.window.winfo_screenwidth() / 4,
                             self.window.winfo_screenheight() / 5))
        self.window.rowconfigure([i for i in range(5)], minsize=25, weight=1)
        self.window.columnconfigure([i for i in range(5)], minsize=25, weight=1)
        self.frame = tk.Frame(self.window, width=150, height=300)
        self.frame.grid(row=0, column=0)
        self.canvas = tk.Canvas(self.frame, bg='red', width=150, height=300)
        # parse config file here
        with open('Config/flir_cam_changables.txt', 'r') as f:
            for i, j in enumerate(f):
                k = j.split(':')[0]
                NumericalParameter(self.canvas, i, 0, k)


        self.rowspan=i
        self.columnspan = 1
        self.canvas.rowconfigure([i for i in range(self.rowspan)], minsize=25, weight=1)
        self.canvas.columnconfigure([i for i in range(self.columnspan)], minsize=25, weight=1)

        scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scroll_y.grid(row=0, column=1, rowspan=5, sticky="ns")
        self.canvas.configure(yscrollcommand=scroll_y.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.grid(row=0, column=0, rowspan=self.rowspan, columnspan=self.columnspan, sticky='nsew')
        self.window.mainloop()



class NumericalParameter:
    def __init__(self, parent, x, y, text):
        self.master = parent
        self.frame = tk.Frame(master=self.master, relief='groove', bg='black')
        self.frame.rowconfigure([i for i in range(1)], minsize=10, weight=1)
        self.frame.columnconfigure([i for i in range(3)], minsize=10, weight=1)

        self.input = tk.Entry(master=self.frame)
        self.input.grid(row=1, column=1, columnspan=2, sticky='nsew')

        self.diaglabel = tk.Label(master=self.frame, text=text)
        self.diaglabel.grid(row=0, column=1, sticky='nsew')

        self.frame.grid(row=x, column=y, sticky='nsew')



if __name__ == '__main__':
    cameraConfig()