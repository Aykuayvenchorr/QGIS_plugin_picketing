from .point import Point


class Picket:
    # Класс описания одного пикета:
    #   Северная координата
    #   Восточная координата
    #   НаименованиеЫ
    def __init__(self, point: Point = Point(), name: str = 'Noname') -> None:
        self.point: Point = point;
        self.name: str = name;

    def __str__(self) -> str:
        return f"{self.name}: (North: {self.point.north} East: {self.point.east})";

    def __repr__(self) -> str:
        return f"{self.__class__}: {self.name}"


if __name__ == "__main__":
    print(str(Picket(Point(10.0, 7.0), 'ПК0')));