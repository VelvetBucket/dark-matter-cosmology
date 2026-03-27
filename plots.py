import numpy as np
import matplotlib.pyplot as plt
import os

cards = sorted([name.replace('.dat','') for name in os.listdir("./cards")])

for card in cards[-1:]:
    
    data_mine = np.loadtxt("./output/"+card+"/TOTALS_T.dat")
    data_mine_micromegas = np.loadtxt("./micromegas_output/m1T-1_vs_sigmaV-0500/"+card+".dat")
    data_mine_micromegas1 = np.loadtxt("./T_vs_sigmaV.txt")
    xs_mine = data_mine[:,0]
    ys_mine = data_mine[:,1]

    xs_mine_micromegas = data_mine_micromegas[:,0] 
    ys_mine_micromegas = data_mine_micromegas[:,1]
    
    xs_mine_micromegas1 = data_mine_micromegas1[:,0] 
    ys_mine_micromegas1 = data_mine_micromegas1[:,1]
    '''
    errs = np.zeros(xs_mine.shape)
    mask = ys_mine_micromegas > 0.0
    errs[mask] = np.abs(ys_mine[mask] - ys_mine_micromegas[mask])/ ys_mine_micromegas[mask]
    errs[~mask] = ys_mine[~mask]
    errs[np.abs(errs) < 1e-3] = 0.0
    
    errs1 = np.zeros(xs_mine.shape)
    mask1 = ys_mine_micromegas1 > 0.0
    errs1[mask1] = np.abs(ys_mine[mask1] - ys_mine_micromegas1[mask1])/ ys_mine_micromegas1[mask1]
    errs1[~mask1] = ys_mine[~mask1]
    errs1[np.abs(errs1) < 1e-3] = 0.0
    
    errs2 = np.zeros(xs_mine_micromegas1.shape)
    mask2 = ys_mine_micromegas1 > 0.0
    errs2[mask2] = np.abs(ys_mine_micromegas[mask2] - ys_mine_micromegas1[mask2])/ ys_mine_micromegas1[mask2]
    errs2[~mask2] = ys_mine[~mask2]
    errs2[np.abs(errs2) < 1e-3] = 0.0
    '''
    plt.plot(xs_mine, ys_mine, label=card)
    #plt.plot(xs_mine_micromegas, ys_mine_micromegas, label='micromegas-'+card)
    plt.plot(xs_mine_micromegas1, ys_mine_micromegas1, label='micromegas-JS-'+card)
    #plt.plot(xs_mine_micromegas, errs, label=card+'-mycode_vs_mymicro')
    #plt.plot(xs_mine_micromegas1, errs1, label=card+'-mycode_vs_JS')
    #plt.plot(xs_mine_micromegas1, errs2, label=card+'-mymicro_vs_JS')
    files = sorted([name for name in os.listdir(f"./output/{card}/") if "P" in name])
    for file in []:
        if 'n1n1_nu1nu1' in file: 
            xs_mine, ys_mine = np.loadtxt(f"./output/{card}/{file}",unpack=True)
            plt.plot(xs_mine, ys_mine, label=file)

#xs, ys = np.loadtxt('./dA.txt',unpack=True)
#plt.plot(xs,ys, label='dA')
 
plt.legend()
plt.xscale("log")
plt.yscale("log")
#plt.xlim(0,15)
plt.ylim(1e-27,1e-14)
plt.xlabel("m1/T")
plt.ylabel("rel_err")
#plt.savefig("./rel_err-mymicro_JSmicro.png")
plt.show()
