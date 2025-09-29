from utils import get_sequence, get_choice, catGen, WCST_trial, Finish
from helper import getUserInfo, set_win_background
from psychopy import visual, core, event, gui, sound
import serial
import time

timer = core.Clock()

def init_eeg_port():
    try:
        eeg_port = serial.Serial('COM3', 9600)
        time.sleep(2)
        return eeg_port
    except serial.SerialException:
        return None
    except Exception:
        return None

def send_eeg_trigger(port, trigger_value, trigger_log):
    if port is not None:
        try:
            port.write(bytes([trigger_value]))
            trigger_time = timer.getTime()
            trigger_log.append({
                'trigger': trigger_value,
                'time': trigger_time,
                'trial': len(trigger_log) + 1
            })
        except Exception:
            pass

usrInfo, again = getUserInfo()
while again:
    usrInfo, again = getUserInfo()

eeg_port = init_eeg_port()
trigger_log = []

send_eeg_trigger(eeg_port, 0, trigger_log)
time.sleep(0.05)

windows, background = set_win_background(display_ints=True)

WCST_trial(windows, background, timer, usrInfo, eeg_port, trigger_log)

send_eeg_trigger(eeg_port, 3, trigger_log)
time.sleep(0.05)

if eeg_port:
    eeg_port.close()

Finish(windows, background)
