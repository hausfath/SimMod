import pandas as pd
import numpy as np
from constants import *


def calc_radiative_forcing(concentrations):
    """
    Translate GHG concentrations into radiative forcing using IPCC
    simplified forcing functions for CO2, CH4, and N2O
    """
    concentrations['co2_forcing'] = (
        5.35 * np.log(concentrations['co2_ppm'] / CO2_PPM_1750)
    )

    concentrations['ch4_forcing'] = (
        0.036 * (np.sqrt(concentrations['ch4_ppb']) - np.sqrt(CH4_PPB_1750)) - 
        (func(concentrations['ch4_ppb'], N2O_PPB_1750) - func(CH4_PPB_1750, N2O_PPB_1750))
    ) * CH4_IND_FORCING_SCALAR

    concentrations['n2o_forcing'] = (
        0.12 * (np.sqrt(concentrations['n2o_ppb']) - np.sqrt(N2O_PPB_1750)) - 
        (func(CH4_PPB_1750, concentrations['n2o_ppb']) - func(CH4_PPB_1750, N2O_PPB_1750))
    )

    concentrations['total_forcing_ghg'] = (
        concentrations['co2_forcing'] +
        concentrations['ch4_forcing'] +
        concentrations['n2o_forcing']
    )

    concentrations['rcp_nonghg_forcing'] = (
        concentrations['total_forcing_rcp'] -
        (concentrations['co2_forcing_rcp'] +
         concentrations['ch4_forcing_rcp'] +
         concentrations['n2o_forcing_rcp'])
    )

    concentrations['historic_nonghg_forcings'] = (
        concentrations['hist_forcing_wm2'] - concentrations['total_forcing_ghg']
    )

    concentrations.loc[concentrations['year'] < 2000, 'rcp_nonghg_forcing'] = concentrations['historic_nonghg_forcings']

    concentrations['rcp_nonghg_forcing'].fillna(0., inplace=True)
    concentrations['total_forcing'] = (
        concentrations['total_forcing_ghg'] + 
        concentrations['rcp_nonghg_forcing']
    )

    concentrations['total_forcing_rcp'].fillna(-9999, inplace=True)
    concentrations.loc[concentrations['total_forcing_rcp'] == -9999, 'total_forcing_rcp'] = (
        concentrations['total_forcing_ghg']
    )

    return concentrations


def func(ch4, n2o):
    """
    IPCC simplified function for calculating CH4/N2O spectral overlap
    """
    val = (
        0.47 * np.log(1 + 2.01 * 10**-5 * (ch4 * n2o)**0.75 + 
        5.31 * 10**-15 * ch4 * (ch4 * n2o)**1.52)
    )
    return val