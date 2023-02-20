# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 10:45:44 2023

@author: toru1
"""
import utils_Hydrus1D as Hydrus1D
import utils_Hydrus2D as Hydrus2D
import utils_Hydrus
import matplotlib.pyplot as plt
# %% 2
CASENAME = '../Final_loam_Spring'

Data = Hydrus1D.Nod_Inf(CASENAME)
print(Data.nnode)
#for j, h in enumerate(Data.header):
#    if j >=2:
#        ax = Data.plot(j, step=10, depthmin=-100)
#        ax.set_xscale('log')
#for j, h in enumerate(Data.header):
j=5
Data.heatmap(j, Data.header[j], vmin=0, vmax=.01)

# %% 3
CASE1 = '../Final_loam_Spring'
CASE2 = '../Final_2D_2'
CASE3 = '../Final_loam_Autumn'
Data1 = Hydrus1D.Obs_Node(CASE1)
Data2 = Hydrus2D.ObsNod(CASE2)
Data3 = Hydrus1D.Obs_Node(CASE3)

ax=Data3.plot(3, 2, label='1D Autumn')
ax=Data2.plot(3, 1, label='2D', ax=ax)
ax=Data1.plot(3, 2, label='1D', ax=ax)

ax.set_title('Depth -100cm')

# %% 3
CASENAME = '../Final_loam_Spring'
#CASENAME = '../Final_2D_2'
#Data = Hydrus2D.ObsNod(CASENAME)
Data = Hydrus1D.Obs_Node(CASENAME)
time = Data.time
for j, h in enumerate(Data.header[1:]):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        for i in range(1, len(Data.nNode)//2):
            ax=Data.plot(j, i, ax=ax)
#        ax = Data.plot(j, ['50cm', '100cm', '150cm', '200cm', '250cm', '300cm', '400cm'])
#        ax.set_xlim(1095, 1460)
# %% 4
CASENAME = '../Final_sandy_Spring'
Data = Hydrus1D.Obs_Node(CASENAME)

for node in range(7):
    flux = Data.GetData(2)[node]
    conc = Data.GetData(3)[node]

    c_flux, mass = utils_Hydrus.C_flux(Data.time, flux, conc)
    print('node:\t{}\tflux:\t{:.3e}\t[{M}/{T}]\tmass:\t{:.3e}\t[{M}/{L}.{T}]'
          .format(Data.nNode[node*2+1], c_flux*10**6, mass,
                  M=Data.unit_M, L=Data.unit_L, T=Data.unit_T))

# %% 5
CASE1 = '../Final_sandy_Spring'
CASE2 = '../Final_loam_Spring'

Data1 = Hydrus1D.T_Level(CASE1)
Data2 = Hydrus1D.T_Level(CASE2)

for j, h in enumerate(Data1.header):
    if j != 0:
        ax = Data1.plot(j, label='sandy loam')
        ax = Data2.plot(j, ax=ax, label='loam')
#        ax.set_xlim(1095, 1460)
#        utils_Hydrus.SeasonBoxPlot(Data1.GetData(j), Data2.GetData(j), Data1.time,
#                               h+Data1.unit[j], ['Sandy Loam', 'Loam'])
        ax.set_xlim(1095, 1460)
        
ax = Data2.plot(8, label='vTop')
ax = Data2.plot(9, label='vRoot', ax=ax)
ax = Data2.plot(10, label='vBot', ax=ax)
#%%
#ax = Data2.plot(2, label='potential')
#ax = Data2.plot(4, label='actual', ax=ax)
#ax = Data2.plot(5, label='bottom flux', ax=ax)
#ax.set_xlim(1095, 1460)

CASENAME = '../Final_sandy_Spring'
Data = Hydrus1D.Nod_Inf(CASENAME)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
for i in range(150):
    ax = Data.plot(10, i, ax=ax)
    
data1 = Data.GetData(3)     #moisture
data2 = Data.GetData(4)     #K
Data.heatmap(3, 'mositure')
Data.heatmap(4, 'k')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
for i in range(10):
#    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    ax.scatter(data1[i], data2[i], label=str(i*10950//150)+'[day]')
#%% 6
CASE1 = '../Final_sandy_Spring'
CASE2 = '../Final_loam_Spring'

Data1 = Hydrus1D.solute1(CASE1)
Data2 = Hydrus1D.solute1(CASE2)
for j, h in enumerate(Data1.header):
    if 0 < j < 17:
        ax = Data1.plot(j, label='sandy loam')
        ax = Data2.plot(j, ax=ax, label='loam')
ax = Data1.plot(3, label=Data1.header[3])
ax = Data1.plot(4, ax=ax, label=Data1.header[4])
ax = Data1.plot(11, ax=ax, label=Data1.header[11])
ax.set_ylabel('[g/cm2]')

#    utils_Hydrus.SeasonBoxPlot(Data1.GetData(j), Data2.GetData(j), Data1.time,
#                               h, ['Sandy Loam', 'Loam'])


#Data1 = Hydrus1D.ATMOSPH(CASE1)

# %%
CASE1 = '../Final_sandy_Spring'
CASE2 = '../Final_sandy_Autmn'
Data1 = Hydrus1D.Balance(CASE1)
Data2 = Hydrus1D.Balance(CASE2)

for j, h in enumerate(Data1.header):  
     ax = Data1.plot(j)
     Data2.plot(j, ax=ax)
# %%
CASE1 = '../Final_loam_spring'
CASE3 = '../Final_2D_2'

Data1 = Hydrus1D.T_Level(CASE1)
Data3 = Hydrus2D.Cum_Q(CASE3)
Data3.data[:, 1:] /= 2000
for j in range(1, 5):
    ax = Data3.plot(j, label='2D')
    Data1.plot(j+5, label='1D', ax=ax)
#    utils_Hydrus.SeasonBoxPlot(Data1.GetData(j+5), Data3.GetData(j), Data1.time,
#                               Data1.header[j+5], ['1D', '2D'])

CASE1 = '../Final_2D_noflux'
CASE3 = '../Final_2D_2'

Data1 = Hydrus1D.solute1(CASE1)
Data3 = Hydrus2D.solute1(CASE3)
#for j, h in enumerate(Data1.header):
Data3.data[:, 1:] /= 2000
ax = Data3.plot(3, label='2D')
Data1.plot(11, ax=ax, label='1D')

# %%
Data3 = Hydrus2D.Balance(CASE3, 30*12)
for j, h in enumerate(Data3.header):  
     Data3.plot(j)

# %%
Data3 = Hydrus2D.Cum_Q(CASE3)
for j, h in enumerate(Data3.header):
    Data3.plot(j)