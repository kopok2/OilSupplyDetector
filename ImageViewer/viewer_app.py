# coding=utf-8
"""Image viewer for dataset annotation."""

try:
    import Tkinter
except:
    import tkinter as Tkinter
from tkinter import ttk
import tkinter as tk

import os
ImageDir = ["../Source/merged/"]

# Image Extensions Allowed
Extension = ['JPG','BMP','PNG', 'jpg']
def get_list():
 Images=[]
 for ImageP in ImageDir:
  for i in os.listdir(ImageP):
   Image = os.path.join(ImageP,i)
   ext = Image.split('.')[::-1][0].upper()
   if ext in Extension:
    Images.append(Image)
 return Images
from PIL import Image, ImageTk

def tk_image(path,w,h):
 img = Image.open(path)
 storeobj = ImageTk.PhotoImage(img)
 return storeobj


# Creating Canvas Widget
class PictureWindow(Tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        Tkinter.Canvas.__init__(self, *args, **kwargs)
        self.imagelist = get_list()
        self.imagelist_p = []
        self.all_function_trigger()

    def show_image(self, path):
        img = tk_image(path, self.winfo_screenwidth(), self.winfo_screenheight())
        self.delete(self.find_withtag("bacl"))
        self.allready = self.create_image(self.winfo_screenwidth() / 2, self.winfo_screenheight() / 2, image=img,
                                          anchor='center', tag="bacl")

        self.image = img
        print
        self.find_withtag("bacl")
        self.master.title("Image Viewer ({})".format(path))
        return

    def previous_image(self):
        try:
            pop = self.imagelist_p.pop()
            self.show_image(pop)
            self.imagelist.append(pop)
        except:
            pass
        return

    def next_image(self):
        try:
            pop = self.imagelist.pop()

            self.show_image(pop)
            self.imagelist_p.append(pop)
        except EOFError as e:
            pass
        return

    def all_function_trigger(self):
        self.create_buttons()
        self.window_settings()
        return

    def window_settings(self):
        self['width'] = 5000
        self['height'] = 5000
        return

    def create_buttons(self):
        Tkinter.Button(self, text=" > ", command=self.next_image).place(x=(self.winfo_screenwidth() / 1.1),
                                                                        y=(self.winfo_screenheight() / 2))
        Tkinter.Button(self, text=" < ", command=self.previous_image).place(x=20, y=(self.winfo_screenheight() / 2))
        self['bg'] = "white"
        return


class DoubleScrollbarFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        '''
          Initialisation. The DoubleScrollbarFrame consist of :
            - an horizontal scrollbar
            - a  vertical   scrollbar
            - a canvas in which the user can place sub-elements
        '''

        ttk.Frame.__init__(self, master, **kwargs)

        # Canvas creation with double scrollbar
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.sizegrip = ttk.Sizegrip(self)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

    def pack(self, **kwargs):
        '''
          Pack the scrollbar and canvas correctly in order to recreate the same look as MFC's windows.
        '''

        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.FALSE)
        self.sizegrip.pack(in_=self.hscrollbar, side=tk.BOTTOM, anchor="se")

        self.canvas.pack(side=tk.LEFT, padx=5, pady=5,
                     fill=tk.BOTH, expand=tk.TRUE)

        ttk.Frame.pack(self, **kwargs)


    def get_frame(self):
        '''
      Return the "frame" useful to place inner controls.
    '''
        return self.canvas

class ScrolledWindow(tk.Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, canv_w = 700, canv_h = 700, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars
        self.xscrlbr = ttk.Scrollbar(self.parent, orient = 'horizontal')
        self.xscrlbr.grid(column = 0, row = 1, sticky = 'ew', columnspan = 2)
        self.yscrlbr = ttk.Scrollbar(self.parent)
        self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')
        # creating a canvas
        self.canv = tk.Canvas(self.parent)
        self.canv.config(relief = 'flat',
                         width = canv_w,
                         heigh = canv_h, bd = 2)
        # placing a canvas into frame
        self.canv.grid(column = 0, row = 0, sticky = 'nsew')
        # accociating scrollbar comands to canvas scroling
        self.xscrlbr.config(command = self.canv.xview)
        self.yscrlbr.config(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = ttk.Frame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(xscrollcommand = self.xscrlbr.set,
                         yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, 100, 100))

        self.yscrlbr.lift(self.scrollwindow)
        self.xscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width = self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height = self.scrollwindow.winfo_reqheight())
if __name__ == '__main__':
    # Top-level frame
    root = tk.Tk()
    root.minsize(width=600, height=600)
    frame = ScrolledWindow(root)

    PW = PictureWindow(frame.scrollwindow, width=5000, height=5000).pack()

#    frame.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

    # launch the GUI
    root.mainloop()