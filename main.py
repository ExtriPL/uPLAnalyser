from matplotlib import pyplot as plt

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.Algorithms.SameWavelengthOverMaximaAlgorithm import SameWavelengthOverMaximaAlgorithm
from Analysing.AnalysedGroup import AnalysedGroup
from Analysing.DataAnalyser import DataAnalyser
from DataLoader import DataLoader

from Measurements.DataProcessor import DataProcessor
from Measurements.MeasurementGroup import MeasurementGroup
from Utilities.Plotter import Plotter
from Utilities.Saver import Saver

loader = DataLoader("Data")
measurement_groups: list[MeasurementGroup] = loader.load_data()

DataProcessor.process(measurement_groups)
# Plotter.plot_normalized_measurement_groups(measurement_groups)
# plt.show()

analysing_algorithms: list[AnalysingAlgorithm] = [
    SameWavelengthOverMaximaAlgorithm(3, 2)
]

analysed_groups: list[AnalysedGroup] = DataAnalyser.analyse_measurement_groups(measurement_groups, analysing_algorithms)
# Plotter.plot_analysed_groups_loglog(analysed_groups, True)
# plt.show()

saver = Saver("Results")
saver.save_measurement_groups_normalized(measurement_groups)
saver.save_analysed_groups(analysed_groups, with_fit=True, over_data=True)
