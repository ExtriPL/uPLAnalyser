import matplotlib.axes

from Measurements.Measurement import Measurement
import matplotlib.pyplot as plt


class MesaGroup:
    def __init__(self, name:str):
        self.__name: str = name
        self.__measurements: list[Measurement] = []

    def name(self) -> str:
        return self.__name

    def measurements(self) -> list[Measurement]:
        return self.__measurements

    def add_measurement(self, measurement: Measurement) -> None:
        self.__measurements.append(measurement)

    def plot_data(self):
        ax: matplotlib.axes.Axes
        fig, ax = plt.subplots()

        for measurement in self.measurements():
            measurement.plot(ax)

        ax.legend()
        ax.set_title(self.__name)
        ax.set_xlabel("Wavelength [nm]")
        ax.set_ylabel("A.U.")

    def plot_normalized_data(self):
        ax: matplotlib.axes.Axes
        fig, ax = plt.subplots()

        for measurement in self.measurements():
            measurement.plot_normalized(ax)

        ax.legend()
        ax.set_title(self.__name)
        ax.set_xlabel("Wavelength [nm]")
        ax.set_ylabel("Intensity [1/s]")
