from Grid import Grid
import numpy as np

class GridNode:
    def __init__(self, parent, dirFromParent, grid, height):
        self.utility = 0
        self.parent = parent
        self.dirFromParent = dirFromParent
        self.grid = grid
        # JUST GETTING ALL THE AVAILABLE MOVES TAKES TOO FUCKING LONG
        # self.availableMoves = grid.getAvailableMoves()
        self.height = height
        pass

    def getHeight(self):
        return self.height

    def getMaxTile(self):
        return max([max(row) for row in self.grid.map])

    def cloneGrid(self):
        gridCopy = Grid()
        gridCopy.map = [[item for item in row] for row in self.grid.map]
        gridCopy.size = self.grid.size

        return gridCopy

    # def getAvailableMovesOptimal(self):
    #     map = self.grid.map
    #     map_t = np.array(self.grid.map).T.tolist()
    #     dirs = []
    #     for i in range(len(map)):
    #         print(f'ROW {i}: ', set(map[i]))
    #         if len(set(map[i])) < 4:
    #             if 0 in map[i][1:-1]:
    #                 dirs = dirs + [2, 3]
    #             elif 0 in map[0]:
    #                 dirs = dirs + [2]
    #             elif 0 in map[-1]:
    #                 dirs = dirs + [3]
    #         if len(set(map_t[i])) < 4:
    #             if 0 in map_t[i][1:-1]:
    #                 dirs = dirs + [0, 1]
    #             elif 0 in map_t[0]:
    #                 dirs = dirs + [0]
    #             elif 0 in map_t[-1]:
    #                 dirs = dirs + [1]
    #
    #     return list(set(dirs))

    def resolveChildren(self, max):
        generator = self.generatePlayerMaps if max else self.generateAversaryMaps
        return [self.createGridNode(grid, dir) for grid, dir in generator()]

    def createGridNode(self, grid, dir):
        return GridNode(self, dir, grid, self.height + 1)

    def generatePlayerMaps(self):
        maps = []
        for dir in self.grid.getAvailableMoves():
        # for dir in self.getAvailableMovesOptimal():
            # copy = state.clone()
            copy = self.cloneGrid()
            copy.move(dir)
            maps.append((copy, dir))
        return maps

    def generateAversaryMaps(self):
        state = self.grid
        maps = []

        for cell in state.getAvailableCells():
            # copy_2 = state.clone()
            # copy_4 = state.clone()
            copy_2 = self.cloneGrid()
            copy_4 = self.cloneGrid()

            copy_2.map[cell[0]][cell[1]] = 2
            copy_4.map[cell[0]][cell[1]] = 4

            maps.append((copy_2, '-'))
            maps.append((copy_4, '-'))
        return maps

    def eval(self):
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
        state = self.grid
        self.utility = (
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
        # length = len(grid)
        # return sum([
        #     sum([pow(grid[0][i], self.resolveExponent(i, 0, length)) for i in range(length)]),
        #     sum([pow(grid[1][i], self.resolveExponent(i, 1, length)) for i in range(length)]),
        #     sum([pow(grid[2][i], self.resolveExponent(i, 2, length)) for i in range(length)]),
        #     sum([pow(grid[3][i], self.resolveExponent(i, 3, length)) for i in range(length)])
        # ])
        return sum([
        sum([pow(grid[0][0], 0), pow(grid[0][1], 0), pow(grid[0][2], 0), pow(grid[0][3], 1)]),
        sum([pow(grid[1][0], 0), pow(grid[1][1], 0), pow(grid[1][2], 1), pow(grid[1][3], 2)]),
        sum([pow(grid[2][0], 0), pow(grid[2][1], 1), pow(grid[2][2], 2), pow(grid[2][3], 3)]),
        sum([pow(grid[3][0], 1), pow(grid[3][1], 2), pow(grid[3][2], 3), pow(grid[3][3], 4)])
        ])

    def highestTileInCorner(self, state):
        grid = state.map
        maxTile = self.maxTile
        return maxTile if grid[3][3] is maxTile else 0

    # def resolveExponent(self, i, row, length):
    #     print(f'\nExponent for: ({row}, {i}) is {i + 1 if (row - length + 1 + i) >= 0 else 0}')
    #     return i if ((i + row) - length) >= 0 else 0
