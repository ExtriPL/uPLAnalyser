import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Analysing.AnalysedSet import AnalysedSet
from Measurements.MesaGroup import MesaGroup


class AnalysedMesa:
    def __init__(self, mesa_group: MesaGroup, algorithm: str):
        self.__mesa: MesaGroup = mesa_group
        self.__algorithm: str = algorithm
        self.__analysed_sets: list[AnalysedSet] = []

    def mesa(self) -> MesaGroup:
        return self.__mesa

    def algorithm(self) -> str:
        return self.__algorithm

    def analysed_sets(self) -> list[AnalysedSet]:
        return self.__analysed_sets

    def add_analysed_set(self, analysed_set: AnalysedSet) -> None:
        self.__analysed_sets.append(analysed_set)

    def plot(self, with_fit: bool = False):
        ax: matplotlib.axes.Axes
        fig, ax = plt.subplots()

        for analysed_set in self.analysed_sets():
            analysed_set.plot(ax)

        ax.legend()
        ax.set_title(self.mesa().name() + "_" + self.algorithm())
        ax.set_xlabel("Power [nW]")
        ax.set_ylabel("Intensity [A.U/s]")
        fig.canvas.manager.set_window_title(self.mesa().name() + "_" + self.algorithm())

        return fig, ax

    def plot_loglog(self, with_fit: bool = False):
        ax: matplotlib.axes.Axes
        fig, ax = plt.subplots()

        for analysed_set in self.analysed_sets():
            analysed_set.plot_loglog(ax, with_fit)

        ax.legend()
        ax.set_title(self.mesa().name() + "_" + self.algorithm())
        ax.set_xlabel("log(Power)")
        ax.set_ylabel("log(Intensity)")
        fig.canvas.manager.set_window_title(self.mesa().name() + "_" + self.algorithm())

        return fig, ax

    def plot_over_data(self):
        ax: matplotlib.axis.Axes
        fig, ax = plt.subplots()

        self.mesa().plot_normalized_data(fig, ax)

        for analysed_set in self.analysed_sets():
            ax.scatter(np.repeat(analysed_set.wavelength(), len(analysed_set.data()[1])), analysed_set.data()[1], marker="x", s=3)

        return fig, ax
