from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet
from datetime import datetime
import random
import csv

# === EEG Marker Stream Setup ===
info = StreamInfo(name='Markers', type='Markers', channel_count=1,
                  channel_format='string', source_id='marker_stream')
outlet = StreamOutlet(info)

# === Window Setup ===
win = visual.Window(size=(800, 600), color="black", units="pix")

# === Display Instructions ===
instructions = visual.TextStim(win, text="Press the SPACE bar when you see a square!\nPress any key to start.",
                               color="white")
instructions.draw()
win.flip()
event.waitKeys()

# === Define Stimuli ===
circle = visual.Circle(win, radius=50, fillColor="white", lineColor="white")
square = visual.Rect(win, width=100, height=100, fillColor="white", lineColor="white")

# === Experiment Parameters ===
num_trials = 20
oddball_probability = 0.15
data_list = []

# === Trial Loop ===
for trial in range(num_trials):
    stimulus_type = "square" if random.random() < oddball_probability else "circle"
    stimulus = square if stimulus_type == "square" else circle

    # Show stimulus
    stimulus.draw()
    win.flip()

    # Send EEG Marker
    marker_timestamp = datetime.now().isoformat()
    outlet.push_sample([stimulus_type])

    # Record response
    timer = core.Clock()
    keys = event.waitKeys(maxWait=1, keyList=['space'], timeStamped=timer)
    response = 1 if keys else 0
    response_time = keys[0][1] if keys else None

    # Check correctness
    is_correct = (response == 1 and stimulus == square) or (response == 0 and stimulus == circle)

    # Save trial data
    data_list.append([
        trial + 1,
        stimulus_type,
        response,
        response_time,
        is_correct,
        stimulus_type,  # Marker
        marker_timestamp
    ])

    # Inter-trial interval
    core.wait(0.5)
    win.flip()
    core.wait(0.5)

# === Save Data to CSV ===
with open("oddball_task_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Trial", "Stimulus", "Response", "Response Time", "Is response correct", "Marker", "Marker Timestamp"])
    writer.writerows(data_list)

# === End Message ===
end_message = visual.TextStim(win, text="Task Complete! Thank you!", color="white")
end_message.draw()
win.flip()
core.wait(2)

# === Close Everything ===
win.close()
core.quit()
