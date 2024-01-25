import API
import sys
from itertools import product
import read_write_matrix

# (x,y) current position; orient orientation
# 0-north   1-east   2-south   3-west
#
#               N(x, y-1)                           
#    W(x-1, y)    (x, y)    E(x+1, y)                  access -> cells[y][x]
#               S(x, y+1)
#

SIZE = 16  # size of the maze
cells =  [[0]*SIZE for _ in range(SIZE)]  # array on which floodfill is done
cells_return = [[0]*SIZE for _ in range(SIZE)]  # array on which floodfill is done while returning

cell_type = [[-1]*SIZE for _ in range(SIZE)]  # array containing type of each known cell; if unknown, type is -1
RETURNING = False
COLORS = ['b', 'y', 'g', 'c', 'w', 'o', 'a', 'Y']
COLOR_IDX = 0
CYCLE = 3


if read_write_matrix.see('cells.txt'):
    if (t:=read_write_matrix.read('cells.txt')) != '':
        cells = t[:]
        cell_type = read_write_matrix.read('cell_types.txt')

def log(string):
    # logs 'string' message into the mms simulator text window
    sys.stderr.write("{}\n".format(string))

def determine_cell_type(cell_coords:tuple, orient:int, left_wall:bool, right_wall:bool, front_wall:bool):
    # assigns cell type based on the pic cell_types.png
    global cell_type
    x, y = cell_coords
    log(f'judging: {x=}, {y=}')
    if left_wall:
        if right_wall:
            if front_wall:
                if orient&1:
                    cell_type[y][x] = 11 + orient
                else:
                    cell_type[y][x] = 13 - orient
            else:
                cell_type[y][x] = 9 + (orient&1)
        elif front_wall:
            if orient==0: cell_type[y][x] = 8
            elif orient==1: cell_type[y][x] = 7
            elif orient==2: cell_type[y][x] = 6
            else: cell_type[y][x] = 5
        else:
            if orient==0: cell_type[y][x] = 1
            elif orient==1: cell_type[y][x] = 2
            elif orient==2: cell_type[y][x] = 3
            else: cell_type[y][x] = 4
    elif right_wall:
        if front_wall:
            if orient==0: cell_type[y][x] = 7
            elif orient==1: cell_type[y][x] = 6
            elif orient==2: cell_type[y][x] = 5
            else: cell_type[y][x] = 8
        else:
            if orient==0: cell_type[y][x] = 3
            elif orient==1: cell_type[y][x] = 4
            elif orient==2: cell_type[y][x] = 1
            else: cell_type[y][x] = 2
    elif front_wall:
        if orient==0: cell_type[y][x] = 2
        elif orient==1: cell_type[y][x] = 3
        elif orient==2: cell_type[y][x] = 4
        else: cell_type[y][x] = 1
    else:
        cell_type[y][x] = 15


def get_surrounds(cell):
    # returns a dictionary containing all nearby cells (keys) and their directions (N, E, W or S) as values
    x, y = cell
    return {(x, y-1):'N', (x+1, y):'E', (x-1, y):'W', (x, y+1):'S'}

def can_water_flow(cell_a:tuple, cell_b:tuple):
    # for two cells a and b; returns True if mouse and move from a to b (there are no walls separating them)
    xa, ya = cell_a
    xb, yb = cell_b
    type_a = cell_type[ya][xa]
    type_b = cell_type[yb][xb]

    if ya==yb:
        if xa > xb:
            # [b] [a]
            return not(type_a in [1,5,8,9,11,13,14,16] or type_b in [3,6,7,9,11,12,13,16])
        elif xa < xb:
            # [a] [b]
            return not(type_a in [3,6,7,9,11,12,13,16] or type_b in [1,5,8,9,11,13,14,16])
        else: log(f'WATER FLOW ERROR {cell_a=} {cell_b=}')
    elif xa==xb:
        if ya > yb: 
            # [b]
            # [a]
            return not(type_a in [2,7,8,10,12,13,14,16] or type_b in [4,5,6,10,11,12,14,16])
        elif ya < yb:
            # [a]
            # [b]
            return not(type_a in [4,5,6,10,11,12,14,16] or type_b in [2,7,8,10,12,13,14,16])
        else: log(f'WATER FLOW ERROR {cell_a=} {cell_b=}')
    else: log(f'WATER FLOW ERROR {cell_a=} {cell_b=}')
    return 'ERROR at water flow'

def turn(direction: int):
    # updates orient depending on turning direction
    # i dont think i used this function in main code

    # direction = 1 for right, -1 for left
    global orient
    orient = (orient + direction + 4) % 4
    # north -> east -> south -> west on adding +1... 
    # west -> north due to (3 + 1 + 4)%4 = 0; north -> west due to (0 - 1 + 4) = 3%4 = 3

def get_goal_locations():
    # returns goal locations (1 if odd size; 4 if even)
    # according to IEEE rules - goal is at the center of maze and is a 2x2 cell
    t = SIZE//2
    if SIZE&1:  return [(t, t)]
    else:       return list(product([t, t-1], repeat=2))

def do_floodfill(goal_loc:list=get_goal_locations()):
    # floodfill occurs here
    queue = goal_loc[:] # the [:] copies the whole array instead of sharing memory address
    checked = []

    while queue:
        # show_mat()
        cur_cell = queue[0]
        nearby = get_surrounds(cur_cell).keys()
        checked.append(cur_cell)

        for cell in nearby:
            x,y = cell
            if 0<=x<SIZE and 0<=y<SIZE:
                if not can_water_flow(cur_cell, cell):
                    continue
                if cell not in checked and cell not in queue: 
                    # works for multiple cells as goals due to 'cell not in queue' but why idk
                    if not RETURNING:
                        cells[y][x] = cells[cur_cell[1]][cur_cell[0]] + 1
                    else:
                        cells_return[y][x] = cells_return[cur_cell[1]][cur_cell[0]] + 1                    
                    queue.append(cell)
        del queue[0]

def show_mat():
    # only for initial debug process
    # prints the whole floodfill matrix
    for row in cells:
        print(' '.join(map(str, row)))
    print()

def showFlood():
    # sets text in mms simulator cells (for some reason doesnt work; nothing i can do to fix this)
    for x in range(SIZE):
        for y in range(SIZE):
            API.setText(x,SIZE-1-y,str(cells[y][x]))

def next_move(current, nxt, orient, nxt_dir:str):
    # uses current and next cell locations; and orientations to find out what the next move should be
    if nxt_dir == '': return 'stop'
    nxt_dir = int(nxt_dir.replace('N', '0').replace('E', '1').replace('S', '2').replace('W', '3'))

    if abs(orient - nxt_dir) == 2: 
        log(f'Going back :: {orient=}, {nxt_dir=}')
        return 'back'

    if orient == 0 and nxt_dir == 3:        return 'left_turn'
    elif orient == 3 and nxt_dir == 0:      return 'right_turn'
    elif orient > nxt_dir:                  return 'left_turn'
    elif orient == nxt_dir:                 return 'forward'
    else:                                   return 'right_turn'

def next_cell(current, orient):
    # determine the nearby cell with the lowest manhattan number in the cells (floodfill) matrix
    if RETURNING:
        flood = cells_return
    else:
        flood = cells
    
    preference = ''
    if orient==0: preference='N'
    elif orient==1: preference='E'
    elif orient==2: preference='S'
    elif orient==3: preference='W'
    nearby = get_surrounds(current)
    xxd = [k for k,v in nearby if v==preference] + list(nearby.keys())

    low = flood[current[1]][current[0]]
    coords = current
    for k in xxd:
        if 0<=k[0]<SIZE and 0<=k[1]<SIZE:
            if not can_water_flow(current, k):
                continue
            val = flood[k[1]][k[0]]
            if val < low:
                low = val
                coords = k
    if coords == current:
        log('cant move in any dir')
        return coords, ''
    return coords, nearby[coords]

def main():
    global RETURNING, CYCLE, COLORS, COLOR_IDX
    start_loc = (0, SIZE-1)
    goal_loc = get_goal_locations()
    color = COLORS[COLOR_IDX]

    current_loc = (0, SIZE-1)
    orient = 0   # north
    do_floodfill(goal_loc) # initial floodfill with no walls

    while True:
        API.setColor(current_loc[0], SIZE - current_loc[1] - 1, color)
        left = API.wallLeft()
        right = API.wallRight()
        front = API.wallFront()
        determine_cell_type(current_loc, orient, left, right, front)
        do_floodfill(goal_loc)
        showFlood()

        if RETURNING:
            val = cells_return[current_loc[1]][current_loc[0]]
        else:
            val = cells[current_loc[1]][current_loc[0]]

        if val == 0:
            # mouse is at goal
            
            log('done')
            log('SWITCHING GOALS')
            RETURNING = not RETURNING
            COLOR_IDX = (COLOR_IDX + 1) % len(COLORS)
            color = COLORS[COLOR_IDX]
            # read_write_matrix.write(cells_return, 'cells.txt')
            # read_write_matrix.write(cell_type, 'cell_types.txt')
            if goal_loc[0] == start_loc:
                goal_loc = get_goal_locations()
            else:
                goal_loc = [start_loc]
                CYCLE -= 1
            do_floodfill(goal_loc)
            log(f'new goal: {goal_loc=}')
            if CYCLE == 0: break

        next_loc, direction = next_cell(current_loc, orient)
        to_do = next_move(current_loc, next_loc, orient, direction) # amongst forward, right_turn, left_turn, stop, back
        log(f'{current_loc=}  cell type:{cell_type[current_loc[1]][current_loc[0]]}  {to_do=}  {next_loc=}  {orient=}')
        # log(f'{current_loc=} {front=} {right=} {left=} {orient=} type={cell_type[current_loc[1]][current_loc[0]]}')
        # log('\n'.join([' '.join(map(str, i)) for i in cells]))

        
        if not can_water_flow(current_loc, next_loc):
            log('water cant flow')
            do_floodfill(goal_loc)
        else:
            if to_do == 'right_turn': 
                orient = (orient + 1) % 4
                API.turnRight()
            elif to_do == 'left_turn': 
                orient = (orient + 3) % 4
                API.turnLeft()
            elif to_do == 'stop':
                continue
            elif to_do == 'back':
                orient = (orient + 2) % 4
                API.turnRight()
                API.turnRight()

            API.moveForward()
            current_loc = next_loc
    log('DONE at GOAL for Final Time')

        #if front:
            # if theres a wall in front of the mouse, redo floodfill
            # do_floodfill()
        
        
''' #code to test if my implementation of updateWalls works or not
    possible = list(product([True, False], repeat=3))
    op = [[-1]]
    op1 = [[-1]]
    ori = [0,1,2,3]
    for i in possible:
        updateWalls(op,  0, 0, ori, L=i[0], R=i[1], F=i[2])
        determine_cell_type(op1, (0, 0), ori, left_wall=i[0], right_wall=i[1], front_wall=i[2])
        print(op[0][0], "  ", op1[0][0], i)
'''


if __name__ == "__main__":
    main()
