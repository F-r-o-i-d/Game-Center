import Gui
import threading
import socket
import os
import Core
import Overlay

if Core.CheckIfRunningAsAdmin() != True:
    if Core.RunAsAdmin() != True:
        popup = Overlay.Overlay()
        popup.SetText("Please run this program as administrator")
        popup.show()
        exit()
    else:
        exit()



App = Gui.App()
runServer = True
#create a simple webserver
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8086
    s.bind((host, port))
    print((host, port))
    s.listen(5)
    while True:
        if runServer:
            c, addr = s.accept()
            print("Got connection from", addr)
            a = c.recv(1024)
            # when the client sends the data, the server will send an html ok response
            c.send(b"HTTP/1.1 200 OK\n\n<html><body><h1>OK</h1></body></html>")
            c.close()
            break
    App.IsDevMode = True

threading.Thread(target=server).start()
App.IsDevMode = True

App.root.mainloop()
runServer = False
os.system("taskkill /f /im python.exe")

