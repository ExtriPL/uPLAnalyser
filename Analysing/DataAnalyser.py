from Analysing.AnalysedGroup import AnalysedGroup
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup
from Utilities.Logger import Logger


class DataAnalyser:
    __logger = Logger("Analyser")

    @staticmethod
    def analyse_measurement_groups(groups: list[MeasurementGroup], algorithms: list[AnalysingAlgorithm]) -> list[AnalysedGroup]:
        DataAnalyser.__logger.log("Start analysing " + str(len(groups)) + " group(s)")
        analysed_groups: list[AnalysedGroup] = []

        for group in groups:
            analysed_group = DataAnalyser.analyse_measurement_group(group, algorithms)
            analysed_groups.append(analysed_group)

        return analysed_groups

    @staticmethod
    def analyse_measurement_group(group: MeasurementGroup, algorithms: list[AnalysingAlgorithm]) -> AnalysedGroup:
        DataAnalyser.__logger.log("Analysing group \"" + group.name() + "\"")
        analysed_group = AnalysedGroup(group.name())

        for mesa in group.mesa_groups():
            analysed_mesas = DataAnalyser.analyse_mesa_group(mesa, algorithms)

            for analysed_mesa in analysed_mesas:
                analysed_group.add_analysed_mesa(analysed_mesa)

        return analysed_group

    @staticmethod
    def analyse_mesa_group(mesa: MesaGroup, algorithms: list[AnalysingAlgorithm]) -> list[AnalysedMesa]:
        DataAnalyser.__logger.log("Analysing mesa \"" + mesa.name() + "\"")
        analysed_mesas: list[AnalysedMesa] = []

        for algorithm in algorithms:
            DataAnalyser.__logger.log("Using algorithm \"" + algorithm.name() + "\"")
            analysed_mesa = algorithm.analyse(mesa)
            analysed_mesas.append(analysed_mesa)

        return analysed_mesas
