# netmiko_threaded.py

# Standard libraries
import logging
from sys import stdout
from multiprocessing.pool import ThreadPool
# Non-standard libraries 
from netmiko import BaseConnection , ConnectHandler

# Configuring Log format for Console 
date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s || %(levelname)s || %(message)s"
logging.basicConfig(format= message_format, datefmt= date_strftime_format, stream=stdout , level=logging.INFO)

# List of devices to multi thread 
example_devices_list = [
							{'host_name' : '#########','ip_address' : '#######'},
						]

def connect_to_device(device_dictionary):
    '''
    Descrption : use Netmiko SSH to devices - Execute the commands needed - Append to file 02_output.txt
    Output :
        No return - save to file
    '''
    logging.info(f' {device_dictionary["host_name"]} ( {device_dictionary["ip_address"]} - Logging in progress )')
    try:
        device_dictionary = {
                    'device_type': '###############',  
                    'host': device_dictionary["ip_address"],
                    'username': '##############',
                    'password' : '############',
                    # 'verbose': False ,        # Uncomment if you need to disable the information Logs of Netmiko to appear in stout
                    # 'session_log': 'log.txt', # Uncomment this line to debug NetmikoConnection in the log file
                    # 'global_delay_factor': 2, # Uncomment if your devices or commands need increased delay 
                }
        net_connect = ConnectHandler(**device_dictionary) # returns Netmiko BaseConnection class instance
        net_connect.find_prompt() # Wait for prompt before proceed
        logging.info(f' {device_dictionary["host_name"]} - Logged in successfully ')
        output = '######################## Start of '+device_dictionary["host_name"]+' Output ########################  \n\r '
        # --------------------------------------------------------------------------
        # Put your commands here , you can replicate the line for multipple commands on the same device
        # --------------------------------------------------------------------------
        output += net_connect.send_command("screen-length 0 tem")
        # --------------------------------------------------------------------------
        # Writing output to file
        output = '######################## End of '+device_dictionary["host_name"]+' Output ########################  \n\r '
        with open("output.txt", "a") as file_object:
            file_object.write(output)
        logging.info(f' {device_dictionary["host_name"]} - Output Generated ')
    except Exception as e:
        logging.error(f' {device_dictionary["host_name"]} ( {device_dictionary["ip_address"]} - Not Parsed )')
        with open("errors.txt", "a") as file_object:
            file_object.write(f' {device_dictionary["host_name"]} ( {device_dictionary["ip_address"]} - Not Parsed )')
            file_object.write(f' {device_dictionary["host_name"]} Error : {e}')
        try:
            net_connect.disconnect()
        except :
            pass
        return
    return

def main():
    # Main Program : we are using  multithreading - creating 30 Parallel threads
    pool = ThreadPool(30) # you can increase or decrease the number of threads depending on you machine and connection speed 
    # Following assigns the pool to apply action
    results = pool.map( connect_to_device , example_devices_list) 

if __name__ == "__main__":
    main()
