from psychopy import visual , core , event , gui , sound 
from helper import check_quit , display_blank , Txt_loader , displayImg ,displayImg2 , SaveDate
import pandas as pd
import random

def get_sequence(path): 
  df = pd.read_csv(path + ".csv")
  arr = df.values
  res = pd.DataFrame(arr.reshape(3, 128))
  return res
  
 
def get_choice(windows ,background, MaxTime, x):
    mouse = event.Mouse(visible=True, newPos=None, win=windows)
    Y_up = 374
    Y_down = 127
    again = False
    imgClk = core.Clock()
    while (imgClk.getTime() < MaxTime and not again):
        check_quit(windows)
        pos = mouse.getPos() 
        clickedX , clickedY = pos[0] , pos[1]
        if (mouse.getPressed() == [1,0,0]):
            check_quit(windows)
            if clickedX > -592 and clickedX < -341 and clickedY < Y_up and clickedY > Y_down:
                formNum = ['1','red','Triangles']
                again = True
            elif clickedX > -282 and clickedX < -32 and clickedY < Y_up and clickedY > Y_down:
                formNum = ['2','green','Stars']
                again = True
            elif clickedX > 28 and clickedX < 279 and clickedY < Y_up and clickedY > Y_down:
                formNum = ['3','yellow','Crosses']
                again = True
            elif clickedX > 341 and clickedX < 595 and clickedY < Y_up and clickedY > Y_down:
                formNum = ['4','blue','Dots']
                again = True
            else:
                again = False
                
    if (not mouse.getPressed() == [1,0,0]):
        x.autoDraw = True
        displayImg(windows ,"feedbacks/" + '2late' ,  1.98 , 0, (400,400), (0,0))
        x.autoDraw = False
        display_blank(windows , background , 0.98)
        formNum = ['Too','Slow','Reaction']
    return formNum
    
def catGen():
    catNum = []
    Color = ['color']
    Other = ['form' , 'color' ,'number' ,'form' , 'number']
    again = True
    while(again):
        again = False
        random.shuffle(Other)
        total = Color+Other
        for i in range (5):
            if total[i]==total[i+1] :
                again = True

    return total 
    
def CFN(i_trial):
    seq = get_sequence("StimuliSequence") 
    color = ['red','green','yellow','blue']
    form = ['Triangles' , 'Stars' , 'Crosses' , 'Dots']
    number = ['1' ,'2' ,'3' ,'4']
    C = seq[i_trial][0] - 1 #color
    F = seq[i_trial][1] - 1 #form
    N = seq[i_trial][2] - 1 #number
    load_img = 'images_' + number[N] + color[C] + form[F]
    return load_img , color[C] , form[F] , number[N]
    
def WCST_trial(windows , background , timer ,usrInfo):
    ID,Name,SurName,Age,Gender,Hand,Type = usrInfo
    Trial = []
    CatNum = []
    Cat = []
    StimCard = []
    ResCard = []
    PersCat = []
    CorrAns = []
    Acc = []
    RTime = []
    TstartTime = []
    RstartTime = []
    Catgenerator = []
    check_quit(windows) 
    category = catGen()
    Catgenerator.append(str(category))
    
    i_trial = 0

    for idx_cat in range(6):                
        check_quit(windows) 
        choices = ['color' , 'form' , 'number']
        cntWrong = 0
        cntCorrect = 0 
        check_quit(windows) 
        if idx_cat > 0:
            trial_containter = i_trial
        while( i_trial < 129 ):
            check_quit(windows) 
            mian_choice = category[idx_cat]
            if (str(category[idx_cat]) == 'color'):
                Cat.append(1)
            elif (str(category[idx_cat]) == 'form'):
                Cat.append(2)     
            else:
                Cat.append(3)
            CatNum.append(str(idx_cat+1))
            load_img , color, form , number = CFN(i_trial)
            StimCard.append(load_img[7:])
            x = displayImg2(windows ,"trial_cards/" + load_img , 0 , 1, (250,250), (0,-300))
            
            
            check_quit(windows)
            nfc_l = []
            trial_start_time = timer.getTime()
            TstartTime.append(trial_start_time)
            chosen = get_choice(windows,background , 5 , x)
            keyresp_start_time = timer.getTime()

            if( mian_choice == 'color' and color == 'red' ):
                CorrAns.append(1)
            elif(mian_choice == 'color' and color == 'green'):
                CorrAns.append(2)                
            elif(mian_choice == 'color' and color == 'yellow'):
                CorrAns.append(3) 
            elif(mian_choice == 'color' and color == 'blue'):
                CorrAns.append(4) 
            if( mian_choice == 'form' and form == 'Triangles' ):
                CorrAns.append(1)
            elif(mian_choice == 'form' and form == 'Stars'):
                CorrAns.append(2)                
            elif(mian_choice == 'form' and form == 'Crosses'):
                CorrAns.append(3) 
            elif(mian_choice == 'form' and form == 'Dots'):
                CorrAns.append(4) 
            if( mian_choice == 'number' and number == '1' ):
                CorrAns.append(1)
            elif(mian_choice == 'number' and number == '2'):
                CorrAns.append(2)                
            elif(mian_choice == 'number' and number == '3'):
                CorrAns.append(3) 
            elif(mian_choice == 'number' and number == '4'):
                CorrAns.append(4)                 
            if 'Slow' in chosen :
                i_trial+=1
                Trial.append(i_trial)
                nfc_l.append('No answer')
                PersCat.append(nfc_l) 
                ResCard.append('No answer')
                Acc.append('No answer')
                RstartTime.append('No answer')
                RTime.append('No answer')
                if idx_cat !=0 and trial_containter + 24 <= i_trial and cntCorrect < 10 :
                    SaveDate(ID, Name ,SurName, Age , Gender ,Hand ,Type , Catgenerator , Trial , CatNum , Cat ,StimCard , ResCard , PersCat , CorrAns , Acc ,RTime , TstartTime , RstartTime)
                    return
                continue

                
            
            RstartTime.append(keyresp_start_time)
            Reaction_time =  keyresp_start_time - trial_start_time ;
            RTime.append(Reaction_time)
            if(not 'Slow' in chosen):
                ResCard.append(str(chosen[0]))
            check_quit(windows) 
            
            if(chosen[1] == color ):
                nfc_l.append(1)
               
            if(chosen[2] == form):
                nfc_l.append(2)  

            if(chosen[0] == number):
                nfc_l.append(3) 

            if(chosen[1] != color and chosen[2] != form and chosen[0] != number):
                nfc_l.append(0)
                
            PersCat.append(nfc_l)  

            if((  mian_choice == 'color'  and chosen[1] != color ) or 
                    (mian_choice == 'form'   and chosen[2] != form  ) or
                    (mian_choice == 'number' and chosen[0] != number)):
                cntCorrect = 0;
                Acc.append(0)
                Trial.append(i_trial+1)
                i_trial += 1
                cntWrong += 1   
                x.autoDraw = True
                displayImg(windows ,'feedbacks/' +'negative' , 1.82 , 0, (400,400), (0,0))
                x.autoDraw = False
                display_blank(windows , background , 0.98)
                if idx_cat !=0 and trial_containter + 24 <= i_trial and cntCorrect < 10 :
                    SaveDate(ID, Name ,SurName, Age , Gender ,Hand ,Type , Catgenerator , Trial , CatNum , Cat ,StimCard , ResCard , PersCat , CorrAns , Acc ,RTime , TstartTime , RstartTime)
                    return
            
            if((  mian_choice == 'color'  and chosen[1] == color ) or 
                    (mian_choice == 'form'   and chosen[2] == form  ) or
                    (mian_choice == 'number' and chosen[0] == number)):
                Acc.append(1)   
                Trial.append(i_trial+1)
                i_trial += 1
                cntCorrect += 1
                load_img , color, form , number = CFN(i_trial)
                x.autoDraw = True
                displayImg(windows ,'feedbacks/' + 'positive' , 1.82 , 0, (400,400), (0,0))
                x.autoDraw = False
                display_blank(windows , background , 0.98)
                if idx_cat !=0 and trial_containter + 24 <= i_trial and cntCorrect < 10 :
                    SaveDate(ID, Name ,SurName, Age , Gender ,Hand ,Type , Catgenerator , Trial , CatNum , Cat ,StimCard , ResCard , PersCat , CorrAns , Acc ,RTime , TstartTime , RstartTime)
                    return
                if cntCorrect == 10 :
                    break
                    
    SaveDate(ID, Name ,SurName, Age , Gender ,Hand ,Type , Catgenerator , Trial , CatNum , Cat ,StimCard , ResCard , PersCat , CorrAns , Acc ,RTime , TstartTime , RstartTime)            
def Finish(windows,background):
    background.autoDraw = False
    displayImg(windows,"finish",0,True,None,None)
    event.waitKeys()
