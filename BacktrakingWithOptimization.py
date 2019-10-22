import sys
from typing import *

from brikerdef import Move, Block, Level
from bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, Solution, State


def bricker_opt_solve(level):
    class BrikerOpt_PS(PartialSolutionWithOptimization):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            self.block = block
            self.decisions = decisions

        def is_solution(self) -> bool:
            return self.block.is_standing_at_pos(level._tPos)

        def get_solution(self) -> Solution:
            return self.decisions

        def successors(self) -> Iterable["BrikerVC_PS"]:
            if not self.is_solution():
                for move in self.block.valid_moves(level.is_valid):
                    yield BrikerOpt_PS(self.block.move(move), self.decisions + (move,))

        def state(self) -> State:
            return self.block

        def f(self) -> Union[int, float]:
            return len(self.decisions)

    initial_block = Block(level.get_startpos(), level.get_startpos())
    initial_ps = BrikerOpt_PS(initial_block, tuple())
    return BacktrackingOptSolver.solve(initial_ps)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso del programa: entregable3b.py <fichero_nivel.txt>")
        exit(-1)
    level_filename = sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")
    solutions = list(bricker_opt_solve(Level(level_filename)))
    if len(solutions) == 0:
        print("No existe solución para este tablero.")
    else:
        print("".join(solutions[-1]))

    print("\n<END BACKTRACKING>")
