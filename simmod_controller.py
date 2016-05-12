import pandas as pd
import numpy as np

from constants import *
from emissions_parser import emissions
from concs_pulse_decay import pulse_decay_runner
from beam_carbon.beam import BEAMCarbon
beam = BEAMCarbon()
from radiative_forcing import calc_radiative_forcing
from heat_diffusion import continuous_diffusion_model

#Model Parameters
run_start_year = 1765.          #Run start year
run_end_year = 2100.            #Inclusive of end year
dt = 1 #/ 100.                  #years
rcp = '2.6'                     #RCP scenario
carbon_model = 'pulse response' #'pulse response', 'box diffusion', or 'BEAM'
normalize_2000_conc = True      #Normalize concentrations to historical year-2000 values
LAMBDA = 1.25                   #Climate sensativity (T = F / LAMBDA)

#BEAM Model Settings (when relevant)
SUBSTEPS = 100                  #Break each timestep into this many substeps
INIT_MAT = 596.                 #In GtC; 596 = preindustrial; 809 = 2005
INIT_MUP = 713.                 #In GtC; 713 = preindustrial; 725 = 2005
INIT_MLO = 35625.               #In GtC; 35625 = preindustrial; 35641 = 2005

#Ocean Box Diffusion Model Settings (when relevant)
MIXING = 'probable'             #options 'fast', 'slow', or 'probable'
DZ = 100                        #meters - thickness of each layer in the deep ocean


def run_simmod(run_start_year, run_end_year, dt, rcp, add_year = 0, c_add = 0, ch4_add = 0, n2o_add = 0):
    """
    Run the various parts of SimMod and export images and CSV files.
    """
    run_years = (run_end_year - run_start_year + 1)
    emission_vals = emissions(run_start_year, run_end_year, dt, rcp, add_year, c_add, ch4_add, n2o_add)

    conc = pulse_decay_runner(run_years, dt, emission_vals)

    if carbon_model == 'BEAM':
        beam._initial_carbon = np.array([596., 713., 35625.])
        beam.intervals = SUBSTEPS
        beam.time_step = dt
        beam.emissions = emission_vals['co2_pg'] / C_TO_CO2
        beam_results = pd.melt(beam.run()[0:1])
        conc['co2_ppm'] = beam_results['value'] * PGC_TO_MOL * 1e6 / MOLES_IN_ATMOSPHERE

    if carbon_model == 'box diffusion':
        box_diffusion_results = box_diffusion_model(
            emission_vals, 
            dt, 
            DZ, 
            MIXING
        )
        conc['co2_ppm'] = box_diffusion_results['co2ppm']

    if normalize_2000_conc == True:
        conc['co2_ppm'] = (
            conc['co2_ppm'] - 
            conc.loc[conc['year'] == 2000, 'co2_ppm'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_co2_ppm'].min()
        )
        conc['ch4_ppb'] = (
            conc['ch4_ppb'] - 
            conc.loc[conc['year'] == 2000, 'ch4_ppb'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_ch4_ppb'].min()
        )
        conc['n2o_ppb'] = (
            conc['n2o_ppb'] - 
            conc.loc[conc['year'] == 2000, 'n2o_ppb'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_n2o_ppb'].min()
        )

    forcing = calc_radiative_forcing(conc)
    warming = continuous_diffusion_model(forcing, run_years, dt, LAMBDA)
    return warming

results = run_simmod(run_start_year, run_end_year, dt, rcp)
results.to_csv('results/simmod_run_'+rcp+' '+carbon_model+'.csv')
