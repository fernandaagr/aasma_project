import tkinter as tk

class deliveryWorld(tk.Frame):
    def __init__(self, master, rows=11, columns=11, size=40):
        super(deliveryWorld, self).__init__(master)
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = 'gray80'
        self.outline = 'gray85'

        width = columns * size
        height = rows * size
        self.canvas = tk.Canvas(self, bg='#aaaaff', borderwidth=0, highlightthickness=0,
                                width=width, height=height)
        #create cells - MUDAR ISSO
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size

                if (col == 0 or col == self.columns - 1 or row == 0 or row == self.rows - 1):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray5", fill="gray10", tags="wall")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.outline, fill=self.color, tags="cell")

                if (row == 3 and col == 2) or (row == 3 and col == 3) or (row == 4 and col == 2) or (row == 4 and col == 3)\
                        or (row == 7 and col == 2) or (row == 7 and col == 3)  or (row == 3 and col == 6) or \
                        (row == 3 and col == 7) or (row == 7 and col == 7) or (row == 7 and col == 8) or\
                        (row == 8 and col == 7) or (row == 8 and col == 8):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray55", fill="gray50", tags="building")


                #if (row == 1 and col == 5):
                #    item = self.canvas.yview()
                #    label = tk.Label(text=f"()")
                #    label.pack()

        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=15)
        self.pack()

        ra = reactiveAgent(self.canvas, 1.0, 1.0)
        ra.run()
        for i in range(7):
            ra.move(0.0, 0.0)
        label = tk.Label(text=f"({self.canvas.yview()})")
        label.pack()


class worldObject(object):
    #the item can be a robot, obstacle or delivery
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class reactiveAgent(worldObject):
    def __init__(self, canvas, x, y):
        self.radius = 15
        self.direction = [1, -1]
        x = 60
        y = 60
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='skyblue3')
        super(reactiveAgent, self).__init__(canvas, item)
    def run(self):
        coords = self.get_position()
        #label = tk.Label(text=f"({coords})")
        #label.pack()
        #if ()
    def move(self, x, y):
        coords = self.get_position()
        super(reactiveAgent, self).move(x+40, 0)

    def rotate(self):
        return 0
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('610x610')
    root.resizable(width=False, height=False)
    root.title('Delivery World')

    label = tk.Label(text="Delivery World", pady=15, font="none 20 bold")
    label.pack()

    btsFrame = tk.Frame(root)
    btsFrame.pack(fill="both", side="top")

    btReset = tk.Button(btsFrame, text='Reset')
    btRun = tk.Button(btsFrame, text='Run')

    btReset.grid(row=0, column=0, sticky="NSEW")
    btRun.grid(row=0, column=1, sticky="NSEW")

    #btsFrame.grid_rowconfigure(0, weight=1)
    #btsFrame.grid_rowconfigure(3, weight=1)
    #btsFrame.grid_columnconfigure(0, weight=1)
    #btsFrame.grid_columnconfigure(3, weight=1)

    world = deliveryWorld(root)
    world.mainloop()