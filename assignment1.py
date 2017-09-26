from tkinter import filedialog
from tkinter import *
from random import *
import time
import math

class Puzzle:
    grid = []
    bfs_grid = []
    best_value = 0
    best_grid = []
    graph = {}
    start_time = 0
    puzzle_values = []
    p = 0
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.generate_button = Button(frame, text = "Generate Random Puzzle", fg = "red",
                                      command = lambda: self.generate_puzzle(frame, int(
                                          input("Enter the size of the puzzle: "))))
        self.read_button = Button(frame, text = "Get Puzzle From File", fg="red", command = lambda: self.read_puzzle(frame))
        self.generate_button.grid(row = 0, columnspan = 10)
        self.read_button.grid(row = 1, columnspan = 10)


    def read_puzzle(self, frame):
        self.grid = []
        path = filedialog.askopenfilename()
        with open(path) as f:
            f.readline() # skip the line the gives the puzzle size
            lines = f.readlines()
            lines = [[int(i) for i in line.split()] for line in lines]
        self.grid = lines
        self.build_graph()
        self.bfs_the_whole_thing()
        self.build_gui(frame)


    def generate_puzzle(self, frame, n):
        self.grid = []
        for x in range(0, n):
            row = []
            for y in range(0, n):
                max_jump = max(n - (x + 1), x, n - (y + 1), y)
                random_jump = randint(1, max_jump)
                row.append(random_jump)        
            self.grid.append(row)
        self.grid[n - 1][n - 1] = 0
        self.build_graph()
        self.bfs_the_whole_thing()
        if self.start_time == 0:
            self.build_gui(frame)


    def build_graph(self):
        n = len(self.grid)
        self.graph = {}
        # initializes the graph with no edgesself.bfs_the_whole_thing()
        for x in range(0, n):
            for y in range(0, n):
                self.graph[(x + 1,y + 1)] = []
                
        # finds the edges of the graph and adds them to the graph
        for x in range(0, n):
            for y in range(0, n):
                # these if statements check which moves are possible
                cell = self.grid[x][y]
                if (x + cell <= n - 1):
                    self.graph[(x + 1, y + 1)].append((x + cell + 1, y + 1))
                if (x - cell >= 0):
                    self.graph[(x + 1, y + 1)].append((x - cell + 1, y + 1))
                if (y + cell <= n - 1):
                    self.graph[(x + 1, y + 1)].append((x + 1, y + cell + 1))
                if (y - cell >= 0):
                    self.graph[(x + 1, y + 1)].append((x + 1, y - cell + 1))

        # remove all edges going out from the goal cell back to itself
        self.graph[(n, n)] = []

    def bfs_the_whole_thing(self):
        self.bfs_grid = []
        n = len(self.grid)
        for x in range(1, n + 1):
            row = []
            for y in range(1, n + 1):
                row.append(bfs(self.graph,(1, 1),(x, y)))
            self.bfs_grid.append(row)

    
    def build_gui(self, frame):
        n = len(self.grid)
        # create the gui of the puzzle
        for x in range(0, n):
            for y in range(0, n):
                self.button =  Button(frame, text = str(self.grid[x][y]), fg = "red")
                self.button.config(width = 2)
                self.button.grid(row=x + 2, column = y)
        
        x_count = 0
        # create the gui showing the shortest distance to each cell
        for x in range(0, n):
            for y in range(0, n):
                shortest_path=self.bfs_grid[x][y]
                if shortest_path == -1:
                    x_count += 1
                    self.button =  Button(frame, text = "X", fg = "blue")
                else:
                    self.button =  Button(frame, text = str(shortest_path), fg = "blue")
                self.button.config(width = 2)
                self.button.grid(row = x + 2 + n, column = y)
                
        if shortest_path == -1:
            function_value = x_count * -1
        else:
            function_value = shortest_path

        # show the function value in the gui
        label_str = "Function value: " + str(function_value)
        self.label = Label(frame, text = label_str, fg = "black")
        self.label.grid(row = 2 * n + 2, columnspan = n)

        # button to perform task 3
        self.climb_button = Button(frame, text = "Task 3", fg = "Purple",
                                   command = lambda: self.task3(frame, int(input("Enter how many iterations to climb: "))))
        self.climb_button.grid(row = 2 * n + 3, columnspan = n)

        # button to perform task 4
        self.task4_button = Button(frame, text = "Task 4", fg = "Green",
                                   command = lambda: self.task4(frame, int(input("Enter how many iterations to climb per restart: ")),
                                                              int(input("Enter the number of random restarts: "))))
        self.task4_button.grid(row = 2 * n + 4, columnspan = n)

        # button to perform task 5
        self.task5_button = Button(frame, text = "Task 5", fg = "Brown",
                                   command = lambda: self.task5(frame, int(input("Enter how many iterations to climb: ")),
                                                              float(input(
                                                                  "Enter the probability of accepting a downhill move: "))))
        self.task5_button.grid(row = 2 * n + 5, columnspan = n)

        # button to perform task 6
        self.task6_button = Button(frame, text = "Task 6", fg = "Brown",
                                   command = lambda: self.task6(frame,
                                                              int(input("Enter how many iterations: ")),
                                                              float(input("Enter the initial temperature: ")),
                                                              float(input("Enter decay rate: "))))
        self.task6_button.grid(row = 2 * n + 6, columnspan = n)

        # button to perform task 7
        self.task7_button = Button(frame, text = "Task 7", fg = "Brown",
                                   command = lambda: self.task7(frame,
                                                              int(input("Enter the size of the population: ")),
                                                                int(input("Enter the number of generations: ")),
                                                                float(input("Enter the probaility of mutation: "))))
        self.task7_button.grid(row = 2 * n + 7, columnspan = n)


    # task 3 and task 4
    def climb_hill(self, frame, iterations):

        n = len(self.grid)

        for i in range(0, iterations):
            x, y = randint(1, n), randint(1, n)
            
            while x == n and y == n:
                x, y = randint(1, n), randint(1, n)
            
            old_jump = self.grid[x - 1][y - 1]
            max_jump = max(n - x, x - 1, n - y, y - 1)
            new_jump = randint(1, max_jump)
            while new_jump == old_jump:
                new_jump = randint(1, max_jump)

            old_grid = self.grid
            self.grid[x - 1][y - 1] = new_jump
            
            old_graph = self.graph
            self.build_graph()

            old_bfs_grid = self.bfs_grid
            self.bfs_the_whole_thing()

            
            if self.bfs_grid[n - 1][n - 1] < old_bfs_grid[n - 1][n - 1] and random() > self.p:
                self.grid = old_grid
                self.graph = old_graph
                self.bfs_grid = old_bfs_grid
            else:
                self.puzzle_values.append(self.bfs_grid[n - 1][n - 1])
                if self.bfs_grid[n - 1][n - 1] > self.best_value:
                    self.best_value = self.bfs_grid[n - 1][n - 1]
                    self.best_grid = self.grid
                    print(self.best_value)
                

    def task3(self, frame, iterations):
        
        self.start_time = time.time()

        self.climb_hill(frame, iterations)
        

        total_time = time.time() - self.start_time
        print("Run time: " + str(total_time) + " seconds!")

        self.build_gui(frame)
        
        self.start_time = 0


    # task 4 stuff
    def task4(self, frame, iterations, restarts):
        
        restart_values = []
        grids = []
        bfs_grids = []
        
        self.start_time = time.time()
        
        for i in range(0, restarts + 1):
            self.puzzle_values = []
            if (restarts > 0):
                self.generate_puzzle(frame, len(self.grid))
            self.climb_hill(frame, iterations)
            grids.append(self.grid)
            bfs_grids.append(self.bfs_grid)
            restart_values.append(max(self.puzzle_values))
            
        total_time = time.time() - self.start_time
        print("Run time: " + str(total_time) + " seconds!")

##        self.grid = []
##        self.bfs_grid = []
##        self.grid = grids[restart_values.index(max(restart_values))]
##        self.bfs_grid = bfs_grids[restart_values.index(max(restart_values))]

        self.grid = self.best_grid
        self.build_graph()
        self.bfs_the_whole_thing()
        
        self.build_gui(frame)
        
        self.start_time = 0

    def task5(self, frame, iterations, p):
        
        self.p = p
        self.puzzle_values = []
        
        self.start_time = time.time()
        self.climb_hill(frame, iterations)
        
        total_time = time.time() - self.start_time
        print("Run time: " + str(total_time) + " seconds!")
        
        
        self.build_gui(frame)
        
        self.p = 0
        self.start_time = 0

    def task6(self, frame, iterations, temp, decay):
        
        self.puzzle_values = []

        self.start_time = time.time()

        n = len(self.grid)

        for i in range(0, iterations):
            x, y = randint(1, n), randint(1, n)
            
            while x == n and y == n:
                x, y = randint(1, n), randint(1, n)
            
            old_jump = self.grid[x - 1][y - 1]
            max_jump = max(n - x, x - 1, n - y, y - 1)
            new_jump = randint(1, max_jump)
            while new_jump == old_jump:
                new_jump = randint(1, max_jump)

            old_grid = self.grid
            self.grid[x - 1][y - 1] = new_jump
            
            old_graph = self.graph
            self.build_graph()

            old_bfs_grid = self.bfs_grid
            self.bfs_the_whole_thing()

            old_val = old_bfs_grid[n - 1][n - 1]
            new_val = self.bfs_grid[n - 1][n - 1]
            
            try:
                self.p = math.exp((old_val - new_val) / temp)
            except OverflowError:
                self.p = 0
            except ZeroDivisionError:
                self.p = 0
                
            
            if new_val < old_val and random() > self.p:
                self.grid = old_grid
                self.graph = old_graph
                self.bfs_grid = old_bfs_grid
            else:
                self.puzzle_values.append(self.bfs_grid[n - 1][n - 1])

            temp = temp * decay


        total_time = time.time() - self.start_time
        print("Run time: " + str(total_time) + " seconds!")
        
        self.build_gui(frame)

        self.p = 0
        self.start_time = 0


    #randomly selects parents and randomly divides them before x-over
    #one cell gets changed every iteration due to mutation
    def generate_child(self, parent1, parent2):
        n = len(self.grid)
        child1 = []
        child2 = []
        selection = randint(1,n-1)
        for i in range(0, n):
            if i < selection:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
    
        return [child1,child2]

    def mutate(self, child):
        n = len(self.grid)

        x, y = randint(1, n), randint(1, n)

        while x == n and y == n:
            x, y = randint(1, n), randint(1, n)
        
        old_jump = child[x - 1][y - 1]
        max_jump = max(n - x, x - 1, n - y, y - 1)
        new_jump = randint(1, max_jump)
        while new_jump == old_jump:
            new_jump = randint(1, max_jump)

        new_child = child
        new_child[x - 1][y - 1] = new_jump
        
        return new_child
        
    def task7(self, frame, population_size, generations, mutation):
        n = len(self.grid)

        self.start_time = time.time()
                
        population = []  
        puzzle_values = []

        best_value = 0
        best_puzzle = []
        
        # generate a random population
        for i in range(0, population_size):
            grid = []
            for x in range(0, n):
                row = []
                for y in range(0, n):
                    max_jump = max(n - (x + 1), x, n - (y + 1), y)
                    random_jump = randint(1, max_jump)
                    row.append(random_jump)
                grid.append(row)
            grid[n - 1][n - 1] = 0
            self.grid = grid
            self.build_graph()
            self.bfs_the_whole_thing()
            population.append(grid)
            puzzle_values.append(self.bfs_grid[n - 1][n - 1])
            if puzzle_values[i] > best_value:
                best_value = puzzle_values[i]
                best_puzzle = population[i]
            
        for i in range(0, generations):

            # compute the probability that a puzzle will be parent
            sum_values = sum(puzzle_values)
            probabilities = []
            for value in puzzle_values:
                if value < 0:
                    # unsolvable puzzle get a really low probability
                    probabilities.append(0.1/len(population))
                else:
                    probabilities.append(value / sum_values)

            new_population = []
            parents = []
            count = 0
            k = 0
            # make the new population based on fitness
            while count != population_size:
                if k == population_size:
                    k = 0
                if random() < probabilities[k]:
                    if population[k] not in parents:
                        parents.append(population[k])
                        count += 1
                    if len(parents) == 2:
            
                        children = self.generate_child(parents[0], parents[1])
                        if random() < mutation:
                            child1 = self.mutate(children[0])
                        else:
                            child1 = children[0]
                        if random() < mutation:
                            child2 = self.mutate(children[1])
                        else:
                            child2 = children[1]
                        new_population.append(child1)
                        new_population.append(child2)
                        parents = []
                k += 1
                
            population = []
            population = new_population
            puzzle_values = []
            
            # compute the fitness of the new population
            for j in range(0, population_size):
                self.grid = population[j]
                self.build_graph()
                self.bfs_the_whole_thing()
                puzzle_values.append(self.bfs_grid[n - 1][n - 1])
                if puzzle_values[j] > best_value:
                    best_value = puzzle_values[j]
                    best_puzzle = population[j]
                    

        total_time = time.time() - self.start_time
        print("Run time: " + str(total_time) + " seconds!")


        self.grid = best_puzzle
        self.build_graph()
        self.bfs_the_whole_thing()
        self.build_gui(frame)

        
    


def bfs(graph ,root, goal):
    visited = []
    queue = [[root]]
    if root == goal:
        return 0
    while queue:
        path = queue.pop(0)
        cell = path[-1]
        if cell not in visited:
            neighbors = graph[cell]
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == goal:
                    return len(new_path) - 1
            visited.append(cell)
    return -1

def print_grid(grid):
    for row in grid:
        print(row)


root = Tk()
puzzle = Puzzle(root)
root.mainloop()
