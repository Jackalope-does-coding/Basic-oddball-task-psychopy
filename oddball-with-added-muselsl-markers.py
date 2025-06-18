from psychopy import visual, core, event, data
import random
import csv
from muselsl import stream, record
import time
from pylsl import StreamInfo, StreamOutlet

# Start streaming
stream()


# Create an LSL stream for event markers
info = StreamInfo(name='Markers', type='Markers', channel_count=1, nominal_srate=0, channel_format='int32', source_id='oddball_task')
outlet = StreamOutlet(info)



# Create a window
win = visual.Window(size=(800, 600), color="black", units="pix")

# Display instructions
instructions = visual.TextStim(win, text="Press the SPACE bar when you see a square!\nPress any key to start.", color="white")
instructions.draw()
win.flip()
event.waitKeys()  # Wait for user input to start

# Define the stimuli
circle = visual.Circle(win, radius=50, fillColor="white", lineColor="white")
square = visual.Rect(win, width=100, height=100, fillColor="white", lineColor="white")

# Parameters
num_trials = 20
oddball_probability = 0.15  # 15% chance of square appearing
data_list = []  # Store trial data

for trial in range(num_trials):
    stimulus_type = "square" if random.random() < oddball_probability else "circle"
    stimulus = square if stimulus_type == "square" else circle

    stimulus.draw()
    win.flip()

    # event markers
    if stimulus_type == "square":  
        event_marker = 1  # '1' marks a square stimulus  
    else:  
        event_marker = 0  # '0' marks a circle stimulus  

    outlet.push_sample([event_marker])  # Send the marker  
    
    # Measure response time
    timer = core.Clock()
    keys = event.waitKeys(maxWait=1, keyList=['space'], timeStamped=timer)
    
    response = 1 if keys else 0  # 1 if space was pressed, 0 otherwise
    response_time = keys[0][1] if keys else None
    
    #checking if its correct
    if response == 1:
        if stimulus == square:
            is_correct = True
        else: 
            is_correct = False
            
    else:
        if stimulus == square:
            is_correct = False
        else: 
            is_correct = True
    
    # Store trial data
    data_list.append([trial+1, stimulus_type, response, response_time, is_correct, event_marker])

    core.wait(0.5)  # Short gap before next trial
    win.flip()
    core.wait(0.5)

# Save results to CSV
with open("oddball_task_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Trial", "Stimulus", "Response", "Response Time", "Is response correct", "Event Marker"])
    writer.writerows(data_list)
    
# Display end message
end_message = visual.TextStim(win, text="Task Complete! Thank you!", color="white")
end_message.draw()
win.flip()
core.wait(2)

# Close the window
