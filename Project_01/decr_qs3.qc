qubits 12

map q0,A0#move
map q0,A1#move
map q0,A2#move
map q0,A3#move
map q1,B0#head0
map q2,B1#head1
map q3,B2#head2
map q4,B3#head3
map q5,C1#ancilla0
map q6,C2#ancilla1
map q7,C3#ancilla2

map q8,test0
map q9,test1
map q10,test2
map q11,test3

h A0
h B0
h B1
h B2
h B3

cnot B0,test0
cnot B1,test1
cnot B2,test2
cnot B3,test3

.carry0
    toffoli A0,B0,C1
    cnot A0,B0
    #toffoli C0,B0,C1
.carry1
    toffoli A1,B1,C2
    cnot A1,B1
    toffoli C1,B1,C2
.carry2
    toffoli A2,B2,C3
    cnot A2,B2
    toffoli C2,B2,C3
.carry3
    #toffoli A3,B3,B4
    cnot A3,B3
    #toffoli C3,B3,B4
.middle
    cnot A3,B3
.sum3
    cnot A3,B3
    cnot C3,B3
.rcarry2
    toffoli C2,B2,C3
    cnot A2,B2
    toffoli A2,B2,C3
.sum2
    cnot A2,B2
    cnot C2,B2
.rcarry1
    toffoli C1,B1,C2
    cnot A1,B1
    toffoli A1,B1,C2
.sum1
    cnot A1,B1
    cnot C1,B1
.rcarry0
    #toffoli C0,B0,C1
    cnot A0,B0
    toffoli A0,B0,C1
.sum0
    cnot A0,B0
    #cnot C0,B0

display