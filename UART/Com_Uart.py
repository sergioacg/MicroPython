from machine import UART, Pin
import time

uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

txData = b'hello world\n\r'
uart1.write(txData)
time.sleep(5)
rxData = bytes()
while uart1.any() > 0:
    rxData += uart1.read(1)

print(rxData.decode('utf-8'))