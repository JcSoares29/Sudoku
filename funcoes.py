def verifica_linha(grid, lin, valor):
    for i in range(0, 9):
        if grid[lin][i] == valor:
            return False
    return True


def verifica_coluna(grid, col, valor):
    for i in range(0, 9):
        if grid[i][col] == valor:
            return False
    return True


def verifica_3x3(grid, lin, col, valor):
    start_row = lin - (lin % 3)
    start_col = col - (col % 3)
    for i in range(0, 3):
        for j in range(0, 3):
            curr = grid[i + start_row][j + start_col]
            if curr == valor:
                return False
    return True


def validaPosicao(grid, lin, col, valor):
    if verifica_linha(grid, lin, valor) and \
            verifica_coluna(grid, col, valor) and \
            verifica_3x3(grid, lin, col, valor):
        return True
    return False


def encontralocalVazio(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                return i, j
    return -1, -1


def exibeSolucao(grid):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' ')
        print('')


def ResolveSudoku(grid):
    lin, col = encontralocalVazio(grid)

    if lin == -1 and col == -1:
        return True

    for i in range(1, 10):
        if validaPosicao(grid, lin, col, i):
            grid[lin][col] = i

            if ResolveSudoku(grid):
                return True

            grid[lin][col] = 0

    return False


# sudoku = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
#           [5, 2, 0, 0, 0, 0, 0, 0, 0],
#           [0, 8, 7, 0, 0, 0, 0, 3, 1],
#           [0, 0, 3, 0, 1, 0, 0, 8, 0],
#           [9, 0, 0, 8, 6, 3, 0, 0, 5],
#           [0, 5, 0, 0, 9, 0, 6, 0, 0],
#           [1, 3, 0, 0, 0, 0, 2, 5, 0],
#           [0, 0, 0, 0, 0, 0, 0, 7, 4],
#           [0, 0, 5, 2, 0, 6, 3, 0, 0]]
#
# # if success print the grid
# if ResolveSudoku(sudoku):
#     exibeSolucao(sudoku)
# else:
#     print("Não é possível resolver este sudoku")
