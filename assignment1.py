from tkinter import *
from random import randint
import collections


class Puzzle:
    grid = []
    bfs_grid = []
    graph = {}
    puzzle_values = []

    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.generate_button = Button(frame,text="Generate Random Puzzle",fg="red", command=lambda: self.generate_puzzle(frame))
        self.read_button = Button(frame,text="Get Puzzle From File",fg="red", command=lambda: self.read_puzzle(frame))
        self.generate_button.grid(row=0,columnspan=10)
        self.read_button.grid(row=1,columnspan=10)


    def read_puzzle(self,frame):
        with open("C:/Users/Kyle/Documents/AI/asst1/test.txt") as f:
            lines = f.readlines()
            lines = [[int(i) for i in line.split()] for line in lines]
        self.grid = lines
        self.build_graph()
        self.bfs_the_whole_thing()
        self.build_gui(frame)


    def generate_puzzle(self,frame):
        n = int(input("Enter the size of the puzzle: "))
        for x in range(0, n):
            row = []
            for y in range(0,n):
                max_jump = max(n-(x+1),x,n-(y+1),y)
                random_jump = randint(1,max_jump)
                row.append(random_jump)        
            self.grid.append(row)
        self.grid[n-1][n-1]=0
        self.build_graph()
        self.bfs_the_whole_thing()
        self.build_gui(frame)


    def build_graph(self):
        n = len(self.grid)
        self.graph={}
        # initializes the graph with no edgesself.bfs_the_whole_thing()
        for x in range(0, n):
            for y in range(0,n):
                self.graph[(x+1,y+1)]=[]
                
        # finds the edges of the graph and adds them to the graph
        for x in range(0, n):
            for y in range(0,n):
                # these if statements check which moves are possible
                cell=self.grid[x][y]
                if (x+cell <= n-1):
                    self.graph[(x+1,y+1)].append((x+cell+1,y+1))
                if (x-cell >= 0):
                    self.graph[(x+1,y+1)].append((x-cell+1,y+1))
                if (y+cell <= n-1):
                    self.graph[(x+1,y+1)].append((x+1,y+cell+1))
                if (y-cell >= 0):
                    self.graph[(x+1,y+1)].append((x+1,y-cell+1))

        # remove all edges going out from the goal cell back to itself
        self.graph[(n,n)]=[]


    def bfs_the_whole_thing(self):
        self.bfs_grid = []
        n = len(self.grid)
        for x in range(1, n+1):
            row = []
            for y in range(1,n+1):
                row.append(len(bfs(self.graph,(1,1),(x,y),n)) - 1)
            self.bfs_grid.append(row)

    
    def build_gui(self,frame):
        n = len(self.grid)
        # create the gui of the puzzle
        for x in range(0, n):
            for y in range(0,n):
                self.button =  Button(frame,text=str(self.grid[x][y]),fg="red")
                self.button.config(width=2)
                self.button.grid(row=x+2,column=y)
        
        x_count = 0
        # create the gui showing the shortest distance to each cell
        for x in range(0, n):
            for y in range(0,n):
                shortest_path=self.bfs_grid[x][y]
                if shortest_path == -1:
                    x_count += 1
                    self.button =  Button(frame,text="X",fg="blue")
                else:
                    self.button =  Button(frame,text=str(shortest_path),fg="blue")
                self.button.config(width=2)
                self.button.grid(row=x+2+n,column=y)
                
        if shortest_path == -1:
            function_value = x_count * -1
        else:
            function_value = shortest_path

        # show the function value in the gui
        label_str = "Function value: " + str(function_value)
        self.label = Label(frame, text=label_str, fg="black")
        self.label.grid(row=2*n+2, columnspan=n)

        # button to perform task 3
        self.climb_button = Button(frame,text="Climb Hill",fg="Purple", command=lambda: self.climb_hill(frame,int(input("Enter how many iterations you would like to climb: "))))
        self.climb_button.grid(row=2*n+3, columnspan=n)


    # task 3
    def climb_hill(self,frame,iterations):
        n = len(self.grid)
        
        x,y = randint(1,n),randint(1,n)
        
        while x == n and y == n:
            x,y = randint(1,n),randint(1,n)
        
        old_jump = self.grid[x-1][y-1]
        max_jump = max(n-x,x-1,n-y,y-1)
        new_jump = randint(1,max_jump)
        while new_jump == old_jump:
            new_jump = randint(1,max_jump)

        old_grid = self.grid
        self.grid[x-1][y-1] = new_jump
        
        old_graph = self.graph
        self.build_graph()

        old_bfs_grid = self.bfs_grid
        self.bfs_the_whole_thing()    
        
        if self.bfs_grid[n-1][n-1] < old_bfs_grid[n-1][n-1]:
            self.grid = old_grid
            self.graph = old_graph
            self.bfs_grid = old_bfs_grid
        else:
            self.puzzle_values.append(self.bfs_grid[n-1][n-1])

        if iterations > 0:
            self.climb_hill(frame,iterations-1)
        else:
            self.build_gui(frame)
            print(self.puzzle_values)
        
        

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
