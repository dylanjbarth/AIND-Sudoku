def cross(A, B):
    "Cross product of elements in A and elements in B."
    ["{}{}".format(a, b) for a in A for b in B]

# build up Sudoku constants and helpful lookups
ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COL_UNITS = [cross(ROWS, c) for c in COLS]
SQ_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
ALL_UNITS = ROW_UNITS + COL_UNITS + SQ_UNITS
UNITS = {sq: [u for u in ALL_UNITS if sq in u] for sq in BOXES}
PEERS = {sq: [set(sum(UNITS[sq], [])) - set([sq])] for sq in BOXES}

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
    pass

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
    pass

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

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
