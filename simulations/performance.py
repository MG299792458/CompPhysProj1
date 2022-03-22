from skeleton import (
    SIGMA, init_fcc, equalise_system, gen_rv_matrices, store_rv, Verlet_integrate_images
)
import cProfile



lattice_spacing = 5.26e-10 #Meters
fcc_space = lattice_spacing/SIGMA

D = 3
L = fcc_space*3+0.001
h = 200
temp = 40


r0, v0 = init_fcc(L, fcc_space, 0, temp)
N = r0.shape[0]
print('equalising')
R, V, pot, r1, v1 = equalise_system(r0, v0, temp, L, grace_time=20, error=2, adaptive=True)
R, V = gen_rv_matrices(D,N,h) # generating matrices for storage
R, V = store_rv(R,V,r1,v1,0) # storing initial condions in matrix
print("integrating")

execute_param = "Rt, Vt, ft, pot = Verlet_integrate_images(\
    N, R, V, 1, h, 0, L, 3, 1e-2)"

cProfile.run(execute_param, sort='tottime')