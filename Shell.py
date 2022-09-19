import subprocess

class Shell():
    def __init__(self) -> None:
        pass
    def Exec(command):
        #split command to list by space but let quotes stay together
        #command = split(command)
        
        command = "powershell " + command 
        return subprocess.check_output(command).decode("utf-8")