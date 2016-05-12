# BEAM Carbon

## Installation
1. Clone the repo: `git clone https://github.com/RDCEP/BEAM-carbon.git`.

2. `cd` into the directory.

3. A typical `python setup.py install` should suffice.
  
## Usage
BEAM carbon can be run in python or a command line.

### In python

1. Import the BEAMCarbon object 
   
    `from beam_carbon.beam import BEAMCarbon`
    
    `beam = BEAMCarbon()`

2. Set the emissions values

    `beam.emissions = [10., 13., 15., ]`
    
3. The following example specifies decadal time steps for emissions values and calculates
   BEAM 10 times each year (or 100 times per 10-year time step).

    `beam.time_step = 10` 
    
    `beam.intervals = 100`
    
4. Finally, run BEAM.

    `beam.run()`
    
5. Several properties of the BEAMCarbon object can affect its output. You
   can use either a DICE-like or linear temperature model. For more detailed
   runs you can also turn off the temperature-dependent recalibration of k_{1},
   k_{2} and k_{h}. 
   
### Command line

* `beam_carbon -h` will acquaint you with the basic options.

* Emissions can be specified as a comma-separated list (without any spaces)
  or in a CSV file with no header row or column:
    
    `beam_carbon -e 10,13,15`
    
    `beam_carbon --csv "./emissions.csv"`
    
* Output is sent to `stdout` but cen be directed to a CSV file instead:
 
    `beam_carbon -e 10,13,15 -o "./beam_output.csv"`
    
* As in python, the emissions time step and BEAM interval can be specified:

    `beam_carbon -e 10,13,15 --timestep 10 --interval 100`

## License

This code is distributed under the Apache 2 License.