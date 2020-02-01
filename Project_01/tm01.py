import os
from math import log2
from openql import openql as ql
import qsdk     # from qsdk import nCX
import qxelarator

# rootDir = os.path.dirname(os.path.realpath(__file__))
curdir = os.path.dirname(__file__)
output_dir = os.path.join(curdir, 'qasm')

ql.set_option('output_dir', output_dir)
ql.set_option('write_qasm_files', 'yes')
# ql.set_option('optimize', 'no')
# ql.set_option('scheduler', 'ASAP')
# ql.set_option('log_level', 'LOG_INFO')

config_fn  = os.path.join(curdir, 'config_qx.json')
platform   = ql.Platform('platform_none', config_fn)

sim_tick = 1        # Number of ticks of the FSM before abort

# asz = 2             # Alphabet size: Binary (0 is blank/default)
# csz = int(log2(asz))# Character symbol size
# tsz = 8             # Turing Tape size
# ssz = 4             # State size (Halt is all 1 state, Initial state is all 0)

# t_now = csz             # Read-Write Tape character
# # h_now = log2(tsz)     # Head position (Binary coded)
# h_now = tsz             # Head position (1-Hot coded)
# # s_now = log2(ssz)     # Current state (Binary coded)
# s_now = ssz             # Current state (1-Hot coded)

# flags = 1               # Tape under/overflow

# q_tt = 0                            # Starting qubit id of Turing Tape
# q_rw = q_tt + tsz*csz               # Starting qubit id of R/W Head
# q_hp = q_rw + t_now                 # Starting qubit id of Head position
# q_cs = q_hp + h_now                 # Starting qubit id of Current State
# q_sm = q_cs + s_now                 # Starting qubit id of State Machine
# q_fg = q_sm + ssz                   # Starting qubit id of Flags

# qbi = [q_tt, q_rw, q_hp, q_cs, q_sm, q_fg, q_fg+flags] # LSQ -- MSQ
# circ_width = qbi[-1]

head = [0, 1, 2]
read = [3]
tape = [4, 5, 6, 7, 8, 9]

circ_width = len(head+read+tape)

p = ql.Program('aritra', platform, circ_width)
k_init = ql.Kernel("init", platform, circ_width)
k_read = ql.Kernel("read", platform, circ_width)

# 1. Initialize
#     Tape to all symbol 0
for i in tape:
    k_init.gate('prepz', [i])
k_init.gate('x',[4]) # Test Read Head
#     Current Tape Head to 0
for i in head:
    k_init.gate('prepz', [i])
#     Flag to 0
#     Read Head to position 0
for i in read:
    k_init.gate('prepz', [i])
#    Write Head to position 0
#     Current Machine State to state 0
#     FSM to equal superposition of all FSMs [TBD]


# k1 = ql.Kernel("min_kernel", platform, circ_width)
# ck = ql.Kernel('controlled_kernel1', platform, circ_width)

def U_read(k,read,head,tape):
    for cell in range(0,len(tape)):
        print(format(cell, '#05b'), tape[cell])
    qsdk.nCX(k,[0, 1, 2],[4],[3])
    # for i in range(0,tsz):
    #     for j in range(0,csz):
    #         k.gate('toffoli', [qbi[0] + i*csz + j, qbi[2] + i , qbi[1] + j])
    
    # multi control X
    
    # k1.gate("x", [0])
    # ck.controlled(k1, [1], [2])
    
    return

def U_fsm():
    # k.gate(fsm, [q_rw, q_hp, q_cs, q_sm])  
    return
    
def U_write():
    # Reset RW Head
    return
 
def U_move():
    # Currently ignore: let Head position under/overflow. Trim bits
    return

# 2. Run machine for n-iterations:
for tick in range(0, sim_tick):
    U_read(k_read,read,head,tape)       # {q_read} << U_read({q_head, q_tape})
    U_fsm()                             # {q_write, q_state, q_move} << U_fsm({q_read, q_state, q_fsm})
    U_write()                           # {q_tape} << U_write({q_head, q_write})
    U_move()                            # {q_head, q_err} << U_move({q_head, q_move})   

# 3. Amplify target sequence using Grover's Gate (QiBAM)

# 4. Create histogram of modal FSMs
# for i in range(0, num_qubits):
#     k.gate('measure', [i])
 
# 5. Choose shortest FSM that doesn't halt or throws error as Kolmogorov Complexity of target DNA sequence
	
p.add_kernel(k_init)
p.add_kernel(k_read)
# p.add_kernel(k1)
p.compile()

qasm = p.qasm()
print(qasm)

qx = qxelarator.QX()
qx.set(output_dir+'/aritra.qasm')

qx.execute()
isv = qx.get_state()
print(isv)
# res = qx.get_measurement_outcome(0)
# print(res)