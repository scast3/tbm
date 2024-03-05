# simple script for plotting time domain raw data from TDMS file

import matplotlib.pyplot as plt
from nptdms import TdmsFile
import numpy as np
import os # use for file navigation
from scipy.signal import stft # STFT


"""
year = input("Year (23 or 24): ")
month = input("Month (1-12): ")
day = input("Day: ")
time = input("Time (0-23): ")
"""
# moves up to parent folder '..' and opens the 'raw' folder for raw data
# might need to cd into python_scripts depending on working directory
tdms_path = f'../raw/10/12/Vibe_Continuous_230521_124306.tdms'

#tdms_path = 'C:/Users/User/Desktop/Mines 3rd Year/Vibration Freq Data Analysis/test.tdms'

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

