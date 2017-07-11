# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation essentially means applying known rules to a problem space to reduce the amount of unknown information. 

In the case of 'naked twins', we know that two possible numbers must appear in one of two peer boxes, which means that they cannot appear in any of the other peers. We can use this information to eliminate those two numbers from the set of possibilities in their peers, which can reduce the overall number of possibilities and simplify the problem.
  
To implement this in code, we search each box in the sudoku grid for candidates (boxes with exactly 2 values). If we find one, we then search through each of it's units for a 'twin' (a box with the exact same 2 possibilities). If we find a twin, we can then go through the rest of the unit and eliminate either value from the set of possibilities for any box that is not one of the twins.    


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku problem introduces a new constraint to the sudoku puzzle, essentially treating diagonal rows as an additional unit (they must contain all of the numbers 1-9). 

Because each of the strategies are applied one box at a time, and for each box, we search through the boxes peer units, we can simply add diagonals to the set of all units, thereby ensuring we will apply our strategies to the diagonal row, as well as the other units (squares, horizontal rows, vertical columns).

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

