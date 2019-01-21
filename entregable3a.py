import sys
from typing import *

from brikerdef import Move, Block, Level
from bt_scheme import PartialSolutionWithVisitedControl, Solution, State, BacktrackingVCSolver


def bricker_vc_solve(level: Level):
    class BrikerVC_PS(PartialSolutionWithVisitedControl):
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
                    yield BrikerVC_PS(self.block.move(move), self.decisions + (move,))

        def state(self) -> State:
            return self.block

    initial_block = Block(level.get_startpos(), level.get_startpos())
    initial_ps = BrikerVC_PS(initial_block, tuple())
    return BacktrackingVCSolver.solve(initial_ps)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso del programa: entregable3a.py <fichero_nivel.txt>")
        exit(-1)
    level_filename = sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")
    for solution in bricker_vc_solve(Level(level_filename)):
        print("".join(solution))
        break
    print("\n<END BACKTRACKING>")
