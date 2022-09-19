#import tkinter 
import os
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from turtle import bgcolor, left
import Core

class App():
    def __init__(self):
        self.GameList = {}
        self.IsDevMode = False
        self.GameCount = 0
        self.LastApp = None
        self.NetworkOptimize = False
        self.GameX = 0
        self.GameY = 0
        self.root = Tk()
        self.root.title("Gui")
        self.root.geometry("844x410")
        self.root.resizable(False, False)
        #open image and show it in the window
        #load assets
        self.bg = PhotoImage(file="assets/bg.png")
        self.assets_buttonHome = PhotoImage(file="assets/ButtonHome.png")
        self.assets_buttonNetwork = PhotoImage(file="assets/ButtonNetwork.png")
        self.assets_buttonSettings = PhotoImage(file="assets/ButtonSettings.png")
        self.assets_off = PhotoImage(file="assets/off.png")
        self.assets_on = PhotoImage(file="assets/on.png")
        self.networkFrame_png = PhotoImage(file="assets/network.png")
        self.frameBg = "#1A1A1A"

        self.irpstackswitch = Core.IsIrpStackSizeSet()
        self.NetworkThrottling = Core.IsNetworkThrottlingSet()
        self.CongestionControl = False

        self.img_label = Label(self.root, image=self.bg)
        self.img_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        #create widgets
        self.buttonHome = Button(self.root, image=self.assets_buttonHome, command=self.buttonHome_click, relief='flat',
                                     activebackground="#141414", activeforeground="#141414",
                                     background="#141414", foreground="#141414", width=100, height=100, bd=0)
        self.buttonHome.place(x=18, y=71)
        self.buttonNetwork = Button(self.root, image=self.assets_buttonNetwork, command=self.buttonNetwork_click, relief='flat',
                                     activebackground="#141414", activeforeground="#141414",
                                     background="#141414", foreground="#141414", bd=0)
        self.buttonNetwork.place(x=29, y=199)
        self.buttonSettings = Button(self.root, image=self.assets_buttonSettings, command=self.buttonSettings_click, relief='flat',
                                     activebackground="#141414", activeforeground="#141414",
                                     background="#141414", foreground="#141414", bd=0)
        self.buttonSettings.place(x=28, y=305)
        threading.Thread(target=self.DetectGameLoop).start()
        self.CreateGameFrame()
    def CreateNetworkFrame(self):
        self.NetworkFrame = Frame(self.root, background=self.frameBg)
        self.NetworkFrame.configure(width=699)
        self.NetworkFrame.configure(height=410)
        self.NetworkFrame.place(x=145, y=0)
        self.NetworkFrame.configure(highlightbackground="#1A1A1A")
            
        self.NetworkFrame.configure(highlightcolor="black")
        self.NetworkFrame.configure(highlightthickness=1)
        self.NetworkFrame.configure(borderwidth=0)
        # add image to background
        self.NetworkFrame_bg = Label(self.NetworkFrame, image=self.networkFrame_png)
        self.NetworkFrame_bg.place(x=0, y=0, relwidth=1, relheight=1)
        #check if the user is in dev mode 
        #if yes : add all options to the network frame
        #if no : show a text in center of the window saying that options are not available 
        if self.IsDevMode == True:
            #add Athos net optimizer button
            self.switch_networkBtn = Button(self.NetworkFrame, image=self.assets_off, command=self.switch_network, relief='flat')
            self.switch_networkBtn.place(x=590, y=136)
            #add tcpno delay button
            self.switch_tcpnodelayBtn = Button(self.NetworkFrame, image=self.assets_off, command=self.switch_tcpnodelay, relief='flat')
            self.switch_tcpnodelayBtn.place(x=314, y=125)

            self.irpstackbutton = Button(self.NetworkFrame, image=self.assets_off, command=self.switch_irpstackbutton, relief='flat')
            if self.irpstackswitch == True:
                self.irpstackbutton.configure(image=self.assets_on)
            self.irpstackbutton.place(x=314, y=170)

            self.NetworkThrottlingButton = Button(self.NetworkFrame, image=self.assets_off, command=self.switch_NetworkThrottling, relief='flat')
            if self.NetworkThrottling == True:
                self.NetworkThrottlingButton.configure(image=self.assets_on)
            self.NetworkThrottlingButton.place(x=314, y=211)

            self.CongestionControlButton = Button(self.NetworkFrame, image=self.assets_off, command=self.switch_CongestionControl, relief='flat')
            self.CongestionControlButton.place(x=314, y=252)
        else:
            self.label = Label(self.NetworkFrame, text="Options are not available", font=("Arial", 10), background=self.frameBg, foreground="#FFFFFF")
            self.label.place(relx=.5, rely=.5,anchor= CENTER)
    def ScanDNS(self):
        messagebox.showinfo("Scan DNS", "The scan may take a while depending on your internet speed. Don't close the window until it's finished.")
        Core.ScanForBestDnsServer()
        messagebox.showinfo("Scan DNS", "Scanning done")
    
    def switch_irpstackbutton(self):
        if self.irpstackswitch == True:
            self.irpstackswitch = False
            Core.IrpStackSize(0)
            self.irpstackbutton.configure(image=self.assets_off)
        else:
            self.irpstackswitch = True
            Core.IrpStackSize(1)
            self.irpstackbutton.configure(image=self.assets_on)

    def switch_NetworkThrottling(self):
        if self.NetworkThrottling == True:
            self.NetworkThrottling = False
            Core.NetworkThrottling(0)
            self.NetworkThrottlingButton.configure(image=self.assets_off)
        else:
            self.NetworkThrottling = True
            Core.NetworkThrottling(1)
            self.NetworkThrottlingButton.configure(image=self.assets_on)
    
    def switch_CongestionControl(self):
        if self.CongestionControl == True:
            self.CongestionControl = False
            Core.CongestionControl(0)
            self.CongestionControlButton.configure(image=self.assets_off)
        else:
            self.CongestionControl = True
            Core.CongestionControl(1)
            self.CongestionControlButton.configure(image=self.assets_on)

    def switch_tcpnodelay(self):
        if self.NetworkOptimize == True:
            # self.NetworkOptimize = False
            self.switch_tcpnodelayBtn.configure(image=self.assets_off)
        else:
            # self.NetworkOptimize = True
            Core.TcpNoDelay()
            self.switch_tcpnodelayBtn.configure(image=self.assets_on)

    def switch_network(self):
        if self.NetworkOptimize == True:
            self.NetworkOptimize = False
            self.switch_networkBtn.configure(image=self.assets_off)
        else:
            self.NetworkOptimize = True
            self.switch_networkBtn.configure(image=self.assets_on)
    def DetectGameLoop(self):
        #detect the process on top of the screen and if it's a game, add a qos rule
        while(1):
            if self.NetworkOptimize:
                Process = Core.active_window_process_name()
                if Process != None:
                    #check if the process is a game and not a system process
                    if "C:\\Windows\\system32\\" not in Process.exe():
                        if self.LastApp == None:
                            self.LastApp = Process
                        if self.LastApp != Process:
                            self.LastApp = Process
                            Core.RemoveAllQosRules()
                            self.Game = Core.QosRule()
                            self.Game.Name = Process.name()
                            self.Game.SetDSCPValue("3")
                            try:
                                self.Game.AppPathName = Process.exe()
                                self.Game.BuildQosRule()
                            except:
                                print("error")
                            print(self.Game)
                        else:
                            pass
    def CreateGameFrame(self):
        self.GameFrame = Frame(self.root, background=self.frameBg)
        #configure the grid
        self.GameFrame.grid(row=1, column=0, sticky=N+S+E+W)
        self.GameFrame.columnconfigure(0, weight=1)
        self.GameFrame.rowconfigure(0, weight=1)
        # add margin to the frame's grid
        self.GameFrame.grid_propagate(False)
        self.GameFrame.grid_rowconfigure(0, weight=1)
        self.GameFrame.grid_columnconfigure(0, weight=1)
        self.GameFrame.grid_rowconfigure(1, weight=1)
        self.GameFrame.grid_columnconfigure(1, weight=1)
        

        self.GameFrame.place(x=145, y=0)
        self.GameFrame.configure(relief=GROOVE, borderwidth=2)
        self.GameFrame.configure(width=699)
        self.GameFrame.configure(height=410)
        #remove border 
        self.GameFrame.configure(highlightbackground="#1A1A1A")
        self.GameFrame.configure(highlightcolor="black")
        self.GameFrame.configure(highlightthickness=1)
        self.GameFrame.configure(borderwidth=0)

    def CreateSettingFrame(self):
        self.SettingFrame = Frame(self.root, background=self.frameBg)
        #configure the grid
        self.SettingFrame.grid(row=1, column=0, sticky=N+S+E+W)
        self.SettingFrame.columnconfigure(0, weight=1)
        self.SettingFrame.rowconfigure(0, weight=1)
        # add margin to the frame's grid
        self.SettingFrame.grid_propagate(False)
        self.SettingFrame.grid_rowconfigure(0, weight=1)
        self.SettingFrame.grid_columnconfigure(0, weight=1)
        self.SettingFrame.grid_rowconfigure(1, weight=1)
        self.SettingFrame.grid_columnconfigure(1, weight=1)
        

        self.SettingFrame.place(x=145, y=0)
        self.SettingFrame.configure(relief=GROOVE, borderwidth=2)
        self.SettingFrame.configure(width=699)
        self.SettingFrame.configure(height=410)
        #remove border 
        self.SettingFrame.configure(highlightbackground="#1A1A1A")
        self.SettingFrame.configure(highlightcolor="black")
        self.SettingFrame.configure(highlightthickness=1)
        self.SettingFrame.configure(borderwidth=0)

    def ResetWindow(self):
        try:
            self.GameFrame.destroy()
        except:
            pass
        try:
            self.NetworkFrame.destroy()
        except:
            pass

    def AddGame(self, game, path):
        self.GameList["{}".format(game)] = path
        self.GameCount += 1
        #create a button and add it to GameFrame
        self.button = Button(self.GameFrame, text=game, command=lambda:os.system(path), relief='flat',
                                    height=10, width=20,)

        """self.GameX = self.GameX + 10
        if self.GameCount > 30:
            self.GameX = 0
            self.GameY = self.GameY + 10"""
        if self.GameCount == 1:
            self.GameX += 1

        if self.GameCount % 3 == 0:
            self.GameX = 0
            self.GameY = self.GameY + 1
        if self.GameCount != 1:
            self.GameX += 1

        #add button to GameFrame and grid it
        self.button.grid(row=self.GameY, column=self.GameX)

    def buttonHome_click(self):
        self.ResetWindow()
        self.CreateGameFrame()


    def buttonNetwork_click(self):
        self.ResetWindow()
        self.CreateNetworkFrame()

    def buttonSettings_click(self):
        self.ResetWindow()
        self.CreateSettingFrame()

    def mainloop(self):
        self.root.mainloop()