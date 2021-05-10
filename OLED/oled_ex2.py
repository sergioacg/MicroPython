"""
OLED with MicroPython: Raspberry Pi Pico  and ESP8266
By: Sergio Andres Castaño Giraldo
site: https://controlautomaticoeducacion.com/micropython/
GitHub: https://github.com/sergioacg/MicroPython

Useful links:
# https://docs.micropython.org/en/latest/library/framebuf.html
# https://micropython-workshop.readthedocs.io/en/latest/pages/shields/oled.html
# http://javl.github.io/image2cpp/
"""

from machine import Pin, I2C, ADC
from utime import sleep_ms
from ssd1306 import SSD1306_I2C
import framebuf
from images import (logo)


def plot_time(yp, t, x, y, var = [0.0,3.3], vpts=[25, 16, 40], hpts = [25, 55, 112]):
    """"
    Graph function of the Cartesian plane in relation to time:
    by: Sergio Andres Castaño Giraldo
    
    plot_time(yp, t, x, y, var = [0.0,3.3], vpts=[25, 16, 40], hpts = [25, 55, 112]):

    yp: dependent variable
    t: time (used while the Cartesian plane is not complete)
    x: List of two positions of variable x, x[0] is the position in past x and x[1] position of current x.
    y: List of two positions of the variable y, y[0] is the position in y past and y[1] position of current x.
    var = [0.0,3.3]: Magnitude of the variable (default voltage)
    vpts = [25, 16, 40]: points on the vertical y axis.
    hpts = [25, 55, 112]: points on the vertical x axis.

    Example:
    #Global Variables
    t = 0
    y = [55, 55]
    x = [25, 25]
    #Function:
    volts = pot.read_u16 () * FACTOR
    t, x, y = plot_time (volts, t, x, y)
    sleep_ms (500)
    """
    #Axis
    oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
    oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
    oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
    oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    #y - axis
    y[1] = int((yp-var[0])/(var[1]-var[0]) * (vpts[1]-hpts[1]) + hpts[1]) #Interpolation
    if t < hpts[2] - hpts[0]:
        x[1] = x[0]+1
    else:
        x[1] = hpts[2]
    
    #Plot the line
    oled.line(x[0],y[0],x[1],y[1],1)
    oled.show()
    
    #Update past values
    y[0] = y[1]
    x[0] = x[1]
    
    #If you have already reached the end of the graph then ...
    if t > hpts[2] - hpts[0]:
        #Erases the first few pixels of the graph and the y-axis.
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0)
        #Clears the entire y-axis scale
        oled.fill_rect(vpts[0]-25, vpts[1],vpts[0],vpts[2]+5,0)
        #shifts the graph one pixel to the left
        oled.scroll(-1,0)
        #Axis
        oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
        oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
        oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
        oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    else:
        t += 1
    
    return t,x,y
        



if __name__ == '__main__':
    
    WIDTH = 128
    HEIGHT = 64
    FACTOR = 3.3 / (65535)
    
    PLACA = False #True: Raspberry Pi Pico, False: ESP8266
    
    if PLACA:
        i2c = I2C(1, scl = Pin(19), sda = Pin(18), freq = 200000)
        pot = ADC(26)
    else:
        i2c = I2C(scl = Pin(5), sda = Pin(4))
        pot = ADC(0)
    
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    
    
    buffer = bytearray(logo)
    
    fb = framebuf.FrameBuffer(buffer,WIDTH,HEIGHT,framebuf.MONO_HLSB)
    

    #Global Variables
    t = 0
    y = [55, 55]
    x = [25, 25]
    
    oled.fill(0)
    oled.text("Control", 35, 0)
    oled.text("Automatico", 20, 20)
    oled.text("Educacion", 25, 40)
    oled.show()
    sleep_ms(3000)
    
    #Image
    oled.fill(0)
    oled.blit(fb,0,0)
    oled.show()
    sleep_ms(3000)
    oled.fill(0)
    
    while True:
        volts = pot.read_u16() * FACTOR
        t,x,y = plot_time(volts,t,x,y)
        oled.fill_rect(0,0,120,15,0)
        oled.text("Volts: ", 0, 0)
        oled.text(str(round(volts,1)), 52, 0)
        oled.show()
        sleep_ms(100)
        

