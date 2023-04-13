from abc import abstractmethod

from Analysing.AnalysedMesa import AnalysedMesa
from Measurements.MesaGroup import MesaGroup


class AnalysingAlgorithm:
    @abstractmethod
    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        pass
