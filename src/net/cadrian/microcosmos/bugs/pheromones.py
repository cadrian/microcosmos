class PheromoneKind:
    def __init__(self, diffusion):
        self.diffusion = diffusion


class Pheromone:
    def __init__(self, kind, value):
        self.kind = kind
        self._value = value

    def fixScent(self, value):
        return self._value + value
