# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:06:25 2023

@author: toru1
"""
import numpy as np
import pandas as pd

class HYDRUS2DSIMPLE_INIT:
    def __init__(self):
        # %%1 new project
        self.Heading = 'Welcome to HYDRUS'
        self.path = 'test'

        # %%2 Domain Type and Units
        self.Kat = 2         # 0:horizontal plane, 1:axisymmetric vertical flow, 2:vertical plane
        self.LUnit = 'cm'

        # %%3 rectangular domain definition
        self.min_x = 0
        self.min_z = 0
        self.max_x = 1000
        self.max_z = 200
        self.Angle = 0       # Angle in degrees between K1 and the x-coordinate axis

        # %%4 Main processes and add-on modules
        self.lWat = True          # transient water flow is considered.

        self.lChem = False         # solute transport is to be considered
        self.lEquil = True        # equilibrium solute transport is considered.
        self.lUnsatCh = False      # the major ion chemistry module (Unsatchem) is to be used to simulate solute transport
        self.lCFSTr = False        # colloid-facilitated solute transport module (C-Ride) is to be used
        self.lHP2 = False          # the general biogeochemical solute transport module is used to solute transport

        self.lTemp = False         # heat transport is to be considered.

        self.lSink = False         # water extraction by roots from the root zone is imposed.
        self.lRootGr = False       # the root growth is to be simulated

        self.lInv = False          # the soil hydraulic or solute transport parameters are to be estimated from measured data

        self.lExtGen = False       # an external mesh generator is to be used to generate the finite element mesh (i.e., when using MESHGEN-2D).

        # %%5 time information
        self.TUnit = 'days'
        self.tInit = 0           # Initial time of the simulation
        self.tMax = 1        # Final time of the simulation             
        self.dt = 0.0001         # Initial time increment
        self.dtMin = 1e-005      # Minimum permitted time increment
        self.dtMax  = 5        # Maximum permitted time increment
        self.AtmIn = False         # atmospheric boundary conditions are supplied
        self.MaxAL = 0       # Number of atmospheric data records.
        self.BC_Cycles = 1       # Number of times, the set of atmospheric data records is to be repeated

        # %%6 Output information
        self.Short = False         # information is to be printed only at preselected times,
        self.PrintStep = 1       # timestep of information to the screen and output files

        self.Inter = False         # information about the pressure heads, water contents, temperatures, and concentrations in observation nodes, and the water and solute fluxes is to be printed at a constant time interval tPrintInterval.
        self.PrintInterval = 1   # timestep of information about the pressure heads, water contents, temperatures, and concentrations in observation nodes, and the water and solute fluxes
        self.lScrn = True         # information is to be printed on the screen
        self.lEnter = False        # Enter key is to be pressed at the end of simulation
        self.NLay = 1            # Number of subregions for which separate water balances are being computed.

        self.MPL = 1           # Number of specified print-times
        self.TPrint = np.linspace(0, self.tMax, self.MPL+1, dtype=int)


        # %%7 iteration criteria
        self.MaxIt =10           # Maximum number of iterations
        self.TolTh = 0.001      # Absolute water content tolerance for nodes in the unsaturated part of the flowregion
        self.TolH = 1            # Absolute pressure head tolerance for nodes in the saturated part of the flow region [L]
        self.ItMin = 3           # lower optimal iteration range
        self.ItMax = 7           # upper optimal iteration range
        self.DMul = 1.3          # multiplier of next time step
        self.DMul2 = 0.7         # multiplier of next time step
        self.hTab1= 0.0001       # lower limit of the tension interval [cm]
        self.hTabN = 10000       # upper limit of the tension interval [cm]
        self.InitH_W = False       # condition is specified in terms of (true:) the pressure head or (flase:) the water content.

        # %%7 recutangular domain discretization
        self.nnode_x = 11
        self.nnode_z = 11
        self.Dim_z = {
                #length: [z_min, z_max]
                20: [0, 200],
                  }
        self.Dim_x = {
                #length: [z_min, z_max]
                100: [0, 1000],
                  }

        self.node_x = []
        for length in self.Dim_x:
            self.node_x.extend(range(self.Dim_x[length][0], self.Dim_x[length][1], length))
        self.node_x.append(self.Dim_x[length][1])

        self.node_z = []
        for length in self.Dim_z:
            self.node_z.extend(range(self.Dim_z[length][0], self.Dim_z[length][1], length))
        self.node_z.append(self.Dim_z[length][1])
        self.NumNP = len(self.node_x)*len(self.node_z)             # Maximum number of nodes in finite element mesh
        self.NumEl = (len(self.node_x)-1)*(len(self.node_z)-1)*2   # Maximum number of elements in finite element mesh
        self.NSurf = len(self.node_x) - 1

        # %%8 soil Hydraulic model
        self.Model = 0           # Soil hydraulic properties model
        #= 0; van Genuchten
        #= 1; modified van Genuchten's model
        #= 2; Brooks and Corey
        #= 3; van Genuchten's model with air-entry value of -2 cm and with six parameters.
        #= 4; Kosugi
        #= 5; dual porosity model of Durner
        #= 6; dual-porosity system with transfer proportional to the effective saturation
        #= 7; dual-porosity system with transfer proportional to the pressure head
        #= 9; look-up tables of soil hydraulic properties
        self.Hysteresis = 0      # Hysteresis in the soil hydraulic properties:

        # = 0; No hysteresis
        # = 1; Hysteresis in the retention curve only
        # = 2; Hysteresis in both the retention and hydraulic conductivity functions
        # = 3; Hysteresis using Bob Lenhard’s model
        if self.Hysteresis != 0:
            self.iKappa = -1 #if the initial condition is to be calculated from the main drying branch (=-1), or from the main wetting branch(=1).
            
        # %%9 Pedotransfer functions

        # %%10 water flow parameters
        self.NMat = 1            # Number of soil materials

        self.soil_Header = {
                '0': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l'],
                '1': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l', 'Qm', 'Qa', 'Qk', 'Kk'],
                '2': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l'],
                '3': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l'],
                '4': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l'],
                '5': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l', 'w2', 'α2', 'n2'],
                '6': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l', 'QrIm', 'QsIm', 'ω'],
                '7': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l', 'QrIm', 'QsIm', 'αIm', 'nIm', 'ω'],
                '8': ['Name', 'Qr', 'Qs', 'α', 'n', 'Ks', 'l', 'Qm', 'QsW', 'αW', 'KsW'],
        }
        
        self.soil_catalog = { 
            '0': {
                'Sand':            ['Sand',            0.045, 0.43, 0.145, 2.68, 712.8, 0.5],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.124, 2.28, 350.2, 0.5],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.075, 1.89, 106.1, 0.5],
                'Loam':            ['Loam',            0.078, 0.43, 0.036, 1.56, 24.96, 0.5],
                'Silt':            ['Silt',            0.034, 0.46, 0.016, 1.37, 6.000, 0.5],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.020, 1.41, 10.80, 0.5],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.059, 1.48, 31.44, 0.5],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.019, 1.31, 6.240, 0.5],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.010, 1.23, 1.680, 0.5],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.027, 1.23, 2.880, 0.5],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.005, 1.09, 0.480, 0.5],
                'Clay':            ['Clay',            0.068, 0.38, 0.008, 1.09, 4.800, 0.5],
            },
            '1': {
                'Sand':            ['Sand',            0.045, 0.43, 0.145, 2.68, 712.8, 0.5, 0.43, 0.045, 0.43, 712.8],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.124, 2.28, 350.2, 0.5, 0.41, 0.057, 0.41, 350.2],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.075, 1.89, 106.1, 0.5, 0.41, 0.065, 0.41, 106.1],
                'Loam':            ['Loam',            0.078, 0.43, 0.036, 1.56, 24.96, 0.5, 0.43, 0.078, 0.43, 24.96],
                'Silt':            ['Silt',            0.034, 0.46, 0.016, 1.37, 6.000, 0.5, 0.46, 0.034, 0.46, 6.000],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.020, 1.41, 10.80, 0.5, 0.45, 0.067, 0.45, 10.80],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.059, 1.48, 31.44, 0.5, 0.39, 0.100, 0.39, 31.44],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.019, 1.31, 6.240, 0.5, 0.41, 0.095, 0.41, 6.240],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.010, 1.23, 1.680, 0.5, 0.43, 0.089, 0.43, 1.680],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.027, 1.23, 2.880, 0.5, 0.38, 0.100, 0.38, 2.880],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.005, 1.09, 0.480, 0.5, 0.36, 0.070, 0.36, 0.480],
                'Clay':            ['Clay',            0.068, 0.38, 0.008, 1.09, 4.800, 0.5, 0.38, 0.068, 0.38, 4.800],
            },
            '2': {
                'Sand':            ['Sand',            0.045, 0.43, 0.1, 0.2, 712.8, 0.5],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.1, 0.2, 350.2, 0.5],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.1, 0.2, 106.1, 0.5],
                'Loam':            ['Loam',            0.078, 0.43, 0.1, 0.2, 24.96, 0.5],
                'Silt':            ['Silt',            0.034, 0.46, 0.1, 0.2, 6.000, 0.5],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.1, 0.2, 10.80, 0.5],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.1, 0.2, 31.44, 0.5],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.1, 0.2, 6.240, 0.5],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.1, 0.2, 1.680, 0.5],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.1, 0.2, 2.880, 0.5],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.1, 0.2, 0.480, 0.5],
                'Clay':            ['Clay',            0.068, 0.38, 0.1, 0.2, 4.800, 0.5],
            },
            '3': {
                'Sand':            ['Sand',            0.045, 0.43, 0.03, 1.5, 712.8, 0.5],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.03, 1.5, 350.2, 0.5],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.03, 1.5, 106.1, 0.5],
                'Loam':            ['Loam',            0.078, 0.43, 0.03, 1.5, 24.96, 0.5],
                'Silt':            ['Silt',            0.034, 0.46, 0.03, 1.5, 6.000, 0.5],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.03, 1.5, 10.80, 0.5],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.03, 1.5, 31.44, 0.5],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.03, 1.5, 6.240, 0.5],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.03, 1.5, 1.680, 0.5],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.03, 1.5, 2.880, 0.5],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.03, 1.5, 0.480, 0.5],
                'Clay':            ['Clay',            0.068, 0.38, 0.03, 1.5, 4.800, 0.5],
            },
            '4': {
                'Sand':            ['Sand',            0.045, 0.43, 100, 1, 712.8, 0.5],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 100, 1, 350.2, 0.5],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 100, 1, 106.1, 0.5],
                'Loam':            ['Loam',            0.078, 0.43, 100, 1, 24.96, 0.5],
                'Silt':            ['Silt',            0.034, 0.46, 100, 1, 6.000, 0.5],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 100, 1, 10.80, 0.5],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 100, 1, 31.44, 0.5],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 100, 1, 6.240, 0.5],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 100, 1, 1.680, 0.5],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 100, 1, 2.880, 0.5],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 100, 1, 0.480, 0.5],
                'Clay':            ['Clay',            0.068, 0.38, 100, 1, 4.800, 0.5],
            },
            '5': {
                'Sand':            ['Sand',            0.045, 0.43, 0.03, 1.5, 712.8, 0.5, 0.5, 0.03],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.03, 1.5, 350.2, 0.5, 0.5, 0.03],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.03, 1.5, 106.1, 0.5, 0.5, 0.03],
                'Loam':            ['Loam',            0.078, 0.43, 0.03, 1.5, 24.96, 0.5, 0.5, 0.03],
                'Silt':            ['Silt',            0.034, 0.46, 0.03, 1.5, 6.000, 0.5, 0.5, 0.03],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.03, 1.5, 10.80, 0.5, 0.5, 0.03],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.03, 1.5, 31.44, 0.5, 0.5, 0.03],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.03, 1.5, 6.240, 0.5, 0.5, 0.03],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.03, 1.5, 1.680, 0.5, 0.5, 0.03],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.03, 1.5, 2.880, 0.5, 0.5, 0.03],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.03, 1.5, 0.480, 0.5, 0.5, 0.03],
                'Clay':            ['Clay',            0.068, 0.38, 0.03, 1.5, 4.800, 0.5, 0.5, 0.03],
            },
            '6': {
                'Sand':            ['Sand',            0.045, 0.43, 0.03, 1.5, 712.8, 0.5, 0, 0.1],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.03, 1.5, 350.2, 0.5, 0, 0.1],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.03, 1.5, 106.1, 0.5, 0, 0.1],
                'Loam':            ['Loam',            0.078, 0.43, 0.03, 1.5, 24.96, 0.5, 0, 0.1],
                'Silt':            ['Silt',            0.034, 0.46, 0.03, 1.5, 6.000, 0.5, 0, 0.1],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.03, 1.5, 10.80, 0.5, 0, 0.1],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.03, 1.5, 31.44, 0.5, 0, 0.1],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.03, 1.5, 6.240, 0.5, 0, 0.1],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.03, 1.5, 1.680, 0.5, 0, 0.1],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.03, 1.5, 2.880, 0.5, 0, 0.1],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.03, 1.5, 0.480, 0.5, 0, 0.1],
                'Clay':            ['Clay',            0.068, 0.38, 0.03, 1.5, 4.800, 0.5, 0, 0.1],
            },
            '7': {
                'Sand':            ['Sand',            0.045, 0.43, 0.03, 1.5, 712.8, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.03, 1.5, 350.2, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.03, 1.5, 106.1, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Loam':            ['Loam',            0.078, 0.43, 0.03, 1.5, 24.96, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Silt':            ['Silt',            0.034, 0.46, 0.03, 1.5, 6.000, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.03, 1.5, 10.80, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.03, 1.5, 31.44, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.03, 1.5, 6.240, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.03, 1.5, 1.680, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.03, 1.5, 2.880, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.03, 1.5, 0.480, 0.5, 0, 0.1, 0.0015, 1.5, 0],
                'Clay':            ['Clay',            0.068, 0.38, 0.03, 1.5, 4.800, 0.5, 0, 0.1, 0.0015, 1.5, 0],
            },
            '8': {
                'Sand':            ['Sand',            0.045, 0.43, 0.145, 2.68, 712.8, 0.5, 0.43, 0.43, 0.290, 712.8],
                'Loamy Sand':      ['Loamy Sand',      0.057, 0.41, 0.124, 2.28, 350.2, 0.5, 0.41, 0.41, 0.248, 350.2],
                'Sandy Loam':      ['Sandy Loam',      0.065, 0.41, 0.075, 1.89, 106.1, 0.5, 0.41, 0.41, 0.150, 106.1],
                'Loam':            ['Loam',            0.078, 0.43, 0.036, 1.56, 24.96, 0.5, 0.43, 0.43, 0.072, 24.96],
                'Silt':            ['Silt',            0.034, 0.46, 0.016, 1.37, 6.000, 0.5, 0.46, 0.46, 0.032, 6.000],
                'Silt Loam':       ['Silt Loam',       0.067, 0.45, 0.020, 1.41, 10.80, 0.5, 0.45, 0.45, 0.040, 10.80],
                'Sandy Clay Loam': ['Sandy Clay Loam', 0.100, 0.39, 0.059, 1.48, 31.44, 0.5, 0.39, 0.39, 0.118, 31.44],
                'Clay Loam':       ['Clay Loam',       0.095, 0.41, 0.019, 1.31, 6.240, 0.5, 0.41, 0.41, 0.038, 6.240],
                'Silty Clay Loam': ['Silty Clay Loam', 0.089, 0.43, 0.010, 1.23, 1.680, 0.5, 0.43, 0.43, 0.020, 1.680],
                'Sandy Clay':      ['Sandy Clay',      0.100, 0.38, 0.027, 1.23, 2.880, 0.5, 0.38, 0.38, 0.054, 2.880],
                'Silty Clay':      ['Silty Clay',      0.070, 0.36, 0.005, 1.09, 0.480, 0.5, 0.36, 0.36, 0.010, 0.480],
                'Clay':            ['Clay',            0.068, 0.38, 0.008, 1.09, 4.800, 0.5, 0.38, 0.38, 0.016, 4.800],
            },
        }

        self.materials = [self.soil_catalog[str(self.Model)]['Loam'] for _ in range(self.NMat)]
        if self.Hysteresis != 0:
            [self.soil_catalog['8']['Loam'] for _ in range(self.NMat)]
        self.lWTDep = False        # hydraulic properties are to be considered as temperature dependent

        # %%1 Solute transport
        self.Epsi = 0.5      # =0.0 for an explicit scheme., =0.5 for a Crank-Nicholson implicit scheme., =1.0 for a fully implicit scheme.
        self.lUpW = False      # (t:) upstream weighing or (f:) Galerkin formulation is to be used.
        self.lArtD  = False    # artificial dispersion is to be added

        self.NS = 1          # Number of solutes in a chain reaction
        if self.lChem: self.NS = 1
        self.tPulse = 1      # Pulse duration [day]
        self.MUnit = 'mmol'
        self.PeCr = 2        # Stability criteria (0 when lUpW = t
        if self.lUpW:
            self.PeCr = 0
        self.lTDep = False     # transport or reaction coefficient (ChPar) is temperature dependent
        self.lWatDep = False   # reaction coefficient is water content dependent.
        self.Tortuosity =True # tortuosity factor is used or 1
        self.lTortM = False    # Per Moldrup’s tortuosity models for the tortuosity factor
        self.Bacter = False    # attachment/detachment approach is to be used to calculate nonequilibrium transport of viruses, colloids, or bacteria
        self.Filtration =False # attachment coefficient is to be evaluated using the filtration theory
        self.lFumigant = False # fumigant transport are used
        self.lAddFum = False   # additional application (injection) of fumigant
        self.cTolA = 0       # Absolute concentration tolerance
        self.cTolR = 0       # Relative concentration tolerance
        self.MaxItC = 1     # Maximum number of iterations allowed during any time step for solute transport
        self.lInitEq = False   # liquid phase concentrations
        self.lInitM = False    # initial condition is given in (t:) the total mass of solute per unit volume of soil or (f:) liquid concentration 
        self.Equilib = 1     # = 1; Equilibrium solute transport, = 0; Nonequilibrium solute transport (1 if lChem = False)

        # %%2 solute transport parameters
        self.soil_param = [[1.5, 0.5, 0.1, 1, 0]]
                    #  Bulk.d., DisperL., DisperT, Frac, ThImob
                    # DifW, DifG
        self.solute_param = [[0, 0]]
        
        # %%3 Reaction parameters for solute
                    # 1, 2, 3, 4, root, well, 7, atm, d
        self.cBnds = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    # Ks, Nu, Beta, Henry, SnkL1, SnkS1, SnkG1, SnkL1', SnkS1', SnkG1', SnkL0, SnkS0, SnkG0, Alfa
        self.react_param = [[0, 0, 1, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        # Add Fumigant 
        self.AddFumTime = 0
        self.AddFumMass = 0
        self.AddFumMinX = 0
        self.AddFumMaxX = 0
        self.AddFumMinZ = 0
        self.AddFumMaxZ = 0
        
        # %%4 temperature dependent solute transport
        # DifW, DifG, Ks, Nu, Beta, Henry, SnkL1, SnkS1, SnkG1, SnkL1', SnkS1' SnkG1', SnkL0, SnkS0, SnkG0, Alfa
        self.TDep_params = [[0, 0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # %%5 water content dependent solute transport
        self.nParamWC = 9
        self.WTDep_params1 = [
            #SnkL1 SnkS1 SnkG1 SnkL1' SnkS1' SnkG1' SnkL0 SnkS0 SnkG0
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.WTDep_params2 = [
            #SnkL1 SnkS1 SnkG1 SnkL1' SnkS1' SnkG1' SnkL0 SnkS0 SnkG0
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        
        # %%1 Heat transport parameters
                        #1, 2, 3, 4, 5, well
        self.tBnds = [[0, 0, 0, 0, 0, 0]]
        self.tAmpl = 5       # Temperature amplitude at the soil surface
        self.tPeriodHeat = 1     # Time interval for the completion of one temperature cycle

        self.Heat_Catalog = {
                'loam': [0.59, 0, 5, 1, 1.56728e+016,  2.53474e+016, 9.89388e+016, 1.43327e+014, 1.8737e+014, 3.12035e+014],
                'clay': [0.59, 0, 5, 1, -1.2706e+016, -6.20464e+016, 1.62598e+017, 1.43327e+014, 1.8737e+014, 3.12035e+014],
                'sand': [0.59, 0, 5, 1, 1.47054e+016, -1.5518e+017,  3.16617e+017, 1.43327e+014, 1.8737e+014, 3.12035e+014],
                }
        self.Tpar = [self.Heat_Catalog['loam'] for _ in range(self.NMat)]

        # %%1 root water and solute uptake model
        self.rootModel = False       #0: Feddes, 1:s-shaped
        self.OmegaC = 1 #critical stress index
        self.lActRSU = False       # Active Solute Transport model is to be used
        if not self.lChem or self.NS > 1:
            self.lActRSU = False
            #no solute stress
        self.SoluteReduction = False   # root water uptake is reduced due to salinity.
        self.SoluteAdditive = True     #the effect of salinity stress is True: additive or False: multiplicative to the pressure head stress.
        self.lMsSink = False            # True: S-shaped root water uptake salinity stress response function, False: threshold function according Maas
        self.aOsm = [1 for i in range(self.NS)]
        
        self.OmegaS = 1
        self.SPot = 0
        self.KM = 0
        self.cMin = 0
        self.OmegaW = True              # whether the potential plant nutrient demand is to be reduced proportionally to the root water uptake reduction.
       # %%Root Water uptake parameters
        self.Uptake_catalog = {
        #                 PO, POptm, P2H, P2L, P3, r2H, r2L
            'Pasture':  [-10, -25, -200, -800, -8000, 0.5, 0.1],
            'Corn':     [-15, -30, -325, -600,  -800, 0.5, 0.1],
            'Alfalfa':  [-15, -30, -1500, -1500,  -8000, 0.5, 0.1],
            'Beans':    [-15, -30, -750, -2000,  -8000, 0.5, 0.1],
            'Cabbage':  [-15, -30, -600, -700,  -8000, 0.5, 0.1],
            'Canning Peas':  [-15, -30, -300, -500,  -8000, 0.5, 0.1],
            'Celery':  [-15, -30, -200, -300,  -8000, 0.5, 0.1],
            'Grass':  [-15, -30, -300, -1000,  -8000, 0.5, 0.1],
            'Lettuce':  [-15, -30, -400, -600,  -8000, 0.5, 0.1],
            'Tobacco':  [-15, -30, -300, -800,  -8000, 0.5, 0.1],
            'Sugar Cane - tensiometers':  [-15, -30, -150, -500,  -8000, 0.5, 0.1],
            'Sugar Cane - blocks':  [-15, -30, -1000, -2000,  -8000, 0.5, 0.1],
            'Sweet Corn':  [-15, -30, -500, -1000,  -8000, 0.5, 0.1],
            'Turfgrass':  [-15, -30, -240, -360,  -8000, 0.5, 0.1],
            'Onions - early growth':  [-15, -30, -450, -550,  -8000, 0.5, 0.1],
            'Onions - bulbing time':  [-15, -30, -550, -650,  -8000, 0.5, 0.1],
            'Sugar Beets':  [-15, -30, -400, -600,  -8000, 0.5, 0.1],
            'Potatoes':  [-15, -30, -300, -500,  -8000, 0.5, 0.1],
            'Carrots':  [-15, -30, -550, -650,  -8000, 0.5, 0.1],
            'Broccoli - early':  [-15, -30, -450, -550,  -8000, 0.5, 0.1],
            'Broccoli - after budding':  [-15, -30, -600, -700,  -8000, 0.5, 0.1],
            'Cauliflower':  [-15, -30, -600, -700,  -8000, 0.5, 0.1],
            'Lemons':  [-15, -30, -400, -400,  -8000, 0.5, 0.1],
            'Oranges':  [-15, -30, -200, -1000,  -8000, 0.5, 0.1],
            'Deciduous':  [-15, -30, -500, -800,  -8000, 0.5, 0.1],
            'Avocados':  [-15, -30, -500, -500,  -8000, 0.5, 0.1],
            'Grapes - early seasons':  [-15, -30, -400, -500,  -8000, 0.5, 0.1],
            'Grapes - during maturity':  [-15, -30, -1000, -1000,  -8000, 0.5, 0.1],
            'Strawberries':  [-15, -30, -200, -300,  -8000, 0.5, 0.1],
            'Cantaloupe':  [-15, -30, -350, -450,  -8000, 0.5, 0.1],
            'Tomatoes':  [-15, -30, -800, -1500,  -8000, 0.5, 0.1],
            'Bananas':  [-15, -30, -300, -1500,  -8000, 0.5, 0.1],
            'Corn - vegetative period':  [-15, -30, -500, -500,  -8000, 0.5, 0.1],
            'Corn - during ripening':  [-15, -30, -8000, -12000,  -24000, 0.5, 0.1],
            'Small Grains - vegetative period':  [-15, -30, -400, -500,  -24000, 0.5, 0.1],
            'Small Grains - during ripening':  [-15, -30, -8000, -12000,  -24000, 0.5, 0.1],
        }
        self.croptype = 'Pasture'
        self.uptake_param = self.Uptake_catalog[self.croptype]
        
        self.S_shape_Param = [-800, 3, -1e+010]

        self.Threshold_Model_catalog = {
        #               c50, P3c
            'Alfalfa':   [4, 3.65],
            'Barley':   [ 16, 2.5],
            'Barley (forage)': [12, 3.55],
            'Bermuda grass':   [13.8, 3.2],
            'Bean':     [  2, 9.5],
            'Beet, red':   [8, 4.5],
            'Broccoli':   [5.6, 4.6],
            'Cabbage':   [3.6, 4.85],
            'Carrot':   [2, 7],
            'Clover, ladino':   [3, 6],
            'Corn':     [3.4,   6],
            'Corn, sweet':     [3.4,   6],
            'Corn (forage)':   [2.6, 3.7],
            'Cotton':  [15.4, 2.6],
            'Cowpea (forage)':   [5, 5.5],
            'Cucumber':   [5, 6.5],
            'Lettuce':   [2.6, 6.5],
            'Onion':     [2.4, 8],
            'Peanut':  [6.4, 14.5],
            'Potato':   [3.4,   6],
            'Rice (paddy)':     [6, 6],
            'Rye':     [22.8, 5.4],
            'Ryegrass, perennial':   [11.2, 3.8],
            'Sorghum':  [13.6,  8],
            'Soybean':    [10, 10],
            'Spinach':     [4, 3.8],
            'Sugar beet': [14, 2.95],
            'Sugar cane': [3.4, 2.95],
            'Sundan grass':   [5.6, 2.15],
            'Tomato':     [5, 4.95],
            'Wheat':     [12, 3.55],
            'Wheat (forage)':   [9, 1.3],
            'Wheat, durum':  [11.8, 1.9],
            
        }
        self.croptype_threshold = 'Barley'
        self.Threshold_Model_param = self.Threshold_Model_catalog[self.croptype_threshold]
        # %% root growth parameters
        self.iRootZoneShape = 2  # =0: The Vrugt function, =1: The van Genuchten-Hoffman function. =2: Constant root distribution.
        self.iRootDepthEntry = 2 # =0: No root growth =2: The rooting depth is time-variable, described using a table. =2: The rooting depth (and horizontal extent) is time variable, described using Verhulst-Pearl logistic growth function.
        self.Horizontal = False    # The Vrugt function is used also for horizontal distribution, or a limited horizontal
        self.NPlants = 1         # Number of plants
        self.rDepth = 40
        self.RootHalfWidth = 20
        #if self.iRootZoneShape == 0:
        self.rZm = 0
        self.rZ0 = 0
        self.rA = 0
        self.rRm = 0
        self.rR0 = 0
        self.rB = 0
        self.rCenter = [0 for _ in range(self.NPlants)]
        #if self.iRootZoneShape == 1:
        self.nGrowth = 1
        self.RootDepth = [
        # time, z, x
            [0, 0, 0],
        ]
        #if self.iRootZoneShape == 2:
        self.iRFak = 0       # = 0; the root growth factor is calculated from given data = 1; the root growth factor is calculated based on the assumption that 50% of the rooting depth
        self.tRMin = 0     # Initial time of the root growth period
        self.tRMed = 0     # Time of known rooting depth
        self.tRMax = 90     #harvest time
        self.tPeriodRoot = 365   # Time period at which the growth function repeat itself.
        self.ZRMin = 0.01    # Initial value of the rooting depth at the beginning of
        self.ZRMed = 0.01      # Value of known rooting depth
        self.ZRMax = 90      # Maximum rooting depth
        self.rRMin = 1          #Initial value of the rooting radius at the beginning of the growth period
        self.rRMax = 1          # Maximum rooting radius, which may be reached at infinite time
        
        #%% time variable boundary condition
        self.L_surf  = 0
        if self.AtmIn: self.L_surf = 1

        # %% Boundary condition options
        # %%% time/variable heat flux
        self.Interp = False    # time-variable boundary pressure heads is interpolated with time.
        self.H_Flux = False    # the time-variable boundary pressure head boundary condition should be changed to zero flux when the specified number is larger than 999999.
        self.H_Flx1 = False    # the zero flux boundary condition should be applied on the part of the boundary where the time-variable boundary pressure head is negative.
        self.Atm_H = False     # atmospheric boundary condition should be applied 
        self.Seep_H = False    # the seepage face boundary condition should be applied
        self.Atm_WL = False    # the atmospheric boundary condition should be applied on the part of the boundary where the time-variable boundary pressure head is negative.
        self.Atm_SF = False    # the time-variable flux boundary condition should be treated similarly as the atmospheric boundary conditions 

        self.Snow = False      # snow accumulates

        # %%% spacial BC
        self.Gradient = False  # a gradient boundary condition with a gradient different than one (free drainage) is to be specified.
        self.xGrad   = 1
        self.SubDrip = False   # a special boundary condition that considers the effect of the back pressure on the subsurface drip irrigation is to be applied
        self.QDrip  = 0
        self.ExpDrip = 0.5      # An empirical constant that reflects the flow characteristics of the emitter. Normally, c = 0.5 corresponds to a turbulent flow emitter and c = 1 to a laminar one.
        self.SurfDrip = False  # special boundary condition with dynamic ponding for surface drip irrigation is to be considered.
        self.iDripCenter = 0
        self.iDripNode = -1      # A code indicating, in which direction the surface ponding spreads. =-1: from left to right, = 0: from center in both directions =+1: from right to left    
        self.SeepFace = False  # a seepage face boundary condition with a specified pressure head (other than zero) is to be applied
        self.hSeep = 0

        # %%% trigger irrigation
        self.TriggIrrig = False# irrigation is to be triggered by the pressure head at a specified observation nodes falling below a specified value.
        self.iIrrig = 1
        self.hIrrig = -1000
        self.kIrrig = -4        # (-4 = atmospheric (sprinkler), -3 or +3 = variable flux or pressure head (dripper)).
        self.rIrrig = 0
        self.tIrrig = 0
        self.lIrrig = 0

        # %%% reservoir BC
        self.WellBC = False    # irrigation the Reservoir Boundary Condition
        self.iWell = 1          # Type of reservoir: =1: Well; =2: Furrow; =3: Wetland
        self.zWBot = 0
        self.zWInit = 0
        self.Radius = 0
        self.WellPump = 0
        self.cWell = 0
        self.TanAlfa = 0
        self.HwMax = 0
        self.zMax = 0
        self.pp = 0

        # %% Observation node
        self.Obs_nodes = []
        self.NObs = len(self.Obs_nodes)                       # Maximum number of observation nodes (<10)

        # %% scaling factor
        self.Axz = 1         # dimensionless scaling factor α h [-] associated with the pressure head.
        self.Bxz = 1         # the dimensionless scaling factor αK [-] associated with the saturated hydraulic conductivity.
        self.Dxz = 1         # dimensionless scaling factor αθ [-] associated with the water content.
        self.Beta = 0        # Value of the water uptake distribution, b(x,y,z)

        # %% anisotropy
        self.AnizA1 = 1      # First principal component, K1, of the dimensionless tensor KA which describes the local anisotropy of the hydraulic conductivity assigned to element e.
        self.AnizA2 = 1      # Second principal component, K2
        # %% subregions
        self.LayNum = 1      # Subregion number assigned to element e.

        # %% drain
        self.DrainF = False            # a drain is to be simulated
        self.ND = []
        self.NDr = len(self.ND)          # Maximum number of drains
        self.EfDim = [500, 4000.01] # Effective diameter of the first drain, Dimension of the square in finite element mesh representing the first drain,
        self.NElDr = 20             # Maximum number of elements surrounding one drain
        self.DrCorr = 4      # Additional reduction in the correction factor
        self.KELDr = [19511, 19512, 19513, 19514, 19711, 19712, 19713, 19714] # Global number of the first element surrounding the first drain.

        # %% flowing particles
        self.NPart = 0       # Number of fictional particles, for which their trajectory is to be calculated.

        # %%
        self.NSeep = 1       # Maximum number of seepage faces
        self.NumSP = 1       # Maximum number of nodes along a seepage face
        self.NumBP = 0     # Maximum number of boundary nodes for which Kode(n)≠0
        self.MBan = 30       # Maximum dimension of the bandwidth of matrix A
        self.SeepF = False     # seepage faces is to be considered.
        self.FreeD = False     # free drainage is used at the bottom boundary.
        self.qQWLF = False     # the discharge-groundwater level relationship is used at the bottom
                
        self.atmosph_data = [[1, 0, 0, 0.4, 10000, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.hCritS = 0      # Maximum allowed pressure head at the soil surface

        self.lDummy = False    # Logical dummy variable


    def _bool2str(self, *args):
        list_t_f = []
        for arg in args:
            if arg: list_t_f.append('t')
            else: list_t_f.append('f')

        return list_t_f
        
    def GenerateMesh(self, node_x, node_z):
        #create nodes array
        x, z = np.meshgrid(node_x, node_z[::-1])
        nodes = np.vstack((x.flatten(), z.flatten())).T
        
        #create mesh array
        #i_ k   i
        # \|j   j|_\k
        
        i = [i for i in range(1, self.NumNP) if i%(self.NSurf+1)][:-self.NSurf]
        i = np.array([i, i])
        i = i.T.flatten()

        j = [j for j in range(1, self.NumNP) if j%(self.NSurf+1)][self.NSurf:]
        j = np.array([j, j])
        j[0] += 1
        j = j.T.flatten()
        
        k = [k+1 for k in range(1, self.NumNP) if k%(self.NSurf+1)][:-self.NSurf]
        k = np.array([k, k])
        k[1] += (self.NSurf+1)
        k = k.T.flatten()
        
        mesh = np.array([i, j, k]).T
        return nodes, mesh


    def write_Meshtria(self, nodes, mesh):
        with open(self.path+  '\\Meshtria.txt', 'w') as (f):
            f.write(('{:>10}'*5).format(1, self.NumNP, 1, self.NumEl, 1)+'\n')
            for i in range(self.NumNP):
                f.write('{:>6}{:>14}{:>14}'.format(i+1, nodes[i, 0], nodes[i, 1])+'\n')
            f.write('Edges\n')
            f.write('\n')
            f.write('       e            i            j            k'+'\n')
            for e in range(self.NumEl):
                f.write(' {:>7} {:>12} {:>12} {:>12}'.format(e+1, mesh[e, 0], mesh[e, 1], mesh[e, 2])+'\n')
            
            f.write('*** End of File *************************************************************************************************************'+'\n')
            f.close()


    def write_Selector(self, TPrint):
        with open(self.path+  '\\Selector.in', 'w') as (f):
            file_version = 4
            f.write('Pcp_File_Version={}'.format(file_version)+'\n')
            f.write('*** BLOCK A: BASIC INFORMATION *****************************************'+'\n')      
            
            f.write('Heading'+'\n')
            f.write('{}'.format(self.Heading)+'\n')
            
            f.write('LUnit  TUnit  MUnit  (indicated units are obligatory for all input data)'+'\n')
            f.write('{}\n{}\n{}\n'.format(self.LUnit, self.TUnit, self.MUnit))
            
            f.write('Kat (0:horizontal plane, 1:axisymmetric vertical flow, 2:vertical plane)'+'\n')
            f.write('{:>3}'.format(self.Kat)+'\n')
            
            f.write('MaxIt   TolTh   TolH InitH/W  (max. number of iterations and tolerances)'+'\n')
            f.write(' {:>3} {:>8} {:>6} {:>5}'.format(self.MaxIt, self.TolTh, self.TolH, *self._bool2str(self.InitH_W))+'\n')
            
            f.write('lWat lChem lSink Short Inter lScrn AtmIn lTemp lWTDep lEquil lExtGen lInv'+'\n')
            f.write(('{:>2}'+' {:>5}'*11).format(*self._bool2str(self.lWat, self.lChem, self.lSink, self.Short,
                                         self.Inter, self.lScrn, self.AtmIn, self.lTemp,
                                         self.lWTDep, self.lEquil, self.lExtGen, self.lInv))+'\n')
            
            f.write('lUnsatCh lCFSTr  lHP2  m_lActRSU lRootGr lDummy  lDummy'+'\n')
            f.write(('{:>2}'+' {:>7}'*7).format(*self._bool2str(self.lUnsatCh, self.lCFSTr, self.lHP2, self.lActRSU,
                                        self.lRootGr, self.lDummy, self.lDummy, self.lDummy))+'\n')
            
            f.write(' PrintStep  PrintInterval lEnter'+'\n')
            f.write(' {:>9} {:>14} {:>7}'.format(self.PrintStep, self.PrintInterval, *self._bool2str(self.lEnter))+'\n')
            
            f.write('*** BLOCK B: MATERIAL INFORMATION **************************************'+'\n')
            f.write('NMat    NLay    hTab1   hTabN     NAniz'+'\n')
            f.write('{:>3} {:>7} {:>9} {:>7}'.format(self.NMat, self.NLay, self.hTab1, self.hTabN)+'\n')
            
            f.write('    Model   Hysteresis'+'\n')
            f.write('{:>7} {:>10}'.format(self.Model, self.Hysteresis)+'\n')
            if self.Hysteresis != 0:
                f.write('---'+'\n')
                f.write('{:>7}'.format(self.iKappa)+'\n')

            f.write('  thr    ths   Alfa     n    Ks      l')
            if self.Model == 1:
                f.write('    Qm    Qa    Qk    Kk'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>6} '*10).format(*self.materials[i][1:])+'\n')
            elif self.Model == 5:
                f.write('    w2    α2    n2'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>6} '*9).format(*self.materials[i][1:])+'\n')
            elif self.Model == 6:
                f.write('    QrIm    QsIm    ω'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>6} '*9).format(*self.materials[i][1:])+'\n')
            elif self.Model == 7:
                f.write('    QrIm    QsIm    αIm    nIm    ω'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>6} '*11).format(*self.materials[i][1:])+'\n')
            else:
                f.write('\n')
                for i in range(self.NMat):
                    f.write(('{:>6} '*6).format(*self.materials[i][1:])+'\n')
                
            f.write('*** BLOCK C: TIME INFORMATION ******************************************'+'\n')
            f.write('        dt       dtMin       dtMax     DMul    DMul2  ItMin ItMax  MPL'+'\n')
            f.write('{:>11} {:>11} {:>11} {:>7} {:>7} {:>5} {:>5} {:>5}'
                    .format(self.dt, self.dtMin, self.dtMax, self.DMul, self.DMul2,
                            self.ItMin, self.ItMax, self.MPL)+'\n')
            
            f.write('      tInit        tMax'+'\n')
            f.write('{:>11} {:>11}'.format(self.tInit, self.tMax)+'\n')
            
            f.write('TPrint(1),TPrint(2),...,TPrint(MPL)'+'\n')
            for i in range(1, self.MPL+1):
                f.write(('{:>11} ').format(TPrint[i]))
                if i%6 == 0:
                    f.write('\n')
            f.write('\n')
            
            if self.lChem:
                f.write('*** BLOCK D: SOLUTE TRANSPORT INFORMATION *****************************************************'+'\n')
                f.write(' Epsi  lUpW  lArtD lTDep    cTolA    cTolR   MaxItC    PeCr  Nu.ofSolutes Tortuosity Bacter Filtration'+'\n')
                f.write('{:>5} {:>5} {:>5} {:>5} {:>9} {:>9} {:>5} {:>8} {:>8} {:>9} {:>9} {:>9}'
                        .format(self.Epsi, *self._bool2str(self.lUpW, self.lArtD, self.lTDep),
                                self.cTolA, self.cTolR, self.MaxItC, self.PeCr,
                                self.NS, *self._bool2str(self.Tortuosity, self.Bacter,
                                self.Filtration))+'\n')
                
                f.write('   lWatDep    lInitM   lInitEq    lTortM    lFumigant lDummy    lDummy    lDummy    lDummy    lDummy    lDummy'+'\n')
                f.write((' {:>9}'*5).format(*self._bool2str(self.lWatDep, self.lInitM, self.lInitEq, self.lTortM, self.lFumigant)))
                f.write((' {:>9}'*6).format( *self._bool2str(self.lDummy)*6)+'\n')
                
                f.write('     Bulk.d.     DisperL.      DisperT     Frac      ThImob (1..NMat)'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>11} '*5).format(*self.soil_param[i])+'\n')
                
                f.write('         DifW       DifG                n-th solute'+'\n')
                for i in range(self.NS):
                    f.write('{:>11} {:>11}'.format(*self.solute_param[i])+'\n')
                
                if self.Bacter:
                    if self.Filtration:
                        f.write('         Ks          Nu        Beta       Henry       SnkL1       SnkS1       D_soil       D_virus      SMax2      Coll.Eff2      DetachS2       SMax1       Coll.Eff1        DetachS1'+'\n')
                    else:
                        f.write('         Ks          Nu        Beta       Henry       SnkL1       SnkS1       iPsi2       iPsi1      SMax2      AttachS2      DetachS2       SMax1       AttachS1        DetachS1'+'\n')
                else:
                    f.write('         Ks          Nu        Beta       Henry       SnkL1       SnkS1       SnkG1       SnkL1\'      SnkS1\'      SnkG1\'      SnkL0       SnkS0       SnkG0        Alfa'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>11} '*14).format(*self.react_param[i])+'\n')

                if self.lTDep:
                    f.write('Temperature Dependence'+'\n')
                    f.write('         DifW       DifG                n-th solute'+'\n')
                    for i in range(self.NS):
                        f.write('{:>11} {:>11}'.format(*self.TDep_params[i][:2])+'\n')
                    
                    f.write('         Ks          Nu        Beta       Henry       SnkL1       SnkS1       SnkG1       SnkL1\'      SnkS1\'      SnkG1\'      SnkL0       SnkS0       SnkG0        Alfa'+'\n')
                    for i in range(self.NS):
                        f.write(('{:>11} '*14).format(*self.TDep_params[i][2:])+'\n')
                
                f.write('       cTop        cBot'+'\n')
                for i in range(self.NS):
                    f.write(('{:>11} '*9).format(*self.cBnds[i])+'\n')
                
                f.write('      tPulse'+'\n')
                f.write('{:>11}'.format(self.tPulse)+'\n')
                if self.lFumigant:
                    f.write('  AddFumigant'+'\n')
                    f.write('{:>10}'.format(*self._bool2str(self.lAddFum))+'\n')
                    if self.lAddFum:
                        f.write('   AddFumTime    AddFumMass'+'\n')
                        f.write('{:>13} {:>13}'.format(self.AddFumTime, self.AddFumMass)+'\n')
                        f.write('   AddFumMinX    AddFumMaxX    AddFumMinZ    AddFumMaxZ    AddFumMinY    AddFumMaxY'+'\n')
                        f.write(('{:>13} '*4).format(self.AddFumMinX, self.AddFumMaxX, self.AddFumMinZ, self.AddFumMaxZ)+'\n')
                
                if self.lWatDep:
                    f.write('Water Content Dependence'+'\n')
                    f.write('Number of Parameters'+'\n')
                    f.write('{:>11}'.format(self.nParamWC))
                    for i in range(self.NS):
                        f.write('      SnkL1       SnkS1       SnkG1       SnkL1\'      SnkS1\'      SnkG1\'      SnkL0       SnkS0       SnkG0'+'\n')
                        f.write(('{:>11} '*self.nParamWC).format(*self.WTDep_params1[i])+'\n')
                        f.write(('{:>11} '*self.nParamWC).format(*self.WTDep_params2[i])+'\n')

            if self.lTemp:            
                f.write('*** BLOCK E: HEAT TRANSPORT INFORMATION *********************************************************'+'\n')
                f.write('    Qn      Qo         Disper.       B1          B2          B3          Cn          Co           Cw'+'\n')
                for i in range(self.NMat):
                    f.write(('{:>7} '*4+'{:>12e} '*6).format(*self.Tpar[i])+'\n')
                    
                f.write('       TTop        TBot'+'\n')
                f.write(('{:>11} '*6).format(*self.tBnds[0])+'\n')
                
                f.write('      tAmpl     tPeriod'+'\n')
                f.write('{:>11} {:>11}'.format(self.tAmpl, self.tPeriodHeat)+'\n')
            
            if self.lSink:
                f.write('*** BLOCK F: ROOT WATER UPTAKE INFORMATION *****************************'+'\n')
                f.write('     Model  (0 - Feddes, 1 - S shape)  Critical Stress Index'+'\n')
                f.write('{:>9} {:>30}'.format(self.rootModel, self.OmegaC)+'\n')
                
                if self.rootModel == 0:
                    f.write('       P0       P2H       P2L       P3          r2H        r2L'+'\n')
                    f.write('{:>9} {:>9} {:>9} {:>9} {:>11} {:>11} '.format(*self.uptake_param[:-1])+'\n')
                    
                    f.write('POptm(1),POptm(2),...,POptm(NMat)'+'\n')
                    for i in range(self.NMat):
                        f.write(('{:>8} ').format(self.uptake_param[-1]))
                    f.write('\n')

                elif self.rootModel == 1:
                    f.write('       P50       P3          PW'+'\n')
                    f.write('{:>9} {:>9} {:>9} '.format(*self.S_shape_Param)+'\n')
                    
                if self.lChem:
                    f.write('     Solute Reduction'+'\n')
                    f.write('{:>9}'.format(*self._bool2str(self.SoluteReduction))+'\n')
                
                    if self.SoluteReduction:
                        f.write('     Additive * multiplicative'+'\n')
                        f.write('{:>9}'.format(*self._bool2str(self.SoluteAdditive))+'\n')
                    if not self.SoluteAdditive:
                        f.write('     c50        p             Osmotic Coefficients'+'\n')
                        f.write('{:>9} {:>9}'.format(self.c50, self.P3c))
                        for i in range(self.NS):
                            f.write(' {:>9}'.format(self.aOsm[i]))
                        f.write(' {:>1}'.format(int(self.lMsSink))+'\n')
                    else:
                        f.write('             Osmotic Coefficients'+'\n')
                        for i in range(self.NS):
                            f.write(' {:>9}'.format(self.aOsm[i]))
                        f.write(' {:>1}'.format(int(self.lMsSink))+'\n')
                if self.lActRSU:
                    f.write('      OmegaS     SPot     KM    cMin    OmegaW'+'\n')
                    f.write('{:>9} {:>9} {:>9} {:>9} {:>9}'.format(self.OmegaS, self.SPot, self.KM, self.cMin, *self._bool2str(self.OmegaW))+'\n')
                
                
            if self.lRootGr:
                f.write('*** BLOCK D: ROOT GROWTH INFORMATION ***********************************'+'\n')
                f.write('iRootZone Shape iRootDepthEntry'+'\n')
                f.write(' {:>8} {:>8}'.format(self.iRootZoneShape, self.iRootDepthEntry)+'\n')
                
                f.write(' Horizontal    NPlants'+'\n')
                f.write(' {:>8} {:>8}'.format(self.Horizontal, self.NPlants)+'\n')
                if self.iRootZoneShape == 0:
                    f.write('      rZm      rZ0       rA'+'\n')
                    f.write('{:>9} {:>9} {:>9}'.format(self.rZm, self.rZ0, self.rA)+'\n')
                    if self.Horizontal:
                        f.write('      rRm      rR0       rB        rCenter(nPlant)'+'\n')
                        f.write('{:>9} {:>9} {:>9}'.format(self.rRm, self.rR0, self.rB))
                        for i in range(self.NPlants):
                            f.write('{:>9}'.format(self.rCenter[i]))
                        f.write('\n')

                else:
                    if self.iRootDepthEntry == 0:
                        f.write(' RootDepth  RootHalfWidth  rCenter(nPlant)'+'\n')
                        f.write('{:>9}'.format(self.rDepth)+'\n')
                        if self.Horizontal:
                            f.write('{:>9} {:>9}'.format(self.RootHalfWidth, self.RootHalfWidth))
                            for i in range(self.NPlants):
                                f.write('{:>9}'.format(self.rCenter[i]))
                            f.write('\n')

                    elif self.iRootDepthEntry == 1:
                        f.write(' rCenter(nPlant)'+'\n')
                        if self.Horizontal:
                            for i in range(self.NPlants):
                                f.write('{:>9}'.format(self.rCenter[i]))
                        f.write('\n')

                if self.iRootDepthEntry == 1:
                    f.write(' nGrowth'+'\n')
                    f.write('{:>9}'.format(self.nGrowth)+'\n')
                    f.write('      Time  RootDepth'+'\n')
                    for i in range(self.nGrowth):
                        f.write('{:>9} {:>9} {:>9}'.format(*self.RootDepth[i])+'\n')
                    
                elif self.iRootDepthEntry == 2:
                    f.write(' rCenter(nPlant)'+'\n')
                    if self.Horizontal:
                        for i in range(self.NPlants):
                            f.write('{:>9}'.format(self.rCenter[i]))
                    f.write('\n')
                    f.write('     iRFak     tRMin     tRMed     tRMax     tPeriod'+'\n')
                    f.write('{:>9} {:>9} {:>9} {:>9} {:>9}'
                            .format(self.iRFak, self.tRMin, self.tRMed, self.tRMax, self.tPeriodRoot)+'\n')
                    f.write('     ZRMin     ZRMed     ZRMax'+'\n')
                    f.write('{:>9} {:>9} {:>9}'.format(self.ZRMin, self.ZRMed, self.ZRMax)+'\n')
                    if self.Horizontal:
                        f.write('     rRMin      rRMax'+'\n')
                        f.write('{:>9} {:>9}'.format(self.rRMin, self.rRMax))                        


            f.write('*** END OF INPUT FILE \'SELECTOR.IN\' ************************************'+'\n')
            f.close()
            
            
    def write_Boundary(self, nNode, Width):
        self.NumBP = len(nNode)
        self.NELD = len(self.KELDr)
        self.KodCB = [-1]*self.NumBP
        self.KodTB = [-1]*self.NumBP
        if self.NumBP == 0:
            nNode = [0]
            Width = [0]

        with open(self.path+  '\\Boundary.in', 'w') as (f):
            file_version = 5
            f.write('Pcp_File_Version={}'.format(file_version)+'\n')
            f.write('*** BLOCK J: BOUNDARY INFORMATION *********************************************'+'\n')
            
            f.write('    NumBP     NObs  SeepF  FreeD DrainF  qQWLF'+'\n')
            f.write(' {:>8} {:>8} {:>6} {:>6} {:>6} {:>6}'
                    .format(self.NumBP, self.NObs, *self._bool2str(self.SeepF, self.FreeD, self.DrainF, self.qQWLF))+'\n')
            
            f.write(' Interp H/Flux H/Flx1  Atm/H Seep/H Atm/WL Atm/SF   Snow'+'\n')
            f.write((' {:>6}'*8).format(*self._bool2str(self.Interp, self.H_Flux, self.H_Flx1,  self.Atm_H,
                                        self.Seep_H, self.Atm_WL, self.Atm_SF, self.Snow))+'\n')
            
            f.write('Gradient SubDrip SurfDrip SeepFace TriggIrrig   WellBC'+'\n')
            f.write((' {:>6}'*8).format(*self._bool2str(self.Gradient, self.SubDrip, self.SurfDrip,
                                        self.SeepFace, self.TriggIrrig, self.WellBC,
                                        self.lDummy, self.lDummy))+'\n')
            if self.Gradient:
                f.write('     Grad'+'\n')
                f.write('{:>10}'.format(self.xGrad)+'\n')
            if self.SubDrip:
                f.write('      Flux   Exponent'+'\n')
                f.write('{:>10} {:>10}'.format(self.QDrip, self.ExpDrip)+'\n')
            if self.SurfDrip:
                f.write(' Direction     Center'+'\n')
                f.write('{:>10} {:>10}'.format(self.iDripCenter, self.iDripNode)+'\n')
            if self.SeepFace:
                f.write(' Seepage Face Pressure'+'\n')
                f.write('{:>10}'.format(self.hSeep)+'\n')
            if self.TriggIrrig:
                f.write(' Triggered Irrigation'+'\n')
                f.write(' Obs.Node  Pressure Boundary     Flux     Duration     LagTime'+'\n')
                f.write('{:>7} {:>10} {:>7} {:>10} {:>10} {:>10}'.format(self.iIrrig, self.hIrrig, self.kIrrig, self.rIrrig, self.tIrrig, self.lIrrig))
            if self.WellBC:
                f.write('Type of reservoir: =1: Well; =2: Furrow; =3: Wetland'+'\n')
                f.write('{:>7}'.format(self.iWell)+'\n')
                f.write('      zWBot     zWInit    RadiusW   WellPump      cWell'+'\n')
                f.write(('{:>10} '*5).format(self.zWBot, self.zWInit, self.Radius, self.WellPump, self.cWell))
                if self.iWell == 2:
                    f.write('{:>10} {:>10} '.format(self.TanAlfa, self.HwMax)+'\n')
                elif self.iWell == 3:
                    f.write('{:>10} {:>10} '.format(self.zMax, self.pp)+'\n')
                else:
                    f.write('\n')
                
            f.write('Node Number Array')
            for i, n in enumerate(nNode):
                if i%10 == 0:
                    f.write('\n')
                f.write(('{:>7} ').format(n))
            f.write('\n')
            
            f.write('Width Array')
            for i, w in enumerate(Width):
                if i%10 == 0:
                    f.write('\n')
                f.write(('{:>7} ').format(w))
            f.write('\n')    
            
            f.write('Length of soil surface associated with transpiration'+'\n')
            f.write('{:>15}'.format(self.L_surf)+'\n')
            
            if self.NObs != 0:
                f.write('Observation nodes. Node(1,....self.NObs)'+'\n')
                f.write(('{:>8} '*self.NObs).format(*self.Obs_nodes)+'\n')
            
            f.write('Number of Flowing points and their indeces'+'\n')
            f.write('{:>5}'.format(self.NPart)+'\n')
            
            if self.DrainF:
                f.write('*** BLOCK Jb: DRAIN INFORMATION *****************************************************'+'\n')
                f.write('NDr    DrCorr                                         (number of drains)'+'\n')
                f.write('{:>3} {:>3}'.format(self.NDr, self.DrCorr)+'\n')
                
                f.write('ND(1,..,NDr)                              (global numbers of the drains)'+'\n')
                f.write(('{:>8} '*self.NDr).format(*self.ND)+'\n')
                
                f.write('NElD(1,..,NDr)                (number of elements surrounding the drain)'+'\n')
                f.write('{:>8} '.format(self.NELD)+'\n')
                
                f.write('EfDim(1..2) (effect.diameter and dimension of square representing drain)'+'\n')
                f.write('{:>10} {:>10}'.format(*self.EfDim)+'\n')
                
                f.write('KElDr(i,1),..,KElDr(i,NElD(i))  (element numbers surrounding i-th drain)'+'\n')
                f.write(('{:>6} '*self.NELD).format(*self.KELDr)+'\n')
            
            if self.lChem:
                f.write('*** BLOCK J-D: Solute transport boundary conditions *****************************'+'\n')
                f.write('KodCB(1),KodCB(2),.....,KodCB(NumBP)')
                for i, C in enumerate(self.KodCB):
                    if i%20 == 0:
                        f.write('\n')
                    f.write(('{:>3} ').format(C))
                f.write('\n')
            
            if self.lTemp:
                f.write('*** BLOCK J-E: Heat transport boundary conditions *******************************'+'\n')
                f.write('KodTB(1),KodTB(2),.....,KodTB(NumBP)')
                for i, T in enumerate(self.KodTB):
                    if i%20 == 0:
                        f.write('\n')
                    f.write(('{:>3} ').format(T))
                f.write('\n')
            f.write('*** End of input file \'BOUNDARY.IN\' *******************************************'+'\n')
            f.close()
        
    def write_Dimensio(self):
        with open(self.path+  '\\Dimensio.in', 'w') as (f):
            file_version = 3
            f.write('Pcp_File_Version={}'.format(file_version)+'\n')
            f.write('  NumNPD  NumElD  NumBPD  MBandD  NSeepD  NumSPD    NDrD  NElDrD   NMatD   NObsD     NSD   NAnis'+'\n')
            f.write((' {:>7}'*11).format(self.NumNP, self.NumEl, self.NumBP, self.MBan,
                                         self.NSeep, self.NumSP, self.NDr, self.NElDr,
                                         self.NMat, self.NObs, self.NS)+'\n')
            f.close()


    def read_Domain_xls(self, sheet):
        data_domain = []
        head_type = ['Code', 'h', 'Q', 'M', 'Temp', 'Conc']
        for h in head_type:
            data = pd.read_excel(sheet, h, header=0, index_col=0, dtype=int)
            data_domain.append(data.to_numpy().flatten())
        return data_domain


    def write_Domain(self, data):
        with open(self.path+  '\\Domain.dat', 'w') as (f):
            file_version = 2
            f.write('Pcp_File_Version={}'.format(file_version)+'\n')
            f.write('*** BLOCK H: DOMAIN INFORMATION ******************************************************'+'\n')
            
            f.write('Number of Solutes   Equilibrium'+'\n')
            f.write('     {:>4} {:>4}'
                    .format(self.NS, self.Equilib)+'\n')
            f.write('Nodal Information'+'\n')
            f.write('         n   Code          h              Q    M     Beta      Axz      Bxz      Dxz        Temp   Conc(1..NS)   '+'\n')
            for i in range(self.NumNP):
                f.write('{:>10d} {:>6} {:>11} {:>13} {:>4} {:>8} {:>8} {:>8} {:>8} {:>11}'
                        .format(i+1, data[0][i], data[1][i], data[2][i], data[3][i],
                                self.Beta, self.Axz, self.Bxz, self.Dxz, data[4][i]))
                for j in range(self.NS):
                    f.write(' {:>13}'.format(data[j+5][i]))
                f.write('\n')
            
            f.write('*** BLOCK I: ELEMENT INFORMATION ******************************************************'+'\n')
            f.write('         e  Angle  AnizA1 AnizA2 LayNum'+'\n')
            for e in range(1, self.NumEl+1):
                f.write('{:>10} {:>6} {:>6} {:>6} {:>5} '
                        .format(e, self.Angle, self.AnizA1, self.AnizA2, self.LayNum)+'\n')
            f.write('*** End of input file \'DOMAIN.IN\' ****************************************************'+'\n')
            f.close()  
            
            
    def write_ATMOSPH(self, data):
        with open(self.path+  '\\Atmosph.in', 'w') as (f):
            file_version = 3
            f.write('Pcp_File_Version={}\n'.format(file_version))
            f.write('*** BLOCK K: ATMOSPHERIC INFORMATION  **********************************'+'\n')
            f.write('   MaxAL  BC_Cycles         (MaxAL = number of atmospheric data-records)'+'\n')
            f.write(' {:>6} {:>6}\n'.format(self.MaxAL, self.BC_Cycles))
            f.write(' hCritS                 (max. allowed pressure head at the soil surface)'+'\n')
            f.write(' {:>6}\n'.format(self.hCritS))
            f.write(('{:>11} '*18)
                    .format('tAtm', 'Prec', 'rSoil', 'rRoot', 'hCritA', 'rt', 'ht',
                            'rt', 'ht', 'rt', 'ht', 'rt', 'ht', 'TValue1',
                            'TValue2', 'cValue1', 'cValue2', 'cValue3')+'\n')
            for i in range(self.MaxAL):
                f.write(('{:>11} '*18).format(*data[i])+'\n')
            f.write('*** END OF INPUT FILE \'ATMOSPH.IN\' *************************************'+'\n')
            f.close()
    
    def _str2bool(self, line):
        if line == 't':
            return True
        elif line == 'f':
            return False
            
    def read_Dimensio(self):
        with open(self.path+'\\Dimensio.in', 'r') as f:
            line = f.readlines()[2].split()
        key = ['NumNP', 'NumEl', 'NumBP', 'MBand', 'NSeep', 'NumSP', 
               'NDr', 'NElDr', 'NMat', 'NObs', 'NS']
        flag = {key[i]:int(line[i]) for i in range(len(key))}
        self.__dict__.update(**flag)
    
    
    def read_Meshtria(self):
        with open(self.path+'\\Meshtria.txt', 'r') as f:
            MaxIter = int(f.readline().split()[1])
            coords = np.array([[float(line.split()[1]), float(line.split()[2])] 
                               for line in f.readlines()[:MaxIter]], dtype=float)
        
        self.node_x = np.unique(coords[:, 0])
        self.node_z = np.unique(coords[:, 1])
        self.min_x = np.min(self.node_x)
        self.min_z = np.min(self.node_z)
        self.max_x = np.max(self.node_x)
        self.max_z = np.max(self.node_z)
        self.nnode_x = self.node_x.size
        self.nnode_z = self.node_z.size

    
    def read_Boundary(self):
        with open(self.path+'\\Boundary.in', 'r') as f:
            f.readline()
            f.readline()
            f.readline()
            line = f.readline().split()
            key = ['NumBP', 'NObs']
            flag = {key[i]:int(line[i]) for i in range(len(key))}
            self.__dict__.update(**flag)
            key = ['SeepF', 'FreeD', 'DrainF', 'qQWLF']
            flag = {key[i]:self._str2bool(line[2+i]) for i in range(len(key))}
            self.__dict__.update(**flag)
            
            f.readline()
            line = f.readline().split()
            key = ['Interp', 'H_Flux', 'H_Flx1', 'Atm_H', 'Seep_H', 'Atm_WL', 'Atm_SF', 'Snow']
            flag = {key[i]:self._str2bool(line[i]) for i in range(len(key))}
            self.__dict__.update(**flag)
            
            f.readline()
            line = f.readline().split()
            key = ['Gradient', 'SubDrip', 'SurfDrip', 'SeepFace', 'TriggIrrig', 'WellBC']
            flag = {key[i]:self._str2bool(line[i]) for i in range(len(key))}
            self.__dict__.update(**flag)
            
            if self.Gradient:
                f.readline()
                line = f.readline().split()
                self.xGrad = line[0]
            if self.SubDrip:
                f.readline()
                line = f.readline().split()
                self.QDrip, self.ExpDrip = line[0], line[1]
            if self.SurfDrip:
                f.readline()
                line = f.readline().split()
                self.iDripCenter, self.iDripNode = line[0], line[1]
            if self.SeepFace:
                f.readline()
                line = f.readline().split()
                self.hSeep = line[0]
            if self.TriggIrrig:
                f.readline()
                f.readline()
                line = f.readline().split()
                key = ['iIrrig', 'hIrrig', 'kIrrig', 'rIrrig', 'tIrrig', 'lIrrig']
                flag = {key[i]:int(line[i]) for i in range(len(key))}
                self.__dict__.update(**flag)

            if self.WellBC:
                f.readline()
                line = f.readline().split()
                self.iWell = int(line[0])
                f.readline()
                line = f.readline().split()
                key = ['zWBot', 'zWInit', 'Radius', 'WellPump', 'cWell']
                flag = {key[i]: float(line[i]) for i in range(len(key))}
                self.__dict__.update(**flag)
                if self.iWell == 2:
                    self.TanAlfa, self.HwMax = line[5], line[6]
                elif self.iWell == 3:
                    self.zMax, self.pp = line[5], line[6]

            
            if self.NumBP%10 == 0:
                nRow = int(self.NumBP//10)
            else: nRow = int(self.NumBP//10)+1
            f.readline()
            nNode, Width = [], []
            for i in range(nRow):
                line = f.readline().split()
                for l in line:
                    nNode.append(int(l))
            f.readline()
            for i in range(nRow):
                line = f.readline().split()
                for l in line:
                    Width.append(float(l))
            self.nNode, self.Width = np.array(nNode, dtype=int), np.array(Width, dtype=int)
            
            f.readline()
            line = f.readline().split()
            self.L_surf = int(line[0])
            
            if self.NObs != 0:
                f.readline()
                line = f.readline().split()
                self.Obs_nodes = [int(l) for l in line]
            
            f.readline()
            line = f.readline().split()
            self.NPart = int(line[0])
            
            if self.DrainF:
                f.readline()
                f.readline()
                line = f.readline().split()
                self.NDr, self.DrCorr = int(line[0]), int(line[1])
                f.readline()
                line = f.readline().split()
                self.ND = [int(l) for l in line]
                f.readline()
                line = f.readline().split()                
                self.NELD = [int(l) for l in line]
                f.readline()
                line = f.readline().split()                
                self.EfDim = [float(l) for l in line]
                f.readline()
                line = f.readline().split()                
                self.KELDr = [int(l) for l in line]
            
            if self.NumBP%20 == 0:
                nRow = int(self.NumBP//20)
            else: nRow =  int(self.NumBP//20)+1
            
            if self.lChem:
                f.readline()
                f.readline()
                KodCB = []
                for i in range(nRow):
                    line = f.readline().split()
                    for l in line:
                        KodCB.append(l)
                self.KodCB = np.array(KodCB, dtype=int)

            if self.lTemp:
                f.readline()
                f.readline()
                KodTB = []
                for i in range(nRow):
                    line = f.readline().split()
                    for l in line:
                        KodTB.append(l)
                self.KodTB = np.array(KodTB, dtype=int)

    def read_Selector(self):
        with open(self.path+'\\Selector.in', 'r') as f:
            f.readline()
            f.readline()
            f.readline()
            self.Heading = f.readline()

            f.readline()            
            self.LUnit = f.readline()
            self.TUnit = f.readline()
            self.MUnit = f.readline()
            
            f.readline()
            line = f.readline().split()
            self.Kat = int(line[0])

            f.readline()
            line = f.readline().split()
            self.MaxIt, self.TolTh, self.TolH= int(line[0]), float(line[1]), int(line[2])
            self.InitH_W = self._str2bool(line[3])
            
            f.readline()
            line = f.readline().split()
            f.readline()
            line += f.readline().split()
            key = ['lWat', 'lChem', 'lSink', 'Short', 'Inter', 'lScrn', 'AtmIn',
                   'lTemp', 'lWTDep', 'lEquil', 'lExtGen', 'lInv', 'lUnsatCh',
                   'lCFSTr', 'lHP2', 'lActRSU', 'lRootGr']
            flag = {key[i]: self._str2bool(line[i]) for i in range(len(key))}
            self.__dict__.update(**flag)

            f.readline()
            line = f.readline().split()
            self.PrintStep, self.PrintInterval = int(line[0]), int(line[1])
            self.lEnter = self._str2bool(line[2])

            f.readline()
            f.readline()
            line = f.readline().split()
            self.NMat, self.NLay, self.hTab1, self.hTabN = int(line[0]), int(line[1]), float(line[2]), int(line[3])
            f.readline()
            line = f.readline().split()
            self.Model, self.Hysteresi =  int(line[0]), int(line[1])
            
            if self.Hysteresis != 0:
                f.readline()
                line = f.readline().split()
                self.iKappa = int(line[0])

            f.readline()
            self.materials = []            
            for i in range(self.NMat):
                line = f.readline().split()
                self.materials.append(line)

            f.readline()
            f.readline()
            line = f.readline().split()
            f.readline()
            line += f.readline().split()
            
            key = ['dt', 'dtMin', 'dtMax', 'DMul', 'DMul2', 'ItMin', 'ItMax', 
                   'MPL', 'tInit', 'tMax']
            flag = {key[i]: float(line[i]) for i in range(len(key))}
            self.__dict__.update(**flag)
            
            f.readline()
            TPrint = []
            if self.MPL%6 == 0:
                nRow = int(self.MPL//6)
            else: nRow = int(self.MPL//6)+1            
            for i in range(nRow):
                    line = f.readline().split()
                    for l in line:
                        TPrint.append(l)
            self.TPrint = np.array(TPrint, dtype=int)
            
            if self.lChem:
                f.readline()
                f.readline()
                line = f.readline().split()
                f.readline()
                line += f.readline().split()
                self.Epsi = float(line[0])
                key = ['lUpW', 'lArtD', 'lTDep', 'cTolA', 'cTolR', 'MaxItC',
                       'PeCr', 'NS', 'Tortuosity', 'Bacter', 'Filtration',
                       'lWatDep', 'lInitM', 'lInitEq', 'lTortM', 'lFumigant']
                flag = {key[i]: self._str2bool(line[1+i]) for i in range(len(key))
                        if not i in range(3, 8)}
                self.__dict__.update(**flag)
                flag = {key[i]: int(line[1+i]) for i in range(3, 8)}
                self.__dict__.update(**flag)


                f.readline()
                self.soil_param = []
                for i in range(self.NMat):
                    line = f.readline().split()
                    self.soil_param.append(line)
                
                f.readline()
                self.solute_param = []
                for i in range(self.NS):
                    line = f.readline().split()
                    self.solute_param.append(line)

                f.readline()
                self.react_param = []
                for i in range(self.NMat):
                    line = f.readline().split()
                    self.react_param.append(line)
                
                if self.lTDep:
                    self.TDep_params = []
                    f.readline()
                    f.readline()
                    for i in range(self.NS):
                        line = f.readline().split()
                        self.TDep_params.append(line)
                    f.readline()
                    for i in range(self.NS):
                        line = f.readline().split()
                        self.TDep_params[i] = self.TDep_params[i]+line
                
                f.readline()
                self.cBnds = []
                for i in range(self.NS):
                    line = f.readline().split()
                    self.cBnds.append(line)
                
                f.readline()
                line = f.readline().split()
                self.tPulse = int(line[0])
                
                if self.lFumigant:
                    f.readline()
                    line = f.readline().split()
                    self.lAddFum = self._str2bool(line[0])
                    if self.lAddFum:
                        f.readline()
                        line = f.readline().split()
                        f.readline()
                        line += f.readline().split()
                        key = ['AddFumTime', 'AddFumMass', 'AddFumMinX', 'AddFumMaxX', 'AddFumMinZ', 'AddFumMaxZ']
                        flag = {key[i]: int(line[i]) for i in range(len(key))}
                        self.__dict__.update(**flag)

                if self.lWatDep:
                    self.WTDep_params1, self.WTDep_params2 = [], []
                    f.readline()
                    f.readline()
                    line = f.readline().split()
                    self.nParamWC = int(line[0])
                    for i in range(self.NS):
                        f.readline()
                        line1 = f.readline().split()
                        line2 = f.readline().split()
                        self.WTDep_params1.append(line1)
                        self.WTDep_params2.append(line2)
                
            if self.lTemp:
                f.readline()
                f.readline()
                self.Tpar = []
                for i in range(self.NMat):
                    line = f.readline().split()
                    self.Tpar.append(line)

                f.readline()
                line = f.readline().split()
                self.tBnds = [line]

                f.readline()
                line = f.readline().split()
                self.tAmpl, self.tPeriodHeat = float(line[0]), float(line[1])
            
            if self.lSink:
                f.readline()
                f.readline()
                
                line = f.readline().split()
                self.rootModel, self.OmegaC = bool(int(line[0])), int(line[1])

                if self.rootModel == 0:
                    f.readline()
                    line = f.readline().split()
                    self.uptake_param = line
        #            key = ['P0', 'P2H', 'P2L', 'P3', 'r2H', 'r2L']
        #            flag = {key[i]: float(line[i]) for i in range(len(key))}
        #            self.__dict__.update(**flag)
             
                    f.readline()
                    line = f.readline().split()
                    self.uptake_param.append(line[0])
        #            self.POptm = [float(l) in line]

                elif self.rootModel == 1:
                    f.readline()
                    line = f.readline().split()
                    self.S_shape_Param = line
                
                if self.lChem:
                    f.readline()
                    line = f.readline().split()
                    self.SoluteReduction = self._str2bool(line[0])
                
                    if self.SoluteReduction:
                        f.readline()
                        line = f.readline().split()
                        self.SoluteAdditive = self._str2bool(line[0])
                        if not self.SoluteAdditive:
                            f.readline()
                            line = f.readline().split()
                            self.c50, self.P3c = line[0], line[1]
                            self.aOsm = line[2:2+self.NS]
                            self.lMsSink = line[-1]
                        else:
                            f.readline()
                            line = f.readline().split()
                            self.aOsm = line[:self.NS]
                            self.lMsSink = line[-1]
                if self.lActRSU:
                        f.readline()
                        line = f.readline().split()
                        self.OmegaS, self.SPot, self.KM, self.cMin = line[0], line[1], line[2], line[3]
                        self.OmegaW = self._str2bool(line[4])
             

            if self.lRootGr:
                f.readline()
                f.readline()
                line = f.readline().split()
                self.iRootZoneShape, self.iRootDepthEntry = int(line[0]), int(line[1])

                f.readline()
                line = f.readline().split()
                self.Horizontal, self.NPlants = self._str2bool(line[0]), int(line[1])
                

                if self.iRootZoneShape == 0:
                    f.readline()
                    line = f.readline().split()
                    self.rZm, self.rZ0, self.rA = line[0], line[1], line[2]
                    if self.Horizontal:
                        f.readline()
                        line = f.readline().split()
                        self.rRm, self.rR0, self.rB = line[0], line[1], line[2]
                        self.rCenter = line[3:]

                else:
                    if self.iRootDepthEntry == 0:
                        f.readline()
                        line = f.readline().split()
                        self.RootDepth =  line[0]
                        if self.Horizontal:
                            f.readline()
                            line = f.readline().split()
                            self.RootHalfWidth, self.RootHalfWidth = line[0], line[1]
                            self.rCenter = line[2:]

                    elif self.iRootDepthEntry == 1:
                        f.readline()
                        if self.Horizontal:
                            self.rCenter = f.readline().split()

                if self.iRootDepthEntry == 1:
                    f.readline()
                    line = f.readline().split()
                    self.RootDepth =  line[0]
                    f.readline()
                    self.RootDepth = []
                    for i in range(self.nGrowth):
                        self.RootDepth.append(f.readline().split())
                    
                elif self.iRootDepthEntry == 2:
                    f.readline()
                    if self.Horizontal:
                        self.rCenter = line

                    f.readline()
                    line = f.readline().split()
                    f.readline()
                    line += f.readline().split()
                    key = ['iRFak', 'tRMin', 'tRMed', 'tRMax', 'tPeriodRoot', 'ZRMin', 'ZRMed', 'ZRMax']
                    flag = {key[i]: line[i] for i in range(len(key))}
                    self.__dict__.update(**flag)

                    if self.Horizontal:
                        f.readline()
                        line = f.readline().split()
                        self.rRMin, self.rRMax = line[0], line[1]
