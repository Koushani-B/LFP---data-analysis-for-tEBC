
def read_ncs_with_neo(filename):
    """
    Read NCS file using the neo library
    Install: pip install neo
    """
    try:
        from neo.io import NeuralynxIO
        
        reader = NeuralynxIO(dirname='/content/gdrive/MyDrive/Code_analysis/Data_ephys/r6565/r6565_S02_trace_250_500_2k')
        block = reader.read_block()
        
        # Access continuous signals
        for seg in block.segments:
            for signal in seg.analogsignals:
                print(f"Signal shape: {signal.shape}")
                print(f"Sampling rate: {signal.sampling_rate}")
                data = signal.magnitude  # Get the actual data
                
        return block
    except ImportError:
        print("neo library not installed. Install with: pip install neo")
        return None
