qubits 12

map q0,move
map q1,head0
map q2,head1
map q3,head2
map q4,head3
map q5,ancilla0
map q6,ancilla1
map q7,ancilla2

map q8,test0
map q9,test1
map q10,test2
map q11,test3

h move
#h head0
#h head1
#h head2
#h head3

cnot head0,test0
cnot head1,test1
cnot head2,test2
cnot head3,test3

toffoli move,head0,ancilla0
cnot move,head0
toffoli ancilla0,head1,ancilla1
toffoli ancilla1,head2,ancilla2
cnot ancilla2,head3
toffoli ancilla1,head2,ancilla2
cnot ancilla1,head2
toffoli ancilla0,head1,ancilla1
cnot ancilla0,head1
cnot move,head0
toffoli move,head0,ancilla0
cnot move,head0

display