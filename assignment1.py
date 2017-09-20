from tkinter import *
from random import randint
import collections


class Puzzle:
    grid = []
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()


        #grid = read_puzzle()
        #n = len(grid)
        self.generate_button = Button(frame,text="Generate Random Puzzle",fg="red", command=lambda: self.generate_puzzle(frame))
        self.read_button = Button(frame,text="Get Puzzle From File",fg="red", command=lambda: self.read_puzzle(frame))
        self.generate_button.grid(row=0,columnspan=10)
        self.read_button.grid(row=1,columnspan=10)
        #self.enter_n(frame)

    def enter_n(self,frame):
        self.e = Entry(frame,text="Enter puzzle size")
        self.e.grid(row=3,columnspan=n)

    def read_puzzle(self,frame):
        with open("C:/Users/Kyle/Documents/AI/asst1/test.txt") as f:
            lines = f.readlines()
            lines = [[int(i) for i in line.split()] for line in lines]
        self.grid = lines
        self.build_gui(frame)


    def generate_puzzle(self,frame):
        n = 7
        for x in range(0, n):
            row = []
            for y in range(0,n):
                max_jump = max(n-(x+1),x,n-(y+1),y)
                random_jump = randint(1,max_jump)
                row.append(random_jump)        
            self.grid.append(row)
        self.grid[n-1][n-1]=0
        self.build_gui(frame)

    def build_graph(self):
        n = len(self.grid)
        graph = {}
        # initializes the graph with no edges
        for x in range(0, n):
            for y in range(0,n):
                graph[(x+1,y+1)]=[]
                
        # finds the edges of the graph and adds them to the graph
        for x in range(0, n):
            for y in range(0,n):
                # these if statements check which moves are possible
                cell=self.grid[x][y]
                if (x+cell <= n-1):
                    graph[(x+1,y+1)].append((x+cell+1,y+1))
                if (x-cell >= 0):
                    graph[(x+1,y+1)].append((x-cell+1,y+1))
                if (y+cell <= n-1):
                    graph[(x+1,y+1)].append((x+1,y+cell+1))
                if (y-cell >= 0):
                    graph[(x+1,y+1)].append((x+1,y-cell+1))

        # remove all edges going out from the goal cell back to itself
        graph[(n,n)]=[]
        return graph

    def build_gui(self,frame):
        n = len(self.grid)
        for x in range(0, n):
            for y in range(0,n):
                self.button =  Button(frame,text=str(self.grid[x][y]),fg="red")
                self.button.config(width=2)
                self.button.grid(row=x+2,column=y)
                
        graph = self.build_graph()
        
        x_count = 0
        # create the gui showing the shortest distance to each cell
        for x in range(1, n+1):
            for y in range(1,n+1):
                shortest_path=len(bfs(graph,(1,1),(x,y),n)) - 1
                if shortest_path == -1:
                    x_count += 1
                    self.button =  Button(frame,text="X",fg="blue")
                else:
                    self.button =  Button(frame,text=str(shortest_path),fg="blue")

                self.button.config(width=2)
                self.button.grid(row=x+1+n,column=y-1)
                

        if shortest_path == -1:
            x_count = x_count * -1
            label_str = "Function value: " + str(x_count)
            self.label = Label(frame, text=label_str, fg="black")
        else:
            label_str = "Function value: " + str(shortest_path)
            self.label = Label(frame, text=label_str, fg="black")

        self.label.grid(row=2*n+2, columnspan=n)

        self.climb_button = Button(frame,text="Climb Hill",fg="Purple", command=lambda: self.climb_hill(frame))
        self.climb_button.grid(row=2*n+3, columnspan=n)

    # task 3 stuff
    def climb_hill(self,frame):
        n = len(self.grid)
        
        x,y = randint(1,n),randint(1,n)
        
        while x == n and y == n:
            x,y = randint(1,n),randint(1,n)
        
        print(x,y)
        
        old_jump = self.grid[x-1][y-1]
        max_jump = max(n-x,x-1,n-y,y-1)
        new_jump = randint(1,max_jump)
        while new_jump == old_jump:
            new_jump = randint(1,max_jump)

        self.grid[x-1][y-1] = new_jump
        self.build_gui(frame)
        


def bfs(graph, start, goal, n):
    queue = []
    queue.append([start])
    count = 0
    while queue:
        if count > n*n*n*n:
            return []
        path = queue.pop(0)
        node = path[-1]
        if node == goal:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)
        count += 1


root = Tk()
puzzle = Puzzle(root)
root.mainloop()
