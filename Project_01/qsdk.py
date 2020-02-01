import math

def nCX(k,c,t,b):
    nc = len(c)
    if nc == 1:
        k.gate("cnot", [c[0], t[0]])
    elif nc == 2:
        k.toffoli(c[0], c[1], t[0])
    else:
        nch = math.ceil(nc/2)
        c1 = c[:nch]
        c2 = c[nch:]
        c2.append(b[0])
        nCX(k,c1,b,[nch+1])
        nCX(k,c2,t,[nch-1])
        nCX(k,c1,b,[nch+1])
        nCX(k,c2,t,[nch-1])
    return