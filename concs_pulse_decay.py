import pandas as pd
import numpy as np
from constants import *


def pulse_decay_runner(run_years, dt, emissions):
    """
    Simple pulse response model adapted from Myhrvold and Caldeira (2012)
    adapted from Joos et al (1996)
    """
    df = emissions
    co2_0 = df['rcp_co2_ppm'][0] 
    ch4_0 = df['rcp_ch4_ppb'][0] 
    n2o_0 = df['rcp_n2o_ppb'][0]

    run_year = 0
    df['co2_pg_atm'] = 0
    df['ch4_tg_atm'] = 0
    df['n2o_tg_atm'] = 0
    df['ch4_co2_decay_marginal'] = 0
    while run_year < run_years:
        df['ch4_step'] = (
            df['ch4_tg'][int(run_year / dt)] * 
            np.exp(-(df['date'] - run_year) / CH4_EFOLD)
        )
        df['ch4_step'][0:int(run_year / dt)] = 0
        
        df['ch4_co2_decay'] = (df['ch4_tg'][int(run_year / dt)] - df['ch4_step']) * CO2_PER_TON_CH4 / 10**3
        #convert from TgC to PgC

        df['ch4_co2_decay'][0:int(run_year / dt)] = 0
        df['ch4_co2_decay_marginal'] += df['ch4_co2_decay'].diff(-1) * -1
        df['ch4_co2_decay_marginal'][-1:] = 0

        df['co2_step'] = (
            (df['co2_pg'][int(run_year / dt)] + df['ch4_co2_decay_marginal'][int(run_year / dt)]) * 
            (0.217 + 0.259 * np.exp(-(df['date'] - run_year) / 172.9) + 
            0.338 * np.exp(-(df['date'] - run_year) / 18.51) + 
            0.186 * np.exp(-(df['date'] - run_year) / 1.186))
        )

        df['n2o_step'] = (
            df['n2o_tg'][int(run_year / dt)] * 
            np.exp(-(df['date'] - run_year) / N2O_EFOLD)
        )
        df['co2_step'][0:int(run_year / dt)] = 0
        df['n2o_step'][0:int(run_year / dt)] = 0

        df['co2_pg_atm'] += df['co2_step']
        df['ch4_tg_atm'] += df['ch4_step']
        df['n2o_tg_atm'] += df['n2o_step']

        run_year += dt

    df['co2_ppm']  = (
        co2_0 + (df['co2_pg_atm'] * 10.**15. / GRAMS_PER_MOLE_CO2) / 
        MOLES_IN_ATMOSPHERE * 10.**6.
    )

    df['ch4_ppb']  = (
        ch4_0 + (df['ch4_tg_atm'] * 10.**12. / GRAMS_PER_MOLE_CH4) / 
        MOLES_IN_ATMOSPHERE * 10.**9.
    )

    df['n2o_ppb']  = (
        n2o_0 + (df['n2o_tg_atm'] * 10.**12. / GRAMS_PER_MOLE_N2O) / 
        MOLES_IN_ATMOSPHERE * 10.**9.
    )
    df = df.drop(['ch4_step', 'co2_step', 'n2o_step', 'ch4_co2_decay'], axis=1)
    return df