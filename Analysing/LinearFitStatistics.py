class LinearFitStatistics:
    def __init__(self, slope: float, intercept: float, r_value: float, point_count: int):
        self.__slope: float = slope
        self.__intercept: float = intercept
        self.__r_value: float = r_value
        self.__point_count: int = point_count

    def slope(self) -> float:
        return self.__slope

    def intercept(self) -> float:
        return self.__intercept

    def r_value(self) -> float:
        return self.__r_value

    def point_count(self) -> int:
        return self.__point_count

    def get_statistics(self) -> list[str]:
        return [
            "slope: " + str(self.slope()),
            "intercept: " + str(self.intercept()),
            "r_value: " + str(self.r_value()),
            "point_count: " + str(self.point_count())
        ]
