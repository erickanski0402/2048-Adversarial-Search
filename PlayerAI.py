from BaseAI import BaseAI
from GridNode import GridNode
from random import randint, random
from math import inf, sqrt, log
import numpy as np

MAX_HEIGHT = 4

class PlayerAI(BaseAI):
    def __init__(self):
        self.maxTile = 0
        pass

    def getMove(self, gridCopy):
        self.maxTile = gridCopy.getMaxTile()
        return self.getDirectionFromParent(
            self.decision(GridNode(None, None, gridCopy, 0))
        )

    def getDirectionFromParent(self, node):
        return (node.dirFromParent if node.parent.parent is None
                else self.getDirectionFromParent(node.parent))

    def minimize(self, state, alpha, beta):
        if self.terminalTest(state):
            return (None, self.eval(state))

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
            return (None, self.eval(state))

        (maxChild, maxUtility) = (None, -inf)

        for child in state.resolveChildren(True):
            (_, utility) = self.minimize(child, alpha, beta)

            if self.eval(child) > maxUtility:
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
        if (self.checkHeight(node)
        or self.checkForAvailableMoves(state)
        or self.checkForNewMaxTile(state)):
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
        return (
                # self.calculateRawScore(state) +
                # self.calculateCellScore(state) * sqrt(state.getMaxTile()) +
                # self.calculateSubCellScore(state) +
                self.calculateWeightedRowScores(state) +
                # self.highestTileInCorner(state) +
                0
        )

    def calculateRawScore(self, state):
        # Calculates the raw score of the given state
        #   Based on tiles
        return sum(map(sum, state.map))
        # return sum([sum(row) for row in state.map])

    def calculateCellScore(self, state):
        return len(state.getAvailableCells())

    def calculateSubCellScore(self, state):
        # for each value in the grid, check the surrounding values (up, down, left, right)
        #   if the same value is found there add to the score weighted by the value of the cell
        score = 0
        return score

    def calculateWeightedRowScores(self, state):
        grid = state.map
        length = len(grid)
        # return sum([
        #     sum([grid[0][i] ** resolveExponent(i, 0, length) for i in range(length)]),
        #     sum([grid[1][i] ** resolveExponent(i, 1, length) for i in range(length)]),
        #     sum([grid[2][i] ** resolveExponent(i, 2, length) for i in range(length)]),
        #     sum([grid[3][i] ** resolveExponent(i, 3, length) for i in range(length)])
        # ])
        return sum([
            sum([grid[0][0] ** 0, grid[0][1] ** 0, grid[0][2] ** 0, grid[0][3] ** 1]),
            sum([grid[1][0] ** 0, grid[1][1] ** 0, grid[1][2] ** 1, grid[1][3] ** 2]),
            sum([grid[2][0] ** 0, grid[2][1] ** 1, grid[2][2] ** 2, grid[2][3] ** 3]),
            sum([grid[3][0] ** 1, grid[3][1] ** 2, grid[3][2] ** 3, grid[3][3] ** 4])
        ])
        # return sum([grid[3][0], grid[3][1] ** 2, grid[3][2] ** 3, grid[3][3] ** 4])

    def highestTileInCorner(self, state):
        grid = state.map
        maxTile = self.maxTile
        return maxTile if grid[3][3] is maxTile else 0

    def resolveExponent(self, i, row):
        return i if ((i + row) - length) >= 0 else 0

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
