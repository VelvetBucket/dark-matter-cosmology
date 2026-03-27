import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import make_interp_spline
from scipy.optimize import root 
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.optimize import fsolve
from scipy.special import kv

cards = sorted([name.replace('.dat','') for name in os.listdir("./cards")])

### Getting JS "true" values
xf_line = "Xf="
mass_line = "MN1="

masses = dict()
xfs = dict()

for card in cards:
    file = "./JS-files/files/output/" + card + ".txt"
    #print(card)
    mass = 0.
    xf = 0.
    found = False
    with open(file) as myfile:
        for line in myfile.readlines():
            if xf_line in line:
                xf = float(line.replace(xf_line,''))
            elif mass_line in line:
                mass = float(line.replace(mass_line,''))
            if mass > 0. and xf > 0.:
                found = True
                break
    if not found:
        print(card + ": Not all parameters found")
    masses[card] = mass
    xfs[card] = xf

### Making interpolation function for DOF(T)
dof_T, dof_heff, dof_geff = np.loadtxt('./std_thg.txt', unpack=True)
dof_func = make_interp_spline(dof_T, dof_geff, k=0)
#dof_func = lambda x: np.interp(x,dof_T, dof_geff)
dof_T_test = np.logspace(np.log10(np.min(dof_T[1:])),np.log10(np.max(dof_T)),num=10*dof_T.size)
dof_geff_test = dof_func(dof_T_test)

plt.scatter(dof_T,dof_geff)
plt.plot(dof_T_test,dof_geff_test,color='r')
plt.xlim(1e-4,1e-2)
plt.xscale('log')
plt.yscale('log')
#plt.show()
plt.close()

### Getting my values

my_masses = dict()
my_xfs = dict()
my_xfs1 = dict()

mi_points='1000'
my_points='0500'

Mp = 2.435e+18

for card in cards:
    # print(card)
    xs_mine1, sv_mine1 = np.loadtxt(f"./output-{my_points}/"+card+"/TOTALS_T.dat", unpack=True)
    xs_mine, sv_mine = np.loadtxt(f"./micromegas_output/m1T-1_vs_sigmaV-{mi_points}/"+card+".dat", unpack=True)
    neq_file = f"./output-{my_points}/" + card + "/neq.dat"
    with open(neq_file) as myfile:
        m1 = float(myfile.readline().replace('# m1 =',''))
    T_mine = m1/xs_mine
    T_mine1 = m1/xs_mine1
    
    order = np.argsort(T_mine)
    T_mine = T_mine[order]
    sv_mine = sv_mine[order]
    
    order = np.argsort(T_mine1)
    T_mine1 = T_mine1[order]
    sv_mine1 = sv_mine1[order]
    
    T_neq, neq = np.loadtxt(neq_file, unpack=True)
    
    order = np.argsort(T_neq)
    T_neq = T_neq[order]
    neq = neq[order]
    neq1 = neq[neq>0]
    T_neq1 = T_neq[neq>0]
    
    neq_func = CubicSpline(T_neq, neq)
    
    ro_r = (np.pi**2/30.)*dof_func(T_mine)*T_mine**4
    H = np.sqrt(ro_r/(3.*Mp**2))
    zy_mine0 = sv_mine*neq_func(T_mine)
    func = CubicSpline(T_mine,zy_mine0 - H)
    
    ro_r1 = (np.pi**2/30.)*dof_func(T_mine1)*T_mine1**4
    H1 = np.sqrt(ro_r1/(3.*Mp**2))
    zy_mine01 = sv_mine1*neq_func(T_mine1)
    func1 = CubicSpline(T_mine1,zy_mine01-H1)

    Tfs = func.roots(extrapolate=False)
    if Tfs.size != 1:
        print("TF: HELP")
    Tf = Tfs[0]
    
    Tf1s = func1.roots(extrapolate=False)
    if Tf1s.size != 1:
        print("TF1: HELP")
    Tf1 = Tf1s[0]
    
    xf = m1/Tf
    xf1 = m1/Tf1
    
    my_masses[card] = m1
    my_xfs[card] = xf
    my_xfs1[card] = xf1

### Plotting
plt.scatter([masses[card] for card in cards], [np.abs(1 - my_xfs[card]/xfs[card]) for card in cards], label='micros', alpha=0.5,color='r')
plt.scatter([masses[card] for card in cards], [np.abs(1 - my_xfs1[card]/xfs[card]) for card in cards], label='mine', alpha=0.5,color='g')
#plt.scatter([masses[card] for card in cards], [np.abs(1 - my_xfs1[card]/my_xfs[card]) for card in cards], label='mine-vs-micro', alpha=0.5,color='b')
plt.legend()
plt.xscale('log')
#plt.yscale('log')
#plt.ylim(0,.1)
plt.xlabel('m1')
plt.title(f'micromegas {mi_points} vs. mycode {my_points}')
plt.ylabel('interpolated')
#plt.savefig(f'./xfs-relerr-mi{mi_points}-my{my_points}-SPLINE.png')
plt.show()
