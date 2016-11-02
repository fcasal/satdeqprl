# DOLEV - YAO symmetric + asymmmetric
# tiny version -- has no projections or principals

filenamemaude = "./maudespec/dolev_yao_full.maude"

rewritesystem = [['equat(dec(enc(X,K),K), X)', ['X','K']],
                 ['equat(adec(aenc(X,pub(K)),prv(K)), X)', ['X','K']]]

signature = [[1, 'pub'],
             [1, 'prv'],
             [2, 'enc'],
             [2, 'dec'],
             [2, 'aenc'],
             [2, 'adec']]

domains = ['symkey', 'plain', 'cipher', 'pubkey',
           'prvkey', 'conf', 'conc']

domrestricimpl = [[[['K','symkey',1,['K']],['X','plain',1,['X']]],
                            [['enc(X,K)', 'cipher', 1, ['X','K']]]],

				  [[['K','symkey',1,['K']],['X','cipher',1,['X']]],
                            [['dec(X,K)', 'plain', 1, ['X','K']]]],

				  [[['X','plain',1,['X']],['Y','plain',1,['Y']]],
                            [['pair(X,Y)', 'conc', 1, ['X','Y']]]],

				  [[['X','conc',1,['X']]],
                            [['X', 'plain', 1, ['X']]]]
				  ]
