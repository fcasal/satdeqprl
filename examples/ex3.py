# EXAMPLE 3 (Example 4.2.2 of [1]) - UNSAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses dolev_yao_sym theory
from theories.dolev_yao_sym import *

Psi = ["""'Forall[{k1:Constant@symkey}]"""]
Sigma = []
Pi = ["""eq[(1)Pr[{k:Constant=k1:Constant}]+(-0.4)Pr[{k1:Constant@symkey}],0]""", """sl[(1)Pr[{dec(enc(m:Constant,k:Constant),k1:Constant)=m:Constant}],0.4]"""]


# Bibliography
# [1] A. Mordido. A probabilistic logic over equations and domain restrictions.
#                 PhD thesis, IST, Universidade de Lisboa.
