import ctypes
import sys
from telnetlib import GA
from turtle import st
import psutil, os, Shell, win32process, win32gui
import kamene.all as scapy
from tkinter import E, messagebox
import winreg as reg
import subprocess
import requests

registry = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)

request = scapy.ARP()

def GetRunningProcess():
    CommunProcess = ["VALORANT-Win64-Shipping.exe", "javaw.exe"]
    NameProcessList = []
    processList = []
    CommunProcessBoosted = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time','cpu_percent', "exe"])
            processList.append(pinfo)
            NameProcessList.append(pinfo['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for process in processList:
        if process["name"] in CommunProcess:
                CommunProcessBoosted.append(process["name"])

    return processList, CommunProcessBoosted, NameProcessList, CommunProcessBoosted

class QosRule:
    def __init__(self) -> None:
        self.Name = ""
        self.AppPathName = ""
        self.DSCPValue = 0

    def __str__(self) -> str:
        return "Name: {}, AppPathName: {}, DSCPValue: {}".format(self.Name, self.AppPathName, self.DSCPValue)

    #add an description for the rule

    def SetDSCPValue(self, scenario : str) -> None:
        """ list of scenarios available
        scenario 1: Applies a low-priority DSCP value for this bulk data.
        scenario 2: Applies high-priority DSCP for ERP server traffic.
        scenario 3: Applies high-priority DSCP for ERP client traffic."""

        if scenario == "1":
            self.DSCPValue = 1
        elif scenario == "2":
            self.DSCPValue = 44
        elif scenario == "3":
            self.DSCPValue = 60
        else:
            raise ValueError("Invalid scenario")

    def BuildQosRule(self) -> str:
        #get the exe name from the app path name
        exeName = os.path.basename(self.AppPathName)

        payload = "New-NetQosPolicy -Name Athos-" + self.Name + " -AppPathNameMatchCondition \""+ exeName + "\" -DSCPAction " + str(self.DSCPValue) + " -IPProtocolMatchCondition Both"
        return Shell.Shell.Exec(payload)
        
    def DestroyQosRule(self) -> str:
        payload = "Remove-NetQosPolicy -Name Athos-" + self.Name + " -Confirm:$false"
        return Shell.Shell.Exec(payload)

def RemoveAllQosRules():
    payload = "Remove-NetQosPolicy -Name \"Athos-*\" -Confirm:$false"
    Shell.Shell.Exec(payload)


def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1])
    except:
        return None
    return None
def get_user_registry_key(key_path):
    try:
        return reg.OpenKey(reg.HKEY_CURRENT_USER, key_path)
    except FileNotFoundError:
        return None
def openRegistryB():
    rawKeyB = reg.OpenKey(registry, "SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces")
    try:
        i = 0
        while 1:
            name, value, type = reg.EnumValue(rawKeyB, i)
            print(name, value, i)
            i += 1

    except WindowsError:
        print("END")

    reg.CloseKey(rawKeyB)

def ScanForNetworkProblem():
    probleme = 0
    optimaleSettings = {
        "Receive Window Auto-Tuning Level": "disabled",
        "Receive-Side Scaling State": "enabled",
        "Max SYN Retransmissions": "2",
    }
    Definition = {
        "Receive Window Auto-Tuning Level":"autotuninglevel",
        "Receive-Side Scaling State":"rss",
        "Max SYN Retransmissions":"MaxSynRetransmissions"}

    #get the current settings
    currentSettings = {}
    ProblemeSettings = {}
    for x in subprocess.check_output("netsh interface tcp show global").splitlines():
        x = x.decode("utf-8")
        if ":" in x:
            currentSettings[x.split(":")[0].replace(" ", "")] = x.split(":")[1]
    print(currentSettings)    
    for setting in optimaleSettings:
        try:
            tsetting = setting.replace(" ", "")
            if optimaleSettings[setting] != currentSettings[tsetting].replace(" ", ""):
                probleme += 1
                ProblemeSettings[tsetting] = currentSettings[tsetting]
            else:
                print("OK")

        except KeyError as e:
            print(e)
    print(probleme)
    if probleme > 0:
        answer = messagebox.askyesno("Network problem", f"There is {probleme} problem with your network, do you want to fix it?")
        if answer:
            for setting in ProblemeSettings:
                print(setting)
                # navigate through the Definition dictionary to remove space
                DefinitionT = {}
                for i,v in Definition.items():
                    DefinitionT[i.replace(" ", "")] = v
                # do the same with optimaleSettings
                optimaleSettingsT = {}
                for i,v in optimaleSettings.items():
                    optimaleSettingsT[i.replace(" ", "")] = v
                
                print(DefinitionT)
                print(optimaleSettingsT)
                # if the setting is in the definition, then we can change it
                if setting in DefinitionT:
                    print(setting)
                    payload = "netsh interface tcp set global " + DefinitionT[setting] + "=" + optimaleSettingsT[setting]
                    Shell.Shell.Exec(payload)
                Shell.Shell.Exec(payload)
    else:
        answer = messagebox.showinfo("Network problem", f"Scan finished, there is no problem with your network")

def ResetNetwork():
    answer = messagebox.askyesno("Network problem", f"Do you want to reset your network?")
    if answer:
        os.system("netsh interface ip reset")
        os.system("netsh int IP reset c:\\resettcpip.txt")
        os.system("netsh int ipv4 reset")
        os.system("netsh int ipv6 reset")
        os.system("netsh int ip reset")
        os.system("ipconfig /flushdns")
        os.system("netsh winsock reset")

        # ask the user to restart the computer
        answer = messagebox.askyesno("Network problem", f"Do you want to restart the computer?")
        if answer:
            Shell.Shell.Exec("shutdown /r /t 0")


# Scan for best dns server
def ScanForBestDnsServer():
    dnsList = []

    dnsPingResults = {}
    # get public ip address
    publicIp = requests.get("https://api.ipify.org").text
    # check the country geoip
    country = requests.get("http://ip-api.com/line/24.48.0.1").text.split("\n")[2]

    dnsList = requests.get(f"https://public-dns.info/nameserver/{country.lower()}.txt").text.split("\n")
    print(dnsList)
    # scan for the best dns server
    for dns in dnsList:
        
        # ping the dns server
        #set max timeout to 1 second
        ping = subprocess.Popen(["ping", "-n", "1","-w","20", dns], stdout=subprocess.PIPE)
        out, error = ping.communicate()
        # get the ping result
        out = out.decode("utf-8")
        # get the ping result
        out = out.split("\n")[-2]
        ms = out.split(",")[1].replace("Maximum = ", "")
        ms = ms.replace("ms", "")
        if "loss" in out:
            #the dns server is not reachable
            pass
        else:
            #the dns server is reachable
            dnsPingResults[dns] = int(ms)
        try:
            print(dnsPingResults[dns])
        except:
            pass
    # short dns ping results
    dnsPingResultsSorted = sorted(dnsPingResults.items(), key=lambda kv: kv[1])
    #get 2 best dns servers
    bestDnsServers = dnsPingResultsSorted[:2]
    _SetDnsServer(bestDnsServers)
def _SetDnsServer(dnsServer):
    #remove the old dns server
    Shell.Shell.Exec("Set-DnsClientServerAddress -InterfaceAlias Wi-Fi -ResetServerAddresses")
    #set the new dns server
    Shell.Shell.Exec(f"Set-DnsClientServerAddress -InterfaceAlias Wi-Fi -ServerAddresses \"{dnsServer[0][0]}\",\"{dnsServer[1][0]}\"")


def StringDiff(str1, str2) -> int:
    score = 0
    str2temp = str2
    # create a list for each var to remove char 
    str2lst = []
    for x in str2:
        str2lst.append(x)
    str1lst = []
    for x in str1:
        str1lst.append(x)
    
    for letter in str1:
        if letter in str2:
            str2lst.remove(letter)
            score+=1
    return score
def SearchForGameInSteam():
    Games = {}
    #look up in steam folder to find game
    steamPath = "C:\Program Files (x86)\Steam\steamapps\common"
    for GameName in os.listdir(steamPath):
        #look in game files to found exe
        for file in os.listdir(steamPath + f"\\{GameName}"):
            if ".exe" in file:
                if StringDiff(GameName, file) > (len(GameName)/2):
                    Games[GameName] = steamPath + "\\" + file
            else:
                pass
    return Games

def SearchForGameInRiot() -> dict:
    Games = {}
    riotPath = "C:\Riot Games"
    for GameName in os.listdir(riotPath):
        if GameName != "Riot Client":
            GamePath = riotPath + "\\" + GameName + "\\live"
            for file in os.listdir(GamePath):
                if file == GameName + ".exe":
                    Games[file] = GamePath + "\\" + GameName + ".exe"
    return Games

def TcpNoDelay():
    # add tcp no delay to registry
    key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters")
    reg.SetValueEx(key, "TcpNoDelay", 0, reg.REG_DWORD, 1)
    reg.CloseKey(key)
    
def NetworkThrottling(state):
    if state == 1:
        # add network throttling to registry
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile")
        reg.SetValueEx(key, "NetworkThrottlingIndex", 0, reg.REG_DWORD, 16777215)
        reg.CloseKey(key)
    else:
        # remove network throttling to registry
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile")
        reg.SetValueEx(key, "NetworkThrottlingIndex", 0, reg.REG_DWORD, 60)
        reg.CloseKey(key)

def CongestionControl(state):
    if state == 1:
        Shell.Shell.Exec("netsh int tcp set supplemental Internet congestionprovider=ctcp")
    else:
        Shell.Shell.Exec("netsh int tcp set supplemental Internet congestionprovider=none")


def IsIrpStackSizeSet():
    # check if IrpStackSize is set
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters")
    try:
        IrpStackSize = reg.QueryValueEx(key, "IrpStackSize")[0]
        print(f"IrpStackSize: {IrpStackSize}")
        reg.CloseKey(key)

        if IrpStackSize == 48:
            return True
        else:
            return False
    except:
        reg.CloseKey(key)
        return False

def IsNetworkThrottlingSet():
    # check if network throttling is set
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile")
    try:
        NetworkThrottling = reg.QueryValueEx(key, "NetworkThrottlingIndex")[0]
        print(f"NetworkThrottling: {NetworkThrottling}")
        reg.CloseKey(key)

        if NetworkThrottling == 16777215:
            return True
        else:
            return False
    except:
        reg.CloseKey(key)
        return False

def IrpStackSize(state):
    if state == 1:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters")
        reg.SetValueEx(key, "IRPStackSize", 0, reg.REG_DWORD, 32)
        reg.CloseKey(key)
    else:
        #delete the key
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters")
        reg.DeleteValue(key, "IRPStackSize")
        reg.CloseKey(key)

def CheckIfRunningAsAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def RunAsAdmin():
    if not CheckIfRunningAsAdmin():
        # if the script is not running as admin
        # re-run the script as admin
        #if i can't re-run the script as admin
        #return false
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            return True
        except:
            return False