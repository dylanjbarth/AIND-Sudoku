from collections import namedtuple

# stores results while we determine which box has the least possibilities
MinPossBox = namedtuple("MinPossBox", ("square", "num_possibilities"))

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return ["{}{}".format(a, b) for a in A for b in B]

# build Sudoku constants and helpful lookups
ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COL_UNITS = [cross(ROWS, c) for c in COLS]
SQ_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
DIAG_UNITS = [[k + v for k, v in zip(ROWS, COLS)], [k + v for k, v in zip(ROWS[::-1], COLS)]]
ALL_UNITS = ROW_UNITS + COL_UNITS + SQ_UNITS + DIAG_UNITS
UNITS = {sq: [u for u in ALL_UNITS if sq in u] for sq in BOXES}
PEERS = {sq: list(set(sum(UNITS[sq], [])) - set([sq])) for sq in BOXES}

# global record of values after each change
assignments = []
def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The possibilities for each box, e.g., '123456789'.
    """
    grid_keys = cross(ROWS, COLS)
    return {k: v if v is not "." else COLS
            for k, v in zip(grid_keys, grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form

    Returns:
        None
    """
    if not values:
        return
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    print("".join([c.center(width) for c in COLS]))
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') + (' ' + r if i == 8 else '')
                      for i, c in enumerate(COLS)))
        if r in 'CF':
            print(line)

def eliminate(values):
    """
    If a box contains a single value, eliminate values
    from its peers which also contain that value.
    """
    for sq, val in values.items():
        if len(val) == 1:
            for p in PEERS[sq]:
                values = assign_value(values, p, values[p].replace(values[sq], ""))
    return values

def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Iterate through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        values: Sudoku in dictionary form.

    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    for u in ALL_UNITS:
        seen = [0] * 9  # holds counts for each time we have seen a digit
        for sq in u:
            # count what we have only by adding a number at that index
            for val in values[sq]:
                seen[int(val) - 1] += 1
        # get the values we have only seen once
        seen_once = [str(i + 1) for i, v in enumerate(seen) if v == 1]
        # finalize values that have only been seen once
        for sq in u:
            for seen in seen_once:
                if len(values[sq]) > 1 and seen in values[sq]:
                    values = assign_value(values, sq, seen)
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # search peers for naked twins
    for sq in BOXES:
        if len(values[sq]) != 2:
            continue
        # check for twins in each unit
        for unit in UNITS[sq]:
            twins = [u for u in unit if values[u] == values[sq]]
            # remove twins if we found them
            if len(twins) > 1:
                values = _eliminate_twins(unit, twins, values, sq)
    return values

def _eliminate_twins(unit, twins, values, sq):
    """Helper for naked twins strategy that eliminates twin values from their peers."""
    for p in unit:
        if p not in twins:
            new_values = values[p]
            for val in values[sq]:
                new_values = new_values.replace(val, "")
            values = assign_value(values, p, new_values)
    return values

def reduce_puzzle(values):
    """
    Apply eliminate, only_choice, and naked twins strategies to reduce the puzzle.

    - If at some point, there is a box with no available values, return False. (this means we tried a search that failed).
    - If the sudoku is solved, return the sudoku.
    - If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Args:
        values: A sudoku in dictionary form.

    Returns:
        The resulting sudoku in dictionary form.
    """
    strategies = [eliminate, only_choice, naked_twins]
    n_solved = lambda: len([box for box in values.keys() if len(values[box]) == 1])
    n_possiblities = lambda: sum([len(poss) for poss in values.values()])
    stalled = False
    # continue applying reduction strategies until it has no effect
    while not stalled:
        print("Reducing...")
        display(values)
        n_solved_before = n_solved()
        for strategy in strategies:
            print("applying {}".format(strategy))
            values = strategy(values)
            display(values)
            print("Number possibilities: {} / {}".format(n_possiblities(), 9*81))
            print("Number solved squares: {} / 81".format(n_solved()))
        # determine if stalled by comparing number of solved squares to snapshot before strategies were applied
        n_solved_after = n_solved()
        stalled = n_solved_before == n_solved_after
        # in case we eliminate a single value, we give up and return
        if any(box for box in values.keys() if not values[box]):
            return False
    return values

def search(values):
    """
    Reduce the Sudoku puzzle to it's solution by applying constraint propagation strategies and search.

    Args:
        values: Sudoku grid (or boolean)
        i: depth of the search
    Returns one of:
         - False: if our strategies have failed to find a solution
         - values: the completed Sudoku grid if we solve the puzzle
    """
    # start by reducing the puzzle with our simple strategies
    values = reduce_puzzle(values)
    if not values:
        print("Unable to reduce any further.")
        return False
    if len(values.keys()) == sum([len(v) for v in values.values()]):
        print("Solved!")
        return values

    # otherwise branch and search, choose candidate with fewest possibilities
    to_search = get_least_possibilites_box(values)
    return any_val(search(assign_value(values.copy(), to_search, v)) for v in values[to_search])


def any_val(seq):
    """Return some element of seq that is true.

    Like python's builtin `any` but instead of returning True returns actual value that is True.
    """
    for e in seq:
        if e: return e
    return False


def get_least_possibilites_box(values):
    """Return the box in the sudoku grid that has yet to be solved and has the fewest possibilities."""
    cur_min = MinPossBox(square=None, num_possibilities=10)
    for b in BOXES:
        if len(values[b]) in range(2, cur_min.num_possibilities):
            cur_min = MinPossBox(square=b, num_possibilities=len(values[b]))
    return cur_min.square

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
