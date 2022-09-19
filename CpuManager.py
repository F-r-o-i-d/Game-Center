import os
import psutil

class Controler:
    def SetMaxCpuUsage(percentage):
        # Set max CPU usage to percentage
        if percentage > 100:
            percentage = 100
        elif percentage < 3:
            percentage = 3
        payload = "powercfg -setacvalueindex scheme_current SUB_PROCESSOR PROCTHROTTLEMAX " + str(percentage)
        os.system(payload)

    def SetMinCpuUsage(percentage):
        # Set min CPU usage to percentage
        if percentage >= 90:
            percentage = 90
        payload = "powercfg -setacvalueindex scheme_current SUB_PROCESSOR PROCTHROTTLEMIN " + str(percentage)
        os.system(payload)

class Listener:
    def __init__(self):
        self.MaxCpuUsage = 0
        self.MinCpuUsage = 0

    def GetMaxCpuUsage(self):
        #make an error to say this function is not implemented
        SyntaxError("This function is not implemented yet")
        return self.MaxCpuUsage

    def GetMinCpuUsage(self):
        #make an error to say this function is not implementeda
        SyntaxError("This function is not implemented yet")
        return self.MinCpuUsage
    
    def GetCpuUsage(self):
        cpu_percent=0
        while(True):
            cpu_percent = psutil.cpu_percent()
            if cpu_percent != 0:
                break
        return cpu_percent
