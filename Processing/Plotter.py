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
