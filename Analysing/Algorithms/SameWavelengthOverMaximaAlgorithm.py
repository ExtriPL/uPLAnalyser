import numpy as np

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.Algorithms.StrongestPowerAlgorithm import StrongestPowerAlgorithm
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.AnalysedSet import AnalysedSet
from Analysing.PeakStatistics import PeakStatistics
from Measurements.MesaGroup import MesaGroup


class SameWavelengthOverMaximaAlgorithm(StrongestPowerAlgorithm):
    __algorithm_name: str = "SWoM"

    def __init__(self, best_peak_count: int, noise_threshold_multiplier: float = 1.0):
        super().__init__(best_peak_count, noise_threshold_multiplier)

    def name(self) -> str:
        return SameWavelengthOverMaximaAlgorithm.__algorithm_name

    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        power_ordered_measurements = mesa.measurements()
        power_ordered_measurements.sort(key=AnalysingAlgorithm.measurement_power)
        peaks: list[PeakStatistics] = self.get_peaks(power_ordered_measurements)

        analysed_mesa = AnalysedMesa(mesa, self.name())
        analysed_sets = []

        def score_order_key(a_set: AnalysedSet) -> float:
            return a_set.score()

        for peak in peaks:
            if peak.is_above_noise():
                continue

            wavelength = peak.wavelength()

            x: list[float] = []
            y: list[float] = []

            for measurement in power_ordered_measurements:
                power = measurement.power()
                intensity = measurement.normalized_data()[1][peak.index()]

                x.append(power)
                y.append(intensity)

            data: np.ndarray = np.empty((2, len(x)))
            data[0] = x
            data[1] = y
            analysed_set = AnalysedSet(np.repeat(wavelength, len(data[1])), data)
            analysed_set.set_score(peak.score())

            analysed_sets.append(analysed_set)

        analysed_sets.sort(key=score_order_key)

        for analysed_set in analysed_sets[-self.best_peak_count():]:
            analysed_mesa.add_analysed_set(analysed_set)

        return analysed_mesa
