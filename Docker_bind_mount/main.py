import os
import pandas as pd

# the directory where the files (.csv) are located
path = "/input_data"
files = os.listdir(path)

frames = []
for i in files:
    frame_i = pd.read_csv(os.path.join(path, i), parse_dates=['saledate'])
    frames.append(frame_i)

concat_df = pd.concat(frames)
print(concat_df.head())