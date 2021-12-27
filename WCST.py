from utils import  get_sequence , get_choice , catGen, WCST_trial , Finish
from helper import getUserInfo  , set_win_background
from psychopy import visual , core , event , gui , sound 

timer = core.Clock()


usrInfo , again = getUserInfo()
while(again):
    usrInfo , again = getUserInfo()
    

windows , background = set_win_background(display_ints = True)
WCST_trial(windows , background , timer , usrInfo)
Finish(windows , background)


