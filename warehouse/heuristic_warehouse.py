from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()
        self._lines_goal_matrix = None
        self._cols_goal_matrix = None
        self.heuristic = None

    def compute(self, state: WarehouseState) -> float:
        self.heuristic = abs(state.line_forklift - self.problem.goal_position.line) + abs(state.column_forklift - self.problem.goal_position.column)
        return self.heuristic
        #esta funcao devolve a distancia do agente ao objetivo
    def __str__(self):
        return "Heuristic:" + str(self.heuristic)
