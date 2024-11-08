from typing import Generator


###
# My Algorithm sucks!!!!
###
class NQueens:
    board_size: int

    def __init__(self, board_size):
        self.board_size = board_size

    def dd(self, board, solution: int):
        ENL = ENL = "\n\r" * 2
        SEPARATOR = ("+---" * self.board_size) + "+"

        print(f"Solution: {solution}")

        for i in range(self.board_size):
            print(SEPARATOR)
            for j in range(self.board_size):
                p = "x" if (i, j) in board else " "
                print(f"| {p} ", end="")
            print("|")

        print(SEPARATOR, end=ENL)

    def resolve(self) -> Generator[list[int, int], None, None]:
        """
        We used Depth Search to resolve the problem based on comments

        For more info: https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/

        TODO: implement board rotation to optimize the the runtime execution
        For more info: https://github.com/NassarX/nqueens-optimization
        """

        stack = [[]]

        while stack:
            solution = stack.pop()
            r = len(solution)

            if r == self.board_size:
                if not self.collision(solution):
                    yield solution

            if r < self.board_size:
                for col in range(self.board_size):
                    queen = (r, col)
                    queens = solution.copy()
                    queens.append(queen)
                    stack.append(queens)

    def collision(self, queens):
        """
        Based on analytic geometry, we calculate the cols, rows and diagonals
        that has a collision
        """
        size = len(queens)

        for i in range(1, size):
            for j in range(0, i):
                a, b = queens[i]
                c, d = queens[j]
                if a == c or b == d or abs(a - c) == abs(b - d):
                    return True
        return False
