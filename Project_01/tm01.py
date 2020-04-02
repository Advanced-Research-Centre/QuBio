import os
from math import log2, ceil
from openql import openql as ql
import qxelarator

import tm_qcirc as tm

ISV_EN = True
EXEC_QX = True

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

asz = 2                                         # Alphabet size: Binary (0 is blank/default)
ssz = 2                                         # State size (Initial state is all 0)
tdim = 1                                        # Tape dimension

csz = ceil(log2(asz))                           # Character symbol size
senc = ceil(log2(ssz))                          # State encoding size
transitions = ssz * asz                         # Number of transition arrows in FSM
dsz = transitions * (tdim + csz + senc)         # Description size

# machines = (ssz * asz * 2**tdim)**transitions
machines = 2 ** dsz
print("Number of "+str(asz)+"-symbol "+str(ssz)+"-state"+str(tdim)+"-dimension Turing Machines: "+str(machines))

tsz = dsz                                       # Turing Tape size (same as dsz to estimating self-replication and algorithmic probability)
hsz = ceil(log2(tsz))                           # Head size

sim_tick = tsz                                  # Number of ticks of the FSM before abort
tlog = (sim_tick+1) * senc                      # Transition log # required?

fsm     = list(range(   0,              dsz                         ))
state   = list(range(   fsm     [-1]+1, fsm     [-1]+1+     senc    ))  # States (Binary coded) # tlog?
move    = list(range(   state   [-1]+1, state   [-1]+1+     tdim    ))
head    = list(range(   move    [-1]+1, move    [-1]+1+     hsz     ))  # Binary coded, 0-MSB 2-LSB, [001] refers to Tape pos 1, not 4
read    = list(range(   head    [-1]+1, head    [-1]+1+     csz     ))
write   = list(range(   read    [-1]+1, read    [-1]+1+     csz     ))  # Can be MUXed with read?
tape    = list(range(   write   [-1]+1, write   [-1]+1+     tsz     ))
# flag
print("FSM:\t",fsm,"\nSTATE:\t",state,"\nMOVE:\t",move,"\nHEAD:\t",head,"\nREAD:\t",read,"\nWRITE:\t",write,"\nTAPE:\t",tape)

ancilla = list(range(   tape    [-1]+1, tape    [-1]+1+     3       ))
test    = list(range(   ancilla [-1]+1, ancilla [-1]+1+     3       ))  # remove?
print("ANCILLA:",ancilla,"\nTEST:\t",test)

circ_width = test[-1]+1
p = ql.Program('aritra', platform, circ_width)

# 1. Initialize
#   FSM 					to equal superposition of all FSMs
#   Current Machine State 	to state 0
#   Move 					to direction 0
#   Current Tape Head 		to position 0
#   Read Head 				to symbol 0
#   Write Head 				to symbol 0
#   Tape 					to all symbol 0
#   Flag                    to 0
#	Ancilla 				to 0
#	Test 					to 0
k_init = ql.Kernel("init", platform, circ_width)
tm.U_init(k_init, circ_width, fsm, state, move, head, read, write, tape, ancilla, test) 
p.add_kernel(k_init)

# 2. Run machine for n-iterations:
for tick in range(0, sim_tick):
    #   {read} << U_read({head, tape})
    print("Tick: ",tick)
    # k_read = ql.Kernel("read"+str(tick), platform, circ_width)
    # tm.U_read(k_read, read, head, tape, move)   # move qubits used as borrowed ancilla
    # p.add_kernel(k_read)
    # # #   {write, state, move} << U_fsm({read, state, fsm})
    # # k_fsm = ql.Kernel("fsm"+str(tick), platform, circ_width)
    # # tm.U_fsm(k_fsm, tick, fsm, state, read, write, move, ancilla)
    # # p.add_kernel(k_fsm)
    # #   {tape} << U_write({head, write})           
    # k_write = ql.Kernel("write"+str(tick), platform, circ_width)
    # tm.U_write(k_write, write, head, tape, ancilla)
    # p.add_kernel(k_write)
    # #   {head, err} << U_move({head, move})    
    # k_move = ql.Kernel("move"+str(tick), platform, circ_width)
    # tm.U_move(k_move, move, head, ancilla, test) 
    # p.add_kernel(k_move)

    # #   UNCOMPUTE
    # # k_read = ql.Kernel("read", platform, circ_width)
    # # tm.U_read(k_read, read, head, tape, ancilla)
    # k_fsm_uc = ql.Kernel("fsm_uc"+str(tick), platform, circ_width)
    # tm.U_fsm_UC(k_fsm_uc, tick, fsm, state, read, write, move, ancilla)  # TBD: Generalize tick = 0, inside sim_tick loop
    # p.add_kernel(k_fsm_uc)

    # k_write = ql.Kernel("write", platform, circ_width)
    # tm.U_write(k_write, write, head, tape, ancilla)
    # k_move = ql.Kernel("move", platform, circ_width)
    # tm.U_move(k_move, move, head, ancilla, test) 
    break

# 3. Amplify target sequence using Grover's Gate (QiBAM) [optional for Virtual-Perfect qubits]

# 4. Measure [optional for Virtual-Perfect qubits]

if (not ISV_EN):
    k_measure = ql.Kernel("measure", platform, circ_width)
    for i in range(0, circ_width):
        k_measure.gate('measure', [i])
    p.add_kernel(k_measure)
 
# 5. Inference of algorithmic features
# e.g. Choose shortest FSM that doesn't halt or throws error as Kolmogorov Complexity of target DNA sequence

p.compile()
print(p.qasm())

if (EXEC_QX):
    qx = qxelarator.QX()
    qx.set(output_dir+'/aritra.qasm')

    qx.execute()
    isv = qx.get_state()
    print(isv)
    # res = qx.get_measurement_outcome(0)
    # print(res)

# Create histogram of modal FSMs