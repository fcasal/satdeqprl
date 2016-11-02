# DOLEV - YAO symmetric + asymmmetric

filenamemaude = "./maudespec/dolev_yao_full.maude"

rewritesystem = [['equat(dec(enc(X,K),K), X)', ['X', 'K']],
                 ['equat(adec(aenc(X,pub(K)),prv(K)), X)', ['X', 'K']],
                 ['equat(proj1(pair(X,Y)), X)', ['X', 'Y']],
                 ['equat(proj2(pair(X,Y)), Y)', ['X', 'Y']]]

signature = [[1, 'proj1'],
             [1, 'proj2'],
             [1, 'pub'],
             [1, 'prv'],
             [2, 'enc'],
             [2, 'dec'],
             [2, 'aenc'],
             [2, 'adec']]

domains = ['symkey', 'plain',  'conc', 'cipher',
           'pubkey', 'prvkey', 'principals', 'conf']

domrestricimpl = [[[['K','symkey',1,['K']],['X','plain',1,['X']]],
                            [['enc(X,K)', 'cipher', 1, ['X','K']]]],

                  [[['K','symkey',1,['K']],['X','cipher',1,['X']]],
                            [['dec(X,K)', 'plain', 1, ['X','K']]]],

                  [[['X','plain',1,['X']],['Y','plain',1,['Y']]],
                            [['pair(X,Y)', 'conc', 1, ['X','Y']]]],

                  [[['X','conc',1,['X']]],
                            [['X', 'plain', 1, ['X']]]],

                  [[['X','conc',1,['X']]],
                            [['proj1(X)', 'plain', 1, ['X']]]],

                  [[['X','conc',1,['X']]],
                            [['proj2(X)', 'plain', 1, ['X']]]],

                  [[['K','principals',1,['K']]],
                            [['pub(K)', 'pubkey', 1, ['K']]]],

                  [[['K','principals',1,['K']]],
                            [['prv(K)', 'prvkey', 1, ['K']]]],

                  [[['K','pubkey',1,['K']],['X','plain',1,['X']]],
                            [['aenc(X,K)', 'cipher', 1, ['X','K']]]],

                  [[['K','prvkey',1,['K']],['X','cipher',1,['X']]],
                            [['adec(X,K)', 'plain', 1, ['X','K']]]]]
