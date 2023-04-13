from Analysing.AnalysedGroup import AnalysedGroup
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup


class DataAnalyser:
    @staticmethod
    def analyse_measurement_groups(groups: list[MeasurementGroup], algorithms: list[AnalysingAlgorithm]) -> list[AnalysedGroup]:
        analysed_groups: list[AnalysedGroup] = []

        for group in groups:
            analysed_group = DataAnalyser.analyse_measurement_group(group, algorithms)
            analysed_groups.append(analysed_group)

        return analysed_groups

    @staticmethod
    def analyse_measurement_group(group: MeasurementGroup, algorithms: list[AnalysingAlgorithm]) -> AnalysedGroup:
        analysed_group = AnalysedGroup(group.name())

        for mesa in group.mesa_groups():
            analysed_mesas = DataAnalyser.analyse_mesa_group(mesa, algorithms)

            for analysed_mesa in analysed_mesas:
                analysed_group.add_analysed_mesa(analysed_mesa)

        return analysed_group

    @staticmethod
    def analyse_mesa_group(mesa: MesaGroup, algorithms: list[AnalysingAlgorithm]) -> list[AnalysedMesa]:
        analysed_mesas: list[AnalysedMesa] = []

        for algorithm in algorithms:
            analysed_mesa = algorithm.analyse(mesa)
            analysed_mesas.append(analysed_mesa)

        return analysed_mesas
