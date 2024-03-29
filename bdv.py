import matplotlib.pyplot as plt
from nptdms import TdmsFile
import numpy as np
from scipy.signal import stft

class BDV_data:
    def __init__(self, tdms_path, sampling_freq, time_steps, bin_size, window_length):
        self.tdms_path = tdms_path
        self.dt = sampling_freq
        self.time_steps = time_steps
        self.bin_size = bin_size
        self.window_length = window_length
        self.raw_data = []
        self.start_time = 0

    def load_tdms_file(self):
        try:
            tdms_file = TdmsFile.read(tdms_path)
            prop = tdms_file.properties
            self.start_time = prop['DateTime'] # getting the time in which data started being collected

            channel_data = [] # 2D array for storing the data for all channels

            for i in range(0,9):
                
                channel_data.append(tdms_file["Time Domain"][f"Channel_0{i}"].data)

            self.raw_data = channel_data

            print("TDMS file loaded successfully.")
        except Exception as e:
            print(f"Error loading TDMS file: {e}")

    def plot_raw_data(self):
        num_samples = len(self.raw_data[0])
        time = np.linspace(0, num_samples - 1, num_samples)

        for i in range(0,9):
            plt.plot(time, self.raw_data[i], label=f"Channel {i}")

        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Data from TDMS file")
        plt.legend()
        plt.show()

    def plot_stft_data(self, channel):
        f, t, Zxx = stft(self.raw_data[channel], window = "hann", fs=self.dt, nperseg=self.bin_size)
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
        plt.colorbar(label='Magnitude')
        plt.title(f'Unfiltered Spectrogram for Channel {channel}')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()

    def calc_BDV(self):
        print("bdv placeholder")

# main code:
tdms_path = '../raw/10/12/Vibe_Continuous_230521_124306.tdms'
plotter = BDV_data(tdms_path, 1/3000, 30, 512, 300)
plotter.load_tdms_file()
#plotter.plot_raw_data()
plotter.plot_stft_data(1)
