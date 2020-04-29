import qsdk     # from qsdk import nCX

DISP_EN = False

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
 
def U_move(k, move, head, anc):
    # Increment/Decrement using Adder

    reg_a = move
    reg_a.extend([-1]*(len(head)-len(move)))
    
    reg_b = head
    
    reg_c = [-1]        # No initial carry
    reg_c.extend(anc)
    reg_c.append(-1)    # Ignore Head position under/overflow. Trim bits. Last carry not accounted, All-ones overflows to All-zeros

    def q_carry(k, q0, q1, q2, q3):
        if (q1 != -1 and q2 != -1 and q3 != -1):    k.gate('toffoli', [q1, q2, q3])
        if (q1 != -1 and q2 != -1):                 k.gate('cnot', [q1, q2])
        if (q0 != -1 and q2 != -1 and q3 != -1):    k.gate('toffoli', [q0, q2, q3])
    def q_mid(k, q0, q1):
        if (q0 != -1 and q1 != -1):                 k.gate('cnot', [q0, q1])
    def q_sum(k, q0, q1, q2):
        if (q0 != -1 and q2 != -1):                 k.gate('cnot', [q0, q2])
        if (q1 != -1 and q2 != -1):                 k.gate('cnot', [q1, q2])
    def q_rcarry(k, q0, q1, q2, q3):
        if (q0 != -1 and q2 != -1 and q3 != -1):    k.gate('toffoli', [q0, q2, q3])
        if (q1 != -1 and q2 != -1):                 k.gate('cnot', [q1, q2])
        if (q1 != -1 and q2 != -1 and q3 != -1):    k.gate('toffoli', [q1, q2, q3])

    # Quantum Adder
    for i in range(0,len(head)):
        q_carry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])
    q_mid(k,reg_a[i],reg_b[i])
    q_sum(k,reg_c[i],reg_a[i],reg_b[i])
    for i in range(len(head)-2,-1,-1):
        q_rcarry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])
        q_sum(k,reg_c[i],reg_a[i],reg_b[i])

    k.gate('x', [reg_a[0]])
    # Quantum Subtractor
    for i in range(0,len(head)-1):
        q_sum(k,reg_c[i],reg_a[i],reg_b[i])
        q_carry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])
    q_sum(k,reg_c[i+1],reg_a[i+1],reg_b[i+1])
    q_mid(k,reg_a[i+1],reg_b[i+1])
    for i in range(len(head)-2,-1,-1):
        q_rcarry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])
    k.gate('x', [reg_a[0]])

    if (DISP_EN): k.display()
    return

import os
from openql import openql as ql
import qxelarator

def unit_tests():

    curdir = os.path.dirname(__file__)
    output_dir = os.path.join(curdir, 'qasm')

    ql.set_option('output_dir', output_dir)
    ql.set_option('write_qasm_files', 'yes')

    config_fn  = os.path.join(curdir, 'config_qx.json')
    platform   = ql.Platform('platform_none', config_fn)

    move = [0]          # Addend: 1-bit Move
    head = [1,2,3,4]    # Augend: 4-bit Head 
    anc = [5,6,7]       # Carry: uncomputed ancilla
    test = [8,9,10,11]

    circ_width = len(move) + len(head) + len(anc) + len(test)

    p = ql.Program('aritra', platform, circ_width)
    k_move = ql.Kernel("move", platform, circ_width)

    # Test using full superposition of head, both inc/dec and association to initial state
    for i in range(0,len(head)):
        k_move.gate('h',[head[i]])
        k_move.gate('cnot',[head[i],test[i]]) 
    k_move.gate('h', [move[0]])

    U_move(k_move, move, head, anc) 

    p.add_kernel(k_move)
    p.compile()
    print(p.qasm())
    qx = qxelarator.QX()
    qx.set(output_dir+'/aritra.qasm')
    qx.execute()
    isv = qx.get_state()
    print(isv)

    #  (+0.176777,+0) | 0000    000     0001    1> +
    #  (+0.176777,+0) | 0000    000     1111    0> +
    #  (+0.176777,+0) | 0001    000     0000    0> +
    #  (+0.176777,+0) | 0001    000     0010    1> +
    #  (+0.176777,+0) | 0010    000     0001    0> +
    #  (+0.176777,+0) | 0010    000     0011    1> +
    #  (+0.176777,+0) | 0011    000     0010    0> +
    #  (+0.176777,+0) | 0011    000     0100    1> +
    #  (+0.176777,+0) | 0100    000     0011    0> +
    #  (+0.176777,+0) | 0100    000     0101    1> +
    #  (+0.176777,+0) | 0101    000     0100    0> +
    #  (+0.176777,+0) | 0101    000     0110    1> +
    #  (+0.176777,+0) | 0110    000     0101    0> +
    #  (+0.176777,+0) | 0110    000     0111    1> +
    #  (+0.176777,+0) | 0111    000     0110    0> +
    #  (+0.176777,+0) | 0111    000     1000    1> +
    #  (+0.176777,+0) | 1000    000     0111    0> +
    #  (+0.176777,+0) | 1000    000     1001    1> +
    #  (+0.176777,+0) | 1001    000     1000    0> +
    #  (+0.176777,+0) | 1001    000     1010    1> +
    #  (+0.176777,+0) | 1010    000     1001    0> +
    #  (+0.176777,+0) | 1010    000     1011    1> +
    #  (+0.176777,+0) | 1011    000     1010    0> +
    #  (+0.176777,+0) | 1011    000     1100    1> +
    #  (+0.176777,+0) | 1100    000     1011    0> +
    #  (+0.176777,+0) | 1100    000     1101    1> +
    #  (+0.176777,+0) | 1101    000     1100    0> +
    #  (+0.176777,+0) | 1101    000     1110    1> +
    #  (+0.176777,+0) | 1110    000     1101    0> +
    #  (+0.176777,+0) | 1110    000     1111    1> +
    #  (+0.176777,+0) | 1111    000     0000    1> +
    #  (+0.176777,+0) | 1111    000     1110    0> +

unit_tests()