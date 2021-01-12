import numpy as np

import random
import time

import tensorflow as tf
from tensorflow import keras


import sys
import os
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from oppo import Human

from util import display_state
from util import str2vec
from util import drop_piece



path = input("specify path:")
if len(path) == 0:
    path = ('./parameters')
    


input("path: {} - press enter".format(path))

try:
    model = keras.models.load_model(path)
    print("load complete")
except:
    input("unable to load")
    exit()
    


model.summary()


#für get_value und play_move gibt es in predict_util.py eine erklärung
#die hier angeführten versionen nehmen aber kein model als input
def get_value(states):
    value = []
    #hier wird der wert eines zustandes bestimmt
    #dabei wird die tabelle durch das netzwerk ersetzt
    s = np.array(states)
    if states != []:
        value = model.predict(s, batch_size = len(s))
    
    return value

def play_move(state,char,lookahead, terminal = 0):
    opp_char = 'O' if char == 'X' else 'X'
    move_values = [0,0,0,0,0,0,0]
    check_moves =[] #züge die weiter betrachtet werden müssen
    index_list = []#wo müssen die wertungen wieder eingefügt werden
    progress = ""
    print(progress, end = "\r")
    for i in range(7):
        
        if state[i*6] != '_':
            if(char == 'X'):
                move_values[i]= -1#unmögliche züge bekommen eine wertungszahl, s.d. mögliche züge immer bevorzugt werden
            else:
                move_values[i] = 2
        else:
            s = drop_piece(state,i,char)
            if winner(s) != '_':
                if char == 'X':
                    move_values[i] =1 
                else:
                    move_values[i] = 0
                progress = progress + ".."  
                continue 
            check_moves.append(s[0])
            index_list.append(i) 
        if terminal == 0:
            print(progress, end = "\r")    
    if terminal >= lookahead:   
        for k in range(len(check_moves)):
            check_moves[k] = str2vec(check_moves[k])
        predicted_values = get_value(check_moves)
        for i in range(len(predicted_values)):
            move_values[index_list[i]] = predicted_values[i][0]
    else:
        t = terminal
        for i in range(len(check_moves)):   
            temp_val = play_move(check_moves[i],opp_char,lookahead,terminal=t+1)
            if char == 'X':
                move_values[index_list[i]] = min(temp_val)
            else:
                move_values[index_list[i]] = max(temp_val)
            progress = progress + ".."
            if(terminal == 0):
                print(progress, end ="\r")
    return move_values

def reverse_move(state, column):
    l = list(state)
    for i in range(6):
        if l[6*column + i] != "_":
            l[6*column + i] = "_"
            break      
    return "".join(l)

def exploration_move(state):
    prob = []
    for i in range(7):
        if state[i*6] =='_':
            prob.append(i)
    return random.choice(prob)


#wenn das program mehr als zwei (halb)züge vorrausschaut, wird es relativ langsam
def play_other(opponent, lookahead = 2, inp=True, char= 'X', human= True):
    state = "".join(['_' for i in range(42)])
    #leeres spielfeld wird initialisiert
    char_human = 'O'
    if char == 'X':
        start = True
        #X beginnt immer
    else:
        char_human = 'X'
        start = False
    if inp:
        display_state(state)

    while(True):
        #folgende if abfrage regelt den ersten zug, entweder der computer oder 
        #der spieler beginnt
        if start:            
            values = play_move(state,char, lookahead)

            if char == 'O':
                move = values.index(min(values))
            else:
                move = values.index(max(values))

            
            if state[6*move] != '_':
                pass
            else:
                state, index = drop_piece(state,move,char)
                if winner([state,index]) != '_':
                    if inp:
                        display_state(state)
                        print("winner is {0}".format(winner([state,index])))
                        input()
                    break
            if inp:
                display_state(state)
                print(values)
                #print(len(total_data))
        else:
            start = True
        if human:
            state, index, move = opponent.choose_move(state, char_human)
        if winner([state,index]) != '_':
            if inp:
                display_state(state)
                print("winner is {0}".format(winner([state,index])))
                input()
            break
            

        if inp:
            display_state(state)
    return



gegner = Human()
state = "".join(["_" for x in range(42)])#empty field

while(True):
    try:
        look_ahead = int(input("specify how many moves to look ahead(2 recommended):"))
        break
    except:
        print("integer value expected!")


while(True):
    play_other(gegner, look_ahead)
    input()

    play_other(gegner,look_ahead, char= 'O')
    input()

input()
