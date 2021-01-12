import sys
import os
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from oppo import Human
from oppo import rand_opp
from oppo import random_rollout

from util import drop_piece

def display_state(state):
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

            r.append(color + char +'\x1b[0m' + ' ' )
        print("".join(r))


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
opp = random_rollout(1500)
opp2 = Human()
play(opp0,opp)
play(opp,opp0)
input()
