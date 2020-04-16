from BaseAI import BaseAI
from GridNode import GridNode
from random import randint, random
from math import inf, sqrt, log
import numpy as np

MAX_HEIGHT = 3

class PlayerAI(BaseAI):
    def __init__(self):
        self.maxTile = 0
        pass

    def getMove(self, gridCopy):
        self.maxTile = gridCopy.getMaxTile()
        # There is a bug where it appears that the min/max algorithm returns
        #   before any children are spawned, so no parent exists to get the
        #   direction from.
        #   Simple solution is to try to get the dir from parent and catch any
        #   exceptions and choose a random direction
        return self.getDirectionFromParent(
            self.decision(GridNode(None, None, gridCopy, 0))
        )

    def getDirectionFromParent(self, node):
        return (node.dirFromParent if node.parent.parent is None
                else self.getDirectionFromParent(node.parent))

    def minimize(self, state, alpha, beta):
        if self.terminalTest(state):
            state.eval()
            return (None, state.utility)

        (minChild, minUtility) = (None, inf)

        for child in state.resolveChildren(False):
            (_, utility) = self.maximize(child, alpha, beta)

            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            pass

            if minUtility <= alpha:
                break

            if minUtility <= beta:
                beta = minUtility

        return (minChild, minUtility)

    def maximize(self, state, alpha, beta):
        if self.terminalTest(state):
            state.eval()
            return (None, state.utility)

        (maxChild, maxUtility) = (None, -inf)

        for child in state.resolveChildren(True):
            (_, utility) = self.minimize(child, alpha, beta)

            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)

            if utility >= beta:
                break

            if utility > alpha:
                alpha = maxUtility

        return (maxChild, maxUtility)

    def decision(self, root):
        (child, _) = self.maximize(root, -inf, inf)
        return child

    def terminalTest(self, node):
        state = node.grid
        if (self.checkForNewMaxTile(node)
        or self.checkHeight(node)
        or self.checkForAvailableMoves(node)):
        # or node.getAvailableMovesOptimal()):
        # or (self.closeToGoodMerge(state))):
            return True
        # return a test of the following values:
        #   - No available moves remain
        #   - Max cell value has increased
        #   - Next move will lead to a merge
        #   - Depth limiting (short-sighted), No.
        return False

    def checkHeight(self, node):
        return node.getHeight() > MAX_HEIGHT

    def checkForAvailableMoves(self, node):
        # Get available moves is a HUGE bottleneck
        return len(node.grid.getAvailableMoves()) is 0
        # return not node.availableMoves

    def checkForNewMaxTile(self, node):
        return node.getMaxTile() > self.maxTile

    # def closeToGoodMerge(self, state):
    #     # - find the max tile
    #     # - check the row/col the max tile is on
    #     # - if there is another tile of that value in the row and/or col
    #     # - return true, else false
    #     maxTile = state.getMaxTile()
    #     map = state.map
    #     map_t = np.array(map).T.tolist()
    #
    #     for i in range(len(map)):
    #         if ((map[i].count(maxTile) > 1)
    #         or (map_t[i].count(maxTile) > 1)):
    #             return True
    #     return False

    # def generatePlayerMaps(self, state):
    #     moves = state.getAvailableMoves()
    #     maps = []
    #
    #     for dir in moves:
    #         copy = state.clone()
    #         copy.move(dir)
    #         maps.append(copy)
    #     return maps
    #
    # def generateAversaryMaps(self, state):
    #     cells = state.getAvailableCells()
    #     maps = []
    #
    #     for cell in cells:
    #         copy_2 = state.clone()
    #         copy_4 = state.clone()
    #
    #         copy_2.map[cell[0]][cell[1]] = 2
    #         copy_4.map[cell[0]][cell[1]] = 4
    #
    #         maps.append(copy_2)
    #         maps.append(copy_4)
    #     return maps
