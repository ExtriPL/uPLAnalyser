from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup


class DataProcessor:
    def __init__(self, output_path: str):
        self.__output_path: str = output_path

    def process(self, measurement_groups: list[MeasurementGroup]) -> None:
        for group in measurement_groups:
            self.__process_group(group)

    def __process_group(self, group: MeasurementGroup) -> None:
        for mesa_group in group.mesa_groups():
            self.__process_mesa_group(mesa_group, group)

    def __process_mesa_group(self, mesa_group: MesaGroup, measurement_group: MeasurementGroup) -> None:
        for measurement in mesa_group.measurements():
            background = measurement_group.backgrounds()[measurement.integration_time()]
            measurement.subtract(background)
            measurement.bring_to_zero()
