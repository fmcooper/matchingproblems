\* Student-Project-Allocator *\
Maximize
OBJ: obj_maxsize
Subject To
_C1: (1,1) + (1,3) + (2,1) + (2,2) + (2,3) + (3,1) + (3,2) + (4,2)
 - obj_maxsize = 0
_C2: obj_maxsize >= 4
lec_lq_0: (1,1) + (2,1) + (3,1) >= 0
lec_lq_1: (2,2) + (3,2) + (4,2) >= 0
lec_lq_2: (1,3) + (2,3) >= 0
lec_uq_0: (1,1) + (2,1) + (3,1) <= 2
lec_uq_1: (2,2) + (3,2) + (4,2) <= 1
lec_uq_2: (1,3) + (2,3) <= 1
proj_lq_0: (1,1) + (2,1) + (3,1) >= 0
proj_lq_1: (2,2) + (3,2) + (4,2) >= 0
proj_lq_2: (1,3) + (2,3) >= 0
proj_uq_0: (1,1) + (2,1) + (3,1) <= 2
proj_uq_1: (2,2) + (3,2) + (4,2) <= 1
proj_uq_2: (1,3) + (2,3) <= 1
_dummy: __dummy = 0
st_limit_0: __dummy <= 1
st_limit_1: (1,1) + (1,3) <= 1
st_limit_2: (2,1) + (2,2) + (2,3) <= 1
st_limit_3: (3,1) + (3,2) <= 1
st_limit_4: (4,2) <= 1
Bounds
__dummy = 0
0 <= obj_maxsize <= 4
Generals
obj_maxsize
Binaries
(1,1)
(1,3)
(2,1)
(2,2)
(2,3)
(3,1)
(3,2)
(4,2)
End
