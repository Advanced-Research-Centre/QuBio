"""
This Python script emulates our restricted TM for all 4096 cases for Case 2-2-1 over multiple cycles
"""

import math

n = 2   # {0,1}
m = 2   # {s_0,s_1}
d = 1

q_fsm = m*n*(d+math.ceil(math.log(n,2))+math.ceil(math.log(m,2)))
q_tape = q_fsm
num_tm = 2**q_fsm

def UTM_AP(prog_set):

	output_tapes = {}
	univ_dist = {}
	
	for desc_num in prog_set:
		
		fsm = str(format(desc_num, '#0'+str(q_fsm+2)+'b'))[2:]
		# FSM encoding: [sMW]^{s_1R_1}[sMW]^{s_1R_0}[sMW]^{s_0R_1}[sMW]^{s_0R_0}

		tape = "o"*q_tape
		head = 0
		state = '1'
		read = '0'
		write = '0'
		move = '0'

		z = len(tape)

		for iter in range(0,z):

			if head < 0 or head >= q_tape:
				break

			read = tape[head]

			if read == 'o':
				read = 0
			else:
				read = int(read)

			sR = 3*n*(m-int(state)-1) + 3*(n-int(read)-1)

			sMW = fsm[sR:sR+3]
			state = sMW[0]
			move = sMW[1]
			write = sMW[2]

			tape = tape[:head] + write + tape[head + 1:]

			if move == '0':
				head = head - 1
			else:
				head = head + 1

		output_tapes[desc_num] = tape
		univ_dist[desc_num] = int(tape.replace('o','0'),2)

	algo_prob = {} 
	for s in univ_dist.values(): 
		if (s in algo_prob): 
			algo_prob[s] += 1
		else: 
			algo_prob[s] = 1

	return algo_prob, univ_dist

prog_set_0 = list(range(0,num_tm))
algo_prob_0, univ_dist_0 = UTM_AP(prog_set_0)

prog_set_1 = list(algo_prob_0.keys())
algo_prob_1, univ_dist_1 = UTM_AP(prog_set_1)

prog_set_2 = list(algo_prob_1.keys())
algo_prob_2, univ_dist_2 = UTM_AP(prog_set_2)

prog_set_3 = list(algo_prob_2.keys())
algo_prob_3, univ_dist_3 = UTM_AP(prog_set_3)

# For utm221_nested.txt

# print("~~~~ Algorithmic frequency ~~~~")
# print("Level 0:",algo_prob_0)
# print("Level 1:",algo_prob_1)
# print("Level 2:",algo_prob_2)
# print("Level 3:",algo_prob_3)

# print("~~~~ Program-Data map ~~~~")
# print("Level 0:",univ_dist_0)
# print("Level 1:",univ_dist_1)
# print("Level 2:",univ_dist_2)
# print("Level 3:",univ_dist_3)

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

G0 = nx.MultiDiGraph()
for p,d in univ_dist_0.items():
	G0.add_edge(p,d)
G0.graph['edge'] = {'arrowsize':'0.5','color':'red'}
A0 = to_agraph(G0)
A0.layout('circo') #neato,dot,twopi,circo,fdp,nop
A0.draw('map0.svg') # hangs due to large number of nodes

G1 = nx.MultiDiGraph()
for p,d in univ_dist_1.items():
	G1.add_edge(p,d)
G1.graph['edge'] = {'arrowsize':'0.5','color':'red'}
A1 = to_agraph(G1)
A1.layout('fdp')
A1.draw('map19.svg')

G2 = nx.MultiDiGraph()
for p,d in univ_dist_2.items():
	G2.add_edge(p,d)
G2.graph['edge'] = {'arrowsize':'0.5','color':'blue'}
A2 = to_agraph(G2)
A2.layout('circo')
A2.draw('map2.svg')

G3 = nx.MultiDiGraph()
for p,d in univ_dist_3.items():
	G3.add_edge(p,d)
G3.graph['edge'] = {'arrowsize':'0.5','color':'magenta'}
A3 = to_agraph(G3)
A3.layout('circo')
A3.draw('map3.svg')