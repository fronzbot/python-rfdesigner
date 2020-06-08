python-rfdesigner
===================
A Python library built to perform system-level RF analysis.

This library is meant to be flexibile to allow easy construction of simple or complex RF signal chains to analyize and run basic simulations to determine feasibility.

Motivation
-----------
The reason behind making the RFDesigner tool is that I found free tools online lacking the functionality I was looking for.  Excel spreadsheet got lost in the weeds pretty quickly, so I whipped something up in python in an afternoon.  The more I played with that script, the more I realized it could be expanded and be far more useful to others.  Hence this tool.  No python knowledge is required, as the entire tool is accessible via the command-line on systems with Python 3.6 and higher.  A GUI is in the works.

Usage
------

The general flow of this tool is to create a netlist and enter an interactive command-line session.

Netlisting
~~~~~~~~~~~
In order to get started, your first step is to create a `TOML <https://github.com/toml-lang/toml>`__ formatted netlist file.  This file will define one (or more!) signal chains that can be used in the analysis phase.  There are a few simple requirements for the file:

1. For every block being defined, the key must be the position in the signal chain.
2. For every block being defined, a secondary key must exist describing the block type.
3. Any block type being defined must match an implemented feature.

The example below shows a netlist file for a signal chain consisiting of an LNA, Filter, and Amplifer:

.. code:: toml

   [example_system]
   1.type = "LNA"  # Note that the type value is case-insensitive
   1.gain = 25
   1.nf = 1.6

   2.type = "bandpass"
   2.gain = -3

   3.type = "amplifier"
   3.gain = 20
   3.nf = 6
   3.p1db = 8
   3.oip3 = 19


In addition, the special ``[simulation]`` header can be added to allow for simulation properties to be netlisted (and thus not needed when calling a simulation method).  A full example is shown below:

.. code:: toml

   [simulation]
   pin = -45  # Input power for cascade analysis
   bw = 10  # Signal bandwidth in MHz
   temp = 290  # Noise temperature in Kelvin


Prior to entering the interactive session, the following options are available to help construct and validate your netlist:
- The implemented block types can be found by typing ``rfdesigner --implemented``
- To get a list of properties than can be set for each block, use the ``rfdesigner --properties [block name]`` command.
- To validate a generated netlist, run ``rfdesigner --validate [netlist file]`` command. If the netlist is valid, its contents will be printed on screen.

Interactive Session
~~~~~~~~~~~~~~~~~~~~
To perform analysis and simulations with the RFDesigner tool, an interactive shell session can be entered by typing ``rfdesigner``.  You know you're in an interactive RFDesigner session when you see the ``%rf>`` prompt.  From here, there are a variety of commands available:

- ``netlist FILE``: generate a netlist from the input file
- ``show_systems``: show available systems extracted from the netlist (and, thus, available for simulation)
- ``cascade --name=SYSTEM_NAME [opts]``: run cascade analysis on the provided system name (must match a name from the netlist)

Cascade Analysis
~~~~~~~~~~~~~~~~~
The options available for cascade analysis are as follows:

- ``--pin=INPUT_POWER``: Input power in dBm (overrides anything defined in the ``[simulation]`` section of the netlist)
- ``--bw=BANDWIDTH``: Signal bandwidth in MHz
- ``--temp=TEMPERATURE``: Temperature (K) to extract noise floor
- ``--save=RESULTS_DIR``: Directory (or file) to save results (csv formatted)
- ``--no-output``: If this option is used, the results are not printed to the terminal after the simulation is finished
