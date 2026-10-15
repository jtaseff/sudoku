import matplotlib.pyplot as plt
import numpy as np

# constants to compare things with
LIST19 = np.array([1,2,3,4,5,6,7,8,9])
SET19 = set(LIST19)

def zero_grid():
    return np.zeros( (9, 9), dtype = np.int8)




def plotsetup():
    fig = plt.figure()
    plt.clf()
    # fig, ax = plt.subplots()
    ax = plt.axis([0.35, 9.6, 0.5, 9])
    plt.axis('square')
    hs = 0.55
    vs = 0.5
    plt.hlines([0+hs, 3+hs, 6+hs, 9+hs], 0, 9.8, 'k', linewidth=3.5)
    plt.vlines([0+vs, 3+vs, 6+vs, 9+vs], 0, 9.5, 'k', linewidth=3.5)
    plt.hlines([1+hs, 2+hs, 4+hs, 5+hs, 7+hs, 8+hs], 0, 10, 'k', linewidth=0.5)
    plt.vlines([1+vs, 2+vs, 4+vs, 5+vs, 7+vs, 8+vs], 0, 9.5, 'k', linewidth=0.5)


def plotgrid(grid, textcolor='k'):
    for ii in range(9):
        for jj in range(9):
            if grid[ii][jj] > 0:
                plt.text(jj+1, 9-ii, str(grid[ii][jj]), color=textcolor, va='center', ha='center', weight='heavy', family='sans', size='x-large')



def plot_candidates(grid, candidates, textcolor='k'):
    for ii in range(9):
        for jj in range(9):
            if grid[ii][jj] == 0:
                for nn in range(1, 10):
                    if candidates[ii, jj] >= {nn}:  # if set contains
                        cand_disp_pos_x = jj + 0.75
                        cand_disp_pos_y = 9 - ii + 0.3
                        
                        if nn == 2 or nn == 5 or nn == 8:
                            cand_disp_pos_x += 0.27
                        elif nn == 3 or nn == 6 or nn == 9:
                            cand_disp_pos_x += 0.5
                            
                        if nn >= 7:
                            cand_disp_pos_y -= 0.5
                        elif nn >= 4:
                            cand_disp_pos_y -= 0.25
                        plt.text(cand_disp_pos_x, cand_disp_pos_y, str(nn), color=textcolor, va='center', ha='center', family='sans', size='x-small')






# set up a starting grid
# todo import from a file
start_grid = np.array( [
        [ 0, 1, 0,    0, 0, 0,    0, 5, 0],
        [ 0, 0, 0,    4, 2, 0,    8, 1, 0],
        [ 9, 7, 4,    1, 0, 0,    0, 0, 0],
        
        [ 3, 0, 6,    0, 0, 0,    0, 0, 0],
        [ 0, 0, 0,    8, 1, 0,    0, 0, 7],
        [ 7, 9, 0,    0, 0, 0,    6, 0, 0],
        
        [ 0, 0, 3,    2, 9, 0,    0, 0, 8],
        [ 8, 0, 0,    5, 0, 3,    0, 0, 0],
        [ 5, 0, 0,    0, 8, 0,    0, 4, 6] ] )


# grid to keep solved numbers
# separate to be displayed
solve_grid = zero_grid()

# place to store candidates. it will be an array of sets
candidates = np.zeros( (9, 9), dtype = object)
for rr in range(9):
    for cc in range(9):
        candidates[rr, cc] = {0}


# tests with some solved numbers
# fill last row
# solve_grid[8,1] = 2
# solve_grid[8,2] = 9
# solve_grid[8,3] = 7
# solve_grid[8,5] = 1
# solve_grid[8,6] = 3

# fill bottom middle box
# solve_grid[6,5] = 4
# solve_grid[7,4] = 6
# solve_grid[8,3] = 7
# solve_grid[8,5] = 1




def find_missing_in_list(mylist):
    return SET19.difference(mylist)


def find_cell_candidates(grid, find_row, find_col):
    this_row = grid[find_row, :]
    this_col = grid[:, find_col]
    this_box = get_box_of_cell(grid, find_row, find_col)
    full_set = set(np.concatenate([this_row, this_col, this_box.flatten()]))
    this_missing = find_missing_in_list(full_set)
    return this_missing


def get_box(grid, box_row, box_col):
    start_row = box_row*3
    start_col = box_col*3
    this_box = grid[start_row:start_row+3, start_col:start_col+3]
    return this_box


def get_box_of_cell(grid, cell_row, cell_col):
    if cell_row < 3:
        start_row = 0
    elif cell_row < 6:
        start_row = 3
    else:
        start_row = 6
    
    if cell_col < 3:
        start_col = 0
    elif cell_col < 6:
        start_col = 3
    else:
        start_col = 6
        
    this_box = grid[start_row:start_row+3, start_col:start_col+3]
    return this_box
    

def get_all_candidates(grid):
    for rr in range(9):
        for cc in range(9):
            # this is breaking somewhere comparing NoneType
            if grid[rr, cc] == 0:
                this_missing = find_cell_candidates(grid, rr, cc)
                candidates[rr, cc] = this_missing
            else:
                candidates[rr, cc] = set()
    return candidates


def update_candidates(grid, candidates):
    # remove any eliminated candidates, but keeping what solver has eliminated
    # take all the cached+eliminated candidates, intersect+update with current
    # modified candidate list in place
    for rr in range(9):
        for cc in range(9):
            if grid[rr, cc] == 0:
                curr_cands = find_cell_candidates(grid, rr, cc)
                candidates[rr, cc] &= curr_cands
            else:
                candidates[rr, cc] = set()    
    return


def try_last_digit_row(grid):
    # check if there are any rows with only 1 number left
    # return whether it found any and a grid with the solved numbers
    found = False
    new_finds = zero_grid()
    for rr in range(9):      # for each row
        this_row = grid[rr, :]
        this_missing = find_missing_in_list(this_row)
        if len(this_missing) == 1:
            # get the index of where it's missing
            index_missing = np.where(this_row == 0)[0][0]
            new_finds[rr, index_missing] = list(this_missing)[0]
            found = True
            print("Found a last digit", list(this_missing)[0], "in row", rr)
    return found, new_finds


def try_last_digit_col(grid):
    # check if there are any columns with only 1 number left
    # return whether it found any and a grid with the solved numbers
    found = False
    new_finds = zero_grid()
    for cc in range(9):      # for each column
        this_col = grid[:, cc]
        this_missing = find_missing_in_list(this_col)
        if len(this_missing) == 1:
            # get the index of where it's missing
            index_missing = np.where(this_col == 0)[0][0]
            new_finds[index_missing, cc] = list(this_missing)[0]
            found = True
            print("Found a last digit", list(this_missing)[0], "in column", cc)
    return found, new_finds


def try_last_digit_box(grid):
    # check if there are any boxes (3x3) with only 1 number left
    # return whether it found any and a grid with the solved numbers
    found = False
    new_finds = zero_grid()
    for rr in range(3):         # for each 3x3 box region
        for cc in range(3):
            this_box = get_box(grid, rr, cc)
            this_missing = find_missing_in_list(set(this_box.flatten()))
            if len(this_missing) == 1:
                # get the index of where it's missing
                row_in_box, col_in_box = np.where(this_box == 0)
                row_missing = rr * 3 + row_in_box
                col_missing = cc * 3 + col_in_box
                new_finds[row_missing, col_missing] = list(this_missing)[0]
                found = True
                print("Found a last digit", list(this_missing)[0], "in box at", row_missing[0], col_missing[0])
    return found, new_finds


def try_naked_single(grid):
    # search for a naked single - only 1 possiblity left in cell
    found = False
    new_finds = zero_grid()
    for rr in range(9):         # check every cell
        for cc in range(9):
            # check for unsolved cells
            if grid[rr][cc] == 0:
                # combine the sets of its row, column, and box
                this_missing = find_cell_candidates(grid, rr, cc)
                if len(this_missing) == 1:
                    new_finds[rr, cc] = list(this_missing)[0]
                    found = True
                    print("Found a naked single", list(this_missing)[0], "at", rr, cc)
    return found, new_finds


# def checK_hidden_single(region_solved, region_cans):
#     # base function to search for a hidden single - only 1 piece for a number to go in the region
#     found = False
#     found_index = False
#     for nn in range(1, 10):
#         if nn not in region_solved:
#             # check for how many cells contain the candidate
#             if sum( {nn} <= region_cans) == 1:
#                 found_index = np.where( {nn} <= region_cans )
#                 found = True
#     # this isn't great, now we would have to stack these up here and in the calling function?
#     return found, found_index
    

# def try_single_row_refactor(grid, cans):
    # found = False
    # new_finds = zero_grid()
    # for rr in range(9):
    #     this_row = grid[rr, :]
    #     this_row_cans = cans[rr, :]
    #     check_found, check_index = checK_hidden_single(this_row, this_row_cans)
    # # this isn't complete at all
    # return False
    

def try_hidden_single_row(grid, cans):
    # search for hidden single - only 1 place for a number to go in the row
    found = False
    new_finds = zero_grid()
    for rr in range(9):
        this_row = grid[rr, :]
        this_row_cans = cans[rr, :]
        for nn in range(1, 10):
            if nn not in this_row:
                # check for how many cells contain the candidate
                if sum( {nn} <= this_row_cans) == 1:
                    # found a hidden single
                    found_col = np.where({nn} <= this_row_cans)[0][0]
                    print("Found hidden single", nn, "in row", rr, "col", found_col)
                    new_finds[rr, found_col] = nn
                    found = True
    return found, new_finds


def try_hidden_single_col(grid, cans):
    # search for hidden single - only 1 place for a number to go in the column
    found = False
    new_finds = zero_grid()
    for cc in range(9):
        this_col = grid[:, cc]
        this_col_cans = cans[:, cc]
        for nn in range(1, 10):
            if nn not in this_col:
                # check for how many cells contain the candidate
                if sum({nn} <= this_col_cans) == 1:
                    # found a hidden single
                    found_row = np.where({nn} <= this_col_cans)[0][0]
                    print("Found hidden single", nn, "in col", cc, "row", found_row)
                    new_finds[found_row, cc] = nn
                    found = True
    return found, new_finds


def try_hidden_single_box(grid, cans):
    # search for hidden single - only 1 place for a number to go in the box
    found = False
    new_finds = zero_grid()
    for rr in range(3):         # for each 3x3 box region
        for cc in range(3):
            this_box = get_box(grid, rr, cc)
            this_box_cans = get_box(cans, rr, cc)
            
            for nn in range(1, 10):
                if nn not in this_box:
                    # check for how many cells contain the candidate
                    if sum(sum( {nn} <= this_box_cans )) == 1:
                        # found a hidden single
                        found_inds = np.where({nn} <= this_box_cans)
                        hidden_row = rr * 3 + found_inds[0][0]
                        hidden_col = cc * 3 + found_inds[1][0]
                        print("Found hidden single", nn, "in box at row", hidden_row, "col", hidden_col)
                        new_finds[hidden_row, hidden_col] = nn
                        found = True
    return found, new_finds









def do_menu():
    
    pass




# start solving

new_found = True
# new_found = False
step_count = 0

full_grid = np.add(start_grid, solve_grid)
cans_elim = get_all_candidates(full_grid)

while new_found == True:
    
    if not np.any(full_grid == 0):
        print("Solved in", step_count, "steps !")
        break
    
    step_count += 1
    
    new_found, new_finds = try_last_digit_row(full_grid)
    
    if new_found == False:
        new_found, new_finds = try_last_digit_col(full_grid)
        
    if new_found == False:
        new_found, new_finds = try_last_digit_box(full_grid)
    
    if new_found == False:
        new_found, new_finds = try_naked_single(full_grid)
        
    if new_found == False:
        new_found, new_finds = try_hidden_single_row(full_grid, cans_elim)
        
    if new_found == False:
        new_found, new_finds = try_hidden_single_col(full_grid, cans_elim)
        
    if new_found == False:
        new_found, new_finds = try_hidden_single_box(full_grid, cans_elim)
        
    

    plotsetup()
    plotgrid(start_grid, 'k')
    plotgrid(solve_grid, 'b')
    if new_found:
        plotgrid(new_finds, 'r')
    solve_grid = np.add(solve_grid, new_finds)
    full_grid = np.add(start_grid, solve_grid)
    
    # calculate and plot candidates
    # basic method recalculating all each time
    # cans = get_all_candidates(full_grid)
    
    # improve by just taking out eliminated candidates from pool
    update_candidates(full_grid, cans_elim)
    plot_candidates(full_grid, cans_elim)
    
    
    plt.show(block=False)
    input()


if new_found == False:
    print("Failed to solve after", step_count, "steps")
    full_grid = np.add(start_grid, solve_grid)
    cans = get_all_candidates(full_grid)
    plotsetup()
    plotgrid(full_grid, 'k')
    plot_candidates(full_grid, cans)
    