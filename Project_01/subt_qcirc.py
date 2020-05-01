def subtract(k, reg_a, reg_b, anc):

    if len(reg_a) != len(reg_b):
        print("Error: both should be of same size in qubits")
        return
   
    reg_c = [-1]        # No initial carry
    reg_c.extend(anc)
    # reg_c.append(-1)    # Ignore Head position under/overflow. Trim bits. Last carry not accounted, All-ones overflows to All-zeros

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

    # Quantum Subtractor
    for i in range(0,len(reg_b)-1):
        q_sum(k,reg_c[i],reg_a[i],reg_b[i])
        q_carry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])
    q_sum(k,reg_c[i+1],reg_a[i+1],reg_b[i+1])
    q_mid(k,reg_a[i+1],reg_b[i+1])
    for i in range(len(reg_b)-2,-1,-1):
        q_rcarry(k,reg_c[i],reg_a[i],reg_b[i],reg_c[i+1])

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

    # 2-bit case
    # reg_a = [0,1]   # Addend
    # reg_b = [2,3]   # Augend
    # anc = [4,5,6]   # Carry: uncomputed ancilla
    # test = [7,8,9,10]

    # 3-bit case
    reg_a = [0,1,2]   # Addend
    reg_b = [3,4,5]   # Augend
    anc = [6,7,8,9]   # Carry: uncomputed ancilla
    test = [10,11,12,13,14,15]

    circ_width = len(reg_a) + len(reg_b) + len(anc) + len(test)

    p = ql.Program('aritra', platform, circ_width)
    k_subt = ql.Kernel("subt", platform, circ_width)

    # Test using full superposition of both registers
    for i in range(0,len(reg_a)):
        k_subt.gate('h',[reg_a[i]])
        k_subt.gate('cnot',[reg_a[i],test[i]])
    for i in range(0,len(reg_b)):
        k_subt.gate('h',[reg_b[i]])
        k_subt.gate('cnot',[reg_b[i],test[i+len(reg_a)]])

    subtract(k_subt, reg_a, reg_b, anc) 

    p.add_kernel(k_subt)
    p.compile()
    print(p.qasm())
    qx = qxelarator.QX()
    qx.set(output_dir+'/aritra.qasm')
    qx.execute()
    isv = qx.get_state()
    print(isv)


# A  B  -> A  D

# 00 00 -> 00 00
# 00 01 -> 00 01
# 00 10 -> 00 10
# 00 11 -> 00 11

# 01 00 -> 01 11
# 01 01 -> 01 00
# 01 10 -> 01 01
# 01 11 -> 01 10

# 10 00 -> 10 00
# 10 01 -> 10 01
# 10 10 -> 10 10
# 10 11 -> 10 11

# 11 00 -> 11 11
# 11 01 -> 11 00
# 11 10 -> 11 01
# 11 11 -> 11 10

# A   B   -> A   D

# 000 000 -> 000 000
# 000 001 -> 000 001
# 000 010 -> 000 010
# 000 011 -> 000 011
# 000 100 -> 000 100
# 000 101 -> 000 101
# 000 110 -> 000 110
# 000 111 -> 000 111

# 001 000 -> 001 111
# 001 001 -> 001 000
# 001 010 -> 001 001
# 001 011 -> 001 010
# 001 100 -> 001 011
# 001 101 -> 001 100
# 001 110 -> 001 101
# 001 111 -> 001 110

# 010 000 -> 010 110
# 010 001 -> 010 111
# 010 010 -> 010 000
# 010 011 -> 010 001
# 010 100 -> 010 010
# 010 101 -> 010 011
# 010 110 -> 010 100
# 010 111 -> 010 101

# 011 000 -> 011 101
# 011 001 -> 011 110
# 011 010 -> 011 111
# 011 011 -> 011 000
# 011 100 -> 011 001
# 011 101 -> 011 010
# 011 110 -> 011 011
# 011 111 -> 011 100

# 100 000 -> 100 000
# 100 001 -> 100 001
# 100 010 -> 100 010
# 100 011 -> 100 011
# 100 100 -> 100 100
# 100 101 -> 100 101
# 100 110 -> 100 110
# 100 111 -> 100 111

# 101 000 -> 101 111
# 101 001 -> 101 000
# 101 010 -> 101 001
# 101 011 -> 101 010
# 101 100 -> 101 011
# 101 101 -> 101 100
# 101 110 -> 101 101
# 101 111 -> 101 110

# 110 000 -> 110 110
# 110 001 -> 110 111
# 110 010 -> 110 000
# 110 011 -> 110 001
# 110 100 -> 110 010
# 110 101 -> 110 011
# 110 110 -> 110 100
# 110 111 -> 110 101

# 111 000 -> 111 101
# 111 001 -> 111 110
# 111 010 -> 111 111
# 111 011 -> 111 000
# 111 100 -> 111 001
# 111 101 -> 111 010
# 111 110 -> 111 011
# 111 111 -> 111 100


unit_tests()