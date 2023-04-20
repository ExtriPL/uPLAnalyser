import numpy as np

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.AnalysedMesa import AnalysedMesa
from Analysing.AnalysedSet import AnalysedSet
from Measurements.Measurement import Measurement
from Measurements.MesaGroup import MesaGroup
import scipy as sc


class PreserveMaximaOverPowerAlgorithm(AnalysingAlgorithm):
    __algorithm_name: str = "PMoP"

    def __init__(self, best_peak_count: int, noise_threshold_multiplier: float = 1.0):
        self.__best_peak_count: int = best_peak_count
        self.__noise_threshold_multiplier: float = noise_threshold_multiplier

    def name(self) -> str:
        return PreserveMaximaOverPowerAlgorithm.__algorithm_name

    def best_peak_count(self) -> int:
        return self.__best_peak_count

    def analyse(self, mesa: MesaGroup) -> AnalysedMesa:
        def power_order_key(m: Measurement) -> int:
            return -m.power()  # order from highest to lowest

        power_ordered_measurements = mesa.measurements()
        power_ordered_measurements.sort(key=power_order_key)

        strongest_measurement = power_ordered_measurements[0]
        peaks, _ = sc.signal.find_peaks(strongest_measurement.normalized_data()[1])
        prominences = sc.signal.peak_prominences(strongest_measurement.normalized_data()[1], peaks)[0]

        analysed_sets = []

        def score_order_key(a_set: AnalysedSet) -> float:
            return a_set.score()

        for i in range(len(peaks)):
            strongest_peak_index = peaks[i]
            strongest_wavelength = strongest_measurement.normalized_data()[0][strongest_peak_index]
            strongest_peak_intensity = strongest_measurement.data()[1][strongest_peak_index]

            if strongest_peak_intensity < self.__noise_threshold_multiplier * strongest_measurement.background_noise():
                continue

            x: list[float] = []
            y: list[float] = []
            wavelengths = []

            analysed_wavelength = strongest_wavelength

            for measurement in power_ordered_measurements:
                power = measurement.power()
                normalized_data = measurement.normalized_data()

                peak_index = PreserveMaximaOverPowerAlgorithm.__find_closest_local_maximum_index(normalized_data, analysed_wavelength)
                analysed_wavelength = normalized_data[0][peak_index]
                intensity = normalized_data[1][peak_index]

                wavelengths.append(analysed_wavelength)
                x.append(power)
                y.append(intensity)

            data: np.ndarray = np.empty((2, len(x)))
            """
            # inverse data because measurements are evaluated from highest to lowest in power 
                and we want to process fit with measurements from lowest to highest
            """
            data[0] = x[::-1]
            data[1] = y[::-1]
            analysed_set = AnalysedSet(np.array(wavelengths[::-1]), data)
            analysed_set.set_score(prominences[i])

            analysed_sets.append(analysed_set)

        analysed_sets.sort(key=score_order_key)
        analysed_mesa = AnalysedMesa(mesa, self.name())

        for analysed_set in analysed_sets[-self.best_peak_count():]:
            analysed_mesa.add_analysed_set(analysed_set)

        return analysed_mesa

    @staticmethod
    def __find_closest_local_maximum_index(data: np.ndarray, start_wavelength: float) -> int:
        peaks, _ = sc.signal.find_peaks(data[1])
        distances = np.abs(data[0][peaks] - start_wavelength)

        peak_index = np.argmin(distances)
        return peaks[peak_index]

