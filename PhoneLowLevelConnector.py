import logging

# import usb.core
# import usb.util
# import bluetooth
import socket
import sys
import os
import subprocess
from usable import *

__author__ = 'MN Ahimbisibwe'

global_text_green = 'Waiting for device >>'
global_text_red = "No Action Made"


# COLOR = color()  # color_list = [RED, GREEN, YELLOW, BLUE, WHITE]

def check_adb():
    """Checks if adb is available and prints its version."""
    try:
        result = subprocess.run(['adb', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"{COLOR[3]}{result.stdout.decode()}{COLOR[4]}")
        return True  # Return True if adb is available
    except FileNotFoundError:
        print(f"{COLOR[0]}adb is not found in your system's PATH. Please install Android SDK and ensure adb is in the "
              f"PATH.{COLOR[4]}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"{COLOR[0]}Error running adb:{COLOR[4]}", e)
        return False


check_adb()


def get_adb_devices():
    try:
        res = subprocess.check_output(['adb', 'devices']).decode('utf8')
        lines = res.strip().split('\n')
        devices = [line.split('\t')[0] for line in lines[1:] if line.split('\t')[1] == 'device']
        if not devices:
            logging.error(" No devices are connected.")
        return devices
    except Exception as e:
        print(f"{COLOR[0]}An error occurred: {COLOR[4]}{str(e)}")
        return []


def stop_adb_server():
    # Execute the command to stop the adb server
    result = subprocess.run(['adb', 'kill-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check the result
    if result.returncode == 0:
        print('ADB server stopped successfully.')
    else:
        print(f'Failed to stop ADB server. Error: {result.stderr.decode()}')


def start_adb_server():
    # Execute the command to start the adb server
    result = subprocess.run(['adb', 'start-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check the result
    if result.returncode == 0:
        print('ADB server started successfully.')
    else:
        print(f'Failed to start ADB server. Error: {result.stderr.decode()}')


class MobilePhoneLowLevelConnector:
    def __init__(self, adb_path: str, target_name=None):
        self.target_name = target_name
        self.adb_path = adb_path

    def detect_device(self):
        # List connected adb devices
        result = subprocess.run([self.adb_path, 'devices'], capture_output=True, text=True)
        # result = subprocess.check_output(['adb', 'devices']).decode('utf8')

        # Split the result by newlines and ignore the first line ("List of devices attached")
        devices = result.stdout.split('\n')[1:]

        # Iterate over the connected devices and find the target device
        for device in devices:
            if device:
                # Device string format is "{device_name}\t{device_status}", we're interested in the name
                device_name = device.split('\t')[0]

                if self.target_name in device_name:
                    global global_text_green
                    global_text_green = f"ADB device {COLOR[3]}{device_name.upper()}{COLOR[4]} found."
                    print(global_text_green)
                    return True, global_text_green

        global global_text_red
        global_text_red = "ADB device not found."
        print(global_text_red)
        return False, global_text_red

    def connect_phone_adb(self):
        if not self.detect_device():
            global global_text_red
            global_text_red = "ADB connection established successfully."

            print(global_text_red)
            return False

        # Now that the device is detected, you can run adb commands as needed For example, to pull a file from the
        # device: result = subprocess.run([self.adb_path, '-s', self.target_name, 'pull', '/path/to/file/on/device',
        # '/path/to/destination/on/pc'])
        else:
            global global_text_green
            global_text_green = f"{COLOR[1]}ADB connection established successfully.{COLOR[4]}"

            print(global_text_green)
        return True

# if __name__ == "__main__":
#     path = "C:\\Android\\platform-tools\\adb"
#
#     device = get_adb_devices()
#     connector = None
#     if device:
#         connector = MobilePhoneLowLevelConnector(path, target_name=device[0])
#         connector.connect_phone_adb()

#
# class MobilePhoneConnector:
#     def __init__(self, target_name=None, host=None, port=None):
#         self.target_name = target_name
#         self.host = host
#         self.port = port
#         self.vendor_id = None
#         self.product_id = None
#
#     def detect_usb_device(self):
#         # Iterate over USB devices and find the one matching the target_name
#         devices = usb.core.find(find_all=True)
#
#         for device in devices:
#             iManufacturer = usb.util.get_string(device, device.iManufacturer)
#             iProduct = usb.util.get_string(device, device.iProduct)
#
#             # Check if target name is in either string
#             if (iManufacturer is not None and self.target_name in iManufacturer) or \
#                     (iProduct is not None and self.target_name in iProduct):
#                 self.vendor_id = device.idVendor
#                 self.product_id = device.idProduct
#                 break
#
#     def connect_phone_usb(self):
#         if self.vendor_id is None or self.product_id is None:
#             self.detect_usb_device()
#
#         if self.vendor_id is None or self.product_id is None:
#             print("USB device not found.")
#             return False
#
#         # Connect to the USB device and perform necessary operations
#         # ...
#
#         print("USB connection established successfully.")
#         return True
#
#         self.run_adb_commands()
#
#     def run_adb_commands(self):
#         try:
#             # Ensure ADB recognizes the device
#             devices = subprocess.check_output(['adb', 'devices']).decode('utf-8')
#             print(devices)
#
#             # Pull a file from the device
#             # Substitute "/sdcard/example.txt" with the actual file path on your device
#             # This will download the file to your current working directory
#             subprocess.check_call(['adb', 'pull', '/sdcard/example.txt'])
#
#         except subprocess.CalledProcessError as e:
#             print(f"Error occurred: {e}")
#             print(f"Vendor ID: {self.vendor_id}, Product ID: {self.product_id}")
#
#
# if __name__ == "__main__":
#     my_connector = MobilePhoneConnector(target_name='MyDevice')
#
#     if my_connector.connect_phone_usb():
#         print("The device was successfully connected.")
#     else:
#         print("The device could not be found or connected.")

# --SN__ = '217005435'
# --ver__ = 'Firmware Hardware Hacking Detection'
# C:\Users\Michael\AppData\Roaming\Python\Python311\site-packages\libusb


# try:
#     import bluetooth
# except ModuleNotFoundError:
#     print(
#         "Bluetooth module not found. Please install the required dependencies or use a platform-specific alternative.")
#     sys.exit(1)

#
# class MobilePhoneConnector:
#     def __init__(self, target_name=None, host=None, port=None):
#         self.target_name = target_name
#         self.host = host
#         self.port = port
#         self.vendor_id = None
#         self.product_id = None
#
#     def detect_usb_device(self):
#         # Iterate over USB devices and find the one matching the target_name
#         devices = usb.core.find(find_all=True)
#
#         for device in devices:
#             # if device is not found
#             if self.device is None:
#                 raise ValueError('Device not found. Please ensure it is connected.')
#                 # sys.exit(1)
#             if self.target_name in usb.util.get_string(device, device.iManufacturer) or \
#                     self.target_name in usb.util.get_string(device, device.iProduct):
#                 self.vendor_id = device.idVendor
#                 self.product_id = device.idProduct
#                 break
#
#     def connect_phone_usb(self):
#         if self.vendor_id is None or self.product_id is None:
#             self.detect_usb_device()
#
#         if self.vendor_id is None or self.product_id is None:
#             print("USB device not found.")
#             return False
#
#         # Connect to the USB device and perform necessary operations
#         # ...
#
#         print("USB connection established successfully.")
#         return True
#
#         self.run_adb_commands()
#
#     def run_adb_commands(self):
#         try:
#             # Ensure ADB recognizes the device
#             devices = subprocess.check_output(['adb', 'devices']).decode('utf-8')
#             print(devices)
#
#             # Pull a file from the device
#             # Substitute "/sdcard/example.txt" with the actual file path on your device
#             # This will download the file to your current working directory
#             subprocess.check_call(['adb', 'pull', '/sdcard/example.txt'])
#
#         except subprocess.CalledProcessError as e:
#             print(f"Error occurred: {e}")
#             print(f"Vendor ID: {self.vendor_id}, Product ID: {self.product_id}")

# def connect_phone_bluetooth(self):
#     nearby_devices = bluetooth.discover_devices()
#
#     for addr in nearby_devices:
#         name = bluetooth.lookup_name(addr)
#         if name == self.target_name:
#             target_address = addr
#             break
#
#     if target_address is None:
#         print("Bluetooth device not found.")
#         return False
#
#     # Connect to the Bluetooth device and perform necessary operations
#     # ...
#
#     print("Bluetooth connection established successfully.")
#     return True
#     self.run_adb_commands()
#
# def connect_phone_wifi(self):
#     try:
#         phone_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         phone_socket.connect((self.host, self.port))
#
#         # Perform necessary operations over the Wi-Fi connection
#         # ...
#
#         print("Wi-Fi connection established successfully.")
#         return True
#
#     except ConnectionRefusedError:
#         print("Failed to connect to the phone.")
#         return False
#
#     finally:
#         phone_socket.close()

#
# if __name__ == "__main__":
#     my_connector = MobilePhoneConnector(target_name='MyDevice')
#
#     if my_connector.connect_phone_usb():
#         print("The device was successfully connected.")
#     else:
#         print("The device could not be found or connected.")
