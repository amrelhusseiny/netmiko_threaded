# netmiko_threaded.py

import logging
from sys import stdout
from json import load
from multiprocessing.pool import ThreadPool
from netmiko import BaseConnection , ConnectHandler

# Configuring Log format for Console 
date_strftime_format = "%d-%b-%y %H:%M:%S"
message_format = "%(asctime)s || %(levelname)s || %(message)s"
logging.basicConfig(format= message_format, datefmt= date_strftime_format, stream=stdout , level=logging.INFO)

# List of devices to multi thread : 
example_devices_list = [
							{
								'host_name' : '#########',
								'ip_address' : '#######',
							}
						]

def device_connections(switch_dictionary):
    '''
    Descrption : use Netmiko SSH to devices - Execute the commands needed - Append to file 02_output.txt
    Output :
        No return - save to file
    '''
    logging.info(f' {switch_dictionary["host_name"]} ( {switch_dictionary["ip_address"]} - Logging in progress )')
    try:
        aterm = {
                    'device_type': 'huawei',
                    'host': switch_dictionary["ip_address"],
                    'username': 'orange',
                    'password' : 'FTcloud2016!',
                    'verbose': False ,
                    # 'session_log': 'log.txt', # Uncomment this line to debug NetmikoConnection in the log file
                    'global_delay_factor': 2,
                }
        net_connect = ConnectHandler(**aterm) # returns Netmiko BaseConnection class instance
        net_connect.find_prompt() # Wait for prompt before proceed
        logging.info(f' {switch_dictionary["host_name"]} - Logged in successfully ')
        output = '######################################### Start of'+switch_dictionary["host_name"]+' ######################################### \n\r '
        # --------------------------------------------------------------------------
        # Put your commands here
        # --------------------------------------------------------------------------
        output += net_connect.send_command("screen-length 0 tem")
        # --------------------------------------------------------------------------
        # Writing output to file
        with open("02_output.txt", "a") as file_object:
            file_object.write(output)
        logging.info(f' {switch_dictionary["host_name"]} - Output Generated ')
    except Exception as e:
        logging.error(f' {switch_dictionary["host_name"]} ( {switch_dictionary["ip_address"]} - Not Parsed )')
        with open("02_errors.txt", "a") as file_object:
            file_object.write(f' {switch_dictionary["host_name"]} ( {switch_dictionary["ip_address"]} - Not Parsed )')
            file_object.write(f' {switch_dictionary["host_name"]} Error : {e}')
        try:
            net_connect.disconnect()
        except :
            pass
        return
    return

def main():
    # Main Program : we are using  multithreading - creating 30 Parallel threads
    pool = ThreadPool(30)
    # Following assigns the pool to apply action
    results = pool.map( device_connections , switches_dictionary_list) # ( list_of_devices , action_function )

if __name__ == "__main__":
    main()



# --------------------------------------------------------------------------------------------

# 2)
# ---------------------------------- NTP Check ----------------------------------------------
#import re
# ntp_status_ouput = net_connect.send_command("display ntp status")
# sync_Status = re.findall(r'(?<=clock status: ).*', ntp_status_ouput)[0]
# try:
#     sync_Server = re.findall(r"\d+\.\d+\.\d+\.\d+",ntp_status_ouput)[0]
# except:
#     sync_Server = ''
# logging.info(f' {switch_dictionary["host_name"]} ( {switch_dictionary["ip_address"]} - NTP Status : {sync_Status} - NTP Source : {sync_Server} )')
# --------------------------------------------------------------------------------------------
