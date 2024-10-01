# Engineering Tools
 Some engineering tools that don't warrant their own repo but that do some useful stuff

### Tools

tstclean.py removes garbage characters that some tools output in Touchstone S-parameter files to allow simulation engines like Keysight ADS to correctly import them.

tstscale.py lets you arbitrarily modify loss profiles in a simulation by scaling a fixed dataset in a Touchstone S-parameter file. For example you can build a 1.5m cable model from only vendor provided 1m or 2m data by linear loss scaling.

pindelay.py converts English units to metric to make mixing of environments less error prone and more human readable in Cadence Allegro constraint manager.  Input assumes Cadence formatted export file in mils, which appears to be what you get in 17.2 regardless of database settings.

cad2hyp.py converts Cadence Allegro board files to ascii for importing into Mentor Hyperlynx, working around a bug/license issue and that kept the automated process from working correctly.  This takes a .brd file as an input and just creates all the correct syntax for the ascii export.

seasim_clean.py cleans up simulation files and resampled .pkl model files when using the Seasim PCI Express channel simulator, for human readability and disk usage limiting.  User controlled selection by age of files to avoid current work.