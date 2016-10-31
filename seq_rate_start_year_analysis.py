import pandas as pd
import numpy as np

from constants import *
from simmod_controller import run_simmod

INIT_YEAR = 2016                #Initial year of reductions (inclusive)
END_YEAR = 2100                 #End year of reductions (inclusive)

run_start_year = 1765.          #Run start year
run_end_year = 2100.            #Inclusive of end year
dt = 1 #/ 100.                  #years
carbon_model = 'pulse response' #'pulse response', 'box diffusion', or 'BEAM'
normalize_2000_conc = True      #Normalize concentrations to historical year-2000 values
c_sens = 1.25                   #Climate sensativity (T = F / LAMBDA)

def test_co2_reduction(run_start_year, run_end_year, dt, rcp):
    base_run = run_simmod(run_start_year, run_end_year, dt, rcp)
    results = base_run[['year']].copy()
    for co2_reduc in range(0,205,5):
        co2_reduc = co2_reduc / 100.
        diffs = (
            run_simmod(run_start_year, run_end_year, dt, rcp, c_sens,
            INIT_YEAR, END_YEAR, co2_reduc, 0, 0)[['year', 't_s']]
        )
        diffs['t_s'] =  diffs['t_s'] - base_run['t_s']
        diffs.rename(columns={'t_s': 't_s'+str(co2_reduc)}, inplace=True)
        results['t_s'+str(co2_reduc)] = diffs['t_s'+str(co2_reduc)]
        print co2_reduc
    results.to_csv('Results/co2_target_year_'+rcp+'.csv')

test_co2_reduction(run_start_year, run_end_year, dt, '2.6')
test_co2_reduction(run_start_year, run_end_year, dt, '4.5')
test_co2_reduction(run_start_year, run_end_year, dt, '6.0')
test_co2_reduction(run_start_year, run_end_year, dt, '8.5')

#results = run_simmod(run_start_year, run_end_year, dt, rcp, c_sens, INIT_YEAR, END_YEAR, 2, 0, 0)
#print results[['year', 't_s']][1990-1765:999999]
#results.to_csv('results/simmod_run_'+rcp+' '+carbon_model+'.csv')
#print results[['year', 'co2_pg']][1990-1765:999999]