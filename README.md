# Engineering Tools
 Some engineering tools that don't warrant their own repo but that do some useful stuff

### Tools

tstclean.py removes garbage characters that some tools output in Touchstone s-paramter files to allow Keysight ADS to correctly import them.

tstscale.py lets you arbitrarily modify loss profiles in a simulation by scaling a fixed dataset in a Touchstone s-paramter file. For example you can build a 1.5m cable model from only vendor provided 1m or 2m lengths by linear loss scaling.

pindelay.py converts English units to metric to make mixing of environments less error prone and more human readable in Cadence Allegro constraint manager.  Input assumes Cadence formatted export file in mils.

cad2hyp.py converts Allegro board files to ascii for importing into Mentor Hyperlynx simulation tools, working around a bug and/or licensing issue that kept the automated process from working.