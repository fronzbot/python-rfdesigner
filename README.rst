python-rfdesigner
===================
A Python library built to perform system-level RF analysis.

This library is meant to be flexibile to allow easy construction of simple or complex RF signal chains to analyize and run basic simulations to determine feasibility.

Motivation
-----------
The reason behind making the RFDesigner tool is that I found free tools online lacking the functionality I was looking for.  Excel spreadsheet got lost in the weeds pretty quickly, so I whipped something up in python in an afternoon.  The more I played with that script, the more I realized it could be expanded and be far more useful to others.  Hence this tool.  No python knowledge is required, as the entire tool is accessible via the command-line on systems with Python 3.6 and higher.  A GUI is in the works.

Usage
------

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


The implemented block types can be found by typing <some command not yet implemented>.

--- TO-DO ---
