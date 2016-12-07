#client code what would be on driver station
#send whatever you want to the table
#here is where one can make a cli interface or read from a file
import sys
import time
from networktables import NetworkTable
import logging
from PythonApplication1 import logging
logging.basicConfig(level=logging.DEBUG)


NetworkTable.setIPAddress("127.0.0.1")#for robot will be 10.2.17.2 aka ip of rio
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("SmartDashboard")

value=217

while True:
    print('Sending... ', value)
    sd.putNumber('VALUE', value)
    time.sleep(1)
    
