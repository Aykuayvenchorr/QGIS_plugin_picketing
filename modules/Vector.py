from modules.point import Point
from modules.angle import rad2grad
import cmath


class Vector:
    # Класс вектора: направленной линии от точки start к точке end

    def __init__(self, point_start: Point, point_end: Point):
        self.point_start = point_start
        self.point_end = point_end

        self.__complex_point_start = complex(point_start)
        self.__complex_point_end = complex(point_end)
        self.__complex_vector = self.__complex_point_end - self.__complex_point_start
        self.__length, self.__phase = cmath.polar(self.__complex_vector)

    def __complex__(self):
        return self.__complex_vector

    def __repr__(self):
        return f"{self.__class__}: {self}"

    def length(self):
        # Длина вектора
        # return abs(self.__complex_vector)
        return self.__length

    def direction(self):
        # Дирекционный угол вектора (радианы)
        if self.__complex_vector.imag == 0.0:
            if self.__complex_vector.real > 0.0:
                return cmath.pi / 2.0
            elif self.__complex_vector.real == 0.0:
                return 0.0
            else:
                return cmath.pi + cmath.pi / 2.0
        elif self.__complex_vector.imag > 0.0:
            if self.__complex_vector.real >= 0.0:
                return cmath.pi / 2.0 - self.__phase
            else:
                return 2 * cmath.pi + cmath.pi / 2.0 - self.__phase
        else:
            return cmath.pi / 2.0 - self.__phase
        # if (self.__complex_vector.imag == 0.0):
        #     if (self.__complex_vector.real > 0.0): return cmath.pi/2.0
        #     elif (self.__complex_vector.real == 0.0): return 0.0
        #     else: return cmath.pi + cmath.pi / 2.0
        # elif (self.__complex_vector.imag > 0.0):
        #     if (self.__complex_vector.real >= 0.0): return cmath.pi/2.0 - cmath.phase(self.__complex_vector)
        #     else: return 2 * cmath.pi + cmath.pi/2.0 - cmath.phase(self.__complex_vector)
        # else: return cmath.pi/2.0 - cmath.phase(self.__complex_vector)

    def point_on_distance(self, point: Point, length: float):
        # Точка на указанном расстоянии от указанной точки по направлению вектора
        temp_c = cmath.rect(length, self.__phase)
        temp_p = Point(temp_c.imag, temp_c.real)
        return point + temp_p


if __name__ == "__main__":
    p1 = Point()
    p2 = Point(3.0, -3.0)
    v1 = Vector(p1, p2)
    print(v1.direction())
    print(rad2grad(v1.direction()))
    print(v1.point_on_distance(p2, 1.414213562373095))
