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
p = ql.Program('aritra', platform, num_qubits)
k = ql.Kernel("min_kernel", platform, num_qubits)

asz = 2             # Alphabet size: Binary
tsz = 8             # Turing Tape size
ssz = 4             # State size (including Halt)

t_now = log2(asz)   # Read-Write Tape character
# h_now = log2(tsz)   # Head position (Binary coded)
h_now = tsz         # Head position (1-Hot coded)
# s_now = log2(ssz)   # Current state (Binary coded)
s_now = ssz         # Current state (1-Hot coded)

flags = 1

num_qb = tsz*log2(asz) + t_now + h_now + s_now + flags
print(num_qb)

for i in range(0,num_qubits):
    k.gate('prepz',[i])
k.gate('h', [0])
k.gate('cnot', [0, 1])
for i in range(0,num_qubits):
    k.gate('measure',[i])

p.add_kernel(k)
p.compile()

qasm = p.qasm()
print(qasm)