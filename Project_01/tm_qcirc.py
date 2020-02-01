import qsdk     # from qsdk import nCX

def U_init(k,tape,head):
    for i in tape:
        k.gate('prepz', [i])
    k.gate('x',[tape[1]]) # Test Read Head
    for i in head:
        k.gate('prepz', [i])
    k.gate('x',[head[2]]) # Test Read Head

def U_read(k, read, head, tape, ancilla):
    k.gate('prepz', read)
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
 
def U_move(k, fa):
    k.gate('h',[fa[0]])
    k.gate('h',[fa[1]])
    q_fa(k, fa[0], fa[1], fa[2], fa[3])     # Quantum Full-Adder
    return

def q_fa(k, a, b, s, c):
    k.gate('toffoli', [a, b, c])
    k.gate('cnot', [a, b])
    k.gate('toffoli', [b, s, c])
    k.gate('cnot', [b, s])
    k.gate('cnot', [a, b])