import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import random

import sys
sys.path.append('.')
#imports aus dem ordner:
from win import winner

from oppo import rand_opp
from oppo import random_rollout

from util import str2vec
from util import drop_piece

def play_game(player, opponent):


    total_data =[]
    game = []
    results = []

    char = 'X'

    movelist = []
    state = "".join(['_' for i in range(42)])

    while(True):
        
        game.append(str2vec(state))
        #zug wird angehängt

        if char == 'O':
            move = opponent.choose_move(state,char)[-1]
        else:
            move = player.choose_move(state,char)[-1]
           

            
        movelist.append(move)

        
        state, index = drop_piece(state, move, char)

        victor = winner([state,index])

        results.append(1)
        
        #je nach dem wer gewonnen hat werden die züge mit labels versehen

        if victor != '_':

            total_data = total_data + game

            if victor == 'X':
                pass
            elif victor == 'O':
                results = [x * 0 for x in results]
            elif victor == '.':
                results = [x * 0.5 for x in results]
            break            

       
        if char == 'X':
            char ='O'
        else:
            char = 'X'

    return np.array(total_data),np.array(results)





try:
    model = keras.models.load_model('./model_generated_data')
    print("load complete")
except:
    model = keras.Sequential()
    model.add(layers.Dense(42, input_dim = 42, activation="sigmoid", name="inputProcesser")) #blaue und rote steine werden seperat in das netzwerk geleitet
    model.add(layers.Dense(30, activation="sigmoid"))
    model.add(layers.Dense(1,activation = "sigmoid"))

    opt = keras.optimizers.Adam(learning_rate=0.008)#original 0.01
    model.compile(loss = "MSE", optimizer = opt)
    print("new network compiled")

model.summary()

input("press enter to start training")







o_list = [rand_opp(),
random_rollout(),
random_rollout(75),
random_rollout(100),
random_rollout(250),
random_rollout(500)]

samples = 10000


data_x , data_y = play_game(random.choice(o_list), random.choice(o_list))
print("{} samples generated".format(1), end="\r")
for i in range(samples - 1):
    tmp_x , tmp_y = play_game(random.choice(o_list), random.choice(o_list))
    data_x = np.concatenate((data_x , tmp_x), axis = 0)
    data_y = np.concatenate((data_y, tmp_y), axis = 0)
    print("{} samples generated".format(i+2), end="\r")

report = model.fit(x=data_x,y=data_y,epochs = 50)
model.save("./model_generated_data")
input("training done")

with open('tlog_gen.txt', 'a') as _file:
        _file.write(str(report))






