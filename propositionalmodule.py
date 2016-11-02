from subprocess import Popen, PIPE
from itertools import product
import re
import copy

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def find_begin( s, first ):
    try:
        start = s.index( first ) + len( first )
        return s[start:]
    except ValueError:
        return ""


def instantiate(rewritesystem, subterms):
	l = []
	for rule in rewritesystem:
		thisrule = rule[0]
		variables = rule[1]
		numvars = len(variables)
		for element in product(subterms, repeat=numvars):
			rep = {}
			for idx, val in enumerate(element): #build dictionary
				rep[variables[idx]] = val
			#replace using reg exps^^^ also iteritems in python2
			rep = dict((re.escape(k), v) for k, v in rep.items())
			pattern = re.compile("|".join(rep.keys()))
			l.append(pattern.sub(lambda m: rep[re.escape(m.group(0))], thisrule))
	return l

def instatiatedomainterms(domainrestric,  subterms):
	l = []
	for restr in domainrestric:
		term = restr[0]
		variables = restr[3]
		numvars = len(variables)
		if numvars==0:
			l.append(term)
		else:
			for element in product(subterms, repeat=numvars):
				rep = {}
				for idx, val in enumerate(element): #build dictionary
					rep[variables[idx]] = val
     			#iteritems in python 2
				rep = dict((re.escape(k), v) for k, v in rep.items())
				pattern = re.compile("|".join(rep.keys()))
				l.append(pattern.sub(lambda m: rep[re.escape(m.group(0))], term))
	return l

def runMaude(filename):
	p = Popen(['./maude.darwin64'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate("load {} .".format(filename).encode())
	output = output.decode().replace('\n', ' ').replace('\r', '').replace(' ','').replace('\t','').replace('sepa,sepa','sepa')
	output = find_between(output, "]:", "Maude>Bye.").split(",sepa,")

	if output[-1].endswith(',sepa'):
		output[-1]=output[-1][:-5]
	# remove duplicates
	output = list(set(output))
	return output



def parseNormMaude(filename):
	p = Popen(['./maude.darwin64'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate("load {} .".format(filename).encode())
	output = find_between(output.decode(),"Maude> ==========================================" ,"Maude> Bye.")
	output = output.split("==========================================")
	output = map( lambda x: x.replace("\n",""), output)
	output = map(lambda x : find_begin(x ,"result Constant: ").replace(" ", ""), output)
	return output


def variablesdomrestr(domrestric):
	l = []
	for elem in domrestric:
		if elem:
			for i in elem:
				if i[3]:
					l.append(i[3])
	l = [item for sublist in l for item in sublist]
	return list(set(l))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

#propositional equality variable name
def propequal(a , b, enumrelterms):
	return "p{}={}".format(enumrelterms[a], enumrelterms[b])

def propequaldic(a,b):
	return "p{}={}".format(a, b)

#propositional domain variable name
def propdom(a , b, enumrelterms):
	return "p{}@{}".format(enumrelterms[a], b)

# implication smt lib
def implic(a, b):
	return "(=> {} {})".format(a, b)

# conjunction smt lib
def conju(a, b):
	return "(and {} {})".format(a, b)

# conjunction smt lib
def conjulist( l):
	if l:
		return "(and {})".format(" ".join(l))
	else:
		return " true "

# disjunction smt lib
def disjulist(l):
	return "(or {})".format(" ".join(l))

# not smt lib
def negation(a):
	return "(not {})".format(a)

# assert smt lib
def assertion(f):
	return "(assert {})\n".format(f)

# reflexivity
def reflex(relterms, atlas, enumrelterms, numbercopies):
	return [ propequal(i, atlas[i], enumrelterms)+"$"+str(idx) for idx in range(numbercopies) for i in relterms]

def symmstring(a, b, idx):
	return "(=> p{}={}${} p{}={}${})".format(a, b,idx, b, a,idx)

# symmetry
def symm(relterms, enumrelterms, numbercopies):
	return [ symmstring( enumrelterms[elem[0]], enumrelterms[elem[1]], str(idx)) for idx in range(numbercopies) for elem in product(relterms, repeat=2) ]

# transitivity
def transistring(a,b,c, idx):
	return "(=> (and p{}={}${} p{}={}${}) p{}={}${})".format(a, b, idx, b, c,idx, a, c, idx)

def transitriangular(relterms, enumrelterms, numbercopies):
	lenlen = len(relterms)
	transi = [ transistring(enumrelterms[elem], enumrelterms[elem2], enumrelterms[relterms[idxelem3]], str(index)) for index in range(numbercopies)
	 for idx, elem in enumerate(relterms) for idxelem3 in range(int(idx),lenlen) for elem2 in relterms ]
	return transi

# congruence
def congru( relterms, enumreltermsglob, atlas, signature, numbercopies ):
	enumrelterms = enumreltermsglob
	congru = []
	for index in range(numbercopies):
		for func in signature:
			arity = func[0]
			symb = func[1]
			if arity == 0:
				value = atlas.get(symb)
				if value:
					congru.append( propequal(symb, symb, enumrelterms)+"$"+str(index))
			else:
				dicaux = {}
				for element in product(relterms, repeat=arity):
					term = symb+"("+",".join(element)+")"
					value = atlas.get(term)
					if value:
						dicaux[element] = value
				iteraa = range(0, arity)
				for element in product(dicaux.items(),repeat=2):
					lista = [ propequal(element[0][0][i], element[1][0][i], enumrelterms)+"$"+str(index) for i in iteraa ]
					congru.append( implic( conjulist(lista), propequal( element[0][1], element[1][1], enumrelterms )+"$"+str(index)))
	return congru

def memberstring(a, b, c, idx):
	return  "(=> (and p{}={}${} p{}@{}${}) p{}@{}${})".format(a, b,idx, a, c,idx, b, c,idx)

# membership
def member( relterms, enumrelterms, domains, numbercopies):
	return [ memberstring(enumrelterms[elem[0]], enumrelterms[elem[1]], elem[2], str(idx)) for idx in range(numbercopies) for elem in product(relterms, relterms, domains)]

# instatiationdomain restristrcition
def instatiatedomainrestr(domainrestric,  relterms):
	init = domainrestric
	r=[]
	variables = variablesdomrestr(domainrestric)
	numvars = len(variables)
	if numvars == 0:
		r.append(domainrestric)
		return r
	else:
		for element in product(relterms, repeat=numvars):
			l = copy.deepcopy(init)
			for lados in l:
				for cond in lados:
					rep = {}
					for idx, val in enumerate(element): #build dictionary
						rep[variables[idx]] = val
					 	#replace using reg exps
					rep = dict((re.escape(k), v) for k, v in rep.items())
					pattern = re.compile("|".join(rep.keys()))
					cond[0] = pattern.sub(lambda m: rep[re.escape(m.group(0))], cond[0])
			r.append(l)
	return r

def dommember(domrestricimpl, subtermsformula, enumrelterms, numbercopies):
	mem = []
	for index in range(numbercopies):
		for dr in domrestricimpl:
			listinst = instatiatedomainrestr(dr, subtermsformula)
			for inst in listinst:
				form = [propdom(elem[0], elem[1], enumrelterms)+"$"+str(index) for elem in inst[0]]
				left = conjulist(form)
				form = [propdom(elem[0], elem[1], enumrelterms)+"$"+str(index) if elem[2] == 1 else negation(propdom(elem[0], elem[1], enumrelterms)+"$"+str(index)) for elem in inst[1]]
				right = conjulist(form)
				mem.append(implic(left, right))
	return mem

def definevariables(relterms, enumrelterms, domains, numbercopies):
	l=[]
	for element in product(relterms, relterms):
		l.append(propequal(element[0],element[1],enumrelterms))
	for element in product(relterms, domains):
		l.append(propdom(element[0],element[1],enumrelterms))
	p = ["".join(map(lambda x: "(define {}::bool)\n".format(x+"$"+str(idx)), l)) for idx in range(numbercopies)]
	return "".join(p)
