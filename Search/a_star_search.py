import pandas as pd
import queue

# The function initializes and returns open
def init_open():
    return queue.PriorityQueue()

# The function inserts s into open
def insert_to_open(open_list, s):  # Should be implemented according to the open list data structure
    open_list.put(s)

# The function returns the best node in open (according to the search algorithm)
def get_best(open_list):
    return open_list.get()

# The function returns neighboring locations of s_location
def get_neighbors(grid, s_location):
    neighbors = []
    x = s_location[0]
    y = s_location[1]
    grid_xs = grid.shape[0]
    grid_ys = grid.shape[1]
    if x < grid_xs - 1 and grid.item((x + 1, y)) != '@':
        neighbors.append((x + 1, y))
    if x > 0 and grid.item((x - 1, y)) != '@':
        neighbors.append((x - 1, y))
    if y < grid_ys - 1 and grid.item((x, y + 1)) != '@':
        neighbors.append((x, y + 1))
    if y > 0 and grid.item((x, y - 1)) != '@':
        neighbors.append((x, y - 1))
    return neighbors

# The function returns whether or not s_location is the goal location
def is_goal(s_location, goal_location):
    if s_location[0] == goal_location[0] and s_location[1] == goal_location[1]:
        return True
    return False

# The function estimates the cost to get from s_location to goal_location
def calculate_heuristic(s_location, goal_location):
    return abs(goal_location[0] - s_location[0]) + abs(goal_location[1] - s_location[1])

# The function returns whether n_location should be generated (checks in open_list)
# removes a node from open_list if needed 
def check_for_duplicates_open(n_location, s, open_list):
    ans = False
    size = open_list.qsize()
    if size == 0:
        return ans
    for node in open_list.queue:
        if n_location == (node[3], node[4]):
            old = node[2]
            new = s[2] + 1
            if old < new:
                return ans
            else:
                ans = True
                tmp = []
                n = open_list.get()
                while n != node:
                    tmp.append(n)
                    n = open_list.get()
                for n in tmp:
                    open_list.put(n)
        return ans

# The function returns whether n_location should be generated (checks in closed_list)
# removes a node from closed_list if needed  
def check_for_duplicates_close(n_location, s, closed_list):
    if n_location in closed_list:
        in_closed = closed_list[n_location][2]
        new = s[2] + 1
        if in_closed > new:
            closed_list.pop(n_location)
            return False
        return True
    return False
    
    
# Locations are tuples of (x, y)
def astar_search(grid, start_location, goal_location):
    # State = (f, h, g, x, y, s_prev) # f = g + h (For Priority Queue)
    # Start_state = (0, 0, 0, x_0, y_0, False)
    start = (0, 0, 0, start_location[0], start_location[1], False)
    open_list = init_open()
    closed_list = {}
    # Mark the source node as
    # visited and enqueue it
    insert_to_open(open_list, start)
    while not open_list.empty():
        # Dequeue a vertex from
        # queue and print it
        s = get_best(open_list)
        s_location = (s[3], s[4])
        if s_location in closed_list:
            continue
        if is_goal(s_location, goal_location):
            print("The number of states visited by AStar Search:", len(closed_list))
            return s
        neighbors_locations = get_neighbors(grid, s_location)
        for n_location in neighbors_locations:
            if check_for_duplicates_open(n_location, s, open_list) or check_for_duplicates_close(n_location, s, closed_list):
                continue
            h = calculate_heuristic(n_location, goal_location)
            g = s[2] + 1
            f = g + h
            n = (f, h, g, n_location[0], n_location[1], s)
            insert_to_open(open_list, n)
        closed_list[s_location] = s

def print_route(s):
    for r in s:
        print(r)

def get_route(s):
    route = []
    while s:
        s_location = (s[3], s[4])
        route.append(s_location)
        s = s[5]
    route.reverse()
    return route

def print_grid_route(route, grid):
    for location in route:
        grid[location] = 'x'
    print(pd.DataFrame(grid))


from route_grid import create_grid
grid, start_location, end_location = create_grid(2)
s = astar_search(grid, start_location, end_location)
print_grid_route(get_route(s),grid)