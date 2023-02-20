# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 22:21:43 2023

@author: toru1
"""

import numpy as np
import matplotlib.pyplot as plt
from utils_Hydrus import GetLines

class v_Mean(GetLines):
    def __init__(self, CASENAME):
        self.CASENAME = CASENAME
        self.FileName = 'v_Mean.out'
        self.HeaderLine = 0
        self.UnitLine = 1
        self.DataLine = 3
        self.skiplines = 10
        self.fopen()
        self.readHeader()
        self.readData()

class h_Mean(GetLines):
    def __init__(self, CASENAME):
        self.CASENAME = CASENAME
        self.FileName = 'h_Mean.out'
        self.HeaderLine = 0
        self.UnitLine = 1
        self.DataLine = 3
        self.skiplines = 3
        self.fopen()

        self.readHeader()
        self.readData()


class Cum_Q(GetLines):
    def __init__(self, CASENAME):
        self.FileName = 'Cum_Q.out'
        self.CASENAME = CASENAME
        self.HeaderLine = 0
        self.UnitLine = 1
        self.DataLine = 3
        self.skiplines = 10
        self.fopen()

        self.readHeader()
        self.readData()

class solute1(GetLines):
    def __init__(self, CASENAME):
        self.FileName = 'solute1.out'
        self.CASENAME = CASENAME
        self.HeaderLine = 0
        self.UnitLine = 1
        self.DataLine = 3
        self.skiplines = 2
        self.fopen()

        self.readData()
        self.header = range(22)
        self.unit = ['[M/L]']*22

class A_Level(GetLines):
    def __init__(self, CASENAME):
        self.FileName = 'A_Level.out'
        self.CASENAME = CASENAME
        self.HeaderLine = 0
        self.UnitLine = 1
        self.DataLine = 3
        self.skiplines = 2
        self.fopen()

        self.readHeader()
        self.readData()
        
class Boundary(GetLines):
    def __init__(self, CASENAME, nnode, nPrintTime):
        self.FileName = 'Boundary.out'
        self.CASENAME = CASENAME
        self.HeaderLine = 4
        self.UnitLine = 5
        self.skiplines = 13
        self.fopen()

        self.readHeader()

        nskip = 7
        self.nnode = nnode
        self.nPrintTime = nPrintTime
        self.nrows = self.nnode+nskip
        self.data = np.array([
                    [line.split() for line in self.lines[nskip+n*self.nrows:(n+1)*self.nrows]]
                    for n in range(self.nPrintTime)],
                dtype=float)
        self.time = np.array([self.lines[2+n*self.nrows].split()[1]
                              for n in range(self.nPrintTime)], dtype=float)
        self.depth = self.data[0, :, 1]
        
    def GetData(self, j):
        return self.data[:, :, j].T
    
    def plot(self, j, ax=None, depthmin=None, step=1):
        if ax==None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        for i in range(0, self.nPrintTime, step):
                ax.plot(self.data[i, :, j], self.depth,
                        label='{:6d} day'.format(int(self.time[i])))
        ax.set_ylabel(self.header[1]+self.unit[0])
        try:
            ax.set_xlabel(self.header[j]+self.unit[j-1]) 
        except:
            ax.set_xlabel(self.header[j])
        if depthmin == None:
            depthmin = -self.nnode
        ax.set_ylim(depthmin, 0)
        ax.legend(bbox_to_anchor=[1, 1])
        return ax


class ObsNod(GetLines):
    def __init__(self, CASENAME):
        self.FileName = 'ObsNod.out'
        self.CASENAME = CASENAME
        self.HeaderLine = 2
        self.DataLine = 3
        self.skiplines = 3
        self.fopen()

        nValues = 5
        data = np.array([line.split() for line in self.lines[self.DataLine:-2]],
                        dtype=float)
        self.data = np.split(data, list(range(1, data[0].size, nValues)), axis=1)
        self.time = self.data[0][:, 0]
        self.nNode = self.lines[0].replace('(', ' ').replace(')', ' ').split()
        self.header = self.lines[self.HeaderLine].split()[:nValues+1]
        
    def GetData(self, j):
        data = [d[:, j] for d in self.data[1:]]
        return data

    def plot(self, j, i, label, timemax=None, ax=None):
        if ax==None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.plot(self.time, self.data[i+1][:, j], label=label)
        ax.set_ylabel(self.header[j+1])
        ax.set_xlabel(self.header[0]+' '+self.unit_T)
        if timemax == None:
            timemax = self.time.max()
        ax.set_xlim(0, timemax)
        ax.legend()
        return ax
        
class Run_Info(GetLines):
    def __init__(self, CASENAME):
        self.FileName = 'Run_Info.out'
        self.CASENAME = CASENAME
        self.skiplines = 2
        self.HeaderLine = 0
        self.DataLine = 2
        self.fopen()

        self.header = self.lines[self.HeaderLine].split()
        self.readData()
        
class Balance(GetLines):
    def __init__(self, CASENAME, nPrintTime):
        self.FileName = 'Balance.out'
        self.CASENAME = CASENAME
        self.skiplines = 7
        self.fopen()


        nskip = 7
        self.nnode = 13
        self.nPrintTime = nPrintTime
        self.nrows = self.nnode+nskip
        while True:
            try:
                data =[[[line[:9], line[9:16], line[19:32]] 
                        for line in self.lines[nskip+n*self.nrows:(n+1)*self.nrows]]
                       for n in range(3, self.nPrintTime)]
                self.data = np.array([[d[2] for d in ds] for ds in data], dtype=float)
                break
            except:
                del self.lines[0]
                self.skiplines += 1
        
        self.header = [d[0] for d in data[0]]
        unit = [d[1] for d in data[0]]
        self.unit = [s.replace('L', self.unit_L)
                     .replace('T', self.unit_T)
                     .replace('M', self.unit_M)
                     .replace('V', self.unit_V) for s in unit]
        self.time = np.array([self.lines[3+n*self.nrows].split()[2]
                              for n in range(3, self.nPrintTime)], dtype=float)
        
    def GetData(self, j):
        return self.data[:, j].T
    
    def plot(self, j, ax=None):
        if ax==None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.plot(self.time, self.data[:, j])
        ax.set_xlabel('time '+self.unit_T)
        try:
            ax.set_ylabel(self.header[j]+self.unit[j]) 
        except:
            ax.set_ylabel(self.header[j])
        ax.legend()
        return ax
