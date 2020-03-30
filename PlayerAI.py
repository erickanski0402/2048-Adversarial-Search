from random import randint
from BaseAI import BaseAI
from math import inf

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class PlayerAI(BaseAI):
    def __init__(self):
        pass

    def getMove(self, gridCopy):
        dir = self.decision(gridCopy)
        moves = gridCopy.getAvailableMoves()
        return moves[randint(0, len(moves ) - 1)] if moves else None


    # Cut off the recursion at some depth
    def minimize(self, gridCopy):
        moves = gridCopy.getAvailableMoves()
        if len(moves) is 0:
            return (None, gridCopy.getMaxTile())

        (minChild, minUtility) = (None, inf)

        for dir in moves:
            child = gridCopy.clone()
            child.move(dir)

            (_, utility) = self.maximize(child)

            if utility < minUtility:
                (minChild, minUtility) = (child, utility)

        return (minChild, minUtility)

    def maximize(self, gridCopy):
        moves = gridCopy.getAvailableMoves()
        if len(moves) is 0:
            return (None, gridCopy.getMaxTile())

        (maxChild, maxUtility) = (None, -inf)

        for dir in moves:
            child = gridCopy.clone()
            child.move(dir)

            (_, utility) = self.minimize(child)

            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)

        return (maxChild, maxUtility)

    def decision(self, gridCopy):
        (child, _) = self.maximize(gridCopy)
        return child
