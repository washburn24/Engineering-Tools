"""
This script generates arbitrarily long HSpice stimulus files with user controlled
jitter profiles injected.  It's purpose is to allow known jitter to be input to
HSpice simulations to generate data in the format that an analysis or statistical
tool might use.  It's usefulness is in the validation of software, as many of
such tools require much longer data patterns than would be normal in a simulation,
though it's probably general enough to be used for some channel analysis.
"""
import random, string, math, sys

# User Sets These Parameters
numBits = int(4e2)    # Number of bits needed (desired simulation length/UI)
bitRate = 8e9         # PCI Express Bit Rate
freqJitter = 8e6      # Frequency of Sinusoidal Jitter
targetJitter = 20     # Max peak-to-peak jitter desired around nominal (in ps)
riseTime = 10         # Rise Time of stimulus signal (in ps)

bitStream = [0 for j in range (numBits)]
timeError = [0 for j in range (numBits)]
#fileWrite = open('jitter.txt','w')
bitPeriod = 1/bitRate; runTime = bitPeriod*numBits; countArgs=0
unitStep = runTime/(10*numBits); dataPoints = runTime/unitStep
riseTime = riseTime*1e-12; print ("\nGenerating stimulus..",)
maxError=0; outFile = "stimulus.inc"

# Can set output file from command line 'c:>hspstim.py whatever.inc'
for arg in sys.argv:
    if(countArgs>0):
        outFile = sys.argv[1]
    countArgs=countArgs+1

#--------------------Use this routine for Gaussian Jitter--------------------#
#print ("\b\b\b with gaussian jitter..",)                                     #
#for i in range (0,numBits):                                                  #
#    timeError[i]=random.gauss(0,1)                                           #
#    if(abs(timeError[i])>maxError): maxError = abs(timeError[i])             #
#    if(i%1000000==0): print ("\b.",)                                         #
#----------------------------------------------------------------------------#

#-------------------Use this routine for Sinusoidal Jitter-------------------#
#print ("\b\b\b with sinusoidal jitter..",)                                   #
#sineClock = [0 for i in range (int(dataPoints+1))]                           #
#for i in range (0,int(dataPoints)):                                          #
#    sineClock[i] = unitStep*i                                                #
#    if(i%3000000==0): print ("\b.",)                                         #
#for i in range (0,numBits):                                                  #
#    timeError[i] = math.sin(2*math.pi*freqJitter*sineClock[i])               #
#    if(abs(timeError[i])>maxError): maxError = abs(timeError[i])             #
#    if(i%1000000==0): print ("\b.",)                                         #
#----------------------------------------------------------------------------#

# Normalize the jitter by using calculated maxError and target jitter number
for i in range (0,numBits):
    if(maxError != 0):
        timeError[i] = (targetJitter/2)*(timeError[i]/maxError)
#    fileWrite.write(str(timeError[i])+"\n")
    if(i%1000000==0): print ("\b.",)
#fileWrite.close()

# Add jitter component to PCIe stimulus and generate output file
fileWrite = open(outFile,'w')
fileWrite.write("vstim stim 0 PWL (\n+ 0 0\n")
for i in range (0,numBits):
    bitStream[i]=random.randint(0,1)
#    if(bitStream[i]==bitStream[i-1]):    # This nested if quasi-enforces 8b/10b
#        if(bitStream[i]==bitStream[i-2]):
#            if(bitStream[i]==bitStream[i-3]):
#                if(bitStream[i]==bitStream[i-4]):
#                    if(bitStream[i]==1):
#                        bitStream[i]=0
#                    else:
#                        bitStream[i]=1

    outStr = "+ " + str((i*bitPeriod+riseTime/2)+(timeError[i]*1e-12))
    if(i!=0):
        if(bitStream[i]!=bitStream[i-1]):  # Print a PWL data point when a bit toggles
            outStr = outStr + "      " + str(bitStream[i]) + "     "
            outStr=outStr+str((i*bitPeriod+riseTime/2)+(timeError[i]*1e-12)+riseTime) + "      "
            if(bitStream[i]==0):
                outStr = outStr + "1\n"
            else:
                outStr = outStr + "0\n"
            fileWrite.write(outStr)
    if(i%100000==0): print ("\b.",)

fileWrite.close()
print ("\bDone!")
#print ("\nJitter Data is is jitter.txt\nHSpice Stimulus is in",outFile)

