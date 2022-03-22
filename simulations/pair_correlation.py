from skeleton import (
    init_fcc, equalise_system, Verlet_integrate_images,
    gen_rv_matrices, store_rv, init_v_gauss, init_rv_uniform,
    SIGMA, pair_correlation
)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 180
mpl.rcParams["legend.loc"] = "best"
mpl.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ["Computer Modern Roman"]
})


lattice_spacing = 5.26e-10 #Meters
fcc_space = lattice_spacing/SIGMA

D = 3
L = fcc_space*3+0.001
h = 1200


#### For simulating a solid
temps = [60,70]

for temp in temps:
    r0, v0 = init_fcc(L, fcc_space, 0, temp)
    N = r0.shape[0]
    print('equalising')
    R, V, pot, r1, v1 = equalise_system(r0, v0, temp, L, grace_time=20, error=2, adaptive=True)
    R, V = gen_rv_matrices(D,N,h) # generating matrices for storage
    R, V = store_rv(R,V,r1,v1,0) # storing initial condions in matrix
    print("integrating")
    Rt, Vt, forcet, pot = Verlet_integrate_images(N, R, V, 1, h, 0, L, 3, 1e-2)

    np.save('simulations\pc_solid_R_{}.npy'.format(int(temp)), Rt)


#### For simulating a gas
temps = [300, 280, 290]
N = 5
h = 5000

for temp in temps:
    r0, v0, = init_rv_uniform(3, N, L)
    v0 = init_v_gauss(N, temp)
    print("equalising")
    R, V, pot, r1, v1 = equalise_system(r0, v0, temp, L, grace_time=20, error=2, adaptive=True)
    R, V = gen_rv_matrices(D,N,h) # generating matrices for storage
    R, V = store_rv(R,V,r1,v1,0) # storing initial condions in matrix
    print("integrating")
    Rt, Vt, forcet, pot = Verlet_integrate_images(N, R, V, 1, h, 0, L, 3, 1e-2)

    np.save('simulations\pc_gas_R_{}.npy'.format(int(temp)), Rt)


#### For simulating a liquid
temps = [120, 130 , 140]
N = 30
h = 2500

for temp in temps:
    r0, v0, = init_rv_uniform(3, N, L)
    v0 = init_v_gauss(N, temp)
    print("equalising")
    R, V, pot, r1, v1 = equalise_system(r0, v0, temp, L, grace_time=20, error=2, adaptive=True)
    R, V = gen_rv_matrices(D,N,h) # generating matrices for storage
    R, V = store_rv(R,V,r1,v1,0) # storing initial condions in matrix
    print("integrating")
    Rt, Vt, forcet, pot = Verlet_integrate_images(N, R, V, 1, h, 0, L, 3, 1e-2)

    np.save('simulations\pc_liquid_R_{}.npy'.format(int(temp)), Rt)



a1 = np.load("..\Data\pc_liquid_R_120.npy")
a2 = np.load("..\Data\pc_gas_R_300.npy")
a3 = np.load("..\Data\pc_solid_R_30.npy")

b1 = np.load("..\Data\pc_solid_R_30.npy")
b2 = np.load("..\Data\pc_solid_R_70.npy")
b3 = np.load("..\Data\pc_solid_R_60.npy")

c1 = np.load("..\Data\pc_liquid_R_120.npy")
c2 = np.load("..\Data\pc_liquid_R_130.npy")
c3 = np.load("..\Data\pc_liquid_R_140.npy")

d1 = np.load("..\Data\pc_gas_R_280.npy")
d2 = np.load("..\Data\pc_gas_R_290.npy")
d3 = np.load("..\Data\pc_gas_R_300.npy")

def pc_wrapper(trace):
    g, bins = pair_correlation(trace, 200, L)
    g = g / np.sum(g)
    return g, bins

ga1, binsa1= pc_wrapper(a1)
ga2, binsa2= pc_wrapper(a2)
ga3, binsa3= pc_wrapper(a3)


gb1, binsb1= pc_wrapper(b1)
gb2, binsb2= pc_wrapper(b2)
gb3, binsb3= pc_wrapper(b3)

gc1, binsc1= pc_wrapper(c1)
gc2, binsc2= pc_wrapper(c2)
gc3, binsc3= pc_wrapper(c3)

gd1, binsd1= pc_wrapper(d1)
gd2, binsd2= pc_wrapper(d2)
gd3, binsd3= pc_wrapper(d3)

def scale(x):
    return x * SIGMA * 1e9

def scaleback(x):
    return x / SIGMA / 1e9

fig, ax = plt.subplots(2,2,sharex=True)

ax[0,0].plot(binsa2, ga2, label=r"$T=300K$", color='blue')
ax[0,0].plot(binsa1, ga1, label=r"$T=120K$", color='red')
ax[0,0].plot(binsa3, ga3, label=r"$T=30K$", color='orange')
ax[0,0].set_ylabel(r"$g_T(r)$")
ax[0,0].title.set_text("A")
secax = ax[0,0].secondary_xaxis('top', functions=(scale, scaleback))
secax.set_xlabel(r"distance [$nm$]")
ax[0,0].legend(frameon=False)

ax[0,1].plot(binsb3, gb3, label=r"$T=60K$", color='orange')
ax[0,1].plot(binsb1, gb1, label=r"$T=30K$", color='red')
ax[0,1].plot(binsb2, gb2, label=r"$T=70K$", color='blue')
ax[0,1].title.set_text("B")
secax = ax[0,1].secondary_xaxis('top', functions=(scale, scaleback))
secax.set_xlabel(r"distance [$nm$]")
ax[0,1].legend(frameon=False)

ax[1,0].plot(binsc3, gc3, label=r"$T=140K$", color='orange')
ax[1,0].plot(binsc2, gc2, label=r"$T=130K$", color='blue')
ax[1,0].plot(binsc1, gc1, label=r"$T=120K$", color='red')
ax[1,0].set_xlabel(r"distance [$\sigma$]")
ax[1,0].set_ylabel(r"$g_T(r)$")
ax[1,0].title.set_text("C")
secax = ax[1,0].secondary_xaxis('top', functions=(scale, scaleback))
ax[1,0].legend(frameon=False)


ax[1,1].plot(binsd3, gd3, label=r"$T=300K$", color='orange')
ax[1,1].plot(binsd2, gd2, label=r"$T=290K$", color='blue')
ax[1,1].plot(binsd1, gd1, label=r"$T=280K$", color='red')
ax[1,1].set_xlabel(r"distance [$\sigma$]")
ax[1,1].title.set_text("D")
secax = ax[1,1].secondary_xaxis('top', functions=(scale, scaleback))
ax[1,1].legend(frameon=False)

plt.gcf().set_size_inches(8,6)
plt.subplots_adjust(hspace=0.3)
plt.savefig("figs/pc_comp.pdf")
