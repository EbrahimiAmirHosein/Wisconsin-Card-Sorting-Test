def WCST_trial(windows, background, timer, usrInfo, eeg_port=None):
    ID, Name, SurName, Age, Gender, Hand, Type = usrInfo
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
        choices = ['color', 'form', 'number']
        cntWrong = 0
        cntCorrect = 0 
        check_quit(windows) 
        
        if idx_cat > 0:
            trial_containter = i_trial
            
        while(i_trial < 129):
            check_quit(windows) 
            mian_choice = category[idx_cat]
            
            if (str(category[idx_cat]) == 'color'):
                Cat.append(1)
            elif (str(category[idx_cat]) == 'form'):
                Cat.append(2)     
            else:
                Cat.append(3)
                
            CatNum.append(str(idx_cat+1))
            load_img, color, form, number = CFN(i_trial)
            StimCard.append(load_img[7:])
            x = displayImg2(windows, "trial_cards/" + load_img, 0, 1, (250,250), (0,-300))
            
            check_quit(windows)
            nfc_l = []
            trial_start_time = timer.getTime()
            TstartTime.append(trial_start_time)
            chosen = get_choice(windows, background, 5, x)
            keyresp_start_time = timer.getTime()

            # Set correct answer
            if(mian_choice == 'color' and color == 'red'):
                CorrAns.append(1)
            elif(mian_choice == 'color' and color == 'green'):
                CorrAns.append(2)                
            elif(mian_choice == 'color' and color == 'yellow'):
                CorrAns.append(3) 
            elif(mian_choice == 'color' and color == 'blue'):
                CorrAns.append(4) 
            if(mian_choice == 'form' and form == 'Triangles'):
                CorrAns.append(1)
            elif(mian_choice == 'form' and form == 'Stars'):
                CorrAns.append(2)                
            elif(mian_choice == 'form' and form == 'Crosses'):
                CorrAns.append(3) 
            elif(mian_choice == 'form' and form == 'Dots'):
                CorrAns.append(4) 
            if(mian_choice == 'number' and number == '1'):
                CorrAns.append(1)
            elif(mian_choice == 'number' and number == '2'):
                CorrAns.append(2)                
            elif(mian_choice == 'number' and number == '3'):
                CorrAns.append(3) 
            elif(mian_choice == 'number' and number == '4'):
                CorrAns.append(4)                 
                
            if 'Slow' in chosen:
                i_trial += 1
                Trial.append(i_trial)
                nfc_l.append('No answer')
                PersCat.append(nfc_l) 
                ResCard.append('No answer')
                Acc.append('No answer')
                RstartTime.append('No answer')
                RTime.append('No answer')
                if idx_cat != 0 and trial_containter + 24 <= i_trial and cntCorrect < 10:
                    SaveDate(ID, Name, SurName, Age, Gender, Hand, Type, Catgenerator, Trial, CatNum, Cat, StimCard, ResCard, PersCat, CorrAns, Acc, RTime, TstartTime, RstartTime)
                    return
                continue

            RstartTime.append(keyresp_start_time)
            Reaction_time = keyresp_start_time - trial_start_time
            RTime.append(Reaction_time)
            
            if(not 'Slow' in chosen):
                ResCard.append(str(chosen[0]))
                
            check_quit(windows) 
            
            if(chosen[1] == color):
                nfc_l.append(1)
            if(chosen[2] == form):
                nfc_l.append(2)  
            if(chosen[0] == number):
                nfc_l.append(3) 
            if(chosen[1] != color and chosen[2] != form and chosen[0] != number):
                nfc_l.append(0)
                
            PersCat.append(nfc_l)  

            # SEND EEG TRIGGERS BASED ON RESPONSE
            if((mian_choice == 'color' and chosen[1] != color) or 
               (mian_choice == 'form' and chosen[2] != form) or
               (mian_choice == 'number' and chosen[0] != number)):
                # WRONG ANSWER - Send trigger 2
                if eeg_port is not None:
                    eeg_port.write(bytes([2]))  # Send trigger 2 for wrong answer
                    print("Sent EEG trigger: 2 (Wrong answer)")
                
                cntCorrect = 0
                Acc.append(0)
                Trial.append(i_trial+1)
                i_trial += 1
                cntWrong += 1   
                x.autoDraw = True
                displayImg(windows, 'feedbacks/' + 'negative', 1.82, 0, (400,400), (0,0))
                x.autoDraw = False
                display_blank(windows, background, 0.98)
                if idx_cat != 0 and trial_containter + 24 <= i_trial and cntCorrect < 10:
                    SaveDate(ID, Name, SurName, Age, Gender, Hand, Type, Catgenerator, Trial, CatNum, Cat, StimCard, ResCard, PersCat, CorrAns, Acc, RTime, TstartTime, RstartTime)
                    return

            if((mian_choice == 'color' and chosen[1] == color) or 
               (mian_choice == 'form' and chosen[2] == form) or
               (mian_choice == 'number' and chosen[0] == number)):
                # CORRECT ANSWER - Send trigger 1
                if eeg_port is not None:
                    eeg_port.write(bytes([1]))  # Send trigger 1 for correct answer
                    print("Sent EEG trigger: 1 (Correct answer)")
                
                Acc.append(1)   
                Trial.append(i_trial+1)
                i_trial += 1
                cntCorrect += 1
                load_img, color, form, number = CFN(i_trial)
                x.autoDraw = True
                displayImg(windows, 'feedbacks/' + 'positive', 1.82, 0, (400,400), (0,0))
                x.autoDraw = False
                display_blank(windows, background, 0.98)
                if idx_cat != 0 and trial_containter + 24 <= i_trial and cntCorrect < 10:
                    SaveDate(ID, Name, SurName, Age, Gender, Hand, Type, Catgenerator, Trial, CatNum, Cat, StimCard, ResCard, PersCat, CorrAns, Acc, RTime, TstartTime, RstartTime)
                    return
                if cntCorrect == 10:
                    break
                    
    SaveDate(ID, Name, SurName, Age, Gender, Hand, Type, Catgenerator, Trial, CatNum, Cat, StimCard, ResCard, PersCat, CorrAns, Acc, RTime, TstartTime, RstartTime)
