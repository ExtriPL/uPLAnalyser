import matplotlib.axes
import numpy as np
import scipy as sc

from Analysing.LinearFitStatistics import LinearFitStatistics


class AnalysedSet:
    def __init__(self, wavelengths: np.ndarray, data: np.ndarray):
        self.__wavelengths: np.ndarray = wavelengths
        self.__data: np.ndarray = data

        fit_statistics = AnalysedSet.__linear_fit(self.__data)
        self.__fit_statistics: LinearFitStatistics = fit_statistics
        self.__score = fit_statistics.r_value()

    def wavelength(self) -> float:
        return self.__wavelengths[0]

    def wavelengths(self) -> np.ndarray:
        return self.__wavelengths

    def label(self) -> str:
        return str(self.__wavelengths[-1]) + " nm"

    def data(self) -> np.ndarray:
        return self.__data

    def score(self) -> float:
        return self.__score

    def set_score(self, value) -> None:
        self.__score = value

    def fit_statistics(self) -> LinearFitStatistics:
        return self.__fit_statistics

    def plot(self, ax: matplotlib.axes.Axes) -> None:
        ax.scatter(self.data()[0], self.data()[1], label=self.label(), s=5)

    def plot_loglog(self, ax: matplotlib.axes.Axes, with_fit: bool = False) -> None:
        ln_x = np.log(np.abs(self.data()[0]))
        ln_y = np.log(np.abs(self.data()[1]))

        slope = self.__fit_statistics.slope()
        intercept = self.__fit_statistics.intercept()

        ax.scatter(ln_x, ln_y, label=self.label() + ", slope=" + str(round(slope, 3)), s=5)
        lower_bound = 0.95 * min(ln_x)
        upper_bound = 1.05 * max(ln_x)

        ax.set_xlim(lower_bound, upper_bound)

        if with_fit:
            x_range = np.array([lower_bound, upper_bound])
            ax.plot(x_range, slope * x_range + intercept, linewidth=0.5)

    @staticmethod
    def __linear_fit(data: np.ndarray) -> LinearFitStatistics:
        log_x = np.log(np.abs(data[0]))
        log_y = np.log(np.abs(data[1]))

        if len(log_x) <= 2:
            slope, intercept, r_value, _, _ = sc.stats.linregress(log_x, log_y)
            return LinearFitStatistics(slope, intercept, r_value, len(log_x))

        best_slop: float = 0
        best_intercept: float = 0
        best_r_value: float = 0
        used_point_count: int = 0

        for point_count in range(len(log_x), 2, -1):
            slope, intercept, r_value, _, _ = sc.stats.linregress(log_x[:point_count], log_y[:point_count])

            if r_value > best_r_value:
                best_slop, best_intercept, best_r_value = slope, intercept, r_value
                used_point_count = point_count

        return LinearFitStatistics(best_slop, best_intercept, best_r_value, used_point_count)
