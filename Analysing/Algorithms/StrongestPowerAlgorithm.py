from abc import abstractmethod

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.PeakStatistics import PeakStatistics
from Measurements.Measurement import Measurement
from Measurements.MesaGroup import MesaGroup

import scipy as sc


class StrongestPowerAlgorithm(AnalysingAlgorithm):
    __algorithm_name: str = "SP"

    def __init__(self, best_peak_count: int, noise_threshold_multiplier: float = 1.0):
        self.__best_peak_count: int = best_peak_count
        self.__noise_threshold_multiplier: float = noise_threshold_multiplier

    def name(self) -> str:
        return StrongestPowerAlgorithm.__algorithm_name

    def best_peak_count(self) -> int:
        return self.__best_peak_count

    def noise_threshold_multiplier(self) -> float:
        return self.__noise_threshold_multiplier

    def get_peaks(self, power_ordered_measurements: list[Measurement]) -> list[PeakStatistics]:
        strongest_measurement = power_ordered_measurements[-1]
        peaks, _ = sc.signal.find_peaks(strongest_measurement.normalized_data()[1])
        prominences = sc.signal.peak_prominences(strongest_measurement.normalized_data()[1], peaks)[0]

        statistics_list = []

        for i in range(len(peaks)):
            peak_index: int = peaks[i]
            wavelength: float = strongest_measurement.data()[0][peak_index]
            score: float = prominences[i]
            intensity: float = strongest_measurement.data()[1][peak_index]
            intensity_normalized: float = strongest_measurement.normalized_data()[1][peak_index]
            above_noise: bool = intensity > self.__noise_threshold_multiplier * strongest_measurement.background_noise()

            statistics: PeakStatistics = PeakStatistics(wavelength, intensity, intensity_normalized, score, peak_index, above_noise)
            statistics_list.append(statistics)

        return statistics_list

    @abstractmethod
    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        pass
