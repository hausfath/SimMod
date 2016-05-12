import pandas as pd
import numpy as np

#Model Variables
LAYER_HEIGHT = 100.
TOTAL_HEIGHT = 3700.

#Model Constants
HEAT_CAPACITY = 3985. * 1024.5 # J m^-3 K^-1
KAPPA = 5.5 * 10**-5           #m^2 s^-1
OCEAN_PERCENT = 0.71


def diffeqs(df, dt, fradfor, clim_sens):
    """
    Differential equation for flux down.
    """
    steps = df.shape[0]
    df.ix[0, 'fluxdown'] = (
        (((fradfor - clim_sens * df['tocean']) / HEAT_CAPACITY) * dt)[0]
    )
    df['fluxdown'] = (
        (KAPPA * (df['tocean'].shift(1) - df['tocean']) / LAYER_HEIGHT) * dt
    )
    df.ix[0, 'fluxdown'] = (
        (((fradfor - clim_sens * df['tocean']) / HEAT_CAPACITY) * dt)[0]
    )

    df['dtocean'] = (df['fluxdown'].diff(periods = -1) / LAYER_HEIGHT) * dt

    df.ix[(steps - 1), 'dtocean'] = (
        (df['fluxdown'] / LAYER_HEIGHT * dt)[steps - 1]
    )
    return df


def continuous_diffusion_model(results, run_years, dt, clim_sens):
    """
    Implement the continuous diffusion model
    used in Myhrvold and Cairdira (2011).
    """
    z = np.array([np.arange(0, (TOTAL_HEIGHT + LAYER_HEIGHT), LAYER_HEIGHT)]).T
    columns = ['z']
    df = pd.DataFrame(z, columns=columns)
    df['tocean'] = 0
    df['dtocean'] = 0
    df['fluxdown'] = 0
    fradfor = results['total_forcing'][0]
    df = diffeqs(df, dt, fradfor, clim_sens)

    for t in range(0,int(run_years / dt)):
        fradfor = results['total_forcing'][t]
        df['tocean'] += dt * df['dtocean'] * 365 * 24 * 60 * 60
        df = diffeqs(df, dt, fradfor, clim_sens)
        results.ix[t, 't_os'] = df.ix[0, 'tocean']

    results['t_eq'] = results['total_forcing'] / clim_sens
    results['t_s'] = (
        results['t_os'] * OCEAN_PERCENT + 
        results['t_eq'] * (1 - OCEAN_PERCENT)
    )

    return results