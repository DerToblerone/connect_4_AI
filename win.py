def winner(gameinfo):
    state = gameinfo[0]
    index = gameinfo[1]
    if any(['_' == c for c in state]):
        pass
    else:
        return '.'
    x = index[0]
    y = index[1]
    char = state[6*x + y]
    

    #wieviele stücke sind mit dem index auf diesen achsen verbunden
    win_condition = [1,1,1,1]
    I = [1, 2, 3]
    k = 0
    for coef in [(0,1),(1,0),(1,1),(-1,1)]:
        for sgn in[-1,1]:
             for i in I:
                _x = x + sgn*coef[0]*i
                _y = y + sgn*coef[1]*i
                if _x < 0:
                    break
                elif _x > 6:
                    break
                elif _y < 0 :
                    break
                elif _y > 5:
                    break
                try:
                    if state[6*(_x) + _y] == char:
                        win_condition[k] += 1
                        if win_condition[k] > 3:
                            pass
                            #print("x: {0}; y: {1}; _x: {2}, _y: {3}, k: {4}".format(x,y,_x,_y,k))
                    else:
                        break
                except:
                    break
        k += 1

    
    for entry in win_condition:
        if entry > 3:
            return char
    return '_'