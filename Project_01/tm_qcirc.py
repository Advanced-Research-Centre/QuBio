import qsdk     # from qsdk import nCX

DISP_EN = True

def U_init(k, circ_width, fsm, state, move, head, read, write, tape, ancilla, test):
    for i in range(0,circ_width):
        k.gate('prepz', [i])
    for i in fsm:                  
        k.gate('h', [i])
    if (DISP_EN): k.display()
    return

def U_init_test(k, circ_width, fsm, state, move, head, read, write, tape, ancilla, test):   
    # k.gate('x',[tape[1]])   # Test Read Head
    # k.gate('x',[head[2]])   # Test Read Head
    k.gate('x',[fsm[0]])    # Test FSM
    k.gate('x',[fsm[1]])    # Test FSM
    k.gate('x',[fsm[2]])    # Test FSM
    k.gate('x',[fsm[3]])    # Test FSM
    k.gate('x',[fsm[4]])    # Test FSM
    k.gate('x',[fsm[5]])    # Test FSM
    if (DISP_EN): k.display()
    return

def U_read(k, read, head, tape, ancilla):
    # Reset read (prepz measures superposed states... need to uncompute)
    for cell in range(0, len(tape)):
        enc = format(cell, '#0'+str(len(head)+2)+'b')   # 2 for '0b' prefix
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
        qsdk.nCX(k, head+[tape[cell]], read, [ancilla[0]])
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
    if (DISP_EN): k.display()
    return

def U_fsm(k, tick, fsm, state, read, write, move, ancilla):
    k.gate('x', [state[tick]])                                             # If s == 0
    k.gate('x', [read[0]])                                                  # If s == 0 && read == 0
    qsdk.nCX(k, [state[tick],fsm[0],read[0]], [state[tick+1]], [ancilla[0]])       # Update state
    qsdk.nCX(k, [state[tick],fsm[1],read[0]], write, [ancilla[0]])                 # Update write
    qsdk.nCX(k, [state[tick],fsm[2],read[0]], move, [ancilla[0]])                  # Update move
    k.gate('x', [read[0]])                                                  # If s == 0 && read == 1
    qsdk.nCX(k, [state[tick],fsm[3],read[0]], [state[tick+1]], [ancilla[0]])       # Update state
    qsdk.nCX(k, [state[tick],fsm[4],read[0]], write, [ancilla[0]])                 # Update write
    qsdk.nCX(k, [state[tick],fsm[5],read[0]], move, [ancilla[0]])                  # Update move
    k.gate('x', [state[tick]])                                             # If s == 1 (no arrows)
    if (DISP_EN): k.display()
    return

def U_fsm_UC(k, tick, fsm, state, read, write, move, ancilla):
    k.gate('x', [state[tick]])                                             # If s == 0
    k.gate('x', [read[0]])                                                  # If s == 0 && read == 0
    # qsdk.nCX(k, [state[tick],fsm[0],read[0]], [state[tick+1]], [ancilla[0]])       # Update state
    qsdk.nCX(k, [state[tick],fsm[1],read[0]], write, [ancilla[0]])                 # Update write
    qsdk.nCX(k, [state[tick],fsm[2],read[0]], move, [ancilla[0]])                  # Update move
    k.gate('x', [read[0]])                                                  # If s == 0 && read == 1
    # qsdk.nCX(k, [state[tick],fsm[3],read[0]], [state[tick+1]], [ancilla[0]])       # Update state
    qsdk.nCX(k, [state[tick],fsm[4],read[0]], write, [ancilla[0]])                 # Update write
    qsdk.nCX(k, [state[tick],fsm[5],read[0]], move, [ancilla[0]])                  # Update move
    k.gate('x', [state[tick]])                                             # If s == 1 (no arrows)
    k.display()
    return
    
def U_write(k, write, head, tape, ancilla):
    # Reset write (prepz measures superposed states... need to uncompute)
    for cell in range(0, len(tape)):
        enc = format(cell, '#0'+str(len(head)+2)+'b')   # 2 for '0b' prefix
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
        qsdk.nCX(k, head+write, [tape[cell]], [ancilla[0]])
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
    if (DISP_EN): k.display()
    return
 
def U_move(k, move, head, test, anc):
    # Prepz measures superposed states... need to uncompute
    # Last carry not accounted, All-ones overflows to All-zeros
    # Currently ignore Head position under/overflow. Trim bits   

    # k.gate('h',[head[0]])               # Test Move Head
    # k.gate('h',[head[1]])               # Test Move Head
    # k.gate('h',[head[2]])               # Test Move Head
    # k.gate('cnot',[head[0],test[0]])    # Test Move Head Association
    # k.gate('cnot',[head[1],test[1]])    # Test Move Head Association
    # k.gate('cnot',[head[2],test[2]])    # Test Move Head Association
    # k.gate('x', move)                   # Test Move Right

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
    k.gate('x', move)

    # q_carry(k, move[0], head[0], anc[0], anc[1])
    # q_carry(k, anc[2], head[1], anc[1], head1[2]) 
    # k.gate('cnot', [anc[2], head[1]])
    # q_sum(k, anc[2], head[1], anc[1])
    # q_rcarry(k, move[0], head[0], anc[0], anc[1])
    # q_sum(k, move[0], head[0], anc[0])

    if (DISP_EN): k.display()
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

