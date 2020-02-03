import qsdk     # from qsdk import nCX

def U_init(k,tape,head):
    for i in tape:
        k.gate('prepz', [i])
    k.gate('x',[tape[1]]) # Test Read Head
    for i in head:
        k.gate('prepz', [i])
    k.gate('x',[head[2]]) # Test Read Head

def U_read(k, read, head, tape, ancilla):
    # Reset read (prepz measures superposed states... need to uncompute)
    for cell in range(0, len(tape)):
        enc = format(cell, '#0'+str(len(head)+2)+'b')   # 2 for '0b' prefix
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
        qsdk.nCX(k, head+[tape[cell]], read, ancilla)
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
    return

def U_fsm():
    # k.gate(fsm, [q_rw, q_hp, q_cs, q_sm])  
    return
    
def U_write(k, write, head, tape, ancilla):
    # Reset write (prepz measures superposed states... need to uncompute)
    for cell in range(0, len(tape)):
        enc = format(cell, '#0'+str(len(head)+2)+'b')   # 2 for '0b' prefix
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
        qsdk.nCX(k, head+write, [tape[cell]], ancilla)
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
    return
 
def U_move(k, move, head, anc, test):
    # Prepz measures superposed states... need to uncompute
    # Last carry not accounted, All-ones overflows to All-zeros

    k.gate('h',[head[0]])               # Test Move Head
    k.gate('h',[head[1]])               # Test Move Head
    k.gate('h',[head[2]])               # Test Move Head
    k.gate('cnot',[head[0],test[0]])    # Test Move Head Association
    k.gate('cnot',[head[1],test[1]])    # Test Move Head Association
    k.gate('cnot',[head[2],test[2]])    # Test Move Head Association
    k.gate('x', move)                   # Test Move Right

    # Quantum Adder
    # TBD: Generalized Head size

    # Simplified Circuit for 1-bit Move and no initial carry
    q_carry0(k, move[0], head[0],         anc[0]) # no c0
    k.gate('toffoli', [anc[0], head[1], anc[1]])  # no a1
    k.gate('cnot',[anc[1],head[2]])
    k.gate('toffoli', [anc[0], head[1], anc[1]])  # no a1 rcarry
    k.gate('cnot',[anc[0],head[1]])
    q_rcarry0(k, move[0], head[0],         anc[0]) # no c0
    q_sum0(k, move[0], head[0])
    #  (+0.353553,+0) |000000 000 00000000 001 1> +
    #  (+0.353553,+0) |000000 001 00000000 010 1> +
    #  (+0.353553,+0) |000000 010 00000000 011 1> +
    #  (+0.353553,+0) |000000 011 00000000 100 1> +
    #  (+0.353553,+0) |000000 100 00000000 101 1> +
    #  (+0.353553,+0) |000000 101 00000000 110 1> +
    #  (+0.353553,+0) |000000 110 00000000 111 1> +
    #  (+0.353553,+0) |000000 111 00000000 000 1> +

    k.gate('x', move)

    # TBD: Quantum Subtractor

    # q_carry(k, move[0], head[0], anc[0], anc[1])
    # q_carry(k, anc[2], head[1], anc[1], head1[2]) 
    # k.gate('cnot', [anc[2], head[1]])
    # q_sum(k, anc[2], head[1], anc[1])
    # q_rcarry(k, move[0], head[0], anc[0], anc[1])
    # q_sum(k, move[0], head[0], anc[0])

    
    return

def q_sum(k, a, b, s):
    k.gate('cnot', [s, b])
    k.gate('cnot', [a, b])
    return

def q_carry(k, a, b, c0, c1):
    k.gate('toffoli', [a, b, c1])
    k.gate('cnot', [a, b])
    k.gate('toffoli', [b, c0, c1])
    return

def q_carry1(k, b, c0, c1):
    k.gate('toffoli', [b, c0, c1])
    return

def q_rcarry(k, a, b, c0, c1):
    k.gate('toffoli', [b, c0, c1])
    k.gate('cnot', [a, b])
    k.gate('toffoli', [a, b, c1])
    return

def q_sum0(k, a, b):
    k.gate('cnot', [a, b])
    return

def q_carry0(k, a, b, c1):
    k.gate('toffoli', [a, b, c1])
    k.gate('cnot', [a, b])
    return

def q_rcarry0(k, a, b, c1):
    k.gate('cnot', [a, b])
    k.gate('toffoli', [a, b, c1])
    return

# k.gate('h',[fa[0]])
# k.gate('h',[fa[1]])
# q_fa(k, fa[0], fa[1], fa[2], fa[3])     # Quantum Full-Adder
def q_fa(k, a, b, s, c):
    k.gate('toffoli', [a, b, c])
    k.gate('cnot', [a, b])
    k.gate('toffoli', [b, s, c])
    k.gate('cnot', [b, s])
    k.gate('cnot', [a, b])

def q_ha(k, a, b, c):
    k.gate('toffoli', [a, b, c])    # c - carry
    k.gate('cnot', [a, b])          # b - sum
    return

