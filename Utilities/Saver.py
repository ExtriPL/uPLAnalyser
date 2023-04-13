import os.path

import matplotlib.pyplot as plt

from Analysing.AnalysedGroup import AnalysedGroup
from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup


class Saver:
    def __init__(self, output_path: str):
        self.output_path: str = output_path

    def save_measurement_groups(self, groups: list[MeasurementGroup]) -> None:
        for group in groups:
            self.save_measurement_group(group)

    def save_measurement_groups_normalized(self, groups: list[MeasurementGroup]) -> None:
        for group in groups:
            self.save_measurement_group_normalized(group)

    def save_measurement_group(self, group: MeasurementGroup) -> None:
        def get_fig_and_ax(mesa_group: MesaGroup):
            return mesa_group.plot_data()

        self.__save_measurement_group_internal(group, "_.png", get_fig_and_ax)

    def save_measurement_group_normalized(self, group: MeasurementGroup) -> None:
        def get_fig_and_ax(mesa_group: MesaGroup):
            return mesa_group.plot_normalized_data()

        self.__save_measurement_group_internal(group, "_normalized.png", get_fig_and_ax)

    def __save_measurement_group_internal(self, group: MeasurementGroup, file_name_subfix: str, get_fig_and_ax):
        path = self.output_path + "/" + group.name() + "/Data/"

        if not os.path.exists(path):
            os.mkdir(path)

        for mesa_group in group.mesa_groups():
            mesa_path = path + mesa_group.name() + file_name_subfix

            fig, ax = get_fig_and_ax(mesa_group)
            fig.savefig(mesa_path, dpi=500)

    def save_analysed_groups(self, groups: list[AnalysedGroup], with_fit: bool = False, over_data: bool = False) -> None:
        for group in groups:
            self.__save_analysed_group(group, with_fit, over_data)

    def __save_analysed_group(self, group: AnalysedGroup, with_fit: bool = False, over_data: bool = False) -> None:
        path = self.output_path + "/" + group.group_name() + "/Analysed/"

        if not os.path.exists(path):
            os.mkdir(path)

        for analysed_mesa in group.analysed_mesa_groups():
            mesa_path = path + analysed_mesa.mesa().name() + "_" + analysed_mesa.algorithm() + ".png"

            fig, ax = analysed_mesa.plot_loglog(with_fit)
            fig.savefig(mesa_path, dpi=500)

            if over_data:
                mesa_path = path + analysed_mesa.mesa().name() + "_" + analysed_mesa.algorithm() + "_over data.png"
                fig, ax = analysed_mesa.plot_over_data()
                fig.savefig(mesa_path, dpi=500)
