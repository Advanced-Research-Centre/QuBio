import qsdk     # from qsdk import nCX

def U_init(k,tape,head):
    for i in tape:
        k.gate('prepz', [i])
    k.gate('x',[5]) # Test Read Head
    for i in head:
        k.gate('prepz', [i])
    k.gate('x',[2]) # Test Read Head

def U_read(k, read, head, tape, ancilla):
    k.gate('prepz', read)
    for cell in range(0, len(tape)):
        enc = format(cell, '#05b')
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
 
def U_move():
    # Currently ignore: let Head position under/overflow. Trim bits
    return