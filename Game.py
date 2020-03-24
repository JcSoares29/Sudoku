from inputBox import InputBox
from button import Button
from time import sleep

import funcoes as fn
import pygame
import copy
from random import randint


def criaSudokuTela(lst_sudoku):
    b = 1
    new_x = b + 0.5
    new_y = b + 0.5
    size = 60
    caixas_sudoku.clear()
    for i in range(9):
        for j in range(9):
            box_i = InputBox(new_x, new_y, size, size, color=pygame.Color('black'),
                             textColor=pygame.Color('black'), border=b)
            box_i.text = str(lst_sudoku[i][j]) if lst_sudoku[i][j] > 0 else ''
            box_i.txt_surface = box_i.font.render(box_i.text, True, box_i.textColor)
            if lst_sudoku[i][j] != 0:
                box_i.editable = False
            caixas_sudoku[(i, j)] = box_i
            new_x += size
        new_y += size
        new_x = b + 0.5


def preencheSudoku(lst_sudoku):
    b = 1
    size = 60
    for i in range(9):
        for j in range(9):
            quadrado_s = caixas_sudoku[(i, j)]
            if quadrado_s.text == "":
                lst_sudoku[i][j] = 0
            else:
                lst_sudoku[i][j] = int(quadrado_s.text)
            quadrado_s.draw(screen)

    new_x = b + 0.5
    new_y = b + 0.5
    for i in range(3):
        for j in range(3):
            box = InputBox(new_x, new_y, size * 3, size * 3, color=pygame.Color('black'),
                           textColor=pygame.Color('black'), border=5)
            box.draw(screen)
            new_x += 3 * size
        new_y += 3 * size
        new_x = b + 0.5


def atualizaTela():
    screen.fill((255, 255, 255))
    btnResolver.draw(screen)
    btnResetar.draw(screen)
    preencheSudoku(sudoku)
    for item in lst_botoes:
        item.draw(screen)
    pygame.display.update()


def resolveSudoku(lst_sudoku):
    lin, col = fn.encontralocalVazio(lst_sudoku)

    if lin == -1 and col == -1:
        return True

    for i in range(1, 10):
        if fn.validaPosicao(lst_sudoku, lin, col, i):
            sleep(0.1)
            caixas_sudoku[(lin, col)].text = str(i)
            caixas_sudoku[(lin, col)].txt_surface = caixas_sudoku[(lin, col)].font.render(str(i),
                                                                                          True, pygame.Color('black'))
            caixas_sudoku[(lin, col)].color = pygame.Color('black')
            atualizaTela()

            if resolveSudoku(lst_sudoku):
                return True

            caixas_sudoku[(lin, col)].text = ""
            caixas_sudoku[(lin, col)].txt_surface = caixas_sudoku[(lin, col)].font.render("",
                                                                                          True, pygame.Color('red'))
            caixas_sudoku[(lin, col)].color = pygame.Color('red')
            atualizaTela()
    return False


def desativaQuadrados(chave_atual):
    for chave, box in caixas_sudoku.items():
        if box != caixas_sudoku[chave_atual]:
            box.negate_active()


def acharQuadradoAtivo():
    for chave, box in caixas_sudoku.items():
        if caixas_sudoku[chave].active:
            return chave
    return None


def criaSudoku(sk):
    attempts = 40
    counter = 1
    while attempts > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while sk[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)
        backup = sk[row][col]
        sk[row][col] = 0

        copyGrid = []
        for r in range(0, 9):
            copyGrid.append([])
            for c in range(0, 9):
                copyGrid[r].append(sk[r][c])

        counter = 0
        if fn.ResolveSudoku(copyGrid):
            attempts -= 1
        else:
            sk[row][col] = backup
        # if counter != 1:
        #     sk[row][col] = backup
        #     attempts -= 1
    return sk


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((650, 610))

    pygame.display.set_caption('Sudoku')
    icon = pygame.image.load('sudoku.png')
    pygame.display.set_icon(icon)

    btnResolver = Button(50, 550, 100, 50, text="Resolver", color=pygame.Color('green'),
                         textColor=pygame.Color('black'))

    btnResetar = Button(200, 550, 100, 50, text="Resetar", color=pygame.Color('yellow'),
                        textColor=pygame.Color('black'))

    font = pygame.font.SysFont("comicsansms", 50)
    # txt_surface = font.render('Sudoku', True, textColor=pygame.Color('black'))

    caixas_sudoku = {}

    lst_botoes = []
    x_i = 580
    y_i = 10
    for it in range(1, 10):
        btn = Button(x_i, y_i, 50, 50, text=str(it), color=pygame.Color('black'),
                     textColor=pygame.Color('black'), border=1)
        lst_botoes.append(btn)
        y_i += 60

    solved_sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    fn.ResolveSudoku(solved_sudoku)

    new_sudoku = criaSudoku(solved_sudoku.copy())

    sudoku = copy.deepcopy(new_sudoku)

    criaSudokuTela(sudoku)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for key, value in caixas_sudoku.items():
                if value.editable:
                    value.handle_event(event)
                    if value.active:
                        desativaQuadrados(key)
            for btn in lst_botoes:
                btn.handle_event(event)
                if btn.active and event.type == pygame.MOUSEBUTTONDOWN:
                    key = acharQuadradoAtivo()
                    if key is not None:
                        caixas_sudoku[key].text = btn.text
                        if fn.validaPosicao(sudoku, key[0], key[1], int(caixas_sudoku[key].text)):
                            sudoku[key[0]][key[1]] = int(caixas_sudoku[key].text) \
                                if caixas_sudoku[key].text != '' else 0
                            caixas_sudoku[key].color = pygame.Color('black')
                            caixas_sudoku[key].txt_surface = caixas_sudoku[key].font.render(caixas_sudoku[key].text,
                                                                                            True, pygame.Color('black'))
                        else:
                            caixas_sudoku[key].txt_surface = caixas_sudoku[key].font.render(caixas_sudoku[key].text,
                                                                                            True, pygame.Color('red'))
                            caixas_sudoku[key].color = pygame.Color('red')

            btnResolver.handle_event(event)
            btnResetar.handle_event(event)

            if btnResolver.active:
                if not resolveSudoku(sudoku):
                    btnResolver.active = False

            if btnResetar.active:
                sudoku.clear()
                sudoku = copy.deepcopy(new_sudoku)
                criaSudokuTela(sudoku)

        atualizaTela()
