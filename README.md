# SimMod - Python Simple Climate Model
Version 0.3 (Alpha - may contain bugs!)
![SimMod vs. CMIP5](https://s3.postimg.org/qhll0hqqb/simmod_cmip5_temperature_comparison_python.png)

## Usage
0. Make sure you have numpy and pandas installed.
1. Open simmod_controller.py in your editing tool of choice
2. Select desired parameters for RCP, carbon model, climate sensitivity, etc.
3. Run simmod_controller.py in your terminal via python simmod_controller.py
4. Results will be saved as a csv in the SimMod/results folder.

## Notes
The heat diffusion module that converts radiative forcing to global mean
surface temperatures currently breaks for timesteps other than 1 year.
This will be fixed in the near future.

The BEAM carbon model overestimates 2100 atmospheric CO2 concentrations
by ~25% relative to RCP scenarios. Using the pulse response carbon model
is recommended for the time being.

The latest BEAM model can be found here: https://github.com/RDCEP/BEAM-carbon/find/master

##CSV Output Legend
MODEL INPUTS/DIAGNOSTIC VALUES

date - Count of timesteps since specified run_start_year

year - Calendar Year

co2_pg - Emissions of CO2 by timestep from selected RCP

ch4_tg - Emissions of CH4 by timestep from selected RCP

n2o_tg - Emissions of N20 by timestep from selected RCP

co2_forcing_rcp - Radiative forcing of CO2 in selected RCP; for comparison purposes

ch4_forcing_rcp - Radiative forcing of CH4 in selected RCP; for comparison purposes

n2o_forcing_rcp - Radiative forcing of N2O in selected RCP; for comparison purposes

total_forcing_rcp - Total radiative forcing in selected RCP; for comparison purposes

rcp_co2_ppm - CO2 ppm in selected RCP; for comparison purposes

rcp_ch4_ppb - CH4 ppm in selected RCP; for comparison purposes

rcp_n2o_ppb - N2O ppm in selected RCP; for comparison purposes



MODEL OUTPUTS

co2_pg_atm - Atmospheric CO2 concentration (in Pg CO2)

ch4_tg_atm - Atmospheric CH4 concentration (in Tg CH4)

n2o_tg_atm - Atmospheric N2O concentration (in Tg N2O)

ch4_co2_decay_marginal - Additional CO2 from oxidation of CH4 (in Pg)

co2_ppm - Parts per million CO2

ch4_ppb - Parts per billion CH4

n2o_ppb - Parts per billion N2O

co2_forcing - Radiative forcing (watts/m^2) from CO2

ch4_forcing - Radiative forcing (watts/m^2) from CH4

n2o_forcing - Radiative forcing (watts/m^2) from N2O

total_forcing_ghg - Total radiative forcing from GHGs

rcp_nonghg_forcing - Non-GHG radiative forcing (taken from RCP)

total_forcing - Sum of GHG and non-GHG forcing

t_os - Aquaworld transient temperature response (no land fraction)

t_eq - Equilibrium temperature reponse (no oceans)

t_s - Transient temperature response (land/ocean)

## License
This code is distributed under the Apache 2 License.

