from Measurements.Measurement import Measurement
from Measurements.MesaGroup import MesaGroup


class MeasurementGroup:
    def __init__(self, group_name: str):
        self.__group_name: str = group_name
        self.__backgrounds: dict[int, Measurement] = dict()
        self.__mesaGroups: list[MesaGroup] = []

    def name(self) -> str:
        return self.__group_name

    def backgrounds(self) -> dict[int, Measurement]:
        return self.__backgrounds

    def add_background(self, background: Measurement) -> None:
        integration_time = background.integration_time()
        self.__backgrounds[integration_time] = background

    def mesa_groups(self) -> list[MesaGroup]:
        return self.__mesaGroups

    def add_mesa_group(self, group: MesaGroup):
        self.__mesaGroups.append(group)
