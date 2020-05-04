import os
from openql import openql as ql
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
num_qubits = 2
p = ql.Program('aritra', platform, num_qubits)
k = ql.Kernel("min_kernel", platform, num_qubits)

k.prepz(0)
k.prepz(1)
k.gate('h', [0])
k.gate('cnot', [0, 1])
k.measure(0)
k.measure(1)

p.add_kernel(k)
p.compile()

qasm = p.qasm()
print(qasm)

qx = qxelarator.QX()
qx.set(output_dir+'/aritra.qasm')

qx.execute()
res = qx.get_measurement_outcome(0)
print(res)