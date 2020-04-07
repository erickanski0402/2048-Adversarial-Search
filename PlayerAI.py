from BaseAI import BaseAI
from GridNode import GridNode
from random import randint, random
from math import inf, sqrt
import numpy as np

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
MAX_HEIGHT = 4

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
        self.maxTile = 0
        pass

    def getMove(self, gridCopy):
        root = GridNode(None, None, gridCopy, 0)
        self.maxTile = gridCopy.getMaxTile()
        best = self.decision(root)
        # print('BEST', best)
        dir = self.getDirectionFromParent(best)
        return dir

        # moves = sorted(gridCopy.getAvailableMoves(), key = lambda x: random())
        # return moves[randint(0, len(moves ) - 1)] if moves else None

    def getDirectionFromParent(self, node):
        if node.parent.parent is None:
            return node.dirFromParent
        else:
            return self.getDirectionFromParent(node.parent)

    def minimize(self, state):
        # print('MINIMIZE STATE', state.dirFromParent)
        if self.terminalTest(state):
            return (None, self.eval(state))

        (minChild, minUtility) = (None, inf)

        for child in state.resolveChildren(False):
            (_, utility) = self.maximize(child)

            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            pass
        # cells = all possible next grids that:
        #   - Don't increase utility
        #
        # for <child> (grid object) in <calculated minimizing cells> (List of grid objects):
        #   (_, utility) = Maximize(child)
        #
        #   if utility < minUtility:
        #       (minChild, minUtility) = (child, utility)
        #
        # print('MIN CHILD ', minChild)
        return (minChild, minUtility)

    def maximize(self, state):
        # print('MAXIMIZE STATE', state.dirFromParent)
        if self.terminalTest(state):
            return (None, self.eval(state))

        (maxChild, maxUtility) = (None, -inf)

        for child in state.resolveChildren(True):
            (_, utility) = self.minimize(child)

            if self.eval(child) > maxUtility:
                (maxChild, maxUtility) = (child, utility)

        # moves = calculate grids possible given all legal moves
        # for <move> (grid object) in <all legal moves> (list of grid objects):
        #   (_, utility) = Minimize(move)
        #
        #   if utility > maxUtility:
        #       (maxChild, maxChild) = (child, utility)

        # print('MAX CHILD ', maxChild)
        return (maxChild, maxUtility)

    def decision(self, root):
        # print('ROOT', root)
        (child, _) = self.maximize(root)
        # print('CHILD', child)
        return child

    def terminalTest(self, node):
        # print('terminal test', state)
        state = node.grid
        if ((self.checkHeight(node))
        or (self.checkForAvailableMoves(state))
        or (self.checkForNewMaxTile(state))):
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

    def checkForAvailableMoves(self, state):
        return state.getAvailableMoves() is 0

    def checkForNewMaxTile(self, state):
        return state.getMaxTile() > self.maxTile

    def closeToGoodMerge(self, state):
        # - find the max tile
        # - check the row/col the max tile is on
        # - if there is another tile of that value in the row and/or col
        # - return true, else false
        maxTile = state.getMaxTile()
        map = state.map
        map_t = np.array(map).T.tolist()

        for i in range(len(map)):
            # print(map)
            if ((map[i].count(maxTile) > 1)
            or (map_t[i].count(maxTile) > 1)):
                return True
        return False

    def eval(self, node):
        # Ideas for utility function:
        #   1. Number of merges for a given direction
        #       i.e.: moving right results in 2 merges, whereas moving up results in 3 merges
        #   2. Number of open spaces after moving a direction:
        #       i.e.: moving up results in 5 open spaces, whereas moving up results in only 2 open spaces
        #   3. Increase in score based on merges
        #       i.e.: merging 2 and 2 adds 4 to the score, 4 and 4 yields 8, etc.
        #   4. Score based on all tiles on the board
        #   5. Combination of 2 and 4
        #
        # Return raw score of tiles greater than 2 plus the number of available cells squared
        #   incentivises score AND keeping the board as clear as possible
        #
        # How to insentivise the algorithm to focus on more tiles of higher values
        state = node.grid
        return (self.calculateRawScore(state)
        + self.calculateCellScore(state)
        + self.calculateSubCellScore(state))

    def calculateRawScore(self, state):
        # Calculates the raw score of the given state
        #   Based on tiles
        score = 0
        for row in state.map:
            for i in range(len(row)):
                # if row[i] is not 2:
                score += row[i]
        return score

    def calculateCellScore(self, state):
        return len(state.getAvailableCells()) * sqrt(state.getMaxTile())

    def calculateSubCellScore(self, state):
        # for each value in the grid, check the surrounding values (up, down, left, right)
        #   if the same value is found there add to the score weighted by the value of the cell
        score = 0
        map = state.map
        return score

    def generatePlayerMaps(self, state):
        moves = state.getAvailableMoves()
        maps = []

        for dir in moves:
            copy = state.clone()
            copy.move(dir)
            maps.append(copy)
        return maps

    def generateAversaryMaps(self, state):
        cells = state.getAvailableCells()
        maps = []

        for cell in cells:
            copy_2 = state.clone()
            copy_4 = state.clone()

            copy_2.map[cell[0]][cell[1]] = 2
            copy_4.map[cell[0]][cell[1]] = 4

            maps.append(copy_2)
            maps.append(copy_4)
        return maps

    # def getWorstMove(self, state):
    #     rowsThatCanMerge = []
    #     columnsThatCanMerge = []
    #     map = state.map
    #     transposeMap = np.array(map).T.tolist()
    #     availableCells = state.getAvailableCells()
    #
    #     for i in range(len(state.map)):
    #         if map[i].count(2) > 2:
    #             rowsThatCanMerge.append((2, i))
    #         elif map[i].count(4) > 2:
    #             rowsThatCanMerge.append((4, i))
    #
    #         if transposeMap[i].count(2) > 2:
    #             columnsThatCanMerge.append((2, i))
    #         elif transposeMap[i].count(4) > 2:
    #             columnsThatCanMerge.append((4, i))
    #
    #
    #     # cells = state.getAvailableCells()
    #     # for cell in cells:
    #     #     # Get all values in row and column
    #     #     rowVector = []
    #     #     colVector = []
    #     #     # if a 2 or 4 is found remove from list...?
    #     #     pass
    #     pass
    #
    # def resolveBadCell(self, cell, rows, cols):
    #     pass
