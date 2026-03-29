from psychopy import parallel
import time

# Initialize the port address: 0x378 (LPT1), 0x278 (LPT2), 0x3BC
port = parallel.ParallelPort(address=0x378)

def send_trigger(code):
    """
    code: integer between 1-255
    """
    port.setData(code)      # send code
    time.sleep(0.01)        # keep 10 ms 
    port.setData(0)         # clear
    
