# simple script for plotting time domain raw data from TDMS file

import matplotlib.pyplot as plt
from nptdms import TdmsFile
import numpy as np
import os # use for file navigation
from scipy.signal import stft # STFT


# moves up to parent folder '..' and opens the 'raw' folder for raw data
tdms_path = '../raw/10/12/Vibe_Continuous_230521_124306.tdms'

dt = 1/3000 # based on sampling rate

tdms_file = TdmsFile.read(tdms_path)
prop = tdms_file.properties
start_time = prop['DateTime'] # getting the time in which data started being collected

print(start_time)

channel_data = [] # 2D array for storing the data for all channels

for i in range(0,9):
    
    channel_data.append(tdms_file["Time Domain"][f"Channel_0{i}"].data)

num_samples = len(channel_data[0])
time = np.linspace(0, num_samples - 1, num_samples)

for i in range(0,9):
    plt.plot(time, channel_data[i], label=f"Channel {i}")

plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Data from TDMS file")
plt.legend()
plt.show()