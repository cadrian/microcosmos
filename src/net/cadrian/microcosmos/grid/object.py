class LocatedObject:
    def __init__(self, grid):
        self.x = None
        self.y = None
        self.grid = grid

    def onGridPut(self, x, y):
        self.x = x
        self.y = y

    def onGridRemove(self, x, y):
        self.x = None
        self.y = None

    def moveTo(self, x, y):
        self.grid.remove(self.x, self.y, self)
        self.grid.put(x, y, self)

    def remove(self):
        self.grid.remove(self.x, self.y, self)
