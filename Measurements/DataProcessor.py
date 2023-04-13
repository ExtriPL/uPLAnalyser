from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup


class DataProcessor:
    @staticmethod
    def process(measurement_groups: list[MeasurementGroup]) -> None:
        for group in measurement_groups:
            DataProcessor.__process_group(group)

    @staticmethod
    def __process_group(group: MeasurementGroup) -> None:
        for mesa_group in group.mesa_groups():
            DataProcessor.__process_mesa_group(mesa_group, group)

    @staticmethod
    def __process_mesa_group(mesa_group: MesaGroup, measurement_group: MeasurementGroup) -> None:
        for measurement in mesa_group.measurements():
            background = measurement_group.backgrounds()[measurement.integration_time()]
            measurement.subtract(background)
            measurement.bring_to_zero()
