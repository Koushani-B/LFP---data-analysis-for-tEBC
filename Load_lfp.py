
mport pandas as pd
import os

def read_single_ncs(filepath):
    """Read a single NCS file manually"""
    
    # NCS file structure
    dt = np.dtype([
        ('timestamp', np.uint64),
        ('channel', np.uint32),
        ('sample_rate', np.uint32),
        ('n_valid', np.uint32),
        ('samples', np.int16, 512)
    ])
    
    with open(filepath, 'rb') as f:
        # Read header (16KB)
        header = f.read(16384).decode('latin-1')
        
        # Extract sampling rate from header
        fs = None
        for line in header.split('\r\n'):
            if '-SamplingFrequency' in line:
                fs = float(line.split()[-1])
                break
        
        # Read data records
        data = np.fromfile(f, dtype=dt)
    
    # Extract signal
    lfp = data['samples'].flatten()
    
    # Create time vector
    times = np.arange(len(lfp)) / fs
    
    # Get channel name from filename
    channel_name = os.path.basename(filepath).replace('.ncs', '')
    
    return {
        'lfp': lfp,
        'times': times,
        'fs': fs,
        'channel': channel_name,
        'timestamps': data['timestamp']
    }

def load_all_ncs_no_stream(dirname):
    """Load all NCS files without Neo's stream organization"""
    
    ncs_files = sorted([f for f in os.listdir(dirname) if f.endswith('.ncs')])
    
    all_channels = {}
    
    for ncs_file in ncs_files:
        filepath = os.path.join(dirname, ncs_file)
        
        try:
            channel_data = read_single_ncs(filepath)
            all_channels[channel_data['channel']] = channel_data
            print(f"✓ Loaded {channel_data['channel']}: {len(channel_data['lfp'])} samples at {channel_data['fs']} Hz")
            
        except Exception as e:
            print(f"✗ Failed {ncs_file}: {e}")
    
    return all_channels

# Usage
dirname = '/content/gdrive/MyDrive/Code_analysis/Data_ephys/r6565/r6565_S02_trace_250_500_2k'
channels_data = load_all_ncs_no_stream(dirname)

# Convert to DataFrame
df = []
for channel_name, data in channels_data.items():
    df_channel = pd.DataFrame({
        'time': data['times'],
        'lfp': data['lfp'],
        'channel': channel_name
    })
    df.append(df_channel)

df_all = pd.concat(df, ignore_index=True)
print(f"\nDataFrame shape: {df_all.shape}")
print(f"Channels: {df_all['channel'].unique()}")
