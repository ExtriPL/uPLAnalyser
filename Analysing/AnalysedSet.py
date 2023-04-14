import matplotlib.axes
import numpy as np
import scipy as sc


class AnalysedSet:
    def __init__(self, wavelength: float, data: np.ndarray):
        self.__wavelength: float = wavelength
        self.__data: np.ndarray = data

        score, slope, intercept = AnalysedSet.__get_score(self.__data)
        self.__score: float = score
        self.__slope: float = slope
        self.__intercept: float = intercept

    def wavelength(self) -> float:
        return self.__wavelength

    def label(self) -> str:
        return str(self.__wavelength) + " nm"

    def data(self) -> np.ndarray:
        return self.__data

    def score(self) -> float:
        return self.__score

    def plot(self, ax: matplotlib.axes.Axes) -> None:
        ax.scatter(self.data()[0], self.data()[1], label=self.label(), s=5)

    def plot_loglog(self, ax: matplotlib.axes.Axes, with_fit: bool = False) -> None:
        ln_x = np.log(np.abs(self.data()[0]))
        ln_y = np.log(np.abs(self.data()[1]))

        ax.scatter(ln_x, ln_y, label=self.label() + "_s:" + str(round(self.__slope, 3)), s=5)
        lower_bound = 0.95 * min(ln_x)
        upper_bound = 1.05 * max(ln_x)

        ax.set_xlim(lower_bound, upper_bound)

        if with_fit:
            x_range = np.array([lower_bound, upper_bound])
            ax.plot(x_range, self.__slope * x_range + self.__intercept, linewidth=0.5)

    @staticmethod
    def __get_score(data: np.ndarray) -> (float, float, float):
        log_x = np.log(np.abs(data[0]))
        log_y = np.log(np.abs(data[1]))

        slope, intercept, r_value, _, _ = sc.stats.linregress(log_x, log_y) # slope, intercept, r_value, p_value, std_err
        return r_value, slope, intercept
        # return np.max(data[1]), slope, intercept
