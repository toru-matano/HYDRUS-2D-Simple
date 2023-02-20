# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 00:02:48 2023

@author: toru1
"""
import os
import numpy as np
import matplotlib.pyplot as plt

class GetLines:
    def __init__(self):
        self.FileName = None
        self.CASENAME = None
        self.header = None
        self.unit = None
        self.data = None
        self.lines = None
        self.skiplines = 0
        self.HeaderLine = 0
        self.UnitLine = 0
        self.DataLine = 0

    def fopen(self):
        self.unit_L = 'cm'
        self.unit_T = 'day'
        self.unit_M = 'g'
        self.unit_V = 'cm2'
        self.path = os.path.join('.', self.CASENAME, self.FileName)

        with open(self.path) as f:
            lines = f.read().split("\n")
        self.lines = lines[self.skiplines:]
    
    def readHeader(self):
        self.header = self.lines[self.HeaderLine].split()
        unit = self.lines[self.UnitLine].split()
        self.unit = [s.replace('L', self.unit_L)
                     .replace('T', self.unit_T)
                     .replace('M', self.unit_M) for s in unit]

    def readData(self):
        self.data = np.array([line.split() for line in self.lines[self.DataLine:-2]], dtype=float)
        self.time =  self.data[:, 0]
    
    def plot(self, j, timemax=None, ax=None, label=None):
        if ax==None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.plot(self.time, self.data[:, j], label=label)
        try:
            ax.set_ylabel(self.header[j]+' '+self.unit[j])
        except:
            ax.set_ylabel(self.header[j])
        try:
            ax.set_xlabel(self.header[0]+' '+self.unit[0])
        except:
            ax.set_xlabel(self.header[0])
        if timemax == None:
            timemax = self.time.max()
        ax.set_xlim(0, timemax)
        if label != None:
            ax.legend()
        return ax

    def GetData(self, j):
        return self.data[:, j]

def C_flux(time, J, C):
    nominator = np.trapz(J*C, x=time)
    denominator = np.trapz(J, x=time)
    c_flux = nominator / denominator
    return c_flux, nominator


def SeasonBoxPlot(data1, data2, time, title, ticklabel):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    ax.boxplot([data1, data2])
    ax.set_xticks(range(1, 3), ticklabel)
    ax.set_title(title)
    
