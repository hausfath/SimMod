#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from math import floor
import numpy as np


class Temperature(object):
    def __init__(self, time_step, periods, n):
        self.time_step = time_step
        self.periods = periods
        self.n = n

    @property
    def initial_temp(self):
        return np.array([.7307, .0068])

    @property
    def forcing_ghg_2000(self):
        """Value from DICE2010
        """
        return .83

    @property
    def forcing_ghg_2100(self):
        return .30

    @property
    def transfer_matrix(self):
        """Values from DICE2010
        """
        return np.array([.208, 0., .310, .050])

    @property
    def forcing_co2_doubling(self):
        return 3.8

    @property
    def temp_co2_doubling(self):
        return 3.2

    @property
    def mass_pi(self):
        """Pre-industrial carbon in GtC

        :rtype: float
        """
        return 592.14

    @property
    def forcing_ghg(self):
        """F_EX, Exogenous forcing for other greenhouse gases

        Returns:
            :return: Array of forcing values
            :rtype: np.ndarray

        """
        _n = int(floor(100 / self.time_step))
        a = self.forcing_ghg_2000 + (1. / _n) * (
                self.forcing_ghg_2100 - self.forcing_ghg_2000
            ) * np.arange(_n + 1)
        b = self.forcing_ghg_2100 * np.ones(self.n - (_n + 1)) \
            if self.n > _n \
            else np.array([])
        return np.concatenate((a, b))[:self.n]

    def forcing(self, index, mass_atmosphere):
        """F, Forcing, W/m^2

        Args:
            :param index: Current time step
            :type index: int
            :param mass_atmosphere: Carbon mass in the atmosphere, GtC
            :type mass_atmosphere: float

        Returns:
            :return: Forcing
            :rtype: float

        """
        return (
            self.forcing_co2_doubling *
            (np.log(
                mass_atmosphere / self.mass_pi
            ) / np.log(2)) + self.forcing_ghg[index]
        )

    def temp_ocean(self, temp_atmosphere, temp_ocean):
        """T_LO, increase in atmospheric temperature since 1750, degrees C

         Args:
            :param temp_atmosphere: Atmospheric temperature at t-1
            :type temp_atmosphere: float
            :param temp_ocean: Ocean temperature at t-1
            :type temp_ocean: float

        Returns:
            :returns: T_Ocean(t-1) + ξ_4 * (T_AT(t-1) - T_Ocean(t-1))
            :rtype: float
        """
        return (
            temp_ocean + self.transfer_matrix[3] *
            (temp_atmosphere - temp_ocean)
        )


class DICETemperature(Temperature):

    def temp_atmosphere(self, index, temp_atmosphere, temp_ocean,
                        mass_atmosphere, **kwargs):
        """T_AT, increase in atmospheric temperature since 1750, degrees C

         Args:
            :param temp_atmosphere: Atmospheric temperature at t-1
            :type temp_atmosphere: float
            :param temp_ocean: Lower ocean temperature at t-1
            :type temp_ocean: float
            :param forcing: Forcings at t
            :type forcing: float

        Returns:
            :returns: T_AT(t-1) + ξ_1 * (F(t) - F2xCO2 / T2xCO2 * T_AT(t-1) - ξ_3 * (T_AT(t-1) - T_Ocean(t-1)))
            :rtype: float
        """
        return (
            temp_atmosphere +
            self.transfer_matrix[0] * (
                self.forcing(index, mass_atmosphere) - (
                    self.forcing_co2_doubling / self.temp_co2_doubling) *
                temp_atmosphere - self.transfer_matrix[2] *
                (temp_atmosphere - temp_ocean)))


class LinearTemperature(Temperature):
    def temp_atmosphere(self, *args, **kwargs):
        # return (
        #     self.initial_temp[0] +
        #     kwargs['carbon'] * (
        #         self.temp_co2_doubling / ((
        #             2 * self.mass_pi + (
        #                 2 * self.mass_pi -
        #                 (kwargs['initial_carbon'][0] * kwargs['phi11']) -
        #                 (kwargs['initial_carbon'][1] * kwargs['phi21'])
        #             )) * 1e-3)
        #     ) * 1e-3
        # )
        return self.initial_temp[0] + 1.7e-3 * kwargs['carbon']