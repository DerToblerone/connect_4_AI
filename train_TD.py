import numpy as np

import random
import time
from datetime import datetime


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


import sys
import os
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from oppo import Human, rand_opp, random_rollout
import test_network

from util import str2vec, drop_piece, reverse_move

#diagnotic  variables
game_counter = 0
gen_counter = 0
error_counter = 0

try:
    model = keras.models.load_model('./model_generated_data')
    print("load complete")
except:
    model = keras.Sequential()
    model.add(layers.Dense(42, input_dim = 42, activation="sigmoid", name="inputProcesser")) #blaue und rote steine werden seperat in das netzwerk geleitet
    model.add(layers.Dense(28, activation="sigmoid"))
    #model.add(layers.Dense(14,activation = "sigmoid"))
    model.add(layers.Dense(1,activation = "sigmoid"))



    opt = keras.optimizers.Adam(learning_rate=0.008)#original 0.01
    model.compile(loss = "binary_crossentropy", optimizer = opt)
    print("new network compiled")

model.summary()

input("press enter to start training")

def display_state(state,value,_type = "self", explore = [-1,-1]):
    os.system('cls||clear')
    print("0 1 2 3 4 5 6")
    for row in range(6):
        r = []
        for column in range(7):
            char = state[6*column + row]
            color = '\x1b[0m'
            if char == 'X':
                color = '\x1b[6;30;42m'
            elif char == 'O':
                color = '\x1b[6;30;41m'

            if column == explore[0] and row == explore[1]:
                color = '\x1b[6;30;44m'
                r.append(color + char +'\x1b[0m' + ' ' )
            else:
                r.append(color + char +'\x1b[0m' + ' ' )
            

        print("".join(r))
    print("current position value estimate: {3} \ngeneration: {0}, total games so far: {1} \nerrors while training: {2}".format(gen_counter, game_counter,error_counter, value))
    print(_type)



def get_value(states):
    value = []
    #hier wird der wert eines zustandes bestimmt
    #dabei wird die tabelle durch das netzwerk ersetzt
    s = np.array(states)
    if states != []:
        value = model.predict(s, batch_size = len(s))
    
    return value

def play_move(state,char,terminal = False):
    #opp_char = 'O' if char == 'X' else 'X'
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
                    move_values[i] = 1
                else:
                    move_values[i] = 0 
                continue            
            check_moves.append(s[0])
            index_list.append(i)

    for k in range(len(check_moves)):
        check_moves[k] = str2vec(check_moves[k])
    predicted_values = get_value(check_moves)
    for i in range(len(predicted_values)):
        move_values[index_list[i]] = predicted_values[i][0]
         
    return move_values


def exploration_move(state):
    prob = []
    for i in range(7):
        if state[i*6] =='_':
            prob.append(i)
    return random.choice(prob)

def play(state, c_start ='X'):

    display_state(state,0.5)

    total_data =[]
    game = []
    results = []

    char = c_start
    m = -1
    movelist = []
    if random.random() < 0.125:
        exploration_rate = 0.25
    else:
        exploration_rate = 0
    value_buffer = 0.5
    explore = False
    #es soll immer der wert des vorherigen zuges in richtung des nächsten streben
    #es wird also zuerst eine position des spielfeldes an game angehängt
    #dann wird ein neuer zug gespielt
    #dann wird der werte liste result(hier stehen die neuen sollwerte der züge)
    #der wert der neuen position angehängt
    #das heisst: pos(n) wird mit val(n+1) abgespeichert(natürlich ist val(n+1) der höchstmögliche zugwert nach 
    # zwei halbzügen)
    while(True):
        
        game.append(str2vec(state))
        #zug wird angehängt

        values = play_move(state,char)
        if m >= 0:
            move = m
            m = -1
        else:
            if char == 'O':
                move = values.index(min(values))
            else:
                move = values.index(max(values))
        #wert der neuen position wird in value buffer gesteckt
        value_buffer = values[move]
        current_value = value_buffer

        if random.random() < exploration_rate:
            move = exploration_move(state)
            exploration_rate =  exploration_rate * 0.2
            current_value = "exploration"
            explore = True
            
            
        movelist.append(move)
        
        state, index = drop_piece(state, move, char)
        if explore:
            display_state(state, current_value,explore = index)
            explore = False
        else:
            display_state(state, current_value)

        victor = winner([state,index])
        
        #je nach dem wer gewonnen hat werden die züge mit labels versehen
        if victor != '_':

            total_data = total_data + game
            if victor == 'X':
                results.append(1) 
            elif victor == 'O':
                results.append(0)
            elif victor == '.':
                results.append(0.5)

            #versuch von kurzen spielen mehr zu lernen


            for k in range(2,4):
                results[-(k)] += (results[-1] - results[-(k)])*(0.8**(k-1))

            break
            #falls ein spieler gewinnt, so wird der vorherige zug zum spielausgang assoziiert

            #code kann sowieso nicht erreicht werden
        else: 
            #der wert des gespielten zuges wird zur vorherigen position assoziiert
            results.append(value_buffer)
       
        if char == 'X':
            char ='O'
        else:
            char = 'X'
    return np.array(total_data),np.array(results)


def play_opp(opponent, state, c_start ='X'):

    type_val = type(opponent)
    display_state(state,0.5,_type= type_val)
    


    total_data =[]
    game = []
    results = []

    char = c_start
    opp_char = 'X'
    if char == 'X':
        opp_char = 'O'
    char = 'X'
    movelist = []
    print("Network is {}".format(c_start))
    value_buffer = 0.5
    
    while(True):
        
        game.append(str2vec(state))
        #zug wird angehängt
        
        values = play_move(state,char)

        if char == 'O':
            move = values.index(min(values))
        else:
            move = values.index(max(values))
        #wert der neuen position wird in value buffer gesteckt
        
        value_buffer = values[move] 

        if char == opp_char:
            move = opponent.choose_move(state,char)[-1]
           

            
        movelist.append(move)

        
        state, index = drop_piece(state, move, char)

        display_state(state, value_buffer,_type= type_val)
        print("Network is {}".format(c_start))

        victor = winner([state,index])
        
        #je nach dem wer gewonnen hat werden die züge mit labels versehen
        if victor != '_':

            total_data = total_data + game
            if victor == 'X':
                results.append(1) 
            elif victor == 'O':
                results.append(0)
            elif victor == '.':
                results.append(0.5)

            #der ausgang des spiels hat auswirkungen auf die vergangenen zug bewertungen
            for k in range(2,min(10,len(results))):
                results[-(k)] += (results[-1] - results[-(k)])*(0.75**(k-1))

            break
            
        else: 
            results.append(value_buffer)

       
        if char == 'X':
            char ='O'
        else:
            char = 'X'

    return np.array(total_data),np.array(results)

#training code beginnt hier

generations = 50
games = 10

#diese gegnerliste wird durchlaufen beim training
opp_list ={
rand_opp(),
random_rollout(30),
random_rollout(50),
random_rollout(70),
random_rollout(100),
random_rollout(250),
random_rollout(1000)}

opp_list = []
#das netzwerk spielt nur gegen sich selbst in diesem fall

state = "".join(["_" for x in range(42)])#empty field



for gen in range(generations):
    total_moves = 0

    data_x, data_y = play(state)
    for g in range(games-1):
        game_counter += 1
        tmp_x, tmp_y = play(state)
        data_x = np.concatenate((data_x , tmp_x), axis = 0)
        data_y = np.concatenate((data_y, tmp_y), axis = 0)
        for o in opp_list:
            #danach spielt es noch gegen die anderen gegner in der liste
            tmp_x, tmp_y = play_opp(o,state,'X')
            data_x = np.concatenate((data_x , tmp_x), axis = 0)
            data_y = np.concatenate((data_y, tmp_y), axis = 0)
            tmp_x, tmp_y = play_opp(o,state,'O')
            data_x = np.concatenate((data_x , tmp_x), axis = 0)
            data_y = np.concatenate((data_y, tmp_y), axis = 0)
            game_counter += 2
    try:
        #es lernt sofort von den gespielten spielen
        model.fit(x=data_x,y=data_y)
        total_moves = len(data_x)
        print("{0} moves in data set, {1} games played, winner: {2}".format(len(data_x),g+1,data_y[-1]), end= "\r")
        
    except:
        print("error training game {0}".format(g))
        error_counter += 1
    
    model.save("./model_step2")

    with open('training_log.txt', 'a') as _file:
        _file.write("{3}_g:{0}c:{1}m:{2}\n".format(gen,game_counter,total_moves,datetime.now()))
    print("generation {0} done".format(gen))
    gen_counter += 1
    if (gen+1)%5 == 0:
        print("testing")
        test_network.main(model,5)
        

input()