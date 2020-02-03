import os
from math import log2, ceil
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

sim_tick = 1                # Number of ticks of the FSM before abort

asz = 2                     # Alphabet size: Binary (0 is blank/default)
csz = ceil(log2(asz))       # Character symbol size
ssz = 2                     # State size (Halt is all 1 state, Initial state is all 0)
tdim = 1                    # Tape dimension
transitions = (ssz-1)*asz   # Number of transition arrows in FSM
machines = (ssz * asz * 2**tdim)**transitions
print("Number of "+str(asz)+"-symbol "+str(ssz)+"-state Turing Machines: "+str(machines))

dsz = transitions*(ceil(log2(ssz))+csz+tdim)    # Description size
tsz = dsz                                       # Turing Tape size (same as dsz to test self-replication)
hsz = ceil(log2(tsz))                           # Head size

fsm     = list(range(   0,              dsz                         ))
state   = list(range(   fsm     [-1]+1, fsm     [-1]+1+     ceil(log2(ssz))    ))  # Current state (Binary coded)
move    = list(range(   state   [-1]+1, state   [-1]+1+     tdim    ))
head    = list(range(   move    [-1]+1, move    [-1]+1+     hsz     ))  # Binary coded, 0-MSB 2-LSB, [001] refers to Tape pos 1, not 4
read    = list(range(   head    [-1]+1, head    [-1]+1+     csz     ))
write   = list(range(   read    [-1]+1, read    [-1]+1+     csz     ))  # Can be MUXed with read?
tape    = list(range(   write   [-1]+1, write   [-1]+1+     tsz     ))
# flag
print("FSM:\t",fsm,"\nSTATE:\t",state,"\nMOVE:\t",move,"\nHEAD:\t",head,"\nREAD:\t",read,"\nWRITE:\t",write,"\nTAPE:\t",tape)

ancilla = list(range(   tape    [-1]+1, tape    [-1]+1+     3       ))
test    = list(range(   ancilla [-1]+1, ancilla [-1]+1+     3       )) 
print("ANCILLA:",ancilla,"\nTEST:\t",test)

circ_width = test[-1]+1
p = ql.Program('aritra', platform, circ_width)

# 1. Initialize
#   Tape to all symbol 0
#   Current Tape Head to 0
#   Flag to 0
#   Read Head to position 0
#   Write Head to position 0
#   Current Machine State to state 0
#   FSM to equal superposition of all FSMs
k_init = ql.Kernel("init", platform, circ_width)
tm.U_init(k_init,tape,head)

# p.add_kernel(k_init)

# 2. Run machine for n-iterations:
#   {q_read} << U_read({q_head, q_tape})
k_read = ql.Kernel("read", platform, circ_width)
tm.U_read(k_read, read, head, tape, ancilla)
#   {q_write, q_state, q_move} << U_fsm({q_read, q_state, q_fsm})
k_fsm = ql.Kernel("fsm", platform, circ_width)
tm.U_fsm(k_fsm, fsm, state, read, write, move)
#   {q_tape} << U_write({q_head, q_write})                              
k_write = ql.Kernel("write", platform, circ_width)
tm.U_write(k_write, write, head, tape, ancilla)
#   {q_head, q_err} << U_move({q_head, q_move})     Currently ignore Head position under/overflow. Trim bits                  
k_move = ql.Kernel("move", platform, circ_width)
tm.U_move(k_move, move, head, ancilla, test)    

for tick in range(0, sim_tick):
    # p.add_kernel(k_read)
    p.add_kernel(k_fsm)
    # p.add_kernel(k_write)
    # p.add_kernel(k_move)

# 3. Amplify target sequence using Grover's Gate (QiBAM)

# 4. Create histogram of modal FSMs
# for i in range(0, circ_width):
#     k_read.gate('measure', [i])
 
# 5. Choose shortest FSM that doesn't halt or throws error as Kolmogorov Complexity of target DNA sequence
	
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