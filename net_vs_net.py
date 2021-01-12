import tensorflow as tf
from tensorflow import keras

from datetime import datetime

import sys
sys.path.append('.')
#imports aus dem ordner:
from win import winner

from util import str2vec
from util import drop_piece
from util import display_state

from predict_util import get_value
from predict_util import play_move



def play_model(opponent, model, opp_name,lookahead = 2, inp=True):
    state = "".join(['_' for i in range(42)])
    #leeres spielfeld wird initialisiert
    char_opp = 'O'
    char = 'X'
        
    if inp:
        display_state(state)
        print("{0} is {1}".format(opp_name,char_opp))

    while(True):
        #folgende if abfrage regelt den ersten zug, entweder der computer oder 
        #der spieler beginnt
                   
        values = play_move(state,char, lookahead, model)
        move = values.index(max(values))
        
            
        if state[6*move] != '_':
            pass
        else:
            state, index = drop_piece(state,move,char)
            if inp:
                display_state(state)
                print("{0} is {1}".format(opp_name,char_opp))
            if winner([state,index]) != '_':
                break
       
        values = play_move(state,char_opp, lookahead, opponent)
        move = values.index(min(values))
        
            
        if state[6*move] != '_':
            pass
        else:
            state, index = drop_piece(state,move,char_opp)
            if inp:
                display_state(state)
                print("{0} is {1}".format(opp_name,char_opp))
            if winner([state,index]) != '_':
                break


    return winner([state,index])

def conduct_test(n_half, opponent, opp_name, model, mod_name, path):
    wins = 0
    losses = 0
    draws = 0
    for i in range(n_half):
        val = play_model(opponent, model,"Game {0} - record w:{1} l:{2} d:{3} \n".format(i,wins,losses,draws) + opp_name, inp=True)
        if val == 'X':
            wins += 1
        elif val == 'O':
            losses += 1
        else:
            draws += 1
        val = play_model(model,opponent,"Game {0} - record w:{1} l:{2} d:{3} \n".format(i+1,wins,losses,draws) + mod_name,inp=True)
        if val == 'O':
            wins += 1
        elif val == 'X':
            losses += 1
        else:
            draws += 1
        
        print("{0}/{1} test games played".format(2*i, 2*n_half))

    with open(path, 'a') as _file:
        _file.write("{3}_w:{0}l:{1}d:{2}o:{4}m:{5}\n".format(wins,losses,draws,datetime.now(),opp_name, mod_name))
    
    return

try:
    mod_old = keras.models.load_model('./parameters')
    mod_new = keras.models.load_model('./model_generated_data')
    print("load complete")
except:
    input("loading error")
    exit()


conduct_test(10,mod_old, "old model", mod_new, "new model", 'net_vs_net_results.txt')
input()