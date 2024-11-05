import pandas as pd
import matplotlib.pyplot as plt

# Sample data import (replace with actual data file)
data = pd.read_csv("data.csv")

# Assuming `data` has columns: datetime, EDA, HR
# Replace '24:00' with '00:00' and adjust the date by adding one day where necessary
data['datetime'] = data['datetime'].str.replace(r'24:(\d{2})', r'00:\1', regex=True)
data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce') + pd.to_timedelta(data['datetime'].str.contains('00:00').astype(int), unit='D')

data.set_index('datetime', inplace=True)

# Resample to hourly means to find patterns by time
hourly_data = data.resample('H').mean()

# Define stress thresholds
eda_threshold = 0.8  # Example threshold for high EDA
hr_threshold = 100   # Example threshold for high HR

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(hourly_data.index, hourly_data['EDA'], label='EDA', color='blue')
plt.plot(hourly_data.index, hourly_data['HR'], label='Heart Rate', color='red')

# Highlighting stressful periods
plt.fill_between(hourly_data.index, eda_threshold, hourly_data['EDA'],
                 where=(hourly_data['EDA'] > eda_threshold), color='blue', alpha=0.3, label='High EDA')
plt.fill_between(hourly_data.index, hr_threshold, hourly_data['HR'],
                 where=(hourly_data['HR'] > hr_threshold), color='red', alpha=0.3, label='High HR')

# Labels and legend
plt.title('Identification of Stressful Times Based on EDA and Heart Rate')
plt.xlabel('Time')
plt.ylabel('Average EDA / Heart Rate')
plt.legend()
plt.show()
