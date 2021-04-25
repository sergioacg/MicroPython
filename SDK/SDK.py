import machine 
import utime


i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=200000) 

direccion = hex(i2c.scan()[0])

print('La dirección I2C es ', direccion)
