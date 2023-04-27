import numpy as np
from matplotlib import pyplot as plt

from Analysing.Algorithms.PreserveMaximaOverPowerAlgorithm import PreserveMaximaOverPowerAlgorithm

import scipy as sc

from Analysing.PeakStatistics import PeakStatistics
from Measurements.Measurement import Measurement


class MaxPeakIntensityOverPower(PreserveMaximaOverPowerAlgorithm):
    __algorithm_name: str = "MPIoP"

    def name(self) -> str:
        return MaxPeakIntensityOverPower.__algorithm_name

    def get_peaks(self, power_ordered_measurements: list[Measurement]) -> list[PeakStatistics]:
        strongest_measurement: Measurement = power_ordered_measurements[-1]
        data = MaxPeakIntensityOverPower.__combine_intensity(power_ordered_measurements)
        peaks, _ = sc.signal.find_peaks(data[1])

        statistics_list = []

        for i in range(len(peaks)):
            peak_index: int = peaks[i]
            wavelength: float = data[0][peak_index]
            score: float = data[1][peak_index]
            intensity_normalized: float = data[1][peak_index]
            intensity: float = data[2][peak_index]
            above_noise: bool = intensity > self.noise_threshold_multiplier() * strongest_measurement.background_noise()

            statistics: PeakStatistics = PeakStatistics(wavelength, intensity, intensity_normalized, score, peak_index, above_noise)
            statistics_list.append(statistics)

        return statistics_list

    @staticmethod
    def __combine_intensity(power_ordered_measurements: list[Measurement]) -> np.ndarray:
        first_data_normalized: np.ndarray = power_ordered_measurements[0].normalized_data()
        first_data: np.ndarray = power_ordered_measurements[0].data()
        data = np.empty((3, len(first_data_normalized[0])))

        data[0] = first_data_normalized[0]

        for i in range(len(first_data_normalized[0])):
            max_intensity_normalized = first_data_normalized[1][i]
            max_intensity = first_data[1][i]

            for measurement in power_ordered_measurements:
                intensity = measurement.normalized_data()[1][i]

                if intensity > max_intensity_normalized:
                    max_intensity_normalized = intensity
                    max_intensity = measurement.data()[1][i]

            data[1][i] = max_intensity_normalized
            data[2][i] = max_intensity

        return data
