#!/usr/bin/env python3
import subprocess
service_name = "filebeat"
def drawline():
    print("-----------------------------------------------------------------------------------------------")
drawline()
try:
    import os,sys,datetime,requests,psutil,time
    print("All the Modules are successfully imported")
except Exception as e:
    print(e)
    sys.exit(1)
drawline()
def stop_service():
    try:
        while True:
            print("wait for 5 sec...")
            time.sleep(5)
            print(f"Stopping the Service {service_name}....................................")
            time.sleep(5)
            os.execv('/home/pi/myPiConfig/Test/restartMySelf.py', [''])
    except KeyboardInterrupt:
        print( " Quit")
    except Exception as e:
        print("------------------------------------------------------------------------------------------")
    stop_cmd='systemctl stop filebeat'.split()
    my_cmd=subprocess.Popen(stop_cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return_code=my_cmd.wait()
    drawline()

def start_service():
    start_cmd = 'systemctl start filebeat'.split()
    my_cmd = subprocess.Popen(start_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = my_cmd.wait()
    drawline()

def pid_of_service():
    process = filter(lambda p: p.name() == service_name, psutil.process_iter())
    pd_list = []
    for i in process:
        my_pds = i.pid
        pd_list.append(my_pds)
    print(len(pd_list))
    print(pd_list)
    if len(pd_list) > 0:
        print(f'The Number of Pids of the services {service_name} are {(len(pd_list))} PID\'s ')
        print("Killing the PID\'s ")
        for kill in pd_list:
            print("Killed the pids for the service")
            i.kill()
        else:
            print(f"No PID\'s for service {service_name} are Running")
def main_pid():
    for proc in psutil.process_iter():
        service_main_pid = []
        if proc.name() == service_name:
            service_pid = proc.pid
            service_main_pid.append(service_pid)
            break
    print(f'The Main PID for the service is {service_main_pid}')

def check_url_health():
    try:
        r = requests.get('https://www.google.com')
        status=r.status_code
        if status==200:
            print(f'The URL is up and Running with status Code : {status}')
    except Exception as ConnectionError:
        print(ConnectionError)
        print("Wait for the services to start")


def check_service_status(service_name):
    status = os.system('systemctl status ' + service_name + ' > /dev/null')
    return status
def main():
    if (check_service_status(service_name) == 0):
        print(f"The Service {service_name} is Running")
        print("Stopping the service")
        stop_service()
        time.sleep(5)
        pid_of_service()
        print("Service stopped ! .....Restarting the service")
        start_service()
        print(f'Service {service_name} is Started')
        main_pid()
        check_url_health()

    else:
        print(f"The Service {service_name} is Stopped")
        print("Starting the service")
        pid_of_service()
        start_service()
        main_pid()
        check_url_health()
main()
drawline()
