import random
import math
import sys
import time
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from util import drop_piece, get_legal_moves
from node import Node


class Human:
    def __init__(self, c = 'O'):
        self.char = c
        
    def choose_move(self, state,char):
        while(True):
            try:
                k = int(input("column:"))
                print(state[6*k])
                if state[6*k] == '_':
                    return drop_piece(state,k,char) + [k]
            except:
                pass


class rand_opp:
    def __init__(self, c = 'O'):
        self.char = c
        
    def choose_move(self, state,char):
        legal_move_list = get_legal_moves(state)
        l = random.choice(legal_move_list)
        return drop_piece(state,l,char) + [l]

       

class random_rollout():
    def __init__(self, n = 50):
        self.n = n

    def choose_move(self,state,char):
        legal_move_list = get_legal_moves(state)
        eval_move_list =[0 for k in legal_move_list]
        
        
        for k in range(len(legal_move_list)):
            for j in range(self.n):
                eval_move_list[k] += self.rollout(state,char,legal_move_list[k]) #das spiel wird mit zufälligen zügen weiter gespielt bis zum ende
            eval_move_list[k] = 1.0*eval_move_list[k]/self.n
        if char == 'X':
            index = eval_move_list.index(max(eval_move_list))
        else:
            index = eval_move_list.index(min(eval_move_list))
        return drop_piece(state,legal_move_list[index],char) + [legal_move_list[index]]

    def rollout(self,state,char,move):
        m = move
        c = char
        s = drop_piece(state,m,c)
        if c == 'X':
            c = 'O'
        else:
            c = 'X'

        while(winner(s) == '_'):
            s = self.play_move(s[0],c)
            if c == 'X':
                c = 'O'
            else:
                c = 'X'
            pass

        if winner(s) == 'X':
            return 1
        else:
            return 0
        

    def play_move(self, state,char):
        legal_move_list = []
        for k in range(7):
            if state[6*k] == '_':
                legal_move_list.append(k)
        
        l = random.choice(legal_move_list)
        return drop_piece(state,l,char)

