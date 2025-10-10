class color_controler():
    def __init__(self):
        self.colors = [
            '\033[91m', #RED
            '\033[92m', #GREEN
            '\033[93m', #YELOW
            '\033[94m', #BLUE
            '\033[95m', #MAGENTA
            '\033[96m', #CYAN
            '\033[97m', #WHITE
            '\033[0m'   #RESET
        ]
    def set_color(self, text):
        global title
        patern = [
        [title, "▒", "WARNING", 'OFF'],
        ["codes list", 'REMOVED', 'default', 'ON'],
        ['ID', 'network adapters', 'BSSID', 'WIFI', 'MAC', 'IP', 'STOPPED', "credit", "help", "show_MAC", "show_IP", 'MAC_spoofing', "IP_spoofing", 'wifi_cracking', 'name_spoofing', 'end', 'exit', 'stop', 'back', 'clear', 'start', 'menu'],
        ["╟", "╢"],
        [],
        ["Mr_DarkFear (Lê Nguyễn Gia Bảo)", "─", "│", "┘", "└", "┌", "┐", "╭", "╮", "╰", "╯", "┬", "┝"]
        ]
        result = text
        for i in patern:
            for i2 in i:
                result = result.replace(i2, self.colors[patern.index(i)] + i2 + self.colors[7])
        return result

title = """
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│██╗   ██╗███╗   ██╗████████╗██████╗  █████╗  ██████╗███████╗ █████╗ ██████╗ ██╗     ███████╗│
│██║   ██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██║     ██╔════╝│
│██║   ██║██╔██╗ ██║   ██║   ██████╔╝███████║██║     █████╗  ███████║██████╔╝██║     █████╗  │
│██║   ██║██║╚██╗██║   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██║██╔══██╗██║     ██╔══╝  │
│╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║██████╔╝███████╗███████╗│
│ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝│
│                                                                                            │
│██╗███╗   ██╗████████╗██████╗ ██╗   ██╗██████╗ ███████╗██████╗                              │
│██║████╗  ██║╚══██╔══╝██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗     ╔                    ╗  │
│██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║  ██║█████╗  ██████╔╝     ║ ███  ███  ███  █   ║  │
│██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║  ██║██╔══╝  ██╔══██╗     ║  █   █ █  █ █  █   ║  │
│██║██║ ╚████║   ██║   ██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║     ║  █   ███  ███  ███ ║  │
│╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚                    ╝  │
└────────────────────────────────────────────────────────────────────────────────────────────┘
"""
credit = f"""
 ╔══════════════════[ credit ]══════════════════╗
╔╝                                              ╚╗
╬   created by: Mr_DarkFear (Lê Nguyễn Gia Bảo)  ╬
╬   github:https://github.com/Mr-DarkFear        ╬
╚╗                                              ╔╝
 ╚══════════════════════════════════════════════╝
"""
warning = []
warning.append("""
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[ WARNING ]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒                                                                   ▒▒
▒▒  WARNING: please use this tool as administrator for best quality  ▒▒
▒▒                                                                   ▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒[ WARNING ]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒                                                                   ▒▒
▒▒  WARNING: This tool is for educational and authorized testing     ▒▒
▒▒  purposes ONLY. You must only use this on networks you own or     ▒▒
▒▒  have explicit permission to test. Unauthorized access to         ▒▒
▒▒  computer networks is illegal and subject to prosecution.         ▒▒
▒▒                                                                   ▒▒
▒▒  By using this tool, you agree that you are solely responsible    ▒▒
▒▒  for your actions.                                                ▒▒
▒▒                                                                   ▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
""")

codes_list = """
╭──────────────────────────╢[ codes list ]╟────────────────────────────╮
│                                                                      │
│    'help' to show codes list (this list)                             │
│                                                                      │
│    ---address---                                                     │
│    ─┬───────────                                                     │
│     ┝═'show_MAC' to show all the MAC addresses in this device        │
│     ┝═'show_IP' to show all the IP addresses in this device          │
│     ┝═'MAC_spoofing' to start / stop spoofing MAC address            │
│     ┝═'IP_spoofing' to start / stop spoofing IPv4 address            │
│     └═'clear' to clear all fake MAC, IP and reset it                 │
│                                                                      │
│    ---wifi crack---                                                  │
│    ─┬──────────────                                                  │
│     └═'wifi_cracking' to crack the target wifi password              │
│                                                                      │
│    ---device name---                                                 │
│    ─┬───────────────                                                 │
│     └═'name_spoofing' to start spoofing hostname                     │
│                                                                      │
│    ---task---                                                        │
│    ─┬────────                                                        │         
│     ┝═ 'end' to stop all tasks and return to the main menu           │
│     ┝═ 'stop' to stop all tasks and return to the main menu          │
│     ┝═ 'back' to return to the main menu without stop any task       │
│     ┝═ 'menu' to return to the main menu without stop any task       │
│     ┝═ 'log' to turn on / off "logging setting" (default: True)      │
│     ┝═ 'save_log' to save current log to a new file with timestamp   │
│     └═ 'exit' to stop and close program incontinently                │
│                                                                      │
│    ---information---                                                 │
│    ─┬───────────────                                                 │
│     ┝═ 'credit' to show author of this tool and more                 │
│     └═ 'other_part' to show link to the necessary parts of the tool  │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
"""