import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()


        self.rows = rows
        self.columns = columns
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)
        self.line_forklift = None
        self.column_forklift = None
        self.previousState = None
        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.FORKLIFT:
                    self.line_forklift = i
                    self.column_forklift = j
                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j


    def can_move_up(self) -> bool:
        if (self.matrix[self.line_forklift][self.column_forklift] == constants.PRODUCT):
            return False
        if (self.line_forklift != 0 and self.matrix[self.line_forklift - 1][self.column_forklift] == constants.EMPTY) \
                or (self.line_forklift != 0 and self.matrix[self.line_forklift - 1][self.column_forklift] == constants.EXIT):
            return True
        else:
            return False

    def can_move_right(self) -> bool:
        if (self.column_forklift != self.columns-1 and self.matrix[self.line_forklift][self.column_forklift + 1] == constants.EMPTY) \
            or (self.column_forklift != self.columns-1 and self.matrix[self.line_forklift][self.column_forklift + 1] == constants.EXIT):
            return True
        else:
            return False

    def can_move_down(self) -> bool:
        if (self.matrix[self.line_forklift][self.column_forklift] == constants.PRODUCT):
            return False
        if (self.line_forklift != self.rows-1 and self.matrix[self.line_forklift + 1][self.column_forklift] == constants.EMPTY) \
            or (self.line_forklift != self.rows-1 and self.matrix[self.line_forklift + 1][self.column_forklift] == constants.EXIT):
            return True
        else:
            return False

    def can_move_left(self) -> bool:
        if (self.column_forklift != 0 and self.matrix[self.line_forklift][self.column_forklift - 1] == constants.EMPTY) \
                or (self.column_forklift != 0 and self.matrix[self.line_forklift][self.column_forklift - 1] == constants.EXIT):
            return True
        else:
            return False

    def move_up(self) -> None:
        if (self.can_move_up()):
            if(self.matrix[self.line_forklift - 1][self.column_forklift] == constants.EXIT):        #verifica se a proxima posicao é a saida
                self.line_forklift = self.line_forklift - 1                                         #como é saida apenas movemos para lá o forklift sem alterar o valor da posicao(3 pois é saida)
            else:
                self.previousState = self.matrix[self.line_forklift - 1][self.column_forklift]      #guarda o valor inicial da posicao para onde o forklift vai
                self.matrix[self.line_forklift - 1][self.column_forklift] = constants.FORKLIFT      #coloca o valor do forklift(4) na posicao para onde vai
                self.line_forklift = self.line_forklift - 1                                         #atualiza a linha do forklift
            self.matrix[self.line_forklift + 1][self.column_forklift] = self.previousState          #decolve o valor incial da posicao de onde o forklift estava


    def move_right(self) -> None:
       if (self.can_move_right()):
           if (self.matrix[self.line_forklift][self.column_forklift + 1] == constants.EXIT):
                self.column_forklift = self.column_forklift + 1
           else:
                self.previousState = self.matrix[self.line_forklift][self.column_forklift + 1]
                self.matrix[self.line_forklift][self.column_forklift + 1] = constants.FORKLIFT
                self.column_forklift = self.column_forklift + 1
           self.matrix[self.line_forklift][self.column_forklift - 1] = self.previousState

    def move_down(self) -> None:
       if (self.can_move_down()):
           if (self.matrix[self.line_forklift + 1][self.column_forklift] == constants.EXIT):
                self.line_forklift = self.line_forklift + 1
           else:
                self.previousState = self.matrix[self.line_forklift + 1][self.column_forklift]
                self.matrix[self.line_forklift + 1][self.column_forklift] = constants.FORKLIFT
                self.line_forklift = self.line_forklift + 1
           self.matrix[self.line_forklift - 1][self.column_forklift] = self.previousState

    def move_left(self) -> None:
        if (self.can_move_left()):
            if (self.matrix[self.line_forklift][self.column_forklift - 1] == constants.EXIT):
                self.column_forklift = self.column_forklift - 1
            else:
                self.previousState = self.matrix[self.line_forklift][self.column_forklift - 1]
                self.matrix[self.line_forklift][self.column_forklift - 1] = constants.FORKLIFT
                self.column_forklift = self.column_forklift - 1
            self.matrix[self.line_forklift][self.column_forklift + 1] = self.previousState

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
