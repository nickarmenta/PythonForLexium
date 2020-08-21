#! python3

import socket

## Class for sending and receiving commands to motor in Python
class Lexium():
    # Connect to motor at specified IP address
    def Connect(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create proper socket instance
        self.s.connect((ip, 503)) # attempt connection
        self.Write('EM 0') # motor MUST be in echo mode 0 to run this Class

    # Write MCode command to motor
    def Write(self, cmd):
        # Create send string while checking for formatting
        try:
            msg = cmd+'\r'
        except (TypeError):
            raise AssertionError('Commands must be strings')

        self.s.sendall(msg.encode()) # send message as bytes
        if '?' in str(self.s.recv(1024)): print("Error", self.Read('ER')) # print error code if received

    # Read MCode parameter from motor
    def Read(self, param):
        # Create send string while checking for formatting
        try:
            msg = 'PR '+param+'\r'
        except (TypeError):
            raise AssertionError('Parameters must be strings')
        
        self.s.sendall(msg.encode()) # send message as bytes
        param_value = [int(i) for i in self.s.recv(1024).split() if i.isdigit()] # extract numbers in reply
        # Make sure there are parameter values before sending
        if len(param_value) > 0:
            return param_value[0]
        else:
            return None

## Sample Use: Connecting, writing, and reading
## Full list of commands can be found here (direct download link):
## https://motion.schneider-electric.com/download/mcode-operating-system/?wpdmdl=6727&refresh=5f40386cba6e01598044268

# Create class and connect
motor = Lexium()
motor.Connect("192.168.1.33")

print(motor.Read('P')) # confirm motor position
motor.Write('MR 512000') # Move 10 revs

exit()