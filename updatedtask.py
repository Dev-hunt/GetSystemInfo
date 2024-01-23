# Task with time efficient aproach 

import psutil
import platform
import speedtest
import socket
import screeninfo
import uuid
import GPUtil
import concurrent.futures
import subprocess

def get_cpu_info():
    return platform.processor()

def get_cpu_cores():
    return psutil.cpu_count(logical=False)

def get_cpu_threads():
    return psutil.cpu_count(logical=True)

def get_gpu_info():
    try:
        return GPUtil.getGPUs()[0].name
    except Exception as e:
        return "N/A"

def get_ram_size():
    ram_byte=psutil.virtual_memory().total
    ram_gb=round(ram_byte/(1024**3),2)
    return f"{ram_gb} GB"

def get_screen_size():
    screen_info = screeninfo.get_monitors()
    screen_width_inches=screen_info[0].width_mm/25.4
    screen_height_inches=screen_info[0].height_mm/25.4
    return f"{screen_width_inches:.2f} x {screen_height_inches:.2f} inches"

def get_mac_address():
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        return mac
    except Exception as e:
        return "N/A"

def get_public_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        public_ip = s.getsockname()[0]
        s.close()
        return public_ip
    except Exception as e:
        return "N/A"

def get_installed_software():
    try:
        result = subprocess.run(["wmic", "product", "get", "name"], capture_output=True, text=True)
        installed_software = [software.strip() for software in result.stdout.strip().split('\n')[1:] if software.strip()]
        for idx, software in enumerate(installed_software, start=1):
            print(f"{idx}. {software}")
        return len(installed_software)
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_internet_speed():
    try:
        st = speedtest.Speedtest()
        download_speed = st.download()
        upload_speed = st.upload()
        download_speed_kbps=round(download_speed/1024,2)
        upload_speed_kbps=round(upload_speed/1024,2)
        return f"{download_speed_kbps}Kbps, ^{upload_speed_kbps}Kbps"
    except Exception as e:
        print(f"Error: {e}")
    

def get_os_version():
    return f"{platform.system()} {platform.version()}"

def gather_system_info():
    with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:
        # Define the functions to run in parallel
        functions = [
            get_installed_software,
            get_cpu_info,
            get_cpu_cores,
            get_cpu_threads,
            get_gpu_info,
            get_ram_size,
            get_screen_size,
            get_mac_address,
            get_public_ip,
            get_internet_speed,
            get_os_version,
        ]


        results = executor.map(lambda func: func(), functions)


        system_info = dict(zip([func.__name__[4:] for func in functions], results))

    return system_info

if __name__ == "__main__":
    system_info = gather_system_info()

    print("\nSystem Information:")
    for key, value in system_info.items():
        print(f"{key}: {value}")

