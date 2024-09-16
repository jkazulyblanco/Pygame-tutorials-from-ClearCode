from pathfinding.core.grid import Grid

# AStarFinder by default works with cross directions
from pathfinding.finder.a_star import AStarFinder
# To add diagonal directions
from pathfinding.core.diagonal_movement import DiagonalMovement

# Map: 1 can navigate 0 no
matrix = [
    [1 ,1, 1, 1, 1, 1],
    [1 ,0, 1, 1, 1, 1],
    [1 ,1, 1, 1, 1, 1] ]

# 1. Create a grid
grid = Grid(matrix= matrix)

# 2. Create: Start - End, cell
start = grid.node(0,0)
end = grid.node(5,2)

# 3. Create a finder with a movement style
finder = AStarFinder(diagonal_movement= DiagonalMovement.always) 

# 4. use the finder 
path,runs = finder.find_path(start,end,grid) # returns 2 info

# print results
print(path)
print(runs, 'times ran the matrix to find the path')

 