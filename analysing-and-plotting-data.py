import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# === Load EEG Data ===
eeg_df = pd.read_csv("EEG_recording_2025-07-07-23.38.37.csv")
eeg_df['timestamps'] = pd.to_datetime(eeg_df['timestamps'], unit='s')
eeg_df.set_index('timestamps', inplace=True)

# === Load Markers and apply 4-hour UTC shift ===
stim_df = pd.read_csv("oddball_task_data.csv")
stim_df['Marker Timestamp'] = pd.to_datetime(stim_df['Marker Timestamp'])
stim_df['Aligned Timestamp'] = stim_df['Marker Timestamp'] + timedelta(hours=4)

# === Normalize EEG Channels ===
channels = [ch for ch in eeg_df.columns if ch != 'Right AUX']
normalized_df = eeg_df[channels].apply(lambda x: (x - x.mean()) / x.std())

# === Plotting ===
plt.figure(figsize=(15, 8))

for i, ch in enumerate(channels):
    offset = i * 10  # Smaller offset now that signals are normalized
    plt.plot(normalized_df.index, normalized_df[ch] + offset, label=ch)

# Marker lines and labels
for _, row in stim_df.iterrows():
    ts = row['Aligned Timestamp']
    label = row['Marker']
    color = 'red' if label == 'square' else 'blue'
    plt.axvline(x=ts, color=color, linestyle='--', alpha=0.6)
    plt.text(ts, offset + 5, label, rotation=90, fontsize=8, color=color)

plt.title("Normalized EEG Signals with Oddball Stimulus Markers")
plt.xlabel("Time")
plt.ylabel("Normalized EEG (Vertically Offset)")
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
