# EXAMPLE - SAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses simple_nat theory
from theories.simple_nat import *

Psi = ["""'Forall[{c:Constant@even}]"""]
Sigma = []
Pi = ["""le[(1)Pr[{c:Constant=zero}]+(-0.25)Pr[{c:Constant@even}],0]""", """ge[(1)Pr[{c:Constant=zero}],0.25]"""]
