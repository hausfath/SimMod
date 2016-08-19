import pandas as pd
import numpy as np

from constants import *
from simmod_controller import run_simmod

INIT_YEAR = 2016                #Initial year of reductions (inclusive)
END_YEAR = 2100                 #End year of reductions (inclusive)

run_start_year = 1765.          #Run start year
run_end_year = 2100.            #Inclusive of end year
dt = 1 #/ 100.                  #years
rcp = '2.6'                     #RCP scenario
carbon_model = 'pulse response' #'pulse response', 'box diffusion', or 'BEAM'
normalize_2000_conc = True      #Normalize concentrations to historical year-2000 values

def test_co2_reduction(run_start_year, run_end_year, dt, rcp, c_sens):
    base_run = run_simmod(run_start_year, run_end_year, dt, rcp, c_sens)
    results = base_run[['year']].copy()
    for co2_reduc in range(0,200,5):
        co2_reduc = co2_reduc / 100.
        for end_year in range (2016, 2101, 1):
            print co2_reduc,
            print end_year
            diffs = (
                run_simmod(run_start_year, run_end_year, dt, rcp, c_sens, 
                INIT_YEAR, end_year, co2_reduc, 0, 0)[['year', 't_s']]
            )
            diffs['t_s'] =  diffs['t_s'] - base_run['t_s']
            #diffs.rename(columns={'t_s': 't_s'+str(co2_reduc)}, inplace=True)
            results.ix[(end_year - 1765), 't_s'+str(co2_reduc)] = diffs['t_s'][END_YEAR - 1765]
    results.to_csv('Results/co2_sat_target_year_'+rcp+'_'+c_sens+'.csv')

#test_co2_reduction(run_start_year, run_end_year, dt, rcp, c_sens)
#results = run_simmod(run_start_year, run_end_year, dt, rcp, add_type = 'continuous', add_year = 2000, c_add = 100)
#results.to_csv('results/simmod_run_'+rcp+' '+carbon_model+'.csv')
#print results[['year', 'co2_pg']][1990-1765:999999]

run_start_year = 1765.          #Run start year
run_end_year = 2100.            #Inclusive of end year
dt = 1 #/ 100.                  #years
rcp = '8.5'                     #RCP scenario
carbon_model = 'pulse response' #'pulse response', 'box diffusion', or 'BEAM'
normalize_2000_conc = True      #Normalize concentrations to historical year-2000 values
c_sens = 0.825
#1.25 for 3 C
#0.825 for 4.5 C
#2.473 for 1.5 C

base_run = run_simmod(run_start_year, run_end_year, dt, rcp, c_sens)
results = base_run[['year']].copy()

co2_reduc = 91 / 100.

diffs = (
    run_simmod(run_start_year, run_end_year, dt, rcp, c_sens, 
    INIT_YEAR, END_YEAR, co2_reduc, 0, 0)[['year', 't_s']]
    )
diffs['t_s'] =  diffs['t_s'] - base_run['t_s']

#print diffs[['year', 't_s']][285:]
print diffs[['year', 't_s']][285:286]
print diffs[['year', 't_s']][310:311]
print diffs[['year', 't_s']][335:]

