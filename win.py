#der sieger wird anhand des spielfelds sowie des letzten gespielten steines ermittelt
def winner(gameinfo):
    state = gameinfo[0]
    index = gameinfo[1]
    #ist unentschieden? wenn ja return '.'
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
                    else:
                        break
                except:
                    break
        k += 1

    #falls in einer der 4 richtungen mehr als 3 steine in einer reihe sind
    #ist das spiel vorbei und jemand hat gewonnen
    for entry in win_condition:
        if entry > 3:
            return char
    return '_'
    #ansonsten hat niemand gewonnen und es geht weiter
