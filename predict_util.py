import numpy as np

import tensorflow as tf
from tensorflow import keras

import sys
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from util import str2vec, drop_piece

def get_value(states, model):
    value = []
    #hier wird der wert eines zustandes bestimmt
    #dabei wird die tabelle durch das netzwerk ersetzt
    s = np.array(states)
    if states != []:
        value = model.predict(s, batch_size = len(s))
    
    return value

def play_move(state,char,lookahead, model, terminal = 0):
    opp_char = 'O' if char == 'X' else 'X'
    move_values = [0,0,0,0,0,0,0]
    check_moves =[] #züge die weiter betrachtet werden müssen
    index_list = []#wo müssen die wertungen wieder eingefügt werden
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
                continue 
            check_moves.append(s[0])
            index_list.append(i) 
        if terminal == 0:
            pass
    if terminal >= lookahead:   
        for k in range(len(check_moves)):
            check_moves[k] = str2vec(check_moves[k])
        predicted_values = get_value(check_moves,model)
        for i in range(len(predicted_values)):
            move_values[index_list[i]] = predicted_values[i][0]
    else:
        t = terminal
        for i in range(len(check_moves)):   
            temp_val = play_move(check_moves[i],opp_char,lookahead,model,terminal=t+1)
            if char == 'X':
                move_values[index_list[i]] = min(temp_val)
            else:
                move_values[index_list[i]] = max(temp_val)
            if(terminal == 0):
                pass
    return move_values