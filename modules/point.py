class Point:
    # Класс точки, хранящей расстояние на Север и Восток

    def __init__(self, north: float = 0.0, east: float = 0.0):
        self.north: float = north
        self.east: float = east

    def __complex__(self):
        return complex(self.east, self.north)

    def __add__(self, other):
        return Point(self.north + other.north, self.east + other.east)

    def __sub__(self, other):
        return Point(self.north - other.north, self.east - other.east)

    def __eq__(self, other):
        if self.north == other.north and self.east == other.east: return True
        return False

    def __str__(self):
        return 'North: ' + str(self.north) + ' East: ' + str(self.east)

    def __repr__(self):
        return f"{self.__class__}: {self}"
