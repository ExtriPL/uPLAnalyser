from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup
from Utilities.Logger import Logger


class DataProcessor:
    __logger = Logger("Processor")

    @staticmethod
    def process(measurement_groups: list[MeasurementGroup]) -> None:
        DataProcessor.__logger.log("Start processing " + str(len(measurement_groups)) + " group(s)")

        for group in measurement_groups:
            DataProcessor.__process_group(group)

    @staticmethod
    def __process_group(group: MeasurementGroup) -> None:
        DataProcessor.__logger.log("Processing group \"" + group.name() + "\"")

        for mesa_group in group.mesa_groups():
            DataProcessor.__process_mesa_group(mesa_group, group)

    @staticmethod
    def __process_mesa_group(mesa_group: MesaGroup, measurement_group: MeasurementGroup) -> None:
        DataProcessor.__logger.log("Processing mesa \"" + mesa_group.name() + "\"")

        for measurement in mesa_group.measurements():
            background = measurement_group.backgrounds()[measurement.integration_time()]
            measurement.subtract(background)
            measurement.bring_to_zero()
