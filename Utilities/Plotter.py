from Analysing.AnalysedGroup import AnalysedGroup
from Measurements.MeasurementGroup import MeasurementGroup


class Plotter:
    @staticmethod
    def plot_measurement_groups(measurement_groups: list[MeasurementGroup]) -> None:
        for group in measurement_groups:
            for mesa in group.mesa_groups():
                mesa.plot_data()

    @staticmethod
    def plot_normalized_measurement_groups(measurement_groups: list[MeasurementGroup]) -> None:
        for group in measurement_groups:
            for mesa in group.mesa_groups():
                mesa.plot_normalized_data()

    @staticmethod
    def plot_analysed_groups(analysed_groups: list[AnalysedGroup]) -> None:
        for group in analysed_groups:
            for analysed_mesa in group.analysed_mesa_groups():
                analysed_mesa.plot()

    @staticmethod
    def plot_analysed_groups_loglog(analysed_groups: list[AnalysedGroup], with_fit: bool = False) -> None:
        for group in analysed_groups:
            for analysed_mesa in group.analysed_mesa_groups():
                analysed_mesa.plot_loglog(with_fit)
