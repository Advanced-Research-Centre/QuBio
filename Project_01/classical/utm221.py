"""
This Python script emulates our restricted TM for all 4096 cases for Case 2-2-1.
This is the classical kernel we want to accelerate using the quantum algorithm.
"""

import math

n = 2   # {0,1}
m = 2   # {s_0,s_1}
d = 1

q_fsm = m*n*(d+math.ceil(math.log(n,2))+math.ceil(math.log(m,2)))
q_tape = q_fsm
num_tm = 2**q_fsm

for desc_num in range(0,num_tm):
    
    fsm = str(format(desc_num, '#0'+str(q_fsm+2)+'b'))[2:]
    # FSM encoding: [sMW]^{s_1R_1}[sMW]^{s_1R_0}[sMW]^{s_0R_1}[sMW]^{s_0R_0}

    tape = "0123456789ab"#"o"*q_tape
    head = 0
    state = 0
    read = 0
    write = 0
    move = 0

    z = len(tape)

    for iter in range(0,z):

        
        #print(tape[iter:])
    
    break
    