from tkinter import Tk, Canvas, mainloop, YES, BOTH
from tkinter import filedialog
# from tkinter import N, W, E, S
# from random import randint
from PIL import Image, ImageTk
# import numpy as np
from os.path import expanduser
from math import ceil


def dialog_open_file():
    fname = filedialog.askopenfilename(
        initialdir=expanduser('~/delasb/neuralnets'),
        title="Select file",
        filetypes=(("png files", "*.png"), ("all files", "*.*")))
    return fname


class SubImage():
    def __init__(self, img0, offx, offy, dx, dy, scale):
        self.img0 = img0
        self.offx = offx
        self.offy = offy
        self.dx = dx
        self.dy = dy
        self.scale = scale
        self.update_sub_img()

    def update_sub_img(self):
        self.img = self.img0.crop(
            (self.offx, self.offy, self.offx + self.dx, self.offy + self.dy))
        self.img = self.img.resize((
            ceil(self.img.width * self.scale),
            ceil(self.img.height * self.scale),
        ))


def main():
    # fname = dialog_open_file()
    fname = '/home/rh/delasb/neuralnets/paper1-01.png'
    pil_img0 = Image.open(fname)
    canvas_width = 600
    canvas_height = 400
    pil_sub_img = SubImage(pil_img0, 0, 0, canvas_width, canvas_height, 1.0)
    # import pdb;pdb.set_trace()
    # pil_img = pil_img.crop((0, 0, 500, 300))
    root = Tk()
    root.title("PNG annotator")
    tk_img = [None]

    canvas = Canvas(
        root,
        width=canvas_width,
        height=canvas_height)
    canvas.pack(fill=BOTH, expand=YES)

    # Lesson learnt: can start with None as image
    img_id = canvas.create_image((0, 0), image=None, anchor='nw')
    img_id  # noqa

    def change_image(pil_img):
        tk_img[0] = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(img_id, image=tk_img[0])

    def move_image(dx, dy):
        pil_sub_img.offx += dx
        pil_sub_img.offy += dy
        pil_sub_img.update_sub_img()
        change_image(pil_sub_img.img)

    change_image(pil_sub_img.img)

    def print_size():
        print(canvas.winfo_width(), canvas.winfo_height())
        root.after(1000, print_size)

    # exc_info = [0]
    # event2 = [None]

    special_keys = (
        'Up', 'Left', 'Down', 'Right',
        'Shift_R', 'Shift_R', 'Alt_R', 'Control_R',
        'Shift_L', 'Shift_L', 'Alt_L', 'Control_L')

    def keyboard(event):
        key = event.char
        keysym = event.keysym
        # event2[0] = event
        if keysym not in special_keys:
            if key in '-':
                #change_image(pil_img.resize((width0 // 2, height0 // 2)))
                print('zoom out')
            elif key in '+=':
                offx, offy = canvas.coords(img_id)
                #change_image(pil_img.resize((width0 * 2, height0 * 2)))
                print('zoom in')
            elif key in '0':
                #change_image(pil_img.resize((width0, height0)))
                print('reset zoom')
        else:
            delta = 10
            if event.state == 1:
                delta = 50
            if keysym == 'Up':
                move_image(0, -delta)
            elif keysym == 'Right':
                move_image(delta, 0)
            elif keysym == 'Down':
                move_image(0, delta)
            elif keysym == 'Left':
                move_image(-delta, 0)
        print(repr(event), canvas.coords(img_id))

    root.bind("<Key>", keyboard)
    # print_size()  # yes it runs.

    mainloop()
    # import pdb; pdb.set_trace()
    # import pdb; pdb.post_mortem(exc_info[0])
    # event2


main()
