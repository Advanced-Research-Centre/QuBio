version 1.0
# this file has been automatically generated by the OpenQL compiler please do not modify it manually.
qubits 12
.move

    h q[1]
    wait 1
    cnot q[1],q[8]
    wait 1
    { h q[2] | h q[0] }
    wait 1
    { cnot q[2],q[9] | toffoli q[0],q[1],q[5] }
    wait 1
    h q[3]
    wait 1
    { cnot q[3],q[10] | toffoli q[5],q[2],q[6] }
    wait 1
    h q[4]
    wait 1
    { cnot q[4],q[11] | toffoli q[6],q[3],q[7] }
    wait 3
    cnot q[7],q[4]
    wait 3
    toffoli q[6],q[3],q[7]
    wait 3
    cnot q[6],q[3]
    wait 3
    { cnot q[0],q[1] | toffoli q[5],q[2],q[6] }
    wait 3
    { cnot q[5],q[2] | cnot q[0],q[1] }
    wait 3
    toffoli q[0],q[1],q[5]
    wait 3
    cnot q[0],q[1]
    wait 3
    x q[0]
    wait 1
    cnot q[0],q[1]
    wait 3
    toffoli q[0],q[1],q[5]
    wait 3
    cnot q[5],q[2]
    wait 3
    toffoli q[5],q[2],q[6]
    wait 3
    cnot q[6],q[3]
    wait 3
    toffoli q[6],q[3],q[7]
    wait 3
    cnot q[7],q[4]
    wait 3
    { cnot q[0],q[1] | toffoli q[6],q[3],q[7] }
    wait 3
    { toffoli q[5],q[2],q[6] | cnot q[0],q[1] }
    wait 3
    toffoli q[0],q[1],q[5]
    wait 3
    x q[0]
    wait 1

