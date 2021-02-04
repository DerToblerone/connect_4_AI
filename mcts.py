import random
import math
import sys
import time
sys.path.append('.')
#imports aus dem ordner:
from win import winner
from util import drop_piece, get_legal_moves,display_state
from node import Node

class mcts():
    def __init__(self, n, exp = 7):
        self.n = n
        self.exp_parameter = exp
        self.color_array = ['\x1b[0;30;41m',#0
                            '\x1b[0;30;41m',#10
                            '\x1b[0;30;41m',#20
                            '\x1b[0;30;41m',#30
                            '\x1b[0;30;43m',#40
                            '\x1b[0;30;42m',#50
                            '\x1b[6;30;42m',#60
                            '\x1b[6;30;42m',#70
                            '\x1b[6;30;42m',#80
                            '\x1b[6;30;42m',#90
                            '\x1b[0;30;46m']#100

    def choose_move(self, state, char):
        factor = self.exp_parameter
        self.side = char
        c = char
        #es gibt maximal 42 züge in 4 gewinnt + leeres spielfeld, deswegen ist layers ein array mit 43 listen
        #in den verschiedenen layern sind Node objekte abgespeichert.
        root = Node(state)
        legal_moves = get_legal_moves(state)
        for move in legal_moves:
            new_state = drop_piece(state,move,c)
            if winner(new_state) != '_':
                return new_state + [move]
            root.add_child(Node(new_state[0], parent = root))

        other = 'X'
        if char == 'X':
            other = 'O'
        
        for i in range(self.n):
            current_node = root
            c = char
            while True:
                scores = [0 for i in range(len(current_node.child_list))]
                j = 0
                break_loop = False
                for child in current_node.child_list:
                    if child.total == 0:
                        if c == char:
                            result = self.rollout(child.get_state(),other)
                        else:
                            result = self.rollout(child.get_state(),char)
                        child.update_stats(result)
                        break_loop = True
                        break
                    else:
                        if c == char:
                            scores[j] = 1.0*child.wins/child.total + factor*math.sqrt(math.log(current_node.total)/child.total)
                        else:
                            scores[j] = 10-1.0*child.wins/child.total + factor*math.sqrt(math.log(current_node.total)/child.total)
                    j += 1
                if break_loop:
                    break
                current_node = current_node.child_list[scores.index(max(scores))]

                if c == 'X':
                    c = 'O'
                else:
                    c = 'X'

                if current_node.is_leaf():
                    if current_node.is_terminal():
                        if current_node.wins > 0:
                            current_node.update_stats(True)
                        else:
                            current_node.update_stats(False)
                        break
                    else:
                        current_state = current_node.get_state()

                        moves = get_legal_moves(current_state)
                        
                        if len(moves) == 0:
                            if current_node.wins > 0:
                                current_node.update_stats(True)
                            else:
                                current_node.update_stats(False)
                            break
                        
                        break_loop = False
                    
                        for move in moves:
                            new_state = drop_piece(current_state,move,c)
                            new_node = Node(new_state[0], parent = current_node)
                            current_node.add_child(new_node)
                            win = winner(new_state)
                            if win != '_':
                                if win == char:
                                    current_node.child_list[-1].update_stats(True)
                                else:
                                    current_node.child_list[-1].update_stats(False)
                                current_node.child_list[-1].terminal = True
                        
                    if break_loop:
                        break
                
            if i%100 == 99:
                vals = [10.0*l.wins/l.total for l in root.child_list]
                print("".join([self.color_array[int(val/10)] + "{0:,.2f}".format(val) + "\x1b[0m " for val in vals]), end = "\r")


        scores = []
        for k in range(len(legal_moves)):
            score = 1.0*root.child_list[k].wins/root.child_list[k].total
            scores.append(score)
        index = scores.index(max(scores))
        return drop_piece(state, legal_moves[index], char) + [legal_moves[index]]

    def update_path(self, layers, path, val):
        for i in range(len(path)):
            layers[i][path[i]].update_stats(val)    

    def rollout(self,state,char):
        c = char
        s = self.play_move(state,c)

        while(winner(s) == '_'):            
            if c == 'X':
                c = 'O'
            else:
                c = 'X'
            s = self.play_move(s[0],c)

        if winner(s) == self.side:
            return True
        else:
            return False
        

    def play_move(self, state,char):
        l = random.choice(get_legal_moves(state))
        return drop_piece(state,l,char)
