import random
import copy
from collections import namedtuple

CheckInfo = namedtuple('CheckInfo', ['matched', 'mismatched', 'violated'])

class Nonogram(object):
    def __init__(self, row_count:int, col_count: int, fill_rate: float):
        """
        Args:
            row: Number of rows for the board.
            col: Number of columns for the board.
            fill_rate: Rate of filled cells.
        """
        
        self.row_count = row_count
        self.col_count = col_count
        self.total_count = self.row_count * self.col_count
        self.fill_rate = fill_rate
        
        self.board = [ [0 for _ in range(col_count)] for _ in range(row_count)]
        self.board_answer = copy.deepcopy(self.board)

        # Initialize board layout
        samples = random.sample(range(self.total_count), int(self.total_count * fill_rate))
        for sample in samples:
            self.board_answer[sample // self.col_count][sample % self.col_count] = 1

        self.row_clues = [] * self.row_count
        self.col_clues = [] * self.col_count
        
        for r in range(row_count):
            row = self.__get_row(self.board_answer, r)
            self.row_clues.append(self.__encode_list(row))
        
        for c in range(col_count):
            col = self.__get_col(self.board_answer, c)
            self.col_clues.append(self.__encode_list(col))

    def __repr__(self) -> str:
        output = "board:\n"
        
        for row in self.board:
            for cell in row:
                output = output + str(cell) + " "
            output = output + "\n"
        return output

    def show_board(self) -> None:
        """Print out the game board."""
        print(self)

    def show_answer(self) -> None:
        output = "answer:\n"
        for row in self.board_answer:
            for cell in row:
                output = output + str(cell) + " "
            output = output + "\n"
        print(output)

    def check(self) -> CheckInfo:
        """
        Check the board with clues and compare it with answer board.
        """
        matched = 0
        mismatched = 0
        violated = 0
        for r in range(self.row_count):
            for c in range(self.col_count):
                if self.board == self.board_answer:
                    matched += 1
                else:
                    mismatched += 1

        for r in range(self.row_count):
            row = self.__get_row(self.board, r)
            row_status = self.__encode_list(row)
            if row_status != self.row_clues[r]:
                violated += 1
        
        for c in range(self.col_count):
            col = self.__get_col(self.board, c)
            col_status = self.__encode_list(col)
            if col_status != self.col_clues[c]:
                violated += 1
        
        return CheckInfo(matched, mismatched, violated)
    
    def set_cell(self, row_num, col_num, value) -> None:
        self.board[row_num][col_num] = value

    def __get_row(self, board, row_num) -> list:
        return [board[row_num][c] for c in range(self.col_count)]
    
    def __get_col(self, board, col_num) -> list:
        return [board[r][col_num] for r in range(self.row_count)]

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
    game = Nonogram(10, 10, 0.1)
    game.show_board()
    game.show_answer()
    result = game.check()
    print(result)