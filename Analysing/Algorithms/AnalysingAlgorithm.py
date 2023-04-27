from abc import abstractmethod

from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.AnalysedSet import AnalysedSet
from Analysing.PeakStatistics import PeakStatistics
from Measurements.Measurement import Measurement
from Measurements.MesaGroup import MesaGroup


class AnalysingAlgorithm:
    @abstractmethod
    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_peaks(self, power_ordered_measurements: list[Measurement]) -> list[PeakStatistics]:
        pass

    @staticmethod
    def score_analysed_set(a_set: AnalysedSet) -> float:
        return a_set.score()

    @staticmethod
    def measurement_power(m: Measurement) -> float:
        return m.power()  # order from lowest to highest
