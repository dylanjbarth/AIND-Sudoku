from collections import namedtuple

# stores results while we determine which box has the least possibilities
MinPossBox = namedtuple("MinPossBox", ("square", "num_possibilities"))

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return ["{}{}".format(a, b) for a in A for b in B]

# build up Sudoku constants and helpful lookups
ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COL_UNITS = [cross(ROWS, c) for c in COLS]
SQ_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
ALL_UNITS = ROW_UNITS + COL_UNITS + SQ_UNITS
UNITS = {sq: [u for u in ALL_UNITS if sq in u] for sq in BOXES}
PEERS = {sq: list(set(sum(UNITS[sq], [])) - set([sq])) for sq in BOXES}

# global record of values after each change
assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_keys = cross(ROWS, COLS)
    return {k: v if v is not "." else COLS
            for k, v in zip(grid_keys, grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        for c in COLS:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')))
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
                values[p] = values[p].replace(values[sq], "")
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
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
                if seen in values[sq]:
                    values[sq] = seen
    return values

def reduce_puzzle(values):
    """Apply eliminate and only_choice strategy to reduce the puzzle.
    If at some point, there is a box with no available values, return False. (this means we tried a search that failed).
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    strategies = [eliminate, only_choice]
    n_solved = lambda: len([box for box in values.keys() if len(values[box]) == 1])
    stalled = False
    while not stalled:
        n_solved_before = n_solved()
        for strategy in strategies:
            values = strategy(values)
        n_solved_after = n_solved()
        stalled = n_solved_before == n_solved_after
        if any(box for box in values.keys() if not values[box]):
            return False
    return values

def search(values, i=1):
    # start by reducing the puzzle with our simple strategies
    print("Search Round: {}".format(i))
    display(values)
    values = reduce_puzzle(values)
    if not values:
        # failed in prev round
        return False
    if len(values.keys()) == len(values.values()):
        # every value is a single digit, done! whoop whoop!
        return values

    # otherwise branch and search, choose candidate with fewest possibilities
    to_search = get_least_possibilites_box(values)
    for v in values[to_search]:
        new_sudoku = values.copy()
        # set a possibility in the box
        new_sudoku[to_search] = v
        return search(new_sudoku, i+1)


def get_least_possibilites_box(values):
    """Return the box in the sudoku grid that has yet to be solved and has the fewest possibilites."""
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
