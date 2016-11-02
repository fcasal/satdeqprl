# EXAMPLE 2 (Example 4.4.1 of [1]) - UNSAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses simple_nat theory
from theories.simple_nat import *

Psi = ["""'Forall[{c:Constant@even}]"""]
Sigma = []
Pi = ["""le[(1)Pr[{c:Constant=zero}]+(-0.6666)Pr[{c:Constant@even}],0]""",
      """sg[(1)Pr[{c:Constant=zero}],0.6666]"""]

# Bibliography
# [1] A. Mordido. A probabilistic logic over equations and domain restrictions.
#                 PhD thesis, IST, Universidade de Lisboa.
