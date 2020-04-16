from GameManager import GameManager, main
from ComputerAI import ComputerAI
from PlayerAI import PlayerAI
from Displayer import Displayer
import numpy as np
import cProfile
import pstats

profile = cProfile.Profile()
profile.runcall(main)
ps = pstats.Stats(profile)
ps.print_stats()

# map = [
#     [2, 2,  4,  8   ],
#     [8, 8,  16, 2   ],
#     [4, 32, 2,  128 ],
#     [2, 8,  256,512 ]
# ]
# map_t = np.array(map).T.tolist()
# dirs = []
# for i in range(len(map)):
#     print(f'MAP ROW {i}     : {set(map[i])}')
#     print(f'MAP_T ROW {i}   : {set(map_t[i])}')
#     if len(set(map[i])) is 4:
#         if 0 in map[i][1:-1]:
#             dirs = dirs + [2, 3]
#         elif 0 in map[0]:
#             dirs = dirs + [2]
#         elif 0 in map[-1]:
#             dirs = dirs + [3]
#     else:
#         dirs = dirs + [2,3]
#     if len(set(map_t[i])) is 4:
#         if 0 in map_t[i][1:-1]:
#             dirs = dirs + [0, 1]
#         elif 0 in map_t[0]:
#             dirs = dirs + [0]
#         elif 0 in map_t[-1]:
#             dirs = dirs + [1]
#     else:
#         dirs = dirs + [0, 1]
# print(list(set(dirs)))
