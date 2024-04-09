import pandas as pd
from nptdms import TdmsFile

def TDMS_to_dframe(direc, channel):
    raw_data = pd.DataFrame
    for t_file in direc:
        tdms_file = TdmsFile.read(t_file)
        prop = tdms_file.properties
        raw_data.append(tdms_file["Time Domain"][f"Channel_0{channel}"].data)

        
