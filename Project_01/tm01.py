import os
from math import log2
from openql import openql as ql

# rootDir = os.path.dirname(os.path.realpath(__file__))
curdir = os.path.dirname(__file__)
# output_dir = os.path.join(curdir, 'qasm')

# ql.set_option('output_dir', output_dir)
# ql.set_option('write_qasm_files', 'yes')
# ql.set_option('optimize', 'no')
# ql.set_option('scheduler', 'ASAP')
# ql.set_option('log_level', 'LOG_INFO')

config_fn  = os.path.join(curdir, 'config_qx.json')
platform   = ql.Platform('platform_none', config_fn)
num_qubits = 2

sim_tick = 1        # Number of ticks of the FSM before abort

asz = 2             # Alphabet size: Binary (0 is blank/default)
csz = int(log2(asz))# Character symbol size
tsz = 8             # Turing Tape size
ssz = 4             # State size (Halt is all 1 state, Initial state is all 0)

# fsm = ql.Unitary('u_fsm', [ complex(0.0, 0.0), complex(1.0, 0.0),
#                             complex(1.0, 0.0), complex(0.0, 0.0)])                # specify unitary matrix
# fsm.decompose()                                                                # decompose
    
t_now = csz             # Read-Write Tape character
# h_now = log2(tsz)     # Head position (Binary coded)
h_now = tsz             # Head position (1-Hot coded)
# s_now = log2(ssz)     # Current state (Binary coded)
s_now = ssz             # Current state (1-Hot coded)

flags = 1               # Tape under/overflow

q_tt = 0                            # Starting qubit id of Turing Tape
q_rw = q_tt + tsz*csz               # Starting qubit id of R/W Head
q_hp = q_rw + t_now                 # Starting qubit id of Head position
q_cs = q_hp + h_now                 # Starting qubit id of Current State
q_sm = q_cs + s_now                 # Starting qubit id of State Machine
q_fg = q_sm + ssz                   # Starting qubit id of Flags

qbi = [q_tt, q_rw, q_hp, q_cs, q_sm, q_fg, q_fg+flags] # LSQ -- MSQ
circ_width = qbi[-1]

p = ql.Program('aritra', platform, circ_width)
k = ql.Kernel("min_kernel", platform, circ_width)

# 1. Initialize 
#     Tape to all symbol 0
#     Current Tape Head to 0
#     Flag to 0
for i in range(qbi[0], qbi[6]):
    k.gate('prepz', [i])
#     R/W Head to position 0
k.gate('x', [qbi[2]])
#     Current Machine State to state 0
k.gate('x', [qbi[3]])
#     FSM to equal superposition of all FSMs [TBD]
for i in range(qbi[4], qbi[5]):
    k.gate('h', [i])

          

# 2. Run machine for n-iterations:
for tick in range(0, sim_tick):
    # [{R Head}] = Toffoli [{Head Position}, {Turing Tape}]
    for i in range(0,tsz):
        for j in range(0,csz):
            k.gate('toffoli', [qbi[0] + i*csz + j, qbi[2] + i , qbi[1] + j])
    # [{W Head}, {Machine State}, {Move}] = U_fsm [{R Head}, {Machine State}, {FSM}]
    # k.gate(fsm, [q_rw, q_hp, q_cs, q_sm])  
    # [{Head Position}, {Error}] = U_move [{Head Position}, {Move}]
    # Currently ignore: let Head position under/overflow. Trim bits
    # [{Turing Tape}] = U_write [{Head Position}, {W Head}]
    # Reset RW Head

# 3. Amplify target sequence using Grover's Gate (QiBAM)

# 4. Create histogram of modal FSMs
# for i in range(0, num_qubits):
#     k.gate('measure', [i])
 
# 5. Choose shortest FSM that doesn't halt or throws error as Kolmogorov Complexity of target DNA sequence
	
p.add_kernel(k)
p.compile()

qasm = p.qasm()
print(qasm)