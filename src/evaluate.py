import numpy as np

board1 = np.array([[1, 3, 8, 6, 9, 4, 7, 2, 5],
                   [6, 9, 4, 7, 2, 5, 1, 3, 8],
                   [7, 2, 5, 1, 3, 8, 6, 9, 4],
                   [3, 8, 1, 9, 4, 6, 2, 5, 7],
                   [9, 4, 6, 2, 5, 7, 3, 8, 1],
                   [2, 5, 7, 3, 8, 1, 9, 4, 6],
                   [8, 1, 3, 4, 6, 9, 5, 7, 2],
                   [4, 6, 9, 5, 7, 2, 8, 1, 3],
                   [5, 7, 2, 8, 1, 3, 4, 6, 9]])

board2 = np.array([[1, 7, 8, 6, 9, 4, 3, 2, 5],
                   [6, 9, 4, 3, 2, 5, 1, 7, 8],
                   [3, 2, 5, 1, 7, 8, 6, 9, 4],
                   [7, 8, 1, 9, 4, 6, 2, 5, 3],
                   [9, 4, 6, 2, 5, 3, 7, 8, 1],
                   [2, 5, 3, 7, 8, 1, 9, 4, 6],
                   [8, 1, 7, 4, 6, 9, 5, 3, 2],
                   [4, 6, 9, 5, 3, 2, 8, 1, 7],
                   [5, 3, 2, 8, 1, 7, 4, 6, 9]])

if __name__ == "__main__":
    print(np.linalg.det(board1))
    print(np.linalg.det(board2))