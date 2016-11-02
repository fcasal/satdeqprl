## SIMPLE-NAT

filenamemaude = "./maudespec/simple_nat.maude"

rewritesystem = [['equat(+(zero, N) , N)', ['N']],
 				['equat(+(s(N) , M) , +(N,s(M)))', ['N', 'M']],
				['equat(s(s(N)) , N)', ['N']]]

signature = [[0, 'zero'], [1, 's'], [2, '+']]

domains = ['even', 'odd']

domrestricimpl = [[[],[['zero', 'even', 1, []]]],[[['N','even',1,'N']],[['s(N)','odd',1,'N']]],
					[[['N','odd',1,'N']],[['s(N)','even',1,'N']]],
					[[['N','odd',1,'N']],[['N','even',0,'N']]]]


domrestricimpl = [  [[] 				    ,  [['zero', 'even', 1, []]]],
					[[['N', 'even', 1, 'N']], [['s(N)','odd',1,'N'   ]]],
					[[['N', 'odd',  1, 'N']], [['s(N)','even',1,'N'  ]]],
					[[['N', 'odd',  1, 'N']], [['N','even',0,'N'    ]]]]
