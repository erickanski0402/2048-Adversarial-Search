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
        children = []
        if max:
            for dir, grid in self.generatePlayerMaps():
                children.append(GridNode(self, dir, grid, self.height + 1))
        else:
            for grid in self.generateAversaryMaps():
                children.append(GridNode(self, "-", grid, self.height + 1))

        return children

    def generatePlayerMaps(self):
        state = self.grid
        moves = state.getAvailableMoves()
        maps = []

        for dir in moves:
            copy = state.clone()
            copy.move(dir)
            maps.append((dir, copy))
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

            maps.append(copy_2)
            maps.append(copy_4)
        return maps
