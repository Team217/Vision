#server code this is what would be on the robot
#can be used to read in values that client sends to it
import time
from networktables import NetworkTable

import logging
logging.basicConfig(level=logging.DEBUG)

sd = NetworkTable.getTable("SmartDashboard")

#attempt to grab value from server
while True:
    try:
        print('value:', sd.getNumber('VALUE'))
    except KeyError:
        print('value: N/A')#in case it cant grab it
 
    time.sleep(1)
