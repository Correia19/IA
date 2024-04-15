
import copy

import constants
from agentsearch.problem import Problem
from warehouse.actions import *
from warehouse.cell import Cell
from warehouse.warehouse_state import WarehouseState


class WarehouseProblemSearch(Problem[WarehouseState]):

    def __init__(self, initial_state: WarehouseState, goal_position: Cell):
        super().__init__(initial_state)
        self.actions = [ActionDown(), ActionUp(), ActionRight(), ActionLeft()]
        self.goal_position = goal_position

    def get_actions(self, state: WarehouseState) -> list:
        valid_actions = []
        for action in self.actions:
            if action.is_valid(state):
                valid_actions.append(action)
        return valid_actions

    def get_successor(self, state: WarehouseState, action: Action) -> WarehouseState:
        successor = copy.deepcopy(state)
        action.execute(successor)
        return successor

    def is_goal(self, state: WarehouseState) -> bool:
        if(state.matrix[self.goal_position.line][self.goal_position.column] == constants.EXIT):                 #se o objetivo for uma saida verificamos se o agente coincide com a posicao da saida
                                                                                                                # se sim retornamos true
            return state.line_forklift == self.goal_position.line and \
                state.column_forklift == self.goal_position.column
        return state.line_forklift == self.goal_position.line and \
            abs(state.column_forklift - self.goal_position.column) == 1                                         # se não for uma saida vai ser um produto e verificamos se o agente se encontra num corredor ao lado
                                                                                                                # do produto que pretendemos recolher uma vez que apenas temos que passar ao lado para o recolher

