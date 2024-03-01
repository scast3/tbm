import matplotlib.pyplot as plt
from nptdms import TdmsFile
import numpy as np
from scipy.signal import stft

class TDMSPlotter:
    def __init__(self, tdms_path):
        self.tdms_path = tdms_path
        self.channel_data = None
        self.num_samples = None
        self.time = None

    def load_tdms_file(self):
        try:
            tdms_file = TdmsFile.read(self.tdms_path)
            self.channel_data = []
            
            for i in range(9):
                self.channel_data.append(tdms_file["Time Domain"][f"Channel_0{i}"].data)
            self.num_samples = len(self.channel_data[0])
            self.time = np.linspace(0, self.num_samples - 1, self.num_samples)
            print("TDMS file loaded successfully.")
        except Exception as e:
            print(f"Error loading TDMS file: {e}")

    def plot_raw_data(self):
        if self.channel_data is None or self.time is None:
            print("Error: No data to plot.")
            return
        for i in range(9):
            plt.plot(self.time, self.channel_data[i], label=f"Channel {i}")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Data from TDMS file")
        plt.legend()
        plt.show()

    def plot_stft_data(self):
        print("stft placeholder")

    def plot_BDV(self):
        print("bdv placeholder")

# Example usage:
tdms_path = '../raw/10/12/Vibe_Continuous_230521_124306.tdms'
plotter = TDMSPlotter(tdms_path)
plotter.load_tdms_file()
plotter.plot_raw_data()
