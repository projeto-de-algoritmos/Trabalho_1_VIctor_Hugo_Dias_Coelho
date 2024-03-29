from random import randint
from math import sqrt

from tkinter import (Canvas,
                     Tk,
                     Button,
                     PanedWindow,
                     filedialog,
                     Frame,
                     Label)
from no import No

WIDTH = 800
HIEGHT = 800
RAIO = 8
COMP = "Componentes: {}"
GRAU = "| NO:{} GRAU: {} "


class Program:
    def __init__(self):
        self.root = Tk()
        self.frame = Frame()
        self.frame.pack(side='top')
        self.label = Label(self.frame, text=COMP.format(0))
        self.label2 = Label(self.frame, text="")
        self.canvas = Canvas(self.root, width=WIDTH, height=HIEGHT,
                             borderwidth=0, highlightthickness=0, bg="black")
        self.painel = PanedWindow(orient='vertical')
        self.list_of_no = []
        self.list_of_vert = []
        self.graph = []
        self.x = []
        self.y = []
        self.components = 0

    def __format_string(self, string):
        string = string.split(" ")
        neighbors = [int(no) for no in string[1:]]
        return (int(string[0]), neighbors)

    def __distance_no(self, x0, y0, x1, y1):
        return sqrt(((x0 * x1) + (y0 * y1)))

    def __create_circles(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill='red')

    def load_graph(self, path):
        graph = open(path, "r")
        text = ""
        for line in graph:
            formated_input = self.__format_string(line)
            no = No(formated_input[0])
            no.neighbors = formated_input[1]
            text += GRAU.format(formated_input[0], len(formated_input[1]))
            self.graph.append(no)
            self.label2.configure(text=text)

    def create_points(self):
        r = RAIO
        for no in self.graph:
            x = randint(0, WIDTH)
            y = randint(0, HIEGHT)
            if no.id == 1:
                self.x.append(x)
                self.y.append(y)
            else:
                for point in range(len(self.x)):
                    flag = True
                    while flag:
                        dist = self.__distance_no(self.x[point],
                                                  self.y[point],
                                                  x, y)
                        if dist < r + 10.0:
                            x = randint(0, WIDTH)
                            y = randint(0, HIEGHT)
                        else:
                            flag = False
                self.x.append(x)
                self.y.append(y)

    def create_no(self):
        for i in range(len(self.x)):
            self.list_of_no.append(
                self.__create_circles(self.x[i], self.y[i], RAIO))
            self.canvas.create_text(self.x[i], self.y[i],
                                    text=str(self.graph[i].id))

    def create_line(self):
        for no in self.graph:
            x0 = self.x[no.id - 1]
            y0 = self.y[no.id - 1]
            for nei in no.neighbors:
                x1 = self.x[nei - 1]
                y1 = self.y[nei - 1]
                vert = self.canvas.create_line(x0, y0, x1, y1, fill='yellow')
                self.list_of_vert.append(vert)

    def load(self):
        filename = filedialog.askopenfilename()
        print(filename)
        self.load_graph(filename)

    def draw_graph(self):
        self.create_points()
        print(len(self.x))
        self.create_line()
        self.create_no()

    def reset_graph(self):
        for no in self.graph:
            no.visited = False

        for item in self.list_of_no:
            self.canvas.itemconfig(item, fill="red")

    def change_color(self):
        for item in self.list_of_no:
            self.canvas.itemconfig(item, fill="blue")

    def use_bfs(self):
        self.components = 0
        for no in self.graph:
            if no.visited is False:
                self.components += 1
            self.canvas.update()
            self.canvas.after(500)
            if no.visited is False:
                no.visited = True
                self.canvas.itemconfig(self.list_of_no[no.id - 1], fill="blue")
                stack = no.neighbors
                for id in stack:
                    if self.graph[id-1].visited is False:
                        self.graph[id-1].visited = True
                        self.canvas.update()
                        self.canvas.after(500)
                        self.canvas.itemconfig(self.list_of_no[id - 1],
                                               fill="blue")
                        stack.extend(self.graph[id-1].neighbors)
                    else:
                        continue
            else:
                continue
        self.label.configure(text=COMP.format(self.components))

    def create_painel(self):
        commands = ['load graph', 'draw graph', 'reset graph', 'change color',
                    'BFS']
        callbacks = [self.load, self.draw_graph, self.reset_graph,
                     self.change_color, self.use_bfs]
        for button in range(len(commands)):
            self.painel.add(Button(self.painel, text=commands[button],
                                   command=callbacks[button]))

    def main(self):
        self.canvas.pack(side='right')
        self.painel.pack(side='left')
        self.label2.pack(side='top')
        self.label.pack(side='top')
        self.create_painel()
        self.root.mainloop()


if __name__ == "__main__":
    program = Program()
    program.main()
