from matplotlib import pyplot as plt

from Analysing.Algorithms.AnalysingAlgorithm import AnalysingAlgorithm
from Analysing.Algorithms.PreserveMaximaOverPowerAlgorithm import PreserveMaximaOverPowerAlgorithm
from Analysing.Algorithms.SameWavelengthOverMaximaAlgorithm import SameWavelengthOverMaximaAlgorithm
from Analysing.AnalysedGroup import AnalysedGroup
from Analysing.DataAnalyser import DataAnalyser
from DataLoader import DataLoader

from Measurements.DataProcessor import DataProcessor
from Measurements.MeasurementGroup import MeasurementGroup
from Utilities.Saver import Saver


analysing_algorithms: list[AnalysingAlgorithm] = [
    SameWavelengthOverMaximaAlgorithm(4, 2),
    PreserveMaximaOverPowerAlgorithm(4, 2)
]

loader = DataLoader("Data")
measurement_groups: list[MeasurementGroup] = loader.load_data()

# raw_analysed_groups: list[AnalysedGroup] = DataAnalyser.analyse_measurement_groups(measurement_groups, analysing_algorithms)
# rawSaver = Saver("Raw")
# rawSaver.save_measurement_groups_normalized(measurement_groups)
# rawSaver.save_analysed_groups(raw_analysed_groups, with_fit=True, over_data=True)

DataProcessor.process(measurement_groups)
processed_analysed_groups: list[AnalysedGroup] = DataAnalyser.analyse_measurement_groups(measurement_groups, analysing_algorithms)

processedSaver = Saver("Results")
processedSaver.save_measurement_groups_normalized(measurement_groups)
processedSaver.save_analysed_groups(processed_analysed_groups, with_fit=True, over_data=True)
