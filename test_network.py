import numpy as np

import random
import time
from datetime import datetime


import tensorflow as tf
from tensorflow import keras

import sys
import os
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from oppo import rand_opp
from oppo import random_rollout

from util import str2vec
from util import drop_piece
from util import display_state

from predict_util import get_value
from predict_util import play_move



#wenn das program mehr als zwei (halb)züge vorrausschaut, wird es relativ langsam
def play_other(opponent, model, opp_name,lookahead = 2, inp=True, char= 'X'):
    state = "".join(['_' for i in range(42)])
    #leeres spielfeld wird initialisiert
    char_opp = 'O'
    if char == 'X':
        start = True
        #X beginnt immer
    else:
        char_opp = 'X'
        start = False
    if inp:
        display_state(state)
        print("{0} is {1}".format(opp_name,char_opp))

    while(True):
        #folgende if abfrage regelt den ersten zug, entweder der computer oder 
        #der spieler beginnt
        if start:            
            values = play_move(state,char, lookahead, model)

            if char == 'O':
                move = values.index(min(values))
            else:
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
        else:
            start = True
        
        state, index, move = opponent.choose_move(state, char_opp)
        if inp:
            display_state(state)
            print("{0} is {1}".format(opp_name,char_opp))
        if winner([state,index]) != '_':
            break

    return winner([state,index])


def play_model(opponent, model, opp_name,lookahead = 2, inp=True, char= 'X'):
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


#testet die win bzw. loss rate gegen einen gegner
def conduct_test(n_half, gegner, gegner_name, model, path):
    wins = 0
    losses = 0
    draws = 0
    for i in range(n_half):
        val = play_other(gegner, model,"Game {0} - record w:{1} l:{2} d:{3} \n".format(i,wins,losses,draws) + gegner_name, inp=True)
        if val == 'X':
            wins += 1
        elif val == 'O':
            losses += 1
        else:
            draws += 1
        val = play_other(gegner,model,"Game {0} - record w:{1} l:{2} d:{3} \n".format(i+1,wins,losses,draws) + gegner_name, char= 'O',inp=True)
        if val == 'O':
            wins += 1
        elif val == 'X':
            losses += 1
        else:
            draws += 1
        
        print("{0}/{1} test games played".format(2*i, 2*n_half))

    with open(path, 'a') as _file:
        _file.write("{3}_w:{0}l:{1}d:{2}o:{4}\n".format(wins,losses,draws,datetime.now(),gegner_name))
    
    return



def main(model, n, path = "test_records.txt"):
    #mit dieser funktion wird das model gegen 4 unterschiedliche starke gegener getestet
    g = rand_opp()
    print("opponent {}".format(type(g)))
    conduct_test(n,g,'RNG',model,path)

    g = random_rollout()
    print("opponent {}".format(type(g)))
    conduct_test(n,g,'R50',model,path)

    g = random_rollout(250)
    print("opponent {}".format(type(g)))
    conduct_test(n,g,'R250',model,path)

    g = random_rollout(500)
    print("opponent {}".format(type(g)))
    conduct_test(n,g,"R500",model,path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
