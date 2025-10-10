#simple_MAC_spoofing.py

import subprocess
import winreg
import random
import re
import json

# target_guid = "{CC1A843D-7EF3-4FE0-9EC2-8E8601066B37}"
# new_mac = "001122334455"

def reset_mac(target_guid):
    try:
        base_key = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        found = False
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key) as adapters:
            for i in range(1000):
                try:
                    subkey_name = winreg.EnumKey(adapters, i)
                    with winreg.OpenKey(adapters, subkey_name, 0, winreg.KEY_ALL_ACCESS) as adapter:
                        try:
                            guid, _ = winreg.QueryValueEx(adapter, "NetCfgInstanceId")
                            if guid.upper() == target_guid.upper():
                                print(f"Found adapter GUID={guid} at subkey {subkey_name}, deleting NetworkAddress...")
                                try:
                                    winreg.DeleteValue(adapter, "NetworkAddress")
                                    print("MAC reset to default (burn-in MAC).")
                                    found = True
                                except FileNotFoundError:
                                    print("No spoofed MAC found, already default.")
                                    found = True
                                break
                        except FileNotFoundError:
                            # Bỏ qua nếu không có NetCfgInstanceId
                            continue
                except WindowsError as e:
                    if e.winerror == 259:  # No more data is available
                        break  # Thoát vòng lặp khi hết subkey
                    else:
                        print(f"WindowsError: {e}")
                        continue
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue
        
        if not found:
            print(f"Adapter with GUID {target_guid} not found in registry")
        return found
        
    except Exception as e:
        print(f'\n\nreset-MAC-processor error:\n{e}\n')
        return False
    
def get_all_mac():
    try:
        result = subprocess.run([
            "powershell",
            "-Command",
            "Get-NetAdapter | Select-Object Name, InterfaceDescription, InterfaceGuid, MacAddress, Status | ConvertTo-Json"
        ], capture_output=True, text=True, check=True)

        adapters = json.loads(result.stdout)
        if isinstance(adapters, dict):
            adapters = [adapters]
        
        # Đổi tên InterfaceGuid thành GUID để tương thích với code cũ
        for adapter in adapters:
            if 'InterfaceGuid' in adapter:
                adapter['GUID'] = adapter['InterfaceGuid']
                
        return adapters
    except Exception as e:
        print(f'GetAll_MAC logs: \n{e}\n')
        return []

def set_mac(new_mac, target_guid, adapter_name='Wi-Fi'):
    try:
        base_key = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        found = False
        adapters = get_all_mac()
        adapter_exists = any(
            (adapter.get('InterfaceGuid') or adapter.get('GUID') or '').upper() == target_guid.upper()
            for adapter in adapters
        )
        
        if not adapter_exists:
            print(f"[-] Adapter with GUID {target_guid} not found")
            return False
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key) as adapters:
            for i in range(1000):
                try:
                    subkey_name = winreg.EnumKey(adapters, i)
                    with winreg.OpenKey(adapters, subkey_name, 0, winreg.KEY_ALL_ACCESS) as adapter:
                        try:
                            guid, _ = winreg.QueryValueEx(adapter, "NetCfgInstanceId")
                            if guid.upper() == target_guid.upper():
                                desc, _ = winreg.QueryValueEx(adapter, "DriverDesc")
                                print(f"Found adapter {desc} at {subkey_name}")
                                winreg.SetValueEx(adapter, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
                                found = True
                                break
                        except FileNotFoundError:
                            continue
                except WindowsError as e:
                    if e.winerror == 259:  # No more data is available
                        break
                    else:
                        print(f"WindowsError: {e}")
                        continue
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue
        
        if found:
            subprocess.run(["powershell", "-Command", f'Disable-NetAdapter -Name "{adapter_name}" -Confirm:$false'])
            subprocess.run(["powershell", "-Command", f'Enable-NetAdapter -Name "{adapter_name}" -Confirm:$false'])
            return True
        else:
            print(f"Adapter with GUID {target_guid} not found in registry")
            return False
            
    except Exception as e:
        print(f'\n\nSetkey-engine error: \n{e}\n')
        return False
    
def is_valid_MAC(mac):
    try:
        if len(mac) != 12 or not all(c in "0123456789ABCDEFabcdef" for c in mac):
            print("MacChecker logs: Invalid MAC format! Must be 12 hex characters.")
            return None
        else:
            return mac
    except Exception as e:
        print(f'\n\nMacChecker error:\n{e}\n')
        return None

def random_mac() -> str:
    try:
        mac = None
        while mac is None:
            mac = is_valid_MAC("".join(f"{random.randint(0, 255):02X}" for _ in range(6)))
        return mac
    except Exception as e:
        print(f'\n\nrandom-MAC-engine error: \n{e}\n')
        return None

def MAC_spoofing(target_guid):
    new_mac = random_mac()
    if new_mac:
        set_mac(new_mac, target_guid)
    
    