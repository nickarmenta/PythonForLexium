#! python3

### TO-DO LIST ###
#1 Add threading to reduce stalls
#2 Optimize data transfer
#3 Add Industrial Protocol Capabilities
#4 Create path to multiple commands
#5 Branch out to other product lines
#6 Increase real-time performance

import socket

## Class for sending and receiving commands to motor in Python
class Lexium():
    
    ## Initialize commands (pitch per rev)
    def __init__(self, pitch=1, ratio=1, units='revs'):
        self.units = units
        if units=='deg':
            self.scale = 142.222
        else:
            self.scale = 51200/pitch*ratio

        # Connect to motor at specified IP address
    def Connect(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create proper socket instance
        self.s.connect((ip, 503)) # attempt connection
        self.Write('EM 0') # motor MUST be in echo mode 0 to run this Class

    # converts val to scaled output
    def _Translate(self, val):
        return str(int(val*self.scale))
        
    # Velocity in distance units per second per second
    def Velocity(self, vel):
        self.Write('VM '+self._Translate(vel))
        return self.Read('VM')

    # Acceleration in distance units per second per second
    def Accel(self, acc):
        self.Write('A '+self._Translate(acc))  
        return self.Read('A')

    # Deceleration in distance units per second per second
    def Decel(self, dec):
        self.Write('D '+self._Translate(dec))
        return self.Read('D')

    # Move by a specific amount in one direction
    def MoveBy(self, dist):
        self.Write('MR '+self._Translate(dist))

    # Move to a specific point
    def MoveTo(self, dist):
        self.Write('MA '+self._Translate(dist))

        # Move to a specific point
    def Jog(self, speed):
        self.Write('SL '+self._Translate(speed))

    def WaitForStop(self):
        while(motor.Read('MV')!=0): continue
        return

    def GetPosition(self):
        while(self.Read('P') is None): continue
        return self.Read('P')

    def ReadInput(self, di):
        return self.Read('I'+str(di)) # motor MUST be in echo mode 0 to run this Class

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
        read_msg = None
        while(read_msg is None): read_msg = self.s.recv(1024)

        param_value = [int(i) for i in read_msg.split() if i.isdigit()] # extract numbers in reply
        # Make sure there are parameter values before sending
        if len(param_value) > 0:
            return param_value[0]
        else:
            return None
