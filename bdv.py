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
        self.time = []
        #  in the future, time array needs to account for for start time

    def __init__(self, filepath):
        self.tdms_path = filepath

    def load_tdms_file(self):

        # need to fix time array
        try:
            tdms_file = TdmsFile.read(tdms_path)
            prop = tdms_file.properties
            self.start_time = prop['DateTime'] # getting the time in which data started being collected

            channel_data = [] # 2D array for storing the data for all channels

            for i in range(0,9):
                
                channel_data.append(tdms_file["Time Domain"][f"Channel_0{i}"].data)

            self.raw_data = channel_data
            num_samples = len(self.raw_data[0])
            self.time = np.linspace(0, num_samples - 1, num_samples)

            print("TDMS file loaded successfully.")
        except Exception as e:
            print(f"Error loading TDMS file: {e}")

    def plot_raw_data(self):
        
        for i in range(0,9):
            plt.plot(self.time, self.raw_data[i], label=f"Channel {i}")

        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Data from TDMS file")
        plt.legend()
        plt.show()

    # plot min, max, rms, 1st quartile, mean, 3rd quartile
    def get_data(self):
        out_2d_array = []
        labels = ["minimum", "maximum", "root mean square", "1Q", "mean", "3Q"]
        mins = []
        maxs = []
        rmss = []
        firstqs = []
        means = []
        thirdqs = []

        for channel in range(9):
            channel_data = self.raw_data[channel]
            mins.append(np.min(channel_data))
            maxs.append(np.max(channel_data))
            rmss.append(np.sqrt(np.mean(np.square(channel_data))))
            firstqs.append(np.percentile(channel_data, 25))
            means.append(np.mean(channel_data))
            thirdqs.append(np.percentile(channel_data, 75))
        
    
    def plot_avg_data(self):
        print("avg placeholder")

    # plots all values: raw, rms, avg, etc per channel to compare them
    def plot_per_channel(self, channel):
        print("all placeholder")

    def plot_stft_data(self, channel):
        f, t, Zxx = stft(self.raw_data[channel], window = "hamm", fs=self.dt, nperseg=self.bin_size)
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
        plt.colorbar(label='Magnitude')
        plt.title(f'Unfiltered Spectrogram for Channel {channel}')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()

    # still working on this
    def calc_BDV(self):

        total_amp_per_channel = []
        for c in range(0,9):
            # first, get the stft data from each channel
            

            # iterate through all timesteps - see if this is the right way first though
            for tm in range(0, len(self.time), self.time_steps):
                data_chunk = self.raw_data[c][tm:tm+self.time_steps]

                # calc stft over the data chunk
                f, t, Zxx = stft(data_chunk, window = "hamm", fs=self.dt, nperseg=self.bin_size)

                magnitude = np.abs(Zxx)

                total_amp_per_channel[c].add(magnitude)

        
        print(magnitude)
        print("bdv placeholder")

# main code:
tdms_path = '../raw/10/12/Vibe_Continuous_230521_124306.tdms'
#plotter = BDV_data(tdms_path, 1/3000, 30, 512, 300)

plotter = BDV_data(tdms_path)
plotter.load_tdms_file()
#plotter.plot_raw_data()
#plotter.plot_stft_data(1)
#plotter.calc_BDV()
plotter.get_data()


# TODO next meeting 4/5
# each tdms file has 45000 datapoints
# try to find an ideal amout tdms files that can be displayed at a 3000 hz resolution
# pull in a week of tdms files at 3000hz - is it possible, probably not
# for each 15 scond tdms file, compile it to 1 datapoint (RMS, average, other metrics(IDV??))
# we need to prove that the downsampled data is the same as the current freq data
# finish IDV/BDV implementation
# run FFT on interval when TBM impacts anchor to find frequencies
# this needs to be done in 2 weeks - April 14th