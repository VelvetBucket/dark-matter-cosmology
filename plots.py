import numpy as np
import matplotlib.pyplot as plt
import os

cards = sorted([name.replace('.dat','') for name in os.listdir("./cards")])
nparticles = ''
for card in ['35_75-1', '35_75-4', '35_75-4v2']:
    
    if nparticles in ['0', '', 'All', 'all']:
        nparticles = 'All'
    else:
        card = card + '-' + nparticles
    xs_mine, ys_mine = np.loadtxt("./output/"+card+"/TOTALS_T.dat", unpack=True)
    order = np.argsort(xs_mine)
    xs_mine = xs_mine[order]
    ys_mine = ys_mine[order]
    mine_code_func = lambda x: np.interp(x, xs_mine, ys_mine)
    
    xs_mine_micromegas, ys_mine_micromegas = np.loadtxt("./output/"+card+"/TOTALS_n1.dat", unpack=True)
    order = np.argsort( xs_mine_micromegas)
    xs_mine_micromegas = xs_mine_micromegas[order]
    ys_mine_micromegas = ys_mine_micromegas[order]
    mine_micro_func = lambda x: np.interp(x, xs_mine_micromegas, ys_mine_micromegas)
    
    xs_mine_micromegas_fast, ys_mine_micromegas_fast = np.loadtxt("./micromegas_output/m1T-1_vs_sigmaV/"+card+".dat", unpack=True)
    order = np.argsort( xs_mine_micromegas_fast)
    xs_mine_micromegas_fast = xs_mine_micromegas_fast[order]
    ys_mine_micromegas_fast = ys_mine_micromegas_fast[order]
    mine_micro_func_fast = lambda x: np.interp(x, xs_mine_micromegas_fast, ys_mine_micromegas_fast)
    
    all_xs = [xs_mine,xs_mine_micromegas,xs_mine_micromegas_fast]
    xs = np.logspace(np.log10(np.max([np.min(x) for x in all_xs])), np.log10(np.min([np.max(x) for x in all_xs])), 50, base=10.0)
    #xs = np.logspace(0,3, 50, base=10.0)
    ys_mycode = mine_code_func(xs)
    ys_mymicro = mine_micro_func(xs)
    ys_mymicro_fast = mine_micro_func_fast(xs)
    
    errs_mycode_mymicro = np.zeros_like(xs)
    mask = (ys_mycode > 0.0) & (ys_mymicro > 0.0)
    errs_mycode_mymicro[mask] = np.abs(1.0 - ys_mycode[mask]/ys_mymicro[mask])
    errs_mycode_mymicro[~mask] = ys_mycode[~mask] + ys_mymicro[~mask]
    
    #plt.plot(xs, errs_mycode_mymicro, label=card)#, alpha=0.8)
    plt.plot(xs, ys_mycode, label=card+"",linestyle=':', alpha=0.8)
    plt.plot(xs, ys_mymicro, label=card+" n1",linestyle='-.', alpha=0.8)
    plt.plot(xs, ys_mymicro_fast, label=card+" micro-fast",linestyle='--', alpha=0.8)
    
    plt.legend()
    plt.xscale("log")
    plt.yscale("log")
    #plt.ylim(bottom=1e-42,top=1e+0)
    plt.xlabel("x")
    plt.ylabel("sigma*v")
    plt.savefig(f"./sigmav_vs_x-{card}.png")
    plt.show()
    plt.close()
