from subprocess import Popen, PIPE
from itertools import product
import re, copy, sys
from shutil import copyfile

from  propositionalmodule import *

from examples.ex1 import *

pathtoyices = '/usr/local/bin/yices'
pathtomaude = '/bin/maude.darwin64'




def runMaudesubformulas(filename):
	p = Popen([pathtomaude], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate("load {} .".format(filename))
	# print output
	output = output.replace('\n', ' ').replace('\r', '').replace(' ','').replace('\t','').replace('sepa,sepa','sepa')
	output = find_between(output, "result", ">Bye.")
	output = find_between(output, ":", "Maude").split(",sepa,")

	if output[-1].endswith(',sepa'):
		output[-1]=output[-1][:-5]
	# remove duplicates
	output = list(set(output))
	return output

def parsepsisubformulas(formulist, string, num):
	subterms = []
	psistar = []
	parsed= []
	for formula in formulist:
		sub = formula[len(string):num]
		partial = find_between(sub, "{", "}")
		parse = []
		while partial!="":
			sub = sub.replace("{"+partial+"}","("+partial+")")
			if "=" in partial:
				#treats equal
				lista = partial.split("=")
				parse.append(["=", lista, partial])
				subterms += lista
			elif "@" in partial:
				#treats dom
				lista = partial.split("@")
				parse.append(["@", lista, partial])
				subterms += [lista[0]]
			else:
				exit("error parsing")
			partial = find_between(sub, "{", "}")
		sub = sub.replace("and(", "(and ").replace("or(", "(or ").replace("not(", "(not ").replace("imp(", "(=> ").replace("equiv(", "(<=> ")
		parsed.append(parse)
		psistar.append(sub)
	# print subterms
	# print psistar
	return subterms, psistar, parsed

def parsePI(formulist):
	subterms = []
	parsed= []
	atomic = []
	for formula in formulist:
		typ = formula[:2]
		formula = formula[2:]
		cl = []
		partial = find_between(formula, "(",")")
		parse = []
		while partial!="":
			formula = formula.replace("("+partial+")","")
			probform = find_between(formula, "Pr[", "]")
			atoms = find_between(probform, "{", "}")
			auxset = []
			while atoms != "":
				probform = probform.replace("{"+atoms+"}","("+atoms+")")
				if "=" in atoms:
					#treats equal
					lista = atoms.split("=")
					auxset.append(["=", lista, atoms])
					subterms += lista
				elif "@" in atoms:
					#treats dom
					lista = atoms.split("@")
					auxset.append(["@", lista, atoms])
					subterms += [lista[0]]
				else:
					exit("error parsing Pi")
				atoms = find_between(probform, "{", "}")
			parse.append(auxset)
			auxset = []
			formula = "]".join(formula.split("]")[1:])
			probform = probform.replace("and(", "(and ").replace("or(", "(or ").replace("not(", "(not ").replace("imp(", "(=> ").replace("equiv(", "(<=> ")
			cl.append([partial,probform])
			partial = find_between(formula, "(",")")
		atomic.append(parse)
		# print cl
		kappa = find_between(formula, ",", "]")
		# print(kappa)
		parsed.append([typ,cl,kappa])
	return subterms, parsed, atomic


def probabilistic( probabilisticformulas, freshlist ):
	n = len(freshlist[0])
	yicescode = ""
	a = [["a"+str(i)+"@"+str(j) for j in range(n+1)] for i in range(n)]
	b = [["b"+str(i)+"@"+str(j) for j in range(n+1)] for i in range(n)]
	p = ["p"+str(i) for i in range(n+1)]
	kappa = ["kappa"+str(i) for i in range(n)]
	atlas = dict(zip(freshlist[0], kappa))
	for i in range(n):
		yicescode += "\n(define "+ kappa[i] +"::real)\n(assert (and (<= "+ kappa[i] +" 1) (>= "+ kappa[i] +" 0)))"
		for j in range(n+1):
			yicescode += "\n(define "+ a[i][j] +"::int)\n(assert (or (= "+ a[i][j] +" 1) (= "+ a[i][j] +" 0)))"
			yicescode += "\n(assert (<=> (= {} 1) {}))".format(a[i][j], freshlist[j][i])
			yicescode += "\n(define "+ b[i][j] +"::real)\n(assert (and (<= "+ b[i][j]+" 1) (>= "+ b[i][j]+ " 0)))"
		yicescode += "\n(define "+ p[i] +"::real)\n(assert (and (<= "+p[i]+" 1) (>= "+ p[i]+" 0)))"
	yicescode += "\n(define "+ p[n] +"::real)\n(assert (and (<= "+p[n]+" 1) (>= "+p[n]+" 0)))"
	for form in probabilisticformulas[0]:
		# print(form)
		typ = form[0]
		indepterm = form[-1]
		constraint = "(+ "
		for parcel in form[1]:
			constraint += " (* " + parcel[0] + " " + atlas[parcel[1]] + " )"
		constraint += " )"
		if typ in "eq":
			yicescode += "\n(assert (= "+ constraint + " " + indepterm + " ))"
		elif typ in "ge":
			yicescode += "\n(assert (>= "+ constraint + " " + indepterm + " ))"
		elif typ in "le":
			yicescode += "\n(assert (<= "+ constraint + " " + indepterm + " ))"
		elif typ in "sl":
			yicescode += "\n(assert (< "+ constraint + " " + indepterm + " ))"
		elif typ in "sg":
			yicescode += "\n(assert (> "+ constraint + " " + indepterm + " ))"
		elif typ in "di":
			yicescode += "\n(assert (/= "+ constraint + " " + indepterm + " ))"

	expr1 = "";
	expr2 = "";
	for i in range(n):
		expr = ""
		for j in range(n+1):
			expr += " " + b[i][j]
			expr1 = b[i][j]
			yicescode +=  "\n(assert (>= " + expr1 + " 0))"
			yicescode += "\n(assert (<= " + expr1 + " " + a[i][j]+ " ))"

			expr2 = "(+ "+ a[i][j] +" "+ p[j] +" -1)"
			yicescode  += "\n(assert (>= " + expr1 + " "+ expr2 +") )"
			yicescode += "\n(assert (<= " + expr1 + " "+ p[j] +") )"

		yicescode += "\n(assert (= (+ "+ expr +" ) "+ kappa[i]+ " ))"

	expr = ""
	for i in range(n+1):
		expr  += " " + p[i]
	yicescode += "\n(assert (= (+ "+ expr + " ) 1))"
	return yicescode


def propositionalize(parse, setcopy, enumrelterms, index):
	setz = copy.deepcopy(setcopy)
	for idx,val in enumerate(parse):
		for term in val:
			rule= term[0]
			if rule is '@':
				aux = propdom( term[1][0], term[1][1], enumrelterms)+"$"+str(index)
				setz[idx] = setz[idx].replace("("+term[2]+")", aux)
			elif rule is "=":
				aux = propequal( term[1][0], term[1][1], enumrelterms)+"$"+str(index)
				setz[idx] = setz[idx].replace("("+term[2]+")", aux)
	setz = map(lambda x: x.replace(",", " "), setz)
	return setz


def propositionalizeprobs(parse, setcopy, enumrelterms, index):
	setz = copy.deepcopy(setcopy)
	for idx,val in enumerate(parse):
		for inds, term in enumerate(val):
			for parcela in term:
				rule= parcela[0]
				if rule is '@':
					aux = propdom( parcela[1][0], parcela[1][1], enumrelterms)+"$"+str(index)
					setz[idx][1][inds][1] = setz[idx][1][inds][1].replace("("+parcela[2]+")", aux+" ")
				elif rule is "=":
					aux = propequal( parcela[1][0], parcela[1][1], enumrelterms)+"$"+str(index)
					setz[idx][1][inds][1] = setz[idx][1][inds][1].replace("("+parcela[2]+")", aux+" ")
	return setz


def newasserts(probabilisticformulas, freshlist, ind):
	newasserts = []
	order = 0
	for i in probabilisticformulas:
		for term in i[1]:
			# print(term)
			form = "(define {}::bool)\n(assert (<=> {} {}))\n".format(freshlist[ind][order],freshlist[ind][order], term[1].replace(",",""))
			term[1] = freshlist[ind][order]
			order +=1
			newasserts.append(form)
	return "".join(newasserts), probabilisticformulas



def addmostassertions(Psi, Sigma, Pi, filenamemaude, rewritesystem, signature, domains, domrestricimpl):
	Psi = list(map(lambda x: x.replace(" ", ""), Psi))
	Sigma = list( map(lambda x: x.replace(" ", ""), Sigma))
	Pi = list(map(lambda x: x.replace(" ", ""), Pi))

	# Extracting subterms from Psi, Sigma, Pi
	instruction = "\n\nred terms(("+",".join(Psi + Sigma + Pi)+")) ."

	with open(filenamemaude, "r") as myfile:
	    working = myfile.read()
	    with open("answer.maude", "w") as f:
	    	f.write(working)
	    	f.write(instruction)
	subtermsformulapsi , psistar , parsepsi = parsepsisubformulas(Psi, "'Forall[", -1)
	subtermsformulasigma , sigmastar , parsesigma = parsepsisubformulas(Sigma, "'not['Forall[", -2)
	subtermsformulapi, probabilisticformulas, atomic = parsePI(Pi)

	numberoffresh = sum([len(i[1]) for i in probabilisticformulas])
	# print(numberoffresh)

	subtermsformula = list(set(subtermsformulapsi + subtermsformulasigma + subtermsformulapi))
	domretricunion = [el for i in domrestricimpl for ite in range(len(i)) for el in i[ite]]

	instancedomains = instatiatedomainterms( domretricunion, subtermsformula)
	instancelist = instantiate(rewritesystem, subtermsformula)
	instancelist = list(set(instancelist + instancedomains))

	instruction = "\n\nred terms(("+",".join(instancelist)+")) ."

	with open(filenamemaude, "r") as myfile:
	    working = myfile.read()
	    with open("answer.maude", "w") as f:
	    	f.write(working)
	    	f.write(instruction)

	subtermsrules = runMaude("answer.maude")
	allsubterms =  list(set(subtermsformula + subtermsrules))
	# print(allsubterms)

	with open(filenamemaude, "r") as myfile:
	    working = myfile.read()
	    with open("tonormalize.maude", "w") as f:
	    	f.write(working)
	    	for term in allsubterms:
	    		f.write("\nred in SIMPLE : " + term + " .")


	allnormforms = list(parseNormMaude("tonormalize.maude"))
	assert( len(allnormforms) == len(allsubterms))
	numbercopies = numberoffresh + 1

	# relevant terms
	relterms = list(set(allsubterms + allnormforms))
	# enumeration of terms in relterms
	print(len(relterms))
	enumrelterms = dict(zip(relterms, range(0,len(relterms))))
	# maps relterms to their normal form
	atlas = dict(zip(allsubterms + allnormforms, allnormforms + allnormforms))
	psicopy = copy.deepcopy(psistar)
	psilist = []
	for ind in range(numbercopies):
		if psistar:
			psilist.append(propositionalize(parsepsi, psicopy, enumrelterms, ind))
	sigmalist = []
	sigmacopy = copy.deepcopy(sigmastar)

	for ind in range(numbercopies):
		if sigmastar:
			sigmalist.append( map(lambda x: negation(x), propositionalize(parsesigma , sigmacopy, enumrelterms, ind) ))

	pistar = [propositionalizeprobs(atomic, probabilisticformulas, enumrelterms, ind) for ind in range(numbercopies)]

	freshlist = [["qq"+str(i)+"$"+str(index) for i in range(numberoffresh)] for index in range(numbercopies)]


	pairsasserts = [newasserts(pistar[index], freshlist, index) for index in range(numbercopies)]
	asserts = "".join([i[0] for i in pairsasserts])
	with open("gotoyicesmaude.txt","w") as f:
		print("im gonna write to file now")
		print("definevars")
		f.write( definevariables(relterms, enumrelterms, domains, numbercopies))

		print("reflex")
		ref = reflex(relterms, atlas, enumrelterms, numbercopies)
		f.write( assertion(conjulist(ref)))
		print(len(ref))

		print("symm")
		sy = symm(relterms, enumrelterms, numbercopies)
		f.write( assertion(conjulist(sy)) )
		print(len(sy))

		print("transi")
		transilist = transitriangular( relterms, enumrelterms, numbercopies)
		print(len(transilist))
		chunky = chunks(transilist, min(len(transilist)//100,len(transilist)))
		# f.write("".join(map(lambda x: assertion(conjulist(x)), chunky)))
		for chun in chunky:
			f.write( assertion(conjulist(chun)) )

		print("congru")
		congr = congru( relterms, enumrelterms, atlas, signature, numbercopies)
		f.write( assertion(conjulist(congr)) )
		print(len(congr))

		print("member")
		mem = member(relterms, enumrelterms, domains, numbercopies)
		f.write( assertion(conjulist(mem)) )
		print(len(mem))

		print("dommember")
		dommem = dommember(domrestricimpl, subtermsformula, enumrelterms,numbercopies)
		f.write( assertion(conjulist(dommem)) )
		print(len(dommem))

		print("psistar")
		print(len(psistar))

		f.write("".join(map(lambda x: assertion(conjulist(x)), psilist )))

	return sigmalist, freshlist, pistar, asserts, numbercopies


def SATDEQPRLS(sigmastar, freshlist, probabilisticformulas, asserts, numbercopies):
	copyfile("gotoyicesmaude.txt", "prob.txt")
	with open("prob.txt","a") as f:
		f.write(asserts)
		f.write( probabilistic(probabilisticformulas, freshlist))
		f.write( "\n(check)\n(show-model)")
	print("***********\nFIRST STEP\n***********\n")
	p = Popen([pathtoyices,'prob.txt'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate()
	output = output.decode()
	err = err.decode()

	if "unsat" in output:
		print("UNSATISFIABLE")
		return 0
	elif "interrupted" in output:
		print("TIMEOUT")
		return 0
	elif "sat" not in output:
		print(output)
		print(err)
		exit("ERRO")

	print("***********\nSECOND STEP\n***********\n")
	flatsigmastar = [item for i in sigmastar for item in i]
	for form in flatsigmastar:
		copyfile("gotoyicesmaude.txt", "formgenp.txt")
		with open("formgenp.txt","a") as f:
			f.write( assertion(form))
			f.write("(check)")
		p = Popen([pathtoyices,'formgenp.txt'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate()
		output = output.decode()
		err = err.decode()
		if "unsat" in output:
			print(output)
			print(err)
			print("UNSATISFIABLE")
			return 0
		elif "interrupted" in output:
			print(output)
			print(err)
			print("TIMEOUT")
			return 0
		elif "sat" not in output:
			print(output)
			print(err)
			exit("ERRO")
	print("SATISFIABLE")
	return 1


sigmastar, freshlist, probabilisticformulas, asserts, numbercopies = addmostassertions(Psi, Sigma, Pi, filenamemaude, rewritesystem, signature, domains, domrestricimpl)
SATDEQPRLS(sigmastar, freshlist, probabilisticformulas, asserts, numbercopies)
