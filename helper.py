from psychopy import visual, core, event, gui, sound
import pandas as pd
import os

def getUserInfo():
    again = False
    DialogGui = gui.Dlg(title="User information WCST")
    DialogGui.addField(" Subject Name: ")
    DialogGui.addField(" Subject Surname: ")
    DialogGui.addField(" Subject Number: ")
    DialogGui.addField(" Age: ")
    DialogGui.addField('Gender', choices=['Male', 'Female'])
    DialogGui.addField('Handedness', choices=['Right', 'Left'])
    DialogGui.addField('Type', choices=['AD', 'HS'])
    DialogGui.show()
    if (DialogGui.data[2] == '' or DialogGui.data[3] == ''):
        DialogGui.data[2], DialogGui.data[3] = 99999999, 99999999
        
    if (not DialogGui.data[2].isdigit() or not DialogGui.data[3].isdigit()):
        again = True
        DialogGui.data[2], DialogGui.data[3] = 99999999, 99999999
        
    if (DialogGui.data[0].isdigit() or DialogGui.data[1].isdigit()):
        again = True

    if (not DialogGui.OK):
        core.quit()
    listInfo = [int(DialogGui.data[2]), DialogGui.data[0], DialogGui.data[1], int(DialogGui.data[3]), DialogGui.data[4], DialogGui.data[5], DialogGui.data[6]]
    if '' or 99999999 in listInfo:
        again = True
    else:
        again = False
    
    return [listInfo, again]
    
def displayImg(win, imgName, duration, instr, size, pos):
    if size == None and pos == None:
        img = visual.ImageStim(
            win=win,
            image="stimuli/VisualStimuli/" + imgName + ".png"
        )
    else:
        img = visual.ImageStim(
            win=win,
            image="stimuli/VisualStimuli/" + imgName + ".png",
            size=(size[0], size[1]),
            pos=(pos[0], pos[1])
        )
    if instr:
        img.draw()
        win.flip()
    else:
        imgClk = core.Clock()
        while (imgClk.getTime() < duration):
            img.draw()
            win.flip()
        win.flip()

def displayImg2(win, imgName, duration, instr, size, pos):
    if size == None and pos == None:
        img = visual.ImageStim(
            win=win,
            image="stimuli/VisualStimuli/" + imgName + ".png"
        )
    else:
        img = visual.ImageStim(
            win=win,
            image="stimuli/VisualStimuli/" + imgName + ".png",
            size=(size[0], size[1]),
            pos=(pos[0], pos[1])
        )
    if instr:
        img.draw()
        win.flip()
    else:
        imgClk = core.Clock()
        while (imgClk.getTime() < duration):
            img.draw()
            win.flip()
        win.flip()
    return img

def print_mouse_pos(windows):
    mouse = event.Mouse(visible=True, newPos=None, win=windows)
    while (not mouse.getPressed() == [1,0,0]):
        textstimlike=visual.TextBox(
            window=windows,
            text=str(mouse.getPos()),
            font_size=18,
            font_color=[-1,-1,1],
            color_space='rgb',
            size=(1.8,.1),
            pos=(0.0,.5),
            units='norm')
        textstimlike.draw()
        windows.flip()
    windows.flip()

def set_win_background(display_ints):
    windows = visual.Window(
        size=[1080, 940],
        fullscr=True,
        units="pix",
        color=[1,1,1]
    )
    if (display_ints):
        windows.color = [1,1,1]
        instructions = ["instr_1","instr_2","instr_3"]
        for instr in instructions:
            displayImg(windows, 'instructions/'+instr, 0, True, size=None, pos=None)
            event.waitKeys(keyList=['m', 'M'], clearEvents=True)
        windows.color = [0,0,0]
        windows.flip()
    
    background = visual.ImageStim(
        win=windows,
        image="stimuli/VisualStimuli/main_cards/" + 'main' + ".png",
        size=(1200,260),
        pos=(0,250)
    )
    background.autoDraw = True
    windows.flip()
    return windows, background

def check_quit(win):
    intrupt = event.getKeys(['q'])
    if 'q' in intrupt:
        win.close()
        core.quit()
        
def display_blank(windows, background, duration):
    imgClk = core.Clock()
    while (imgClk.getTime() < duration):
        windows.flip()
        background.autoDraw = False
    background.autoDraw = True    
    windows.flip()
    
def Txt_loader(win, title, duration):
    textstimlike=visual.TextBox(
        window=win,
        text=str(title),
        font_size=18,
        font_color=[-1,-1,1],
        color_space='rgb',
        size=(1.8,.1),
        pos=(0.0,.5),
        units='norm')
    imgClk = core.Clock()
    while (imgClk.getTime() < duration):
        textstimlike.draw()
        win.flip()
    win.flip()
    
def Index_check(arr, maxim):
    for i in range(maxim-len(arr)):
        arr.append(' ')
    
def SaveDate(usrNum, usrName, usrLastName, usrAge, usrGender, usrHand, usrType, Catgenerate, Trial, CatNum, Cat, StimCard, ResCard, PersCat, CorrAns, Acc, RTime, TstartTime, RstartTime, trigger_log=None):
    Id = []
    Name = []
    LastName = []
    Age = []
    Gender = []
    DomHand = []
    Type = []
    maxim = max(len(Catgenerate), len(Trial), len(CatNum), len(Cat), len(PersCat), len(CorrAns), len(Acc), len(RTime), len(TstartTime), len(RstartTime), len(StimCard), len(ResCard))
    for i in range(maxim):
        Id.append(usrNum)
        Name.append('')
        LastName.append('')
        Age.append('')
        Gender.append('')
        DomHand.append('')
        Type.append('')
    Id[0] = usrNum
    Name[0] = usrName
    LastName[0] = usrLastName
    Age[0] = usrAge
    Gender[0] = usrGender
    DomHand[0] = usrHand
    Type[0] = usrType
    if ((len(Catgenerate)+len(Trial)+len(CatNum)+len(Cat)+len(PersCat)+len(ResCard)+len(CorrAns)+len(Acc)+len(RTime)+len(TstartTime)+len(RstartTime)+len(StimCard)) / 10 != maxim):
        l = [Catgenerate, Trial, CatNum, Cat, StimCard, PersCat, ResCard, CorrAns, Acc, RTime, TstartTime, RstartTime]
        for ind_l in l:
            Index_check(ind_l, maxim)
    
    data_dict = {
        "Subject.num": Id,
        "Subject.name": Name,
        "Subject.surName": LastName,
        "Age": Age,
        "Gender": Gender,
        "Handedness": DomHand,
        "Type": Type,
        "Catgenerator": Catgenerate,
        "Trial": Trial,
        "Category.number": CatNum,
        "Category": Cat,
        "Person.category": PersCat,
        "Response.card": StimCard,
        "Stimuli.card": ResCard,
        "Correct.answer": CorrAns,
        "Acuuracy": Acc,
        "R_time": RTime,
        "Trial.start": TstartTime,
        "Key_Resp.start": RstartTime
    }
    
    userinf = []
    UserInfoDF1 = pd.DataFrame(data_dict, columns=['Subject.num','Trial','Category.number','Category', 'Person.category', 'Response.card', 'Stimuli.card', 'Correct.answer', 'Acuuracy','R_time','Trial.start','Key_Resp.start'])
    UserInfoDF2 = pd.DataFrame(data_dict, columns=['Subject.name','Subject.surName', 'Age', 'Gender', 'Handedness', 'Type', 'Catgenerator'])
    
    UserInfoDF1.to_csv('OutputFile/' + str(usrNum) + '_' + usrName + '_' + usrLastName + '.csv', index=False, header=True, lineterminator='\r\n')
    UserInfoDF2.to_csv('1.csv', index=False, header=True)
    
    file1 = open('OutputFile/' + str(usrNum) + '_' + usrName + '_' + usrLastName + '.csv', "a")
    file2 = open("1.csv", "r")
    for line in file2:
        file1.write(line)
    file1.close()
    file2.close()
    os.remove("1.csv")
    
    if trigger_log:
        trigger_df = pd.DataFrame(trigger_log)
        trigger_file = 'OutputFile/' + str(usrNum) + '_' + usrName + '_' + usrLastName + '_triggers.csv'
        trigger_df.to_csv(trigger_file, index=False)
