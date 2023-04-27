from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup
from Utilities.Logger import Logger


class DataProcessor:
    __logger = Logger("Processor")

    @staticmethod
    def process(measurement_groups: list[MeasurementGroup], subtract_background: bool = True,
                bring_to_zero: bool = True) -> None:
        DataProcessor.__logger.log("Start processing " + str(len(measurement_groups)) + " group(s)")

        for group in measurement_groups:
            DataProcessor.__process_group(group, subtract_background, bring_to_zero)

    @staticmethod
    def __process_group(group: MeasurementGroup, subtract_background: bool, bring_to_zero: bool) -> None:
        DataProcessor.__logger.log("Processing group \"" + group.name() + "\"")

        for mesa_group in group.mesa_groups():
            DataProcessor.__process_mesa_group(mesa_group, group, subtract_background, bring_to_zero)

    @staticmethod
    def __process_mesa_group(mesa_group: MesaGroup, measurement_group: MeasurementGroup, subtract_background: bool,
                             bring_to_zero: bool) -> None:
        DataProcessor.__logger.log("Processing mesa \"" + mesa_group.name() + "\"")

        for measurement in mesa_group.measurements():
            if subtract_background and measurement.integration_time() in measurement_group.backgrounds():
                background = measurement_group.backgrounds()[measurement.integration_time()]
                measurement.subtract(background)
            if bring_to_zero:
                measurement.bring_to_zero()
