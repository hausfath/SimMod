#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from math import floor
import numpy as np
import pandas as pd
from beam_carbon.temperature import DICETemperature, LinearTemperature


__version__ = '0.3'


class BEAMCarbon(object):
    """Class for computing BEAM carbon cycle from emissions input.
    """
    def __init__(self, emissions=None, time_step=1, intervals=10):
        """BEAMCarbon init

        Args:
            :param emissions: Array of annual emissions in GtC, beginning
                in 2005
            :type emissions: list
            :param time_step: Time between emissions values in years
            :type time_step: float
            :param intervals: Number of times to calculate BEAM carbon
                per timestep
            :type intervals: int
        """
        self._temperature_dependent = True
        self._intervals = intervals
        self._time_step = time_step
        self.temperature = DICETemperature(self.time_step, self.intervals, 0)

        if emissions is not None and type(emissions) in [list, np.ndarray]:
            self.emissions = emissions
        else:
            self.emissions = np.zeros(1)

        self._k_1 = 8e-7
        self._k_2 = 4.53e-10
        self._k_h = 1.23e3
        self._A = None
        self._B = None
        self._Alk = 767.

        self._initial_carbon = np.array([808.9, 725., 35641.])
        self._carbon_mass = None

        self._linear_temperature = False

    @property
    def initial_carbon(self):
        """Values for initial carbon in atmosphere, upper and lower oceans
        in GtC. Default values are from 2005.
        """
        return self._initial_carbon

    @initial_carbon.setter
    def initial_carbon(self, value):
        self._initial_carbon = value

    @property
    def carbon_mass(self):
        if self._carbon_mass is None:
            self._carbon_mass = self.initial_carbon.copy()
        return self._carbon_mass

    @carbon_mass.setter
    def carbon_mass(self, value):
        self._carbon_mass = value

    @property
    def transfer_matrix(self):
        """3 by 3 matrix of transfer coefficients for carbon cycle.
        """
        return np.array([
            -self.k_a, self.k_a * self.A * self.B, 0,
            self.k_a, -(self.k_a * self.A * self.B) - self.k_d,
            self.k_d / self.delta,
            0, self.k_d, -self.k_d / self.delta,
        ]).reshape((3, 3,))

    @property
    def emissions(self):
        """Array of emissions values in GtC per year.
        """
        return self._emissions

    @emissions.setter
    def emissions(self, value):
        self._emissions = value
        self.temperature.n = self.n

    @property
    def time_step(self):
        """Size of time steps in emissions array.
        """
        return self._time_step

    @time_step.setter
    def time_step(self, value):
        self._time_step = value
        self.temperature.time_step = self.time_step

    @property
    def n(self):
        return len(self.emissions)

    @property
    def intervals(self):
        """Number of intervals in each time step.
        """
        return self._intervals

    @intervals.setter
    def intervals(self, value):
        self._intervals = value
        self.temperature.periods = self.intervals

    @property
    def k_a(self):
        """Time constant k_{a} (used for building transfer matrix).
        """
        return .2

    @property
    def k_d(self):
        """Time constant k_{d} (used for building transfer matrix).
        """
        return .05

    @property
    def delta(self):
        """Ratio of lower ocean to upper ocean (used for building transfer
        matrix).
        """
        return 50.

    @property
    def k_h(self):
        """CO2 solubility.
        """
        if self._k_h is None:
            self._k_h = self.get_kh(self.temperature.initial_temp[1])
        return self._k_h

    @k_h.setter
    def k_h(self, value):
        self._k_h = value

    @property
    def k_1(self):
        """First dissociation constant.
        """
        if self._k_1 is None:
            self._k_1 = self.get_k1(self.temperature.initial_temp[1])
        return self._k_1

    @k_1.setter
    def k_1(self, value):
        self._k_1 = value

    @property
    def k_2(self):
        """Second dissociation constant.
        """
        if self._k_2 is None:
            self._k_2 = self.get_k2(self.temperature.initial_temp[1])
        return self._k_2

    @k_2.setter
    def k_2(self, value):
        self._k_2 = value

    @property
    def AM(self):
        """Moles in the atmosphere.
        """
        return 1.77e20

    @property
    def OM(self):
        """Moles in the ocean.
        """
        return 7.8e22

    @property
    def Alk(self):
        """Alkalinity in GtC.
        """
        return self._Alk

    @Alk.setter
    def Alk(self, value):
        self._Alk = value

    @property
    def A(self):
        """Ratio of mass of CO2 in atmospheric to upper ocean dissolved CO2.
        """
        if self._A is None:
            if self.temperature_dependent:
                self.k_h = self.get_kh(self.temperature.initial_temp[1])
            self._A = self.get_A()
        return self._A

    @A.setter
    def A(self, value):
        self._A = value

    @property
    def B(self):
        """Ratio of dissolved CO2 to total oceanic carbon.
        """
        if self._B is None:
            self.temp_calibrate(self.temperature.initial_temp[1])
            self._B = self.get_B(self.get_H(self.initial_carbon[1]))
        return self._B

    @B.setter
    def B(self, value):
        self._B = value

    @property
    def salinity(self):
        """Salinity in g / kg of seawater.
        """
        return 35.

    @property
    def temperature_dependent(self):
        """Switch for calculating temperature-dependent parameters k_1,
        k_2, and k_h.
        """
        return self._temperature_dependent

    @property
    def linear_temperature(self):
        return self._linear_temperature

    @linear_temperature.setter
    def linear_temperature(self, value):
        if value:
            self.temperature = LinearTemperature(self.time_step,
                                                 self.intervals, self.n)
        else:
            self.temperature = DICETemperature(self.time_step,
                                               self.intervals, self.n)
        self._linear_temperature = value

    @temperature_dependent.setter
    def temperature_dependent(self, value):
        if type(value) is bool:
            self._temperature_dependent = value
        else:
            raise TypeError('BEAMCarbon.temperature_dependent must be True or False.')

    def temp_calibrate(self, to):
        """Recalibrate temperature-dependent parameters k_1, k_2, and k_h.
        """
        self.k_1 = self.get_k1(to)
        self.k_2 = self.get_k2(to)
        self.k_h = self.get_kh(to)
        self.A = self.get_A()

    def get_B(self, h):
        """Calculate B (Ratio of dissolved CO2 to total oceanic carbon),
         given H (the concentration of hydrogen ions)

        :param h: H, concentration of hydrogen ions [H+] (the (pH) of seawater)
        :type h: float
        :return: B, ratio of dissolved CO2 to total oceanic carbon
        :rtype: float
        """
        return 1 / (1 + self.k_1 / h + self.k_1 * self.k_2 / h ** 2)

    def get_A(self):
        """Calculate A based on temperature-dependent changes in k_h

        :return: A
        :rtype: float
        """
        return self.k_h * self.AM / (self.OM / (self.delta + 1))

    def get_H(self, mass_upper):
        """Solve for H+, the concentration of hydrogen ions
        (the (pH) of seawater).

        :param mass_upper: Carbon mass in ocenas in GtC
        :type mass_upper: float
        :return: H
        :rtype: float
        """
        p0 = 1
        p1 = (self.k_1 - mass_upper * self.k_1 / self.Alk)
        p2 = (1 - 2 * mass_upper / self.Alk) * self.k_1 * self.k_2
        return max(np.roots([p0, p1, p2]))

    def get_kh(self, temp_ocean):
        """Calculate temperature dependent k_h

        :param temp_ocean: ocean temperature (C)
        :type temp_ocean: float
        :return: k_h
        :rtype: float
        """
        t = 283.15 + temp_ocean
        k0 = np.exp(
            9345.17 / t - 60.2409 + 23.3585 * np.log(t / 100.) +
            self.salinity * (
                .023517 - .00023656 * t + .0047036 * (t / 100.) ** 2))
        kh = 1 / (k0 * 1.027) * 55.57
        self.A = kh * self.AM / (self.OM / (self.delta + 1.))
        return kh

    def get_pk1(self, t):
        return (
            -13.721 + 0.031334 * t + 3235.76 / t + 1.3e-5 * self.salinity * t -
            0.1031 * self.salinity ** 0.5)

    def get_pk2(self, t):
        return (
            5371.96 + 1.671221 * t + 0.22913 * self.salinity +
            18.3802 * np.log10(self.salinity)) - (128375.28 / t +
            2194.30 * np.log10(t) + 8.0944e-4 * self.salinity * t +
            5617.11 * np.log10(self.salinity) / t) + 2.136 * self.salinity / t

    def get_k1(self, temp_ocean):
        """Calculate temperature dependent k_1

        :param temp_ocean: ocean temperature (C)
        :type temp_ocean: float
        :return: k_1
        :rtype: float
        """
        return 10 ** -self.get_pk1(283.15 + temp_ocean)

    def get_k2(self, temp_ocean):
        """Calculate temperature dependent k_2

        :param temp_ocean: ocean temperature (C)
        :type temp_ocean: float
        :return: k_2
        :rtype: float
        """
        return 10 ** -self.get_pk2(283.15 + temp_ocean)

    def run(self):
        N = self.n * self.intervals
        self.carbon_mass = self.initial_carbon.copy()
        total_carbon = 0
        emissions = np.zeros(3)
        temp_atmosphere, temp_ocean = self.temperature.initial_temp

        output = np.tile(np.concatenate((
            self.initial_carbon,
            self.temperature.initial_temp,
            np.array([
                self.transfer_matrix[0][1], self.transfer_matrix[1][1]]),
            np.zeros(3),
        )).reshape((10, 1)).copy(), (self.n + 1, ))
        output = pd.DataFrame(
            output,
            index=['mass_atmosphere', 'mass_upper', 'mass_lower',
                   'temp_atmosphere', 'temp_ocean', 'phi12', 'phi22',
                   'cumulative', 'A', 'B'],
            columns=np.arange(self.n + 1) * self.time_step,
        )

        for i in xrange(N):

            _i = int(floor(i / self.intervals)) # time_step

            if i % self.intervals == 0 and self.temperature_dependent:
                self.temp_calibrate(temp_ocean)

            h = self.get_H(self.carbon_mass[1])
            self.B = self.get_B(h)

            emissions[0] = self.emissions[_i] * self.time_step / self.intervals
            total_carbon += emissions[0]

            self.carbon_mass += (
                (self.transfer_matrix *
                 np.divide(self.carbon_mass, self.intervals)).sum(axis=1) +
                emissions)

            if (i + 1) % self.intervals == 0:

                emissions[0] = self.emissions[_i] * self.time_step
                total_carbon += emissions[0]

                ta = temp_atmosphere
                temp_atmosphere = self.temperature.temp_atmosphere(
                    index=_i, temp_atmosphere=ta,
                    temp_ocean=temp_ocean, mass_atmosphere=self.carbon_mass[0],
                    carbon=total_carbon, initial_carbon=self.initial_carbon,
                    phi11=self.transfer_matrix[0][0],
                    phi21=self.transfer_matrix[1][0])
                temp_ocean = self.temperature.temp_ocean(
                    ta, temp_ocean)

                output.iloc[:, _i + 1] = (
                    np.concatenate((self.carbon_mass.copy(),
                                    np.array([temp_atmosphere, temp_ocean]),
                                    np.array([self.transfer_matrix[0][1],
                                              self.transfer_matrix[1][1],
                                              total_carbon,
                                              self.A, self.B]))))

        return output


def main():
    def create_args():
        import argparse
        parser = argparse.ArgumentParser(
            description='TKTK.'
        )
        input_group = parser.add_mutually_exclusive_group()
        input_group.add_argument(
            '-e', '--emissions', type=str,
            help='Comma separated values to use as emissions input.')
        input_group.add_argument(
            '-c', '--input', '--csv', type=str,
            help='Path to CSV file to use as input.')
        parser.add_argument(
            '-t', '--timestep', type=float, default=1,
            help='Time step for input values in years. Default is 1.')
        parser.add_argument(
            '-i', '--intervals', type=int, default=10,
            help='BEAM calculation intervals per time step. Default is 10.')
        parser.add_argument(
            '-o', '--output', type=str, default='beam_output.csv',
            help='Write values to CSV file instead of stdout')

        return parser.parse_args()

    args = create_args()

    def run_beam(e):
        beam = BEAMCarbon(e)
        if args.timestep:
            beam.time_step = args.timestep
        if args.intervals:
            beam.intervals = args.intervals
        return beam.run()

    def write_beam(output, csv=None):
        if csv is not None:
            output.to_csv(csv)
        else:
            print(output.to_string())
        return True

    csv = args.output if args.output else None
    emissions = np.array([float(n) for n in args.emissions.split(',')]) \
        if args.emissions else None

    if args.input:
        with open(args.input, 'r') as f:
            for line in f:
                write_beam(run_beam(line.split(',')), csv=csv)
    else:
        write_beam(run_beam(emissions), csv=csv)


if __name__ == '__main__':
    b = BEAMCarbon()
    b.time_step = 10.
    b.intervals = 200
    N = 100
    b.emissions = np.array([
        # 7.10, 7.97,
        9.58, 12.25, 14.72, 16.07, 17.43, 19.16, 20.89, 23.22, 26.15, 29.09
    ])
    # df = pd.DataFrame.from_csv('webDICE-CSV.csv', header=-1, index_col=0)
    # b.emissions = np.array(df.ix['emissions_total', :])
    # b.emissions = np.concatenate((10. * np.exp(-np.arange(N) / 40), np.zeros(100-N)))
    b.temperature_dependent = False
    b.linear_temperature = False
    r = b.run()
    print(r)