# EXAMPLE 7 - UNSAT
# 4 disjuncts to test satisfiability - if some of them returns SAT, the problem is satisfiable
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# uses dolev_yao_sym theory
from theories.dolev_yao_tiny import *

# # # 1st disjunct UNSAT
Psi = ["""'Forall[{p1:Constant@symkey}]""","""'Forall[{c1:Constant@conf}]""","""'Forall[and({m1:Constant=aenc(pair(n:Constant,c:Constant),pub(b:Constant))},{m2:Constant=enc(n:Constant,p:Constant)})]"""]
Sigma = []
Pi = ["""sg[(1)Pr[and({p:Constant=p1:Constant},{c:Constant=c1:Constant})]+(-1)Pr[{aenc(pair(dec(m2:Constant,p1:Constant),c1:Constant),pub(b:Constant))=m1:Constant}],0]""","""eq[(1)Pr[and({p:Constant=p1:Constant},{c:Constant=c1:Constant})],0.25]""","""eq[(1)Pr[{c:Constant=c1:Constant}],0.5]""","""eq[(1)Pr[{p:Constant=p1:Constant}],0.5]"""]


# 2nd disjunct UNSAT
# Psi = ["""'Forall[{p1:Constant@symkey}]""","""'Forall[{c1:Constant@conf}]""","""'Forall[and({m1:Constant=aenc(pair(n:Constant,c:Constant),pub(b:Constant))},{m2:Constant=enc(n:Constant,p:Constant)})]"""]
# Sigma = ["""'not['Forall[{p1:Constant@symkey}]]"""]
# Pi = ["""sg[(1)Pr[and({p:Constant=p1:Constant},{c:Constant=c1:Constant})]+(-1)Pr[{aenc(pair(dec(m2:Constant,p1:Constant),c1:Constant),pub(b:Constant))=m1:Constant}],0]""","""eq[(1)Pr[{c:Constant=c1:Constant}],0.5]""", """di[(1)Pr[{p:Constant=p1:Constant}],0.5]"""]

# 3rd disjunct UNSAT
# Psi = ["""'Forall[{p1:Constant@symkey}]""","""'Forall[{c1:Constant@conf}]""","""'Forall[and({m1:Constant=aenc(pair(n:Constant,c:Constant),pub(b:Constant))},{m2:Constant=enc(n:Constant,p:Constant)})]"""]
# Sigma = ["""'not['Forall[{c1:Constant@conf}]]"""]
# Pi = ["""sg[(1)Pr[and({p:Constant=p1:Constant},{c:Constant=c1:Constant})]+(-1)Pr[{aenc(pair(dec(m2:Constant,p1:Constant),c1:Constant),pub(b:Constant))=m1:Constant}],0]""","""di[(1)Pr[{c:Constant=c1:Constant}],0.5]""","""eq[(1)Pr[{p:Constant=p1:Constant}],0.5]"""]


# 4th disjunct UNSAT
# Psi = ["""'Forall[{p1:Constant@symkey}]""","""'Forall[{c1:Constant@conf}]""","""'Forall[and({m1:Constant=aenc(pair(n:Constant,c:Constant),pub(b:Constant))},{m2:Constant=enc(n:Constant,p:Constant)})]"""]
# Sigma = ["""'not['Forall[{c1:Constant@conf}]]""", """'not['Forall[{p1:Constant@symkey}]]"""]
# Pi = ["""sg[(1)Pr[and({p:Constant=p1:Constant},{c:Constant=c1:Constant})]+(-1)Pr[{aenc(pair(dec(m2:Constant,p1:Constant),c1:Constant),pub(b:Constant))=m1:Constant}],0]""",
#          """di[(1)Pr[{c:Constant=c1:Constant}],0.5]"""]

# Bibliography
# [1] A. Mordido. A probabilistic logic over equations and domain restrictions.
#                 PhD thesis, IST, Universidade de Lisboa.
