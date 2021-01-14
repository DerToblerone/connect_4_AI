import tensorflow as tf
from tensorflow import keras

import sys
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from oppo import Human

from util import str2vec, display_state, drop_piece
from predict_util import get_value, play_move



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
            print("calculating", end = "\r")         
            values = play_move(state,char, lookahead, model)
            print("calculation done")         

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

    play_other(gegner,look_ahead, char= 'O')

input()
