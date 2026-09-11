# ---------------------------------------------------------------------- 
# This model file was automatically created by SARAH version4.15.3
# SARAH References: arXiv:0806.0538, arXiv:0909.2863, arXiv:1002.0840   
# (c) Florian Staub, Mark Goodsell, Werner Porod and Martin Gabelmann 2023 
# ---------------------------------------------------------------------- 
# File created at 12:58 on 2.9.2024  
# ---------------------------------------------------------------------- 


from __future__ import division
from object_library import all_particles,Particle
import parameters as Param


N1 = Particle(pdg_code =1012,
    name = 'N1' ,
    antiname = 'N1' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.MN1 ,
    width = Param.WN1 ,
    line = 'swavy' ,
    charge = 0 ,
    texname = '{N}_1' ,
    antitexname = '{N}_1' )

N2 = Particle(pdg_code =1014,
    name = 'N2' ,
    antiname = 'N2' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.MN2 ,
    width = Param.WN2 ,
    line = 'swavy' ,
    charge = 0 ,
    texname = '{N}_2' ,
    antitexname = '{N}_2' )

N3 = Particle(pdg_code =1016,
    name = 'N3' ,
    antiname = 'N3' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.MN3 ,
    width = Param.WN3 ,
    line = 'swavy' ,
    charge = 0 ,
    texname = '{N}_3' ,
    antitexname = '{N}_3' )

nu1 = Particle(pdg_code =12,
    name = 'nu1' ,
    antiname = 'nu1' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = 0 ,
    texname = '{\\nu}_1' ,
    antitexname = '{\\nu}_1' )

nu2 = Particle(pdg_code =14,
    name = 'nu2' ,
    antiname = 'nu2' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = 0 ,
    texname = '{\\nu}_2' ,
    antitexname = '{\\nu}_2' )

nu3 = Particle(pdg_code =16,
    name = 'nu3' ,
    antiname = 'nu3' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = 0 ,
    texname = '{\\nu}_3' ,
    antitexname = '{\\nu}_3' )

d1 = Particle(pdg_code =1,
    name = 'd1' ,
    antiname = 'd1bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Md1 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1/3 ,
    texname = '{d}_1' ,
    antitexname = '{\\bar{d}}_1' )

d1bar = d1.anti()


d2 = Particle(pdg_code =3,
    name = 'd2' ,
    antiname = 'd2bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Md2 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1/3 ,
    texname = '{d}_2' ,
    antitexname = '{\\bar{d}}_2' )

d2bar = d2.anti()


d3 = Particle(pdg_code =5,
    name = 'd3' ,
    antiname = 'd3bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Md3 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1/3 ,
    texname = '{d}_3' ,
    antitexname = '{\\bar{d}}_3' )

d3bar = d3.anti()


u1 = Particle(pdg_code =2,
    name = 'u1' ,
    antiname = 'u1bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Mu1 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = 2/3 ,
    texname = '{u}_1' ,
    antitexname = '{\\bar{u}}_1' )

u1bar = u1.anti()


u2 = Particle(pdg_code =4,
    name = 'u2' ,
    antiname = 'u2bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Mu2 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = 2/3 ,
    texname = '{u}_2' ,
    antitexname = '{\\bar{u}}_2' )

u2bar = u2.anti()


u3 = Particle(pdg_code =6,
    name = 'u3' ,
    antiname = 'u3bar' ,
    spin = 2 ,
    color = 3 ,
    mass = Param.Mu3 ,
    width = Param.Wu3 ,
    line = 'straight' ,
    charge = 2/3 ,
    texname = '{u}_3' ,
    antitexname = '{\\bar{u}}_3' )

u3bar = u3.anti()


e1 = Particle(pdg_code =11,
    name = 'e1' ,
    antiname = 'e1bar' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.Me1 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1 ,
    texname = '{e}_1' ,
    antitexname = '{\\bar{e}}_1' )

e1bar = e1.anti()


e2 = Particle(pdg_code =13,
    name = 'e2' ,
    antiname = 'e2bar' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.Me2 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1 ,
    texname = '{e}_2' ,
    antitexname = '{\\bar{e}}_2' )

e2bar = e2.anti()


e3 = Particle(pdg_code =15,
    name = 'e3' ,
    antiname = 'e3bar' ,
    spin = 2 ,
    color = 1 ,
    mass = Param.Me3 ,
    width = Param.ZERO ,
    line = 'straight' ,
    charge = -1 ,
    texname = '{e}_3' ,
    antitexname = '{\\bar{e}}_3' )

e3bar = e3.anti()


Hp = Particle(pdg_code =999900,
    name = 'Hp' ,
    antiname = 'Hpc' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.MHp ,
    width = Param.ZERO,
    goldstone = True ,
    line = 'dashed' ,
    charge = -1 ,
    texname = 'H^+' ,
    antitexname = 'H^-' )

Hpc = Hp.anti()


etp = Particle(pdg_code =1003,
    name = 'etp' ,
    antiname = 'etpc' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.Metp ,
    width = Param.ZERO ,
    line = 'dashed' ,
    charge = 1 ,
    texname = '\\eta^+' ,
    antitexname = '{\\eta^+}^*' )

etpc = etp.anti()


Ah = Particle(pdg_code =999901,
    name = 'Ah' ,
    antiname = 'Ah' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.MAh ,
    width = Param.ZERO,
    goldstone = True ,
    line = 'dashed' ,
    charge = 0 ,
    texname = 'A^0' ,
    antitexname = 'A^0' )

h = Particle(pdg_code =25,
    name = 'h' ,
    antiname = 'h' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.Mh ,
    width = Param.Wh ,
    line = 'dashed' ,
    charge = 0 ,
    texname = 'h' ,
    antitexname = 'h' )

etI = Particle(pdg_code =1002,
    name = 'etI' ,
    antiname = 'etI' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.MetI ,
    width = Param.WetI ,
    line = 'dashed' ,
    charge = 0 ,
    texname = '\\eta_I' ,
    antitexname = '\\eta_I' )

etR = Particle(pdg_code =1001,
    name = 'etR' ,
    antiname = 'etR' ,
    spin = 1 ,
    color = 1 ,
    mass = Param.MetR ,
    width = Param.WetR ,
    line = 'dashed' ,
    charge = 0 ,
    texname = '\\eta_R' ,
    antitexname = '\\eta_R' )

g = Particle(pdg_code =21,
    name = 'g' ,
    antiname = 'g' ,
    spin = 3 ,
    color = 8 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    line = 'wavy' ,
    charge = 0 ,
    texname = 'g' ,
    antitexname = 'g' )

A = Particle(pdg_code =22,
    name = 'A' ,
    antiname = 'A' ,
    spin = 3 ,
    color = 1 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    line = 'wavy' ,
    charge = 0 ,
    texname = '\\gamma' ,
    antitexname = '\\gamma' )

Z = Particle(pdg_code =23,
    name = 'Z' ,
    antiname = 'Z' ,
    spin = 3 ,
    color = 1 ,
    mass = Param.MZ ,
    width = Param.WZ ,
    line = 'wavy' ,
    charge = 0 ,
    texname = 'Z' ,
    antitexname = 'Z' )

Wp = Particle(pdg_code =24,
    name = 'Wp' ,
    antiname = 'Wpc' ,
    spin = 3 ,
    color = 1 ,
    mass = Param.MWp ,
    width = Param.WWp ,
    line = 'wavy' ,
    charge = 1 ,
    texname = 'W^+' ,
    antitexname = 'W^-' )

Wpc = Wp.anti()


gG = Particle(pdg_code =999902,
    name = 'gG' ,
    antiname = 'gGc' ,
    spin = -1 ,
    color = 8 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    propagating = False,
    line = 'dotted' ,
    charge = 0 ,
    texname = '\\eta^G' ,
    antitexname = '\\bar{\\eta^G}' )

gGc = gG.anti()


gA = Particle(pdg_code =999903,
    name = 'gA' ,
    antiname = 'gAc' ,
    spin = -1 ,
    color = 1 ,
    mass = Param.ZERO ,
    width = Param.ZERO ,
    propagating = False,
    line = 'dotted' ,
    charge = 0 ,
    texname = '\\eta^{\\gamma}' ,
    antitexname = '\\bar{\\eta^{\\gamma}}' )

gAc = gA.anti()


gZ = Particle(pdg_code =999904,
    name = 'gZ' ,
    antiname = 'gZc' ,
    spin = -1 ,
    color = 1 ,
    mass = Param.MgZ ,
    width = Param.WZ ,
    propagating = False,
    line = 'dotted' ,
    charge = 0 ,
    texname = '\\eta^Z' ,
    antitexname = '\\bar{\\eta^Z}' )

gZc = gZ.anti()


gWp = Particle(pdg_code =999905,
    name = 'gWp' ,
    antiname = 'gWpc' ,
    spin = -1 ,
    color = 1 ,
    mass = Param.MgWp ,
    width = Param.WWp ,
    propagating = False,
    line = 'dotted' ,
    charge = 1 ,
    texname = '\\eta^+' ,
    antitexname = '\\bar{\\eta^+}' )

gWpc = gWp.anti()


gWC = Particle(pdg_code =999906,
    name = 'gWC' ,
    antiname = 'gWCc' ,
    spin = -1 ,
    color = 1 ,
    mass = Param.MgWC ,
    width = Param.WWp ,
    propagating = False,
    line = 'dotted' ,
    charge = -1 ,
    texname = '\\eta^-' ,
    antitexname = '\\bar{\\eta^-}' )

gWCc = gWC.anti()


