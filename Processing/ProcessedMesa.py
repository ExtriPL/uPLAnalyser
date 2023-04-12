from Measurements.MesaGroup import MesaGroup


class ProcessedMesa:
    def __init__(self, mesa_group: MesaGroup, algorithm: str):
        self.__mesa: MesaGroup = mesa_group
        self.__algorithm: str = algorithm

    def mesa(self):
        return self.__mesa

    def algorithm(self):
        return self.__algorithm
