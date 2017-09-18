from tkinter import *
from random import randint
import collections


n = 5


class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


class Puzzle: 
    def __init__(self, master):
        frame1 = Frame(master)
        frame1.pack()
     
        count = 1
        grid = []
        graph = {}

        # builds the gui
        for x in range(0, n):
            row = []
            for y in range(0,n):
                if count == n*n:
                    self.button =  Button(frame1,text="0",fg="red")
                    row.append(0)
                else: 
                    max_jump = max(n-(x+1),x,n-(y+1),y)
                    random_jump = randint(1,max_jump)
                    row.append(random_jump)
                    self.button =  Button(frame1,text=str(random_jump),fg="red")
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

##        visited = bfs(graph,(1,1))
##        
##        if (n,n) not in visited:
##            print("This puzzle cannot be solved")


        x_count = 0
        solvable = False
        for x in range(1, n+1):
            for y in range(1,n+1):
                shortest_path=len(bfs(graph,(1,1),(x,y))) - 1 
                if x == n and y == n and not shortest_path == -1 :
                    print("The function value is: " + str(shortest_path))                    
                    solvable = True
                if shortest_path == -1:
                    x_count += 1
                    self.button =  Button(frame1,text="X",fg="blue")
                else:
                    self.button =  Button(frame1,text=str(shortest_path),fg="blue")
                
                self.button.grid(row=x-1+n,column=y-1)
                

        if not solvable:
            x_count = x_count * -1
            print("The function value is: " + str(x_count))
##def bfs(graph, root):
##    visited = set()
##    queue = collections.deque([root])
##    while queue:
##        vertex = queue.popleft()
##        print(vertex)
##        print(graph[vertex])
##        for neighbor in graph[vertex]:
##            print(neighbor)
##            if neighbor not in visited: 
##                visited.add(neighbor) 
##                queue.append(neighbor) 
##    return visited

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    count = 0
    while queue:
        if count > n*n:
            return []
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)
        count += 1

root = Tk()
puzzle = Puzzle(root)
root.mainloop()