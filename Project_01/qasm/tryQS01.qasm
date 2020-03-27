qubits 20
.init
    x q0
    x q6
    x q11
x q19
    h q19
    toffoli q6,q0,q19
    h q19
    x q11
    x q6
display
