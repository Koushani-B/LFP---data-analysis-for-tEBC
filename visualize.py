
import matplotlib.pyplot as plt
import numpy as np

# Get a list of unique channels
channels = df_all['channel'].unique()

# Select specific channels to plot by providing their names in a list
# You can customize this list with any valid channel names from your 'channels' array
selected_channels = ['CSC1', 'CSC10', 'CSC11', 'CSC12', 'CSC13', 'CSC14', 'CSC15', 'CSC16', 'CSC2',
 'CSC3', 'CSC4', 'CSC5', 'CSC6', 'CSC7', 'CSC8', 'CSC9', 'EMG'] # Example: Plot CSC1, CSC2, and EMG channels

# Define a time window for plotting (e.g., first 5 seconds)
start_time = 0
end_time = 5 # seconds

plt.figure(figsize=(15, 8))

for i, channel_name in enumerate(selected_channels):
    # Filter data for the current channel and time window
    channel_df = df_all[(df_all['channel'] == channel_name) &
                        (df_all['time'] >= start_time) &
                        (df_all['time'] <= end_time)]

    # Plot the LFP signal
    plt.plot(channel_df['time'], channel_df['lfp'], label=f'Channel {channel_name}')

plt.title(f'LFP Signals for Selected Channels ({start_time}-{end_time}s)')
plt.xlabel('Time (s)')
plt.ylabel('LFP Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
