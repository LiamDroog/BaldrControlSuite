import tkinter as tk
import PIL.Image, PIL.ImageTk
import keyboard
class ImageHistory:
    def __init__(self):
        self.window = tk.Tk(className='\Image History')

        frame = tk.Frame(self.window)  # relief=SUNKEN)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=tk.E + tk.W)

        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

        canvas = tk.Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        imageFrame(canvas, 0, 0)

        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

        frame.pack()
        self.window.mainloop()

class imageFrame:
    def __init__(self, master, x, y):
        File = "C:/Users/Liam/PycharmProjects/BaldrControlHub py3.8/Images/Shot-19129388-2.bmp"
        img = PIL.ImageTk.PhotoImage(PIL.Image.open(File))
        master.create_image(x, y, image=img, anchor="nw")

if __name__ == '__main__':
    ImageHistory()
