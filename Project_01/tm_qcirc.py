import qsdk     # from qsdk import nCX

def U_init(k,tape,head):
    for i in tape:
        k.gate('prepz', [i])
    k.gate('x',[tape[1]]) # Test Read Head
    for i in head:
        k.gate('prepz', [i])
    k.gate('x',[head[2]]) # Test Read Head

def U_read(k, read, head, tape, ancilla):
    k.gate('prepz', read)   # Prepz measures superposed states... need to uncompute
    for cell in range(0, len(tape)):
        enc = format(cell, '#0'+str(len(head)+2)+'b')   # 2 for '0b' prefix
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
        qsdk.nCX(k, head+[tape[cell]], read, ancilla)
        for i in range(2, len(enc)):
            if(enc[i] == '0'):
                k.gate('x', [head[i-2]])
    return

def U_fsm():
    # k.gate(fsm, [q_rw, q_hp, q_cs, q_sm])  
    return
    
def U_write():
    # Reset RW Head
    return
 
def U_move(k, move, head, head1, anc):

    k.gate('h',[head[0]]) # Test Move Head
    k.gate('h',[head[1]]) # Test Move Head
    k.gate('h',[head[2]]) # Test Move Head

        #  (+0.353553,+0) |000 001 000 000000000001> +
        #  (+0.353553,+0) |001 010 001 000000000001> +
        #  (+0.353553,+0) |000 011 010 000000000001> +
        #  (+0.353553,+0) |011 100 011 000000000001> +
        #  (+0.353553,+0) |000 101 100 000000000001> +
        #  (+0.353553,+0) |001 110 101 000000000001> +
        #  (+0.353553,+0) |000 111 110 000000000001> +
        #  (+0.353553,+0) |111 000 111 000000000001> +

    k.gate('x', move)

    # Move Right (increase Head Position value) if Move == 1
    q_fa(k, move[0], head[0], head1[0], anc[0])
    q_fa(k, anc[0], head[1], head1[1], anc[1])
    q_fa(k, anc[1], head[2], head1[2], anc[2])

    for i in anc:
        print(i)
        k.gate('prepz', [i])    # Prepz measures superposed states... need to uncompute
    # k.gate('h',[fa[0]])
    # k.gate('h',[fa[1]])
    # q_fa(k, fa[0], fa[1], fa[2], fa[3])     # Quantum Full-Adder
    return

def q_fa(k, a, b, s, c):
    k.gate('toffoli', [a, b, c])
    k.gate('cnot', [a, b])
    k.gate('toffoli', [b, s, c])
    k.gate('cnot', [b, s])
    k.gate('cnot', [a, b])