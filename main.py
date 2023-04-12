from DataLoader import DataLoader
import matplotlib.pyplot as plt

from Processing.Plotter import Plotter
from Processing.DataProcessor import DataProcessor

loader = DataLoader("Data")
measurement_groups = loader.load_data()
data_processor = DataProcessor("Results/")

data_processor.process(measurement_groups)
Plotter.plot_normalized_measurement_groups(measurement_groups)

plt.show()
