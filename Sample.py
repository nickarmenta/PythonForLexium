import Lexium

## Sample Use: Connecting, writing, and reading
## Full list of commands can be found here (direct download link):
## https://motion.schneider-electric.com/download/mcode-operating-system/?wpdmdl=6727&refresh=5f40386cba6e01598044268

# Create class and connect
motor = Lexium()
motor.Connect("192.168.1.33")

## Use low-leve read/write functions
print(motor.Read('P')) # confirm motor position
motor.Write('RC 1') # Lower run current
motor.Write('HC 1') # Lower hold current

## User higher-level intuitive functions
motor.Accel(100)
motor.Decel(100)
motor.Velocity(10)
motor.MoveBy(-10)
motor.WaitForStop()
motor.MoveTo(0)
motor.WaitForStop()
