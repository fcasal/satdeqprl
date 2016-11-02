# EXAMPLE 4 (Example 4.2.2 of [1]) -  UNSAT
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses dolev_yao_sym theory
from theories.dolev_yao_sym import *

Psi = ["""'Forall[and({k:Constant@symkey},{m:Constant@plain})]"""]
Sigma = ["""'not['Forall[imp(not({dec(enc(m:Constant,k:Constant),k1:Constant)@plain}), not({k:Constant=k1:Constant}) )]]"""]
Pi = []

# Bibliography
# [1] A. Mordido. A probabilistic logic over equations and domain restrictions.
#                 PhD thesis, IST, Universidade de Lisboa.
