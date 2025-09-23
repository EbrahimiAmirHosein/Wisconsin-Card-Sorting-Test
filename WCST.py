from utils import get_sequence, get_choice, catGen, WCST_trial, Finish
from helper import getUserInfo, set_win_background
from psychopy import visual, core, event, gui, sound
import serial  # Add this import
import time

timer = core.Clock()

# Init EEG  port 
def init_eeg_port():
    try:
        eeg_port = serial.Serial('COM5', 9600)  # Change COM5 to your port
        time.sleep(2)  # 2 secs for port initialization
        return eeg_port
    except serial.SerialException as e:
        print(f"EEG port initialization failed: {e}")
        return None


def send_eeg_trigger(port, trigger_value):
    if port is not None:
        try:
            port.write(bytes([trigger_value]))
            print(f"Sent trigger: {trigger_value}")
        except Exception as e:
            print(f"Error sending trigger: {e}")

usrInfo, again = getUserInfo()
while again:
    usrInfo, again = getUserInfo()

eeg_port = init_eeg_port()
send_eeg_trigger(eeg_port, 0)

windows, background = set_win_background(display_ints=True)

WCST_trial(windows, background, timer, usrInfo, eeg_port)  

send_eeg_trigger(eeg_port, 3)

if eeg_port:
    eeg_port.close()

Finish(windows, background)
