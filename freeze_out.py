import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import make_interp_spline
from scipy.optimize import root 
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.optimize import fsolve
from scipy.special import kv
from scipy.optimize import bisect

cards = sorted([name.replace('.dat','') for name in os.listdir("./cards_v2")])

### Getting JS "true" values
xf_line = "Xf="
mass_line = "MN1="

masses = dict()
xfs = dict()

for card in cards:
    file = "./JS-files/files_v2/output/" + card + ".txt"
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
my_xfs_mycode = dict()
my_xfs_micromegas = dict()

mi_points=''
my_points=''

Mp = 2.435e+18

def getting_Tf(filename):
    
    ## T vs neq
    T_neq, neq = np.loadtxt(neq_file, unpack=True)
    
    mask = neq > 0.0
    T_neq = T_neq[mask]
    neq = neq[mask]
    
    order = np.argsort(T_neq)
    T_neq = T_neq[order]
    neq = neq[order]
    
    neq_func = lambda x: np.exp(np.interp(np.log(x), np.log(T_neq), np.log(neq)))
    
    ## T vs sigmaV
    xs, sv = np.loadtxt(filename, unpack=True)
    Ts = m1/xs
    
    mask = sv > 0.0
    Ts = Ts[mask]
    sv = sv[mask]
    
    mask1 = (Ts < np.max(T_neq)) & (Ts > np.min(T_neq))
    Ts = Ts[mask1]
    sv = sv[mask1]
    
    order = np.argsort(Ts)
    Ts = Ts[order]
    sv = sv[order]
    
    ## H
    ro_r = (np.pi**2/30.)*dof_func(Ts)*Ts**4
    H = np.sqrt(ro_r/(3.*Mp**2))
    
    ## neq*sigmaV/H = 1
    z = sv*neq_func(Ts)/H
    func = lambda x: np.interp(np.log(x), np.log(Ts), np.log(z))
    Tf = bisect(func, np.min(Ts), np.max(Ts))
    
    return Tf

for card in cards:
    # print(card)
    
    neq_file = f"./output{my_points}/" + card + "/neq.dat"
    with open(neq_file) as myfile:
        m1 = float(myfile.readline().replace('# m1 =',''))
    
    Tf_mycode = getting_Tf(f"./output{my_points}/"+card+"/TOTALS_T.dat")
    Tf_micromegas = getting_Tf(f"./micromegas_output/m1T-1_vs_sigmaV{mi_points}/"+card+".dat")
   
    xf_mycode = m1/Tf_mycode
    xf_micromegas = m1/Tf_micromegas
    
    my_masses[card] = m1
    my_xfs_mycode[card] = xf_mycode
    my_xfs_micromegas[card] = xf_micromegas

### Plotting
plt.scatter([masses[card] for card in cards], [np.abs(1 - my_xfs_mycode[card]/xfs[card]) for card in cards], label='micros', alpha=0.5,color='r')
plt.scatter([masses[card] for card in cards], [np.abs(1 - my_xfs_micromegas[card]/xfs[card]) for card in cards], label='mine', alpha=0.5,color='g')
plt.legend()
plt.xscale('log')
#plt.yscale('log')
#plt.ylim(0.030,.230)
plt.xlabel('m1')
plt.title(f'micromegas{mi_points} vs. mycode{my_points}')
#plt.ylabel('interpolated')
#plt.savefig(f'./xfs-relerr-mi-my-OnlyN1.png')
plt.show()
