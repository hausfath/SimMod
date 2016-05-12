import pandas as pd
import numpy as np

from constants import *
from simmod_controller import run_simmod

run_start_year = 1765.          #Run start year
run_end_year = 2100.            #Inclusive of end year
dt = 1 #/ 100.                  #years
rcp = '8.5'                     #RCP scenario
carbon_model = 'pulse response' #'pulse response', 'box diffusion', or 'BEAM'
normalize_2000_conc = True      #Normalize concentrations to historical year-2000 values
c_add = -1.
ch4_add = -C_TO_CO2 * 1000. / 34.     #Convert to pg co2, divide by 100-year GWP
n2o_add = -C_TO_CO2 * 1000. / 298.    #Convert to pg co2, divide by 100-year GWP


def test_co2_reduction(run_start_year, run_end_year, dt, rcp, c_add):
    base_run = run_simmod(run_start_year, run_end_year, dt, rcp)
    results = base_run[['year']].copy()
    for t in range(2001,2101):
        diffs = run_simmod(run_start_year, run_end_year, dt, rcp, t, c_add, 0, 0)[['year', 't_s']]
        diffs['t_s'] =  diffs['t_s'] - base_run['t_s']
        diffs.rename(columns={'t_s': 't_s'+str(t)}, inplace=True)
        results['t_s'+str(t)] = diffs['t_s'+str(t)]
    results.to_csv('Results/co2_mit_eff_results_'+rcp+'.csv')


def test_ch4_reduction(run_start_year, run_end_year, dt, rcp, ch4_add):
    base_run = run_simmod(run_start_year, run_end_year, dt, rcp)
    results = base_run[['year']].copy()
    for t in range(2001,2101):
        diffs = run_simmod(run_start_year, run_end_year, dt, rcp, t, 0, ch4_add, 0)[['year', 't_s']]
        diffs['t_s'] =  diffs['t_s'] - base_run['t_s']
        diffs.rename(columns={'t_s': 't_s'+str(t)}, inplace=True)
        results['t_s'+str(t)] = diffs['t_s'+str(t)]
    results.to_csv('Results/ch4_mit_eff_results_'+rcp+'.csv')


def test_n2o_reduction(run_start_year, run_end_year, dt, rcp, n2o_add):
    base_run = run_simmod(run_start_year, run_end_year, dt, rcp)
    results = base_run[['year']].copy()
    for t in range(2001,2101):
        diffs = run_simmod(run_start_year, run_end_year, dt, rcp, t, 0, 0, n2o_add)[['year', 't_s']]
        diffs['t_s'] =  diffs['t_s'] - base_run['t_s']
        diffs.rename(columns={'t_s': 't_s'+str(t)}, inplace=True)
        results['t_s'+str(t)] = diffs['t_s'+str(t)]
    results.to_csv('Results/n2o_mit_eff_results_'+rcp+'.csv')

test_co2_reduction(run_start_year, run_end_year, dt, rcp, c_add)
test_ch4_reduction(run_start_year, run_end_year, dt, rcp, ch4_add)
test_n2o_reduction(run_start_year, run_end_year, dt, rcp, n2o_add)
