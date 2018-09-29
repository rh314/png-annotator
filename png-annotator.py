from tkinter import Tk, Canvas, mainloop, YES, BOTH
from tkinter import filedialog
from PIL import Image, ImageTk
from os.path import expanduser
from math import floor, ceil


def dialog_open_file():
    fname = filedialog.askopenfilename(
        initialdir=expanduser('~/delasb/neuralnets'),
        title="Select file",
        filetypes=(("png files", "*.png"), ("all files", "*.*")))
    return fname


class SubImage():
    def __init__(self, img0, transform):
        self.img0 = img0
        self.transform = transform
        self.update_sub_img()

    def update_sub_img(self):
        x0A, y0A, x1A, y1A = self.transform.xysA
        dxB = self.transform.xysB[2] - self.transform.xysB[0]
        dyB = self.transform.xysB[3] - self.transform.xysB[1]
        self.img = self.img0.crop((
            floor(x0A), floor(y0A),
            ceil(x1A), ceil(y1A)
        ))
        self.img = self.img.resize((
            ceil(dxB),
            ceil(dyB),
        ))


class Rectangle():
    def __init__(self, canvas, transform, coords):
        # PS: Coords are image relative, not canvas relative
        self.transform = transform
        self.canvas = canvas
        self.x0A, self.y0A = coords[:2]
        self.x1A, self.y1A = coords[2:]
        x0B, y0B, x1B, y1B = self.canvas_coords()
        self.id2 = canvas.create_rectangle((x0B, y0B, x1B, y1B))

    def canvas_coords(self):
        transform = self.transform
        x0B, y0B = transform.a2b([self.x0A, self.y0A])
        x1B, y1B = transform.a2b([self.x1A, self.y1A])
        return (int(x0B), int(y0B), int(x1B), int(y1B))

    def updated_coords(self):
        x0B, y0B, x1B, y1B = self.canvas_coords()
        self.canvas.coords(
            self.id2,
            (x0B, y0B, x1B, y1B))

    def change_x1y1(self, x1y1A):
        self.x1A, self.y1A = x1y1A
        self.updated_coords()

    def delete(self):
        self.canvas.delete(self.id2)


class Transform():
    def __init__(self, xysA, xysB):
        self.xysA = list(xysA)
        self.xysB = list(xysB)

    def a2b(self, xyA):
        xA, yA = xyA
        xB = ((xA - self.xysA[0]) / (
            self.xysA[2] - self.xysA[0]) * (self.xysB[2] - self.xysB[0]) +
            self.xysB[0])
        yB = ((yA - self.xysA[1]) / (
            self.xysA[3] - self.xysA[1]) * (self.xysB[3] - self.xysB[1]) +
            self.xysB[1])
        return [xB, yB]

    def b2a(self, xyB):
        xB, yB = xyB
        xA = ((xB - self.xysB[0]) / (
            self.xysB[2] - self.xysB[0]) * (self.xysA[2] - self.xysA[0]) +
            self.xysA[0])
        yA = ((yB - self.xysB[1]) / (
            self.xysB[3] - self.xysB[1]) * (self.xysA[3] - self.xysA[1]) +
            self.xysA[1])
        return [xA, yA]

    def zoom(self, mult):
        # zoom in by multiplier
        xysA = self.xysA
        xysA[:] = [
            xysA[0], xysA[1],
            xysA[0] + (xysA[2] - xysA[0]) / mult,
            xysA[1] + (xysA[3] - xysA[1]) / mult]

    def moveB(self, dxB, dyB):
        xysA = self.xysA
        xysB = self.xysB
        dxA = dxB / (xysB[2] - xysB[0]) * (xysA[2] - xysA[0])
        dyA = dyB / (xysB[3] - xysB[1]) * (xysA[3] - xysA[1])
        xysA[:] = [
            xysA[0] + dxA, xysA[1] + dyA,
            xysA[2] + dxA, xysA[3] + dyA,
        ]


def main():
    # fname = dialog_open_file()
    fname = '/home/rh/delasb/neuralnets/paper1-01.png'
    pil_img0 = Image.open(fname)
    canvas_width = 600
    canvas_height = 400
    # transform: from image pixel position to canvas position
    transform = Transform(
        (0, 0, canvas_width, canvas_height),
        (0, 0, canvas_width, canvas_height)
    )
    pil_sub_img = SubImage(pil_img0, transform)
    root = Tk()
    root.title("PNG annotator")
    tk_img = [None]
    rectangles = []

    canvas = Canvas(
        root,
        width=canvas_width,
        height=canvas_height)
    canvas.pack(fill=BOTH, expand=YES)

    # Lesson learnt: can start with None as image
    img_id = canvas.create_image((0, 0), image=None, anchor='nw')

    def change_image(pil_img):
        tk_img[0] = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(img_id, image=tk_img[0])

    change_image(pil_sub_img.img)

    def update_canvas():
        print(transform.xysA, transform.xysB)
        pil_sub_img.update_sub_img()
        change_image(pil_sub_img.img)
        for rectangle in rectangles:
            rectangle.updated_coords()

    special_keys = (
        'Up', 'Left', 'Down', 'Right', 'Caps_Lock', 'Escape', 'Super_L',
        'Menu',
        'Shift_R', 'Shift_R', 'Alt_R', 'Control_R',
        'Shift_L', 'Shift_L', 'Alt_L', 'Control_L')

    def keyboard(event):
        key = event.char
        keysym = event.keysym
        # event2[0] = event
        if keysym not in special_keys:
            if key in '-' and event.state == 0:
                transform.zoom(0.5)
                update_canvas()
                print('zoom out', event)
            elif key in '+=' and event.state in (0, 1):
                transform.zoom(2)
                update_canvas()
                print('zoom in', event.state)
            elif key == '0':
                transform.xysA[2] = (
                    transform.xysA[0] + transform.xysB[2] - transform.xysB[0])
                transform.xysA[3] = (
                    transform.xysA[1] + transform.xysB[3] - transform.xysB[1])
                update_canvas()
                print('reset zoom')
            elif key == 'z' and len(rectangles) > 0:
                rectangles[-1].delete()
                rectangles.pop()
            elif key == 's':
                for r in rectangles:
                    print(r.x0A, r.y0A, r.x1A, r.y1A)
            elif key == 'p':
                import pdb
                pdb.set_trace()
        else:
            delta = 10
            if event.state == 1:
                delta = 50
            if keysym == 'Up':
                transform.moveB(0, -delta)
                update_canvas()
            elif keysym == 'Right':
                transform.moveB(delta, 0)
                update_canvas()
            elif keysym == 'Down':
                transform.moveB(0, delta)
                update_canvas()
            elif keysym == 'Left':
                transform.moveB(-delta, 0)
                update_canvas()
            elif keysym == 'Escape':
                root.after(0, lambda: root.destroy())
        # print(repr(event), canvas.coords(img_id))

    root.bind("<Key>", keyboard)

    last_mouse_evtype = [None]
    last_mouse_down = [None, None]

    def mouse_down(event):
        last_mouse_down[:] = transform.b2a([event.x, event.y])
        last_mouse_evtype[0] = 'down'

    canvas.bind('<Button-1>', mouse_down)

    def mouse_up(event):
        # pos = [event.x, event.y]
        last_mouse_evtype[0] = 'up'

    canvas.bind('<ButtonRelease-1>', mouse_up)

    last_mouse_mouse_hold_move = [None, None]

    def mouse_hold_move(event):
        pos = transform.b2a([event.x, event.y])
        last_mouse_mouse_hold_move[:] = pos
        if last_mouse_evtype[0] == 'down':
            rectangles.append(
                Rectangle(canvas, transform, last_mouse_down + pos)
            )
        elif last_mouse_evtype[0] == 'hold_move':
            rectangles[-1].change_x1y1(pos)
        last_mouse_evtype[0] = 'hold_move'

    canvas.bind('<B1-Motion>', mouse_hold_move)

    def mouse_move(event):
        last_mouse_evtype[0] = 'move'

    canvas.bind('<Motion>', mouse_move)

    mainloop()


main()
