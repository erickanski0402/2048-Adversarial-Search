from random import randint, random
from BaseAI import BaseAI
from math import inf

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


##################################DELETE ME#####################################
################################################################################
def winDisplay(grid):
    for i in range(grid.size):
        for j in range(grid.size):
            print("%6d  " % grid.map[i][j], end="")
        print("")
    print("")
################################################################################
################################################################################

class PlayerAI(BaseAI):
    def __init__(self):
        pass

    def getMove(self, gridCopy):
        dir = self.decision(gridCopy)
        
        moves = sorted(gridCopy.getAvailableMoves(), key = lambda x: random())
        return moves[randint(0, len(moves ) - 1)] if moves else None


    def minimize(self, state):
        if self.terminalTest(state):
            return (None, self.eval(state))

        (minChild, minUtility) = (None, inf)

        # cells = all possible next grids that:
        #   - Don't increase utility
        #
        # for <child> (grid object) in <calculated minimizing cells> (List of grid objects):
        #   (_, utility) = Maximize(child)
        #
        #   if utility < minUtility:
        #       (minChild, minUtility) = (child, utility)
        #
        return (minChild, minUtility)

    def maximize(self, state):
        if self.terminalTest(state):
            return (None, self.eval(state))

        (maxChild, maxUtility) = (None, -inf)

        # moves = calculate grids possible given all legal moves
        # for <move> (grid object) in <all legal moves> (list of grid objects):
        #   (_, utility) = Minimize(move)
        #
        #   if utility > maxUtility:
        #       (maxChild, minChild) = (child, utility)
        #
        return (maxChild, maxUtility)

    def decision(self, gridCopy):
        (child, _) = self.maximize(gridCopy)
        return child

    def terminalTest(self, state):
        # return a test of the following values:
        #   - No available moves remain
        #   -
        return False

    def eval(state):
        # Ideas for utility function:
        #   -number of merges for a given direction
        #       i.e.: moving right results in 2 merges, whereas moving up results in 3 merges
        #   -Number of open spaces after moving a direction:
        #       i.e.: moving up results in 5 open spaces, whereas moving up results in only 2 open spaces
        #  - Increase in score based on merges
        #       i.e.: merging 2 and 2 adds 4 to the score, 4 and 4 yields 8, etc.
        return 0
