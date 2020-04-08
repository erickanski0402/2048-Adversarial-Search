class GridNode:
    def __init__(self, parent, dirFromParent, grid, height):
        self.parent = parent
        self.dirFromParent = dirFromParent
        self.grid = grid
        self.height = height
        pass

    def getHeight(self):
        return self.height

    def resolveChildren(self, max):
        generator = self.generatePlayerMaps if max else self.generateAversaryMaps
        return [self.createGridNode(grid, dir) for grid, dir in generator()]

    def createGridNode(self, grid, dir):
        return GridNode(self, dir, grid, self.height + 1)

    def generatePlayerMaps(self):
        state = self.grid
        moves = state.getAvailableMoves()
        maps = []

        for dir in moves:
            copy = state.clone()
            copy.move(dir)
            maps.append((copy, dir))
        return maps

    def generateAversaryMaps(self):
        state = self.grid
        cells = state.getAvailableCells()
        maps = []

        for cell in cells:
            copy_2 = state.clone()
            copy_4 = state.clone()

            copy_2.map[cell[0]][cell[1]] = 2
            copy_4.map[cell[0]][cell[1]] = 4

            maps.append((copy_2, '-'))
            maps.append((copy_4, '-'))
        return maps
