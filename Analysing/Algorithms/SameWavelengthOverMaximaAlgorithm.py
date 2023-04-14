import numpy as np

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.AnalysedSet import AnalysedSet
from Measurements.Measurement import Measurement
from Measurements.MesaGroup import MesaGroup

import scipy as sc


class SameWavelengthOverMaximaAlgorithm(AnalysingAlgorithm):
    __algorithm_name = "SWoM"

    def __init__(self, best_peak_count: int, noise_threshold_multiplier: float = 1.0):
        self.__best_peak_count: int = best_peak_count
        self.__noise_threshold_multiplier: float = noise_threshold_multiplier

    def name(self) -> str:
        return SameWavelengthOverMaximaAlgorithm.__algorithm_name

    def best_peak_count(self) -> int:
        return self.__best_peak_count

    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        def power_order_key(m: Measurement) -> int:
            return m.power()

        power_ordered_measurements = mesa.measurements()
        power_ordered_measurements.sort(key=power_order_key)

        strongest_measurement = power_ordered_measurements[-1]
        peaks, _ = sc.signal.find_peaks(strongest_measurement.normalized_data()[1])

        analysed_mesa = AnalysedMesa(mesa, SameWavelengthOverMaximaAlgorithm.__algorithm_name)
        analysed_sets = []

        def score_order_key(a_set: AnalysedSet) -> float:
            return a_set.score()

        for peak_index in peaks:
            wavelength = strongest_measurement.normalized_data()[0][peak_index]

            strongest_peak_intensity = strongest_measurement.normalized_data()[1][peak_index]

            if strongest_peak_intensity < self.__noise_threshold_multiplier * strongest_measurement.background_noise():
                continue

            x: list[float] = []
            y: list[float] = []

            for measurement in power_ordered_measurements:
                power = measurement.power()
                intensity = measurement.normalized_data()[1][peak_index]

                x.append(power)
                y.append(intensity)

            data: np.ndarray = np.empty((2, len(x)))
            data[0] = x
            data[1] = y
            analysed_set = AnalysedSet(wavelength, data)
            analysed_sets.append(analysed_set)

        analysed_sets.sort(key=score_order_key)

        for analysed_set in analysed_sets[-self.best_peak_count():]:
            analysed_mesa.add_analysed_set(analysed_set)

        return analysed_mesa
