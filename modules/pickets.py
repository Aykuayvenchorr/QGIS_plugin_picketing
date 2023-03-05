from typing import List, NoReturn;
from .point import Point;
from .picket import Picket;
from .vector import Vector;


class Pickets:
    # Класс списка пикетов

    def __init__(self,  points: List[Point] = [], distance: float = 100.0, name_picket: str = 'ПК') -> NoReturn:
        self.__txt: str = name_picket;
        self.__line: List[Point] = points;
        self.__distance: float = distance;
        self.__domer: float = 0.0;
        self.__pickets: List[Picket] = [];
        self.__create_pickets();

    def __str__(self) -> str:
        st: str = '';
        for pk in self.__pickets:
            st += f'{pk} / ';
        return st;

    def __create_pickets(self) -> NoReturn:
        self.__pickets = [];
        self.__domer = 0.0;
        namepk = 0;
        for i, pnt in enumerate(self.__line):
            if (i == len(self.__line) - 1): return;
            if (i == 0):
                self.__pickets.append(Picket(pnt, f'{self.__txt}{namepk}'));
                namepk += 1;

            vector = Vector(pnt, self.__line[i+1]);

            if (vector.length() < (self.__distance - self.__domer)):
                self.__domer += vector.length();
                continue;

            if (vector.length() == (self.__distance - self.__domer)):
                self.__domer = 0.0;
                self.__pickets.append(Picket(pnt, f'{self.__txt}{namepk}'));
                namepk += 1;
                continue;

            if (vector.length() > (self.__distance - self.__domer)):
                l: float = self.__distance - self.__domer;
                while l <= vector.length():
                    p: Point = vector.point_on_distance(pnt, l);
                    self.__pickets.append(Picket(p, f'{self.__txt}{namepk}'));
                    self.__domer = 0.0;
                    l += (self.__distance - self.__domer);
                    namepk += 1;
                self.__domer = self.__distance - (l - vector.length());

    def change_line(self,  points: List[Point] = []) -> NoReturn:
        self.__line = points;
        self.__create_pickets();

    def change_name_picket(self,  name_picket: str = 'ПК') -> NoReturn:
        self.__txt = name_picket;
        self.__create_pickets();

    def change_distance(self,  distance: float = 100.0) -> NoReturn:
        self.__distance = distance;
        self.__create_pickets();

    def get(self) -> List[Picket]:
        return self.__pickets;



if __name__ == "__main__":
    line = [Point(0, 0), Point(150, 0), Point(150, 150), Point(0, 150)];
    p1 = Pickets(line);
    p1.get();
    print(p1);


