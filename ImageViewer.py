import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk


class ImageFrame:
    def __init__(self, text, image):
        self.window = tk.Toplevel()
        self.window.title('Spectra View-o-matic 9000')
        self.screenwidth = str(int(self.window.winfo_screenwidth() * 0.3))
        self.screenheight = str(int(self.window.winfo_screenheight() * 0.3))
        self.window.geometry(self.screenwidth + 'x' + self.screenheight)
        self.grid = [16, 9]
        self.rowarr = list(i for i in range(self.grid[1]))
        self.colarr = list(i for i in range(self.grid[0]))
        self.window.rowconfigure(self.rowarr, minsize=25, weight=1)
        self.window.columnconfigure(self.colarr, minsize=25, weight=1)
        self.imageList = []
        self.imageList.append(image)
        self.currentimage = 0

        self.factor = 0.35
        self.canvas = tk.Canvas(self.window, height=300, width=400)
        self.canvas.grid(row=1, column=6, rowspan=8, columnspan=16, sticky='nswe')
        im = Image.fromarray(self.imageList[0])
        self.canvas.image = ImageTk.PhotoImage(
            im.resize((int(self.factor * im.size[0]), int(self.factor * im.size[1]))))
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        self.attributes_frame = tk.Frame(master=self.window, relief='raised', borderwidth=3)
        self.attributes_frame.grid(row=1, column=0, columnspan=6, rowspan=7, sticky='nsew')
        self.atext = tk.Label(master=self.attributes_frame, text='Image')
        self.atext.pack()

        self.nextbutton = tk.Button(master=self.window, text='>>', command=lambda: self.__changeimg('fwd'))
        self.nextbutton.grid(row=8, column=4, columnspan=2, sticky='nsew')

        self.prevbutton = tk.Button(master=self.window, text='<<', command=lambda: self.__changeimg('bck'))
        self.prevbutton.grid(row=8, column=0, columnspan=2, sticky='nsew')


        #self.window.mainloop()

    def changepos(self):
        pass

    def getsize(self):
        return len(self.imageList)

    def addImage(self, image):
        self.imageList.append(image)

    def __showImage(self, image):
        self.img = Image.fromarray(image)
        print(self.img.size[0])
        self.img2 = ImageTk.PhotoImage(self.img.resize((int(self.factor * self.img.size[0]),
                                                   int(self.factor * self.img.size[1]))))
        self.canvas.image = self.img2
        print(self.img2)
        #self.canvas.image = self.canvas.create_image(0, 0, image=self.img2, anchor='nw')
        #.image_on_canvas = self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self.canvas.itemconfig(self.image_on_canvas, image=self.img2)

    def __changeimg(self, dir):
        if dir == 'fwd':
            if self.currentimage < len(self.imageList)-1:
                self.currentimage += 1
                self.__showImage(self.imageList[self.currentimage])

        elif dir == 'bck':
            if self.currentimage > 0:
                self.currentimage -= 1
                self.__showImage(self.imageList[self.currentimage])
        print(self.currentimage)