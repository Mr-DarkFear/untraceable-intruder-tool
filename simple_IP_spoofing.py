# simple_IP_spoofing.py

import subprocess
import random
import json
import ipaddress
import datetime
import os

_fake_ips = []

BACKUP_FILE = os.path.join(os.getcwd(), f"network_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def run_powershell(cmd):
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
            capture_output=True, text=True, shell=False, check=False
        )
        return {"rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    except Exception as e:
        return {"rc": 1, "stdout": "", "stderr": str(e)}

def get_all_ip():
    try:
        cmd = "Get-NetIPAddress | Select-Object InterfaceAlias, InterfaceIndex, AddressFamily, IPAddress, PrefixLength | ConvertTo-Json -Depth 3"
        res = run_powershell(cmd)
        if res["rc"] != 0:
            print(f"[!] Error getting IP: {res['stderr']}")
            return []
        data = json.loads(res["stdout"]) if res["stdout"].strip() else []
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception as e:
        print(f"[!] GetAll_IP exception: {e}")
        return []

def get_interface_ipv4_info(interface='Wi-Fi'):
    try:
        cmd = f'Get-NetIPAddress -InterfaceAlias "{interface}" -AddressFamily IPv4 | Select-Object -First 1 IPAddress,PrefixLength | ConvertTo-Json'
        res = run_powershell(cmd)
        if res["rc"] != 0 or not res["stdout"].strip():
            return None
        data = json.loads(res["stdout"])
        if not data:
            return None
        if isinstance(data, dict):
            return {"ip": data.get("IPAddress"), "prefix": int(data.get("PrefixLength")) if data.get("PrefixLength") else None}
        return None
    except Exception as e:
        print(f"[!] get_interface_ipv4_info exception: {e}")
        return None

def backup_network_state(interface='Wi-Fi'):
    try:
        data = {}
        data['all_ip'] = get_all_ip()
        data['interface_ipv4_info'] = get_interface_ipv4_info(interface)
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"[i] Network backup saved: {BACKUP_FILE}")
        return True
    except Exception as e:
        print(f"[!] Backup error: {e}")
        return False

def restore_instructions():
    print("=== MANUAL RESTORE INSTRUCTIONS ===")
    print(f"1) Open PowerShell as Admin.")
    print(f"2) Check backup file: {BACKUP_FILE}")
    print("3) Use Remove-NetIPAddress to delete fake IPs, or Set-NetIPAddress to restore original IPs from backup.")
    print("Example (PowerShell): Get-Content -Raw -Path '{0}' | ConvertFrom-Json".format(BACKUP_FILE))
    print("====================================")

def random_private_ipv4(interface='Wi-Fi'):
    info = get_interface_ipv4_info(interface)
    if info and info.get("ip") and info.get("prefix"):
        try:
            ip = ipaddress.IPv4Interface(f"{info['ip']}/{info['prefix']}")
            network = ip.network
            hosts = list(network.hosts())
            if len(hosts) > 200:
                candidates = random.sample(hosts, 200)
            else:
                candidates = hosts
            cur = ip.ip
            choices = [str(h) for h in candidates if h != cur]
            if not choices:
                raise Exception("No candidate hosts in same network")
            return random.choice(choices)
        except Exception:
            pass

    choice = random.choice(["10", "172", "192"])
    if choice == "10":
        return f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    elif choice == "172":
        return f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
    else:
        return f"192.168.{random.randint(0,31)}.{random.randint(1,254)}"

def set_ip_powershell(ip, interface='Wi-Fi'):
    try:
        cmd = f"New-NetIPAddress -InterfaceAlias '{interface}' -IPAddress '{ip}' -PrefixLength 24 -SkipAsSource $true -Confirm:$false"
        res = run_powershell(cmd)
        if res["rc"] == 0:
            print(f"[+] IP {ip} set successfully on {interface} (SkipAsSource enabled)")
            _fake_ips.append(ip)
            return True
        else:
            stderr = (res["stderr"] or "").lower()
            if "already exists" in stderr or "exist" in stderr:
                print(f"[*] IP {ip} already exists on {interface}")
                if ip not in _fake_ips:
                    _fake_ips.append(ip)
                return True
            else:
                print(f"[-] PowerShell error adding IP: {res['stderr']}")
                return False
    except Exception as e:
        print(f"[!] Exception in set_ip_powershell: {e}")
        return False

def set_ip_netsh(ip, interface='Wi-Fi'):
    try:
        proc = subprocess.run(
            ["netsh", "interface", "ip", "add", "address", f"name={interface}", f"addr={ip}", "mask=255.255.255.0"],
            capture_output=True, text=True, shell=False
        )
        if proc.returncode == 0:
            print(f"[+] IP {ip} set successfully via netsh")
            _fake_ips.append(ip)
            return True
        else:
            print(f"[-] netsh error: {proc.stderr}")
            return False
    except Exception as e:
        print(f"[!] netsh set IP exception: {e}")
        return False

def clear_fake_IP(interface='Wi-Fi'):
    current = []
    try:
        cmd = f'Get-NetIPAddress -InterfaceAlias "{interface}" | Select-Object IPAddress | ConvertTo-Json'
        res = run_powershell(cmd)
        if res["rc"] == 0 and res["stdout"].strip():
            data = json.loads(res["stdout"])
            if isinstance(data, dict):
                current = [data.get("IPAddress")]
            elif isinstance(data, list):
                current = [item.get("IPAddress") for item in data if item.get("IPAddress")]
    except Exception as e:
        print(f"[!] Error getting current IPs: {e}")

    removed_count = 0
    for ip in _fake_ips[:]:
        if ip not in current:
            _fake_ips.remove(ip)
            continue
            
        try:
            cmd = f'Remove-NetIPAddress -InterfaceAlias "{interface}" -IPAddress "{ip}" -Confirm:$false'
            res = run_powershell(cmd)
            if res["rc"] == 0:
                print(f"[+] Removed fake IP: {ip}")
                _fake_ips.remove(ip)
                removed_count += 1
            else:
                stderr = (res["stderr"] or "").lower()
                if "not found" in stderr:
                    _fake_ips.remove(ip)
                else:
                    print(f"[-] Failed to remove IP {ip}: {res['stderr']}")
        except Exception as e:
            print(f"[!] Remove IP error: {e}")

    if removed_count > 0:
        print(f"[+] Total {removed_count} fake IPs removed")
    else:
        print("[*] No fake IPs to remove")

def private_IP_spoofing(interface='Wi-Fi'):
    interfaces = get_all_ip()
    if not any(adapter.get('InterfaceAlias', '').lower() == interface.lower() for adapter in interfaces):
        print(f"[-] Interface {interface} not found")
        return False
    if not any('backup' in f for f in os.listdir('.')):
        backup_network_state(interface)
    
    new_ip = random_private_ipv4(interface)
    
    if set_ip_powershell(new_ip, interface):
        return True
    elif set_ip_netsh(new_ip, interface):
        return True
    else:
        print(f"[-] All methods failed for IP {new_ip}")
        return False