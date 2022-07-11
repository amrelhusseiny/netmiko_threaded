# netmiko_threaded
 This script runs the standard simple Netmiko connection in a prallel threaded manner , in this example , we are running 30 threads in parallel , and then writing Output and Error files .
## Requiremnts : 
    - Python 3.6 or later 
    - Netmiko library installed
    - Devices to have the same type , user , password , or you can edit the list of dictionaries to add the user and password per device 
## Output Files : 
    - output.txt : This will include the output of your commands per device .
    - errors.txt : This file will include the devices that were unable to login or were unable to execute the commands to .


