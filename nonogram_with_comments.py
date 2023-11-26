import random  # Import the random module for random number generation
import copy    # Import the copy module for creating deep copies of objects
from collections import namedtuple  # Import the namedtuple class from collections module

# Define a named tuple CheckInfo to store information about checking the solution
CheckInfo = namedtuple('CheckInfo', ['matched', 'mismatched', 'violated'])

# Define a class called Nonogram
class Nonogram(object):
    def __init__(self, row_count:int, col_count: int, fill_rate: float):
        """
        Args:
            row: Number of rows for the board.
            col: Number of columns for the board.
            fill_rate: Rate of filled cells.
        """
        # Initialize the Nonogram object with row_count, col_count, and fill_rate
        
        self.row_count = row_count  # Store the number of rows
        self.col_count = col_count  # Store the number of columns
        self.total_count = self.row_count * self.col_count  # Calculate the total number of cells
        self.fill_rate = fill_rate  # Store the fill rate as a float
        
        # Create an empty game board (2D list) initialized with zeros
        self.board = [ [0 for _ in range(col_count)] for _ in range(row_count)]
        
        # Create a copy of the game board called board_answer
        self.board_answer = copy.deepcopy(self.board)

        # Initialize board layout with randomly filled cells based on the fill_rate
        samples = random.sample(range(self.total_count), int(self.total_count * fill_rate)) # Select total_count*fill_rate cells from total_count number of cells
        for sample in samples:
            self.board_answer[sample // self.col_count][sample % self.col_count] = 1 # Each cell's coordinate (i / col_count, i % col_count)

        # Initialize empty lists to store row and column clues
        self.row_clues = [] * self.row_count
        self.col_clues = [] * self.col_count
        
        # Generate row clues by encoding the filled cell sequences in each row
        for r in range(row_count):
            row = self.__get_row(self.board_answer, r)
            self.row_clues.append(self.__encode_list(row))
        
        # Generate column clues by encoding the filled cell sequences in each column
        for c in range(col_count):
            col = self.__get_col(self.board_answer, c)
            self.col_clues.append(self.__encode_list(col))

    # Define a string representation of the Nonogram object
    def __repr__(self) -> str:
        output = "board:\n"
        
        # Loop through the game board and add its content to the output string
        for row in self.board:
            for cell in row:
                output = output + str(cell) + " "
            output = output + "\n"
        return output

    # Method to print the current state of the game board
    def show_board(self) -> None:
        """Print out the game board."""
        print(self)

    # Method to print the answer board (solution)
    def show_answer(self) -> None:
        output = "answer:\n"
        for row in self.board_answer:
            for cell in row:
                output = output + str(cell) + " "
            output = output + "\n"
        print(output)

    # Method to check the current game board against the answer board
    def check(self) -> CheckInfo:
        """
        Check the board with clues and compare it with the answer board.
        """
        matched = 0
        mismatched = 0
        violated = 0
        
        # Loop through each cell in the game board and compare it with the answer board
        for r in range(self.row_count):
            for c in range(self.col_count):
                if self.board == self.board_answer:  # Check if the cell matches the answer
                    matched += 1
                else:
                    mismatched += 1  # If not, it's a mismatch

        # Check the row clues for violations
        for r in range(self.row_count):
            row = self.__get_row(self.board, r)
            row_status = self.__encode_list(row)
            if row_status != self.row_clues[r]:  # Check if the row clues match
                violated += 1
        
        # Check the column clues for violations
        for c in range(self.col_count):
            col = self.__get_col(self.board, c)
            col_status = self.__encode_list(col)
            if col_status != self.col_clues[c]:  # Check if the column clues match
                violated += 1
        
        # Return a CheckInfo named tuple containing the counts of matched, mismatched, and violated cells
        return CheckInfo(matched, mismatched, violated)
    
    # Method to set the value of a cell in the game board
    def set_cell(self, row_num, col_num, value) -> None:
        self.board[row_num][col_num] = value

    # Helper method to get a row from the game board
    def __get_row(self, board, row_num) -> list:
        return [board[row_num][c] for c in range(self.col_count)]
    
    # Helper method to get a column from the game board
    def __get_col(self, board, col_num) -> list:
        return [board[r][col_num] for r in range(self.row_count)]

    # Helper method to encode a list of cell values into a tuple of clue values
    def __encode_list(self, target_list) -> list:
        clue = []
        cnt = 0
        for item in target_list:
            if item == 1:
                cnt += 1
            elif cnt:
                clue.append(cnt)
                cnt = 0
        if cnt:
            clue.append(cnt)
        return tuple(clue)
    

if __name__ == "__main__":
    # Create an instance of the Nonogram class with a 10x10 grid and 10% fill rate
    game = Nonogram(10, 10, 0.1)
    
    # Display the current game board
    game.show_board()
    
    # Display the answer board (solution)
    game.show_answer()
    
    # Check the current game board against the answer and print the result
    result = game.check()
    print(result)
