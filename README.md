# Thunderchickens
Code repository for FRC team 217: the Thunderchickens

GRIP V1.2.0   2/8/16

    -https://github.com/WPIRoboticsProjects/GRIP/releases
    
VProcessCalc.cpp 1/30/16

    -Is current vision robot code, obtains camera stream, processes image, and outputs/inputs from network tables.
    -Included is basic tank drive logic, to trigger the align to target vision process press and hold button 1.

Bugs:

-Curently running into memory allocation issues with the Native JVM

    -Atempt to remedy: include JVM args to increase overhead and influence Garbage Collection on Rio
    -update:fixed in 1.2.0 needs to be tested
    
-Robot rotates when button is held but doesn't stop when aligned with target(when memory allocation isnt bad)

 *objxCur is not getting properly set from vectors(most ikely as rilog was printing zero for it)

    -Atempt to remedy: included alternate index for vector and different method to obtain vector value at index.

  *Could be going too fast thus bluring the image.

    -Attempt to remedy(not implemented bc above is most likely current error): slow down rotation speed by multiplying visionpid by         lower constant.
 
    
  
  
