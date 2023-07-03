import os.path

import matplotlib.pyplot as plt

from Analysing.AnalysedGroup import AnalysedGroup
from Analysing.AnalysedMesa import AnalysedMesa
from Measurements.MeasurementGroup import MeasurementGroup
from Measurements.MesaGroup import MesaGroup
from Utilities.Logger import Logger


class Saver:
    __logger = Logger("Saver")

    def __init__(self, output_path: str, overwrite_files: bool = True):
        self.output_path: str = output_path
        self.__overwrite_files: bool = overwrite_files

    def save_measurement_groups(self, groups: list[MeasurementGroup]) -> None:
        Saver.__logger.log("Begin saving " + str(len(groups)) + " group(s) in \"" + self.output_path + "\"")

        for group in groups:
            self.save_measurement_group(group)

    def save_measurement_groups_normalized(self, groups: list[MeasurementGroup]) -> None:
        Saver.__logger.log("Begin saving " + str(len(groups)) + " normalized group(s) in \"" + self.output_path + "\"")

        for group in groups:
            self.save_measurement_group_normalized(group)

    def save_measurement_group(self, group: MeasurementGroup) -> None:
        Saver.__logger.log("Save \"" + group.name() + "\"")

        def get_fig_and_ax(mesa_group: MesaGroup):
            return mesa_group.plot_data()

        self.__save_measurement_group_internal(group, "_.png", get_fig_and_ax)

    def save_measurement_group_normalized(self, group: MeasurementGroup) -> None:
        Saver.__logger.log("Save \"" + group.name() + "\" normalized")

        def get_fig_and_ax(mesa_group: MesaGroup):
            return mesa_group.plot_normalized_data()

        self.__save_measurement_group_internal(group, "_normalized.png", get_fig_and_ax)

    def __save_measurement_group_internal(self, group: MeasurementGroup, file_name_subfix: str, get_fig_and_ax):
        path = self.output_path + "/" + group.name() + "/Data/"

        if not os.path.exists(path):
            os.makedirs(path)

        for mesa_group in group.mesa_groups():
            Saver.__logger.log("Saving \"" + mesa_group.name() + "\"")

            mesa_path = path + mesa_group.name() + file_name_subfix

            if not self.__overwrite_files and os.path.exists(mesa_path):
                continue

            fig, ax = get_fig_and_ax(mesa_group)
            fig.savefig(mesa_path, dpi=500)
            plt.close("all")

    def save_analysed_groups(self, groups: list[AnalysedGroup], with_fit: bool = False, over_data: bool = False) -> None:
        Saver.__logger.log("Begin saving " + str(len(groups)) + " analysed group(s) "
                                                                + "with_fit=" + str(with_fit)
                                                                + ", over_data=" + str(over_data))

        for group in groups:
            self.__save_analysed_group(group, with_fit, over_data)

    def __save_analysed_group(self, group: AnalysedGroup, with_fit: bool = False, over_data: bool = False) -> None:
        Saver.__logger.log("Saving \"" + group.group_name() + "\" analysed group")
        path = self.output_path + "/" + group.group_name() + "/Analysed/"

        if not os.path.exists(path):
            os.makedirs(path)

        statistics: dict[str, list[AnalysedMesa]] = dict()

        for analysed_mesa in group.analysed_mesa_groups():
            Saver.__logger.log("Saving \"" + analysed_mesa.mesa().name() + "\"")
            mesa_directory = path + analysed_mesa.algorithm() + "/"

            if not os.path.exists(mesa_directory):
                os.makedirs(mesa_directory)

            if analysed_mesa.algorithm() not in statistics:
                statistics[analysed_mesa.algorithm()] = []

            statistics[analysed_mesa.algorithm()].append(analysed_mesa)
            Saver.__save_analysed_mesa(analysed_mesa, mesa_directory, with_fit, over_data, self.__overwrite_files)

        statistics_text = Saver.__generate_statistic_string(statistics)
        statistics_file = open(path + "statistics.txt", "w")
        statistics_file.write(statistics_text)
        statistics_file.close()

    @staticmethod
    def __save_analysed_mesa(analysed_mesa: AnalysedMesa, mesa_directory: str, with_fit: bool
                             , over_data: bool, overwrite_files: bool) -> None:
        mesa_path = mesa_directory + analysed_mesa.mesa().name() + "_" + analysed_mesa.algorithm() + ".png"

        if not overwrite_files and os.path.exists(mesa_path):
            return

        fig, ax = analysed_mesa.plot_loglog(with_fit)
        fig.savefig(mesa_path, dpi=500)

        if over_data:
            mesa_path = mesa_directory + analysed_mesa.mesa().name() + "_" + analysed_mesa.algorithm() + "_over data.png"
            fig, ax = analysed_mesa.plot_over_data()
            fig.savefig(mesa_path, dpi=500)
            plt.close("all")

    @staticmethod
    def __generate_statistic_string(statistics: dict[str, list[AnalysedMesa]]) -> str:
        statistics_text = ""

        for algorithm in statistics:
            statistics_text += algorithm + ":\n"

            analysed_mesas = statistics[algorithm]

            for mesa in analysed_mesas:
                statistics_text += "\t" + mesa.mesa().name() + ":\n"

                for a_set in mesa.analysed_sets():
                    statistics_text += "\t\t" + str(a_set.wavelength()) + " nm:\n"

                    for line in a_set.fit_statistics().get_statistics():
                        statistics_text += "\t\t\t" + line + "\n"

        return statistics_text
