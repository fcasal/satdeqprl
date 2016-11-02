# EXAMPLE 5 (Example 2.5.2 of [1]) -  SAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses dolev_yao_sym theory
from theories.dolev_yao_sym import *

Psi = ["""'Forall[and({m1:Constant=pair(a:Constant,n:Constant)},{m2:Constant=enc(n:Constant,k1:Constant)})]"""]
Sigma = ["""'not['Forall[{dec(m2:Constant,k:Constant)=proj2(m1:Constant)}]]"""]
Pi = []

# Bibliography
# [1] A. Mordido. A probabilistic logic over equations and domain restrictions.
#                 PhD thesis, IST, Universidade de Lisboa.
