from __future__ import annotations
import matplotlib.axes
import numpy as np


class Measurement:
    def __init__(self, integration_time: int, power_string: str, data: np.ndarray):
        self.__integration_time: int = integration_time
        self.__power: int = Measurement.__power_from_name(power_string)
        self.__data: np.ndarray = data
        self.__normalized_data: np.ndarray = Measurement.__transfer_data_to_intensity_per_second(data, integration_time)
        self.__label: str = Measurement.__create_label(integration_time, power_string)
        self.__normalized_label: str = power_string
        self.__background_noise: float = 0

    def integration_time(self) -> int:
        return self.__integration_time

    def power(self) -> int:
        return self.__power

    def label(self) -> str:
        return self.__label

    def normalized_data(self) -> np.ndarray:
        return self.__normalized_data

    def data(self) -> np.ndarray:
        return self.__data

    def background_noise(self) -> float:
        return self.__background_noise

    def subtract(self, measurement: Measurement) -> None:
        self.__data[1] = np.subtract(self.__data[1], measurement.__data[1])
        self.__generate_normalized_data()

    def bring_to_zero(self) -> None:
        data_length: int = len(self.__data[1])
        sample_count: int = int(data_length * 0.05)
        left_mean = np.mean(self.__data[1][:sample_count])
        right_mean = np.mean(self.__data[1][-sample_count:])

        shift: float = (left_mean + right_mean) / 2.0

        self.__data[1] -= shift
        self.__generate_normalized_data()
        self.__background_noise = max(abs(left_mean - shift), abs(right_mean - shift))

    def plot(self, ax: matplotlib.axes.Axes) -> None:
        x = self.__data[0]
        y = self.__data[1]

        self.__plot_internal(ax, x, y, self.label())

    def plot_normalized(self, ax: matplotlib.axes.Axes) -> None:
        x = self.__normalized_data[0]
        y = self.__normalized_data[1]

        self.__plot_internal(ax, x, y, self.__normalized_label)

    def __generate_normalized_data(self) -> None:
        self.__normalized_data = Measurement.__transfer_data_to_intensity_per_second(self.__data, self.integration_time())

    @staticmethod
    def __plot_internal(ax: matplotlib.axes.Axes, x, y, label) -> None:
        ax.plot(x, y, label=label, linewidth=0.5)

    @staticmethod
    def __create_label(integration_time: int, power_string: str) -> str:
        return str(integration_time) + "s_" + power_string

    @staticmethod
    def __transfer_data_to_intensity_per_second(data, integration_time: int) -> np.ndarray:
        _normalizedData = np.array(data)
        _normalizedData[1] /= integration_time

        return _normalizedData

    @staticmethod
    def __power_from_name(power_name: str) -> int:
        if len(power_name) == 0:
            return 0

        suffix = "nW"
        multiplier = 1

        if power_name.endswith("uW"):
            suffix = "uW"
            multiplier *= 1000

        return int(power_name.removesuffix(suffix)) * multiplier
