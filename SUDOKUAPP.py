
import pygame
import time
from Tkinter import *


inicio = time.time()


pygame.font.init()

# INICIO ALGORITMO IA

# BUSCAR LINHA E COLUNA VAZIA


def procurar_lugar_vazio(arr, l):
    for row in range(9):
        for col in range(9):
            if(arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


def usado_na_linha(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False


def usado_na_coluna(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False


def usado_no_quadro(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if(arr[i+row][j+col] == num):
                return True
    return False


def verificar_disponibilidade(arr, row, col, num):

    return not usado_na_linha(arr, row, num) and not usado_na_coluna(arr, col, num) and not usado_no_quadro(arr, row - row % 3, col - col % 3, num)

# ALGORITMO DE PROFUNDIDADE


def sudoku_resolucao(arr):
    l = [0, 0]

    # procurar onde esta vazio
    if(not procurar_lugar_vazio(arr, l)):
        return True

    # Pegar as coordenadas para procurar um numero valido
    row = l[0]
    col = l[1]

    # Preencher o numero
    for num in range(1, 10):

        # verificar um numero disponivel
        if(verificar_disponibilidade(arr, row, col, num)):

            # preencher
            arr[row][col] = num

            # Se for um numero ok, sair
            if(sudoku_resolucao(arr)):
                return True

            # caso errado preencher com 0 e procurar outro
            arr[row][col] = 0

    return False

# FINAL ALGORITMO IA

# INICIO INTERFACE E MAIN


class Grid:
    # To change the starting board change this
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def atualizar_modelo(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[int(row)][int(col)].value == 0:
            self.cubes[row][col].set(val)
            self.atualizar_modelo()
            Grid.board[row][col] = val

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0),
                             (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height, master=None):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))

        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                            y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def desenhar_aplicativo(win, board, solucao, solved):
    win.fill((213, 218, 247))  # COR DO FUNDO
    fnt = pygame.font.SysFont("comicsans", 40)
    # Draw solucao
    text = fnt.render("SEM SOLUCAO" * solucao, 1, (255, 0, 0))
    win.blit(text, (20, 560))

    text = fnt.render("PARABENS!" * solved, 1, (000, 255, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    solucao = 0
    solved = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_DELETE:
                    i, j = board.selected
                    board.place(0)

                    board = Grid(9, 9, 540, 540)
                    key = 0

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        board.place(board.cubes[i][j].temp)

                if event.key == pygame.K_F5:
                    Grid.board = [
                        [7, 8, 0, 4, 0, 0, 1, 2, 0],
                        [6, 0, 0, 0, 7, 5, 0, 0, 9],
                        [0, 0, 0, 6, 0, 1, 0, 7, 8],
                        [0, 0, 7, 0, 4, 0, 2, 6, 0],
                        [0, 0, 1, 0, 5, 0, 9, 3, 0],
                        [9, 0, 4, 0, 6, 0, 0, 0, 5],
                        [0, 7, 0, 3, 0, 0, 0, 1, 2],
                        [1, 2, 0, 0, 0, 7, 4, 0, 0],
                        [0, 4, 9, 2, 0, 6, 0, 0, 7]
                    ]

                    board = Grid(9, 9, 540, 540)

                if event.key == pygame.K_SPACE:
                    if(sudoku_resolucao(Grid.board)):
                        solucao = 0
                        solved = 1
                        board = Grid(9, 9, 540, 540)
                    else:
                        solucao = 1

                    if(sudoku_resolucao(Grid.board)):
                        board = Grid(9, 9, 540, 540)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    Grid.board[clicked[0]][clicked[1]] = 0
                    key = 0

                if(solved == 1 or solucao == 1):
                    Grid.board = [
                        [7, 8, 0, 4, 0, 0, 1, 2, 0],
                        [6, 0, 0, 0, 7, 5, 0, 0, 9],
                        [0, 0, 0, 6, 0, 1, 0, 7, 8],
                        [0, 0, 7, 0, 4, 0, 2, 6, 0],
                        [0, 0, 1, 0, 5, 0, 9, 3, 0],
                        [9, 0, 4, 0, 6, 0, 0, 0, 5],
                        [0, 7, 0, 3, 0, 0, 0, 1, 2],
                        [1, 2, 0, 0, 0, 7, 4, 0, 0],
                        [0, 4, 9, 2, 0, 6, 0, 0, 7]
                    ]

                    board = Grid(9, 9, 540, 540)
                    solved = 0
                    solucao = 0
        if board.selected and key != None:
            board.sketch(key)

        desenhar_aplicativo(win, board, solucao, solved)
        pygame.display.update()


main()
pygame.quit()
fim = time.time()
print(fim - inicio)
# FINAL INTERFACE E MAIN
