from tkinter import *
from random import randint
import collections


class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


class Puzzle: 
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        n = 5
        count = 1
        grid = []
        graph = {}

        # builds the gui
        for x in range(0, n):
            row = []
            for y in range(0,n):
                if count == n*n:
                    self.button =  Button(frame,text="0",fg="red")
                    row.append(0)
                else: 
                    max_jump = max(n-(x+1),x,n-(y+1),y)
                    random_jump = randint(1,max_jump)
                    row.append(random_jump)
                    self.button =  Button(frame,text=str(random_jump),fg="red")
                    #self.button.config(height=frame.winfo_height()/n,width=frame.winfo_width()/n)
                
                self.button.grid(row=x,column=y)
                count += 1
                
            grid.append(row)


        # initializes the graph with no edges
        for x in range(0, n):
            for y in range(0,n):
                graph[(x+1,y+1)]=[]
                
        # finds the edges of the graph and adds them to the graph
        for x in range(0, n):
            for y in range(0,n):
                # these if statements check which moves are possible
                if (x+grid[x][y] <= n-1):
                    graph[(x+1,y+1)].append((x+grid[x][y]+1,y+1))
                if (x-grid[x][y] >= 0):
                    graph[(x+1,y+1)].append((x-grid[x][y]+1,y+1))
                if (y+grid[x][y] <= n-1):
                    graph[(x+1,y+1)].append((x+1,y+grid[x][y]+1))
                if (y-grid[x][y] >= 0):
                    graph[(x+1,y+1)].append((x+1,y-grid[x][y]+1))

        # remove all edges going out from the goal cell back to itself
        graph[(n,n)]=[]
        
        print(bfs(graph,(1,1)))

def bfs(graph, root):
    visited = set()
    queue = collections.deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]: 
            if neighbor not in visited: 
                visited.add(neighbor) 
                queue.append(neighbor) 
    return visited

root = Tk()
puzzle = Puzzle(root)
root.mainloop()
