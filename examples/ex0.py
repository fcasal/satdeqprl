# EXAMPLE 0 - UNSAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses simple_nat theory
from theories.simple_nat import *

# formulas
Psi = ["""'Forall[{c:Constant@even}]""", """'Forall[or({c:Constant=zero} , {d:Constant=s(+(zero,d:Constant))})]"""]
Sigma = ["""'not['Forall[{s(c:Constant)@odd}]]"""]
Pi = ["""ge[(1)Pr[{c:Constant=zero}]+(-0.3)Pr[imp({zero=zero}{zero@even})],0.66]"""]
