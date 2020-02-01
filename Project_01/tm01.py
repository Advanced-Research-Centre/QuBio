import os
from math import log2
from openql import openql as ql
import qxelarator

import tm_qcirc as tm

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

head = [0, 1, 2]    # 0-MSB 2-LSB, [001] refers to Tape pos 1, not 4
read = [3]
tape = [4, 5, 6, 7, 8, 9]
ancilla = [10]

circ_width = len(head+read+tape+ancilla)

p = ql.Program('aritra', platform, circ_width)

k_init = ql.Kernel("init", platform, circ_width)
# 1. Initialize
#   Tape to all symbol 0
#   Current Tape Head to 0
#   Flag to 0
#   Read Head to position 0
#   Write Head to position 0
#   Current Machine State to state 0
#   FSM to equal superposition of all FSMs
tm.U_init(k_init,tape,head)

k_read = ql.Kernel("read", platform, circ_width)
# 2. Run machine for n-iterations:
for tick in range(0, sim_tick):
    tm.U_read(k_read,read,head,tape,ancilla)    # {q_read} << U_read({q_head, q_tape})
    tm.U_fsm()                                  # {q_write, q_state, q_move} << U_fsm({q_read, q_state, q_fsm})
    tm.U_write()                                # {q_tape} << U_write({q_head, q_write})
    tm.U_move()                                 # {q_head, q_err} << U_move({q_head, q_move})   

# 3. Amplify target sequence using Grover's Gate (QiBAM)

# 4. Create histogram of modal FSMs
# for i in range(0, circ_width):
#     k_read.gate('measure', [i])
 
# 5. Choose shortest FSM that doesn't halt or throws error as Kolmogorov Complexity of target DNA sequence
	
p.add_kernel(k_init)
p.add_kernel(k_read)
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




### LEGACY

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