from Analysing.AnalysedMesa import AnalysedMesa


class AnalysedGroup:
    def __init__(self, group_name: str):
        self.__group_name: str = group_name
        self.__analysed_mesa_groups: list[AnalysedMesa] = []

    def group_name(self) -> str:
        return self.__group_name

    def analysed_mesa_groups(self) -> list[AnalysedMesa]:
        return self.__analysed_mesa_groups

    def add_analysed_mesa(self, mesa: AnalysedMesa) -> None:
        self.__analysed_mesa_groups.append(mesa)