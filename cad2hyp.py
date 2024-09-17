"""
This script automates the Allegro to Hyperlynx Boardsim translation process.  File naming for the ASCII export is
extremely rigid and prone to errors, so this script does all that handling.  It takes only a .brd file as an
argument and generates all the output files.  Hyperlynx can then import the textual data by reading file.a_b
Multiple periods in filenames should work but are untested, multiple .brd text strings probably won't, also untested
Control files required are control_hyp.txt and control_hyp2.txt from a Hyperlynx install or peer to this script
"""

from os import system
from os import path
from sys import argv

if(__name__=="__main__"):
   # Simple error checking to make sure the number of arguments is right so we get the filename
   if(len(argv)==1):
      exit("\nNo input file given, program takes filename.brd")
   elif(len(argv)>2):
      exit("\nToo many arguments given, program takes filename.brd")
   else:
      # Simple error checking to make sure the file exists so we don't pass junk to the translation tool
      if(path.isfile(argv[1])):
         print("Opening " + argv[1])
      else:
         exit("\nInput file " + argv[1] + " not found")
      fileName = argv[1].split(".brd")
      fileBase = fileName[0]

   # Build command line calls with ugly brute force for first control file
   osCommand = "extracta " + fileBase + ".brd"
   osCommand = osCommand + " control_hyp.txt " + fileBase + ".a_b "
   osCommand = osCommand + fileBase + "_COMPONENT.txt "
   osCommand = osCommand + fileBase + "_COMPONENT_PIN.txt "
   osCommand = osCommand + fileBase + "_COMPOSITE_PAD.txt "
   osCommand = osCommand + fileBase + "_CONNECTIVITY.txt "
   osCommand = osCommand + fileBase + "_FULL_GEOMETRY.txt "
   osCommand = osCommand + fileBase + "_LAYER.txt"
   print("\nCalling extracta...")
   system(osCommand)

   # Build command line calls with ugly brute force for second control file
   osCommand = "extracta " + fileBase + ".brd"
   osCommand = osCommand + " control_hyp2.txt " + fileBase + "_NET.txt "
   osCommand = osCommand + fileBase + "_RAT_PIN.txt "
   osCommand = osCommand + fileBase + "_SYMBOL.txt"
   print("\nCalling extracta...")
   system(osCommand)

   print("\nTranslation Done!")
