class Node():
    #in Node wird ein gamestate, die anzahl der siege, die totale anzahl an spielen
    #und eine liste von verzweigenden nodes in der nächsten ebene gespeichert
    def __init__(self, state, parent = None):
        self.state = state
        self.wins = 0
        self.total = 0
        self.leaf = True
        self.child_list = []
        self.parent = parent
        self.terminal = False
    
    def __str__(self):
        return "{0}--{1}--{2}--{3}".format(self.wins, self.total, self.leaf, self.child_list)
    
    
    def add_child(self, node):
        self.leaf = False
        self.child_list.append(node)
    
    def get_children(self):
        return self.child_list
    
    def get_state(self):
        return self.state
    
    def is_leaf(self):
        return self.leaf

    def is_terminal(self):
        return self.terminal
    
    def update_stats(self, win):
        if win == True:
            self.wins += 10
        self.total += 1
        try:
            self.parent.update_stats(win)
        except:
            pass


