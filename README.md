# Engineering Tools
 Some engineering tools that don't warrant their own repo but that do some useful stuff

### Tools

tstclean.py removes garbage characters that some tools output to allow Keysight ADS to correctly import.

tstscale.py lets you arbitrarily modify loss profiles in a simulation by scaling a fixed dataset. For example you can build a 1.5m cable model from only vendor provided 1m and 2m lengths.

pindelay.py converts English units to metric to make mixing of environments less error prone and more human readable in Cadence Allegro constraint manager.