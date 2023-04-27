import numpy as np

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.Algorithms.StrongestPowerAlgorithm import StrongestPowerAlgorithm
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.AnalysedSet import AnalysedSet
from Analysing.PeakStatistics import PeakStatistics
from Measurements.MesaGroup import MesaGroup
import scipy as sc


class PreserveMaximaOverPowerAlgorithm(StrongestPowerAlgorithm):
    __algorithm_name: str = "PMoP"

    def __init__(self, best_peak_count: int, noise_threshold_multiplier: float = 1.0, max_distance: float = 1.0):
        super().__init__(best_peak_count, noise_threshold_multiplier)
        self.__max_distance: float = max_distance

    def name(self) -> str:
        return PreserveMaximaOverPowerAlgorithm.__algorithm_name

    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        power_ordered_measurements = mesa.measurements()
        power_ordered_measurements.sort(key=AnalysingAlgorithm.measurement_power)

        peaks: list[PeakStatistics] = self.get_peaks(power_ordered_measurements)

        analysed_sets = []

        for peak in peaks:
            if not peak.is_above_noise():
                continue

            x: list[float] = []
            y: list[float] = []
            wavelengths = []

            analysed_wavelength = peak.wavelength()
            analysed_index = peak.index()

            for measurement in power_ordered_measurements:
                power = measurement.power()
                normalized_data = measurement.normalized_data()

                analysed_index = PreserveMaximaOverPowerAlgorithm.__find_closest_local_maximum_index(
                    normalized_data, analysed_wavelength, self.__max_distance, analysed_index)
                analysed_wavelength = normalized_data[0][analysed_index]
                intensity = normalized_data[1][analysed_index]

                wavelengths.append(analysed_wavelength)
                x.append(power)
                y.append(intensity)

            data: np.ndarray = np.empty((2, len(x)))
            data[0] = x
            data[1] = y
            analysed_set = AnalysedSet(np.array(wavelengths), data)
            analysed_set.set_score(peak.score())

            analysed_sets.append(analysed_set)

        analysed_sets.sort(key=AnalysingAlgorithm.score_analysed_set)
        analysed_mesa = AnalysedMesa(mesa, self.name())

        for analysed_set in analysed_sets[-self.best_peak_count():]:
            analysed_mesa.add_analysed_set(analysed_set)

        return analysed_mesa

    @staticmethod
    def __find_closest_local_maximum_index(data: np.ndarray, start_wavelength: float, max_distance: float, start_index: int) -> int:
        peaks, _ = sc.signal.find_peaks(data[1])
        distances = np.abs(data[0][peaks] - start_wavelength)

        peak_index = np.argmin(distances)

        if distances[peak_index] < max_distance:
            return peaks[peak_index]

        return start_index
