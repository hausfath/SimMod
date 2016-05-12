#Constants used in SimMod modules

TEMP_0 = 10.                #Mean Earth surface temp (degrees C)
C_TO_CO2 = 3.67
PGC_TO_MOL = 1e15/12.
MOLES_IN_ATMOSPHERE = 1.8 * 10.**20.
GRAMS_PER_MOLE_CO2 = 44.01
GRAMS_PER_MOLE_CH4 = 16.04
GRAMS_PER_MOLE_N2O = 44.01
CO2_PER_TON_CH4 = 1.5       #Tons CO2 produced when ton CH4 decays
CH4_EFOLD = 10.
N2O_EFOLD = 114.
CO2_PPM_1750 = 277.01467
CH4_PPB_1750 = 721.89411
N2O_PPB_1750 = 272.95961

CH4_IND_FORCING_SCALAR = 1. #0.970 / 0.641 #Based on IPCC AR5 WG1 Chapter 8 Supp Mats table 8.SM.6. 
#Accounts for indirect CH4 forcing due to tropospheric ozone and stratospheric water vapor. Assumed to scale linearly with atmospheric CH4.