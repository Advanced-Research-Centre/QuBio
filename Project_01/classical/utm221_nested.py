"""
This Python script emulates our restricted TM for all 4096 cases for Case 2-2-1.
This is the classical kernel we want to accelerate using the quantum algorithm.
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

		# if desc_num == 1024:
		# 	break

	# print(univ_dist)
	algo_prob = {} 
	for s in univ_dist.values(): 
		if (s in algo_prob): 
			algo_prob[s] += 1
		else: 
			algo_prob[s] = 1

	return algo_prob, univ_dist

# print("Self-replicating machines: ",end='')
# for i in univ_dist:
# 	if i == univ_dist[i]:
# 		print(i,end=',')

prog_set_0 = list(range(0,num_tm))
algo_prob_0, univ_dist_0 = UTM_AP(prog_set_0)

prog_set_1 = list(algo_prob_0.keys())
algo_prob_1, univ_dist_1 = UTM_AP(prog_set_1)

prog_set_2 = list(algo_prob_1.keys())
algo_prob_2, univ_dist_2 = UTM_AP(prog_set_2)

prog_set_3 = list(algo_prob_2.keys())
algo_prob_3, univ_dist_3 = UTM_AP(prog_set_3)

print("~~~~ Algorithmic frequency ~~~~")
print("Level 0:",algo_prob_0)
print("Level 1:",algo_prob_1)
print("Level 2:",algo_prob_2)
print("Level 3:",algo_prob_3)

print("~~~~ Program-Data map ~~~~")
print("Level 0:",univ_dist_0)
print("Level 1:",univ_dist_1)
print("Level 2:",univ_dist_2)
print("Level 3:",univ_dist_3)

# print("\nUniversal distribution:")
# for key in sorted(algo_prob.keys()) :
# 	print ("% d : % d"%(key, algo_prob[key])) 

# import numpy as np
# import matplotlib.pyplot as plt
# plt.plot(univ_dist.keys(), univ_dist.values(), 1, color='g')

# print("\nTM tape output values: ")
# plt.show()



# for key, value in algo_prob.items(): 
# 	print ("% d : % d"%(key, value)) 


# for i in output_tapes:

# 	univ_dist[i] = output_tapes[i].replace('o','0')
# 	print()
    