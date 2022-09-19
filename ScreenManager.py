import Shell
#initialize var
width = 0
height = 0 

def UpdateScreenSize():
    #get screen size
    global width, height
    width = Shell.Shell.Exec("wmic path Win32_VideoController get CurrentHorizontalResolution").replace("CurrentHorizontalResolution", "").strip()
    height = Shell.Shell.Exec("wmic path Win32_VideoController get CurrentVerticalResolution").replace("CurrentVerticalResolution", "").strip()
    #convert to int
    width = int(width)
    height = int(height)
    