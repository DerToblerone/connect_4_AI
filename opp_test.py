import sys
import os
sys.path.append('.')
#imports aus dem ordner:
from win import winner

from oppo import Human, rand_opp, random_rollout
from mcts import mcts
from util import drop_piece, display_state


def play(player, opponent, lookahead = 2, inp=True, char= 'X', human= True):
    state = "".join(['_' for i in range(42)])
    #leeres spielfeld wird initialisiert
    char_human = 'O'

    if inp:
        display_state(state)

    while(True):
        #folgende if abfrage regelt den ersten zug, entweder der computer oder 
        #der spieler beginnt
        
        state, index, _ = player.choose_move(state, char)
        if winner([state,index]) != '_':
            if inp:
                display_state(state)
                print("winner is {0}".format(winner([state,index])))
                input()
            break

        if inp:
            display_state(state)

        state, index, _ = opponent.choose_move(state, char_human)
        if winner([state,index]) != '_':
            if inp:
                display_state(state)
                print("winner is {0}".format(winner([state,index])))
                input()
            break
            

        if inp:
            display_state(state)
    return


pl = random_rollout(50)
opp0 = random_rollout(250)
opp = random_rollout(3000)
opp2 = Human()
montecarlo = mcts(15000, 20)
mc2 = mcts(15000, 7)
play(montecarlo, mc2)
play(mc2, montecarlo)

input()
