import csv
import os

import numpy as np

from Measurements.Measurement import Measurement
from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup
from Utilities.Logger import Logger


class DataLoader:
    __logger: Logger = Logger("Loader")

    def __init__(self, path: str):
        self.__path: str = path

    def path(self) -> str:
        return self.__path

    def load_data(self) -> list[MeasurementGroup]:
        DataLoader.__logger.log("Begin loading data from \"" + self.__path + "/\"")
        groups = []

        for measurement_group_name in os.listdir(self.__path):
            path = self.__path + "/" + measurement_group_name

            if os.path.isfile(path):
                continue

            measurement_group = self.__load_measurement_group(path, measurement_group_name)
            groups.append(measurement_group)

        return groups

    @staticmethod
    def __load_measurement_group(group_path, group_name) -> MeasurementGroup:
        DataLoader.__logger.log("Loading group \"" + group_name + "\"")
        group: MeasurementGroup = MeasurementGroup(group_name)

        for name in os.listdir(group_path):
            name_path = group_path + "/" + name

            if os.path.isfile(name_path):
                background = DataLoader.__load_measurement_file(name_path, name)
                group.add_background(background)
                continue

            mesa_group = DataLoader.__load_mesa_group(name_path, name)
            group.add_mesa_group(mesa_group)

        return group

    @staticmethod
    def __load_mesa_group(mesa_group_path: str, mesa_group_name: str) -> MesaGroup:
        DataLoader.__logger.log("Loading mesa \"" + mesa_group_name + "\"")
        mesa_group: MesaGroup = MesaGroup(mesa_group_name)

        for name in os.listdir(mesa_group_path):
            name_path = mesa_group_path + "/" + name

            if not os.path.isfile(name_path):
                continue

            measurement = DataLoader.__load_measurement_file(name_path, name)
            mesa_group.add_measurement(measurement)

        return mesa_group

    @staticmethod
    def __load_measurement_file(measurement_path: str, measurement_name: str) -> Measurement:
        DataLoader.__logger.log("Loading measurement \"" + measurement_name + "\"")
        measurement_name = measurement_name.removesuffix(".dat")
        split = measurement_name.split("_")

        integration_time: int
        power_name: str = ""
        power_label: str = ""

        if len(split) == 2:  # Background file
            integration_time = int(split[-1].removesuffix("s"))
        else:  # Mesa point data
            power_name = split[3].replace("p", ".")
            power_label = "_".join(split[3:])
            integration_time = int(split[2].removesuffix("s"))

        x_data = []
        y_data = []

        with open(measurement_path, 'r', newline='') as in_file:
            reader = csv.reader(in_file)
            # skip header
            next(reader)

            for row in reader:
                split_row = row[0].split("\t")
                x = float(split_row[0])
                y = float(split_row[1])

                x_data.append(x)
                y_data.append(y)

        data = np.empty((2, len(x_data)))
        data[0] = np.array(x_data)
        data[1] = np.array(y_data)

        return Measurement(integration_time, power_name, power_label, data)
