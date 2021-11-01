"""
Nivel de un Tanque

by: Sergio Andrés Castaño Giraldo
Sitio web: https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import Pin, PWM, ADC, I2C, Timer
from utime import sleep_ms
from ssd1306 import SSD1306_I2C


#OLED
WIDTH = 128
HEIGHT = 64  
#Configuración de PINES
sensor = ADC(26) 
voltaje = ADC(27)
potenciometro = ADC(28)
pwm = PWM(Pin(20)) 
pwm.freq(40000)
i2c = I2C(1, scl = Pin(19), sda = Pin(18), freq = 200000)

#OLED
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

#Global Variables
t = 0
y = [55, 55]
x = [25, 25]
level = 0

   
    
def plot_time(yp, t, x, y, var = [0.0,18], vpts=[25, 16, 40], hpts = [25, 55, 112]):
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
    global dt
    #Axis
    oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
    oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
    oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
    oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    #Level
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

        

def main():
    global level, t, y, x
    
    #Sensor Presión
    tolP=0.4 # Ajusta la medida de presión
    rho = 1000 #Densidad del Agua
    g=9.8     #Gravedad
    factor_16 = 3.3 / (65535)

    while True:         
        
        #Presión en Kpa según gráfica 4 del Datasheet
        level_sum = 0
        for i in range(200):
            Vout = sensor.read_u16() * factor_16
            Vs = voltaje.read_u16() * factor_16
            presion = ( Vout - 0.04*Vs ) / (0.09 * Vs) + tolP #kPa
            level_sum += ((presion*1000)/(rho*g))*100;  #Medida de Nivel del tanque
            
        level_x = level_sum / 200
        level = 1.157 * level_x - 2.1208
        
        #print(level)
        
        t,x,y = plot_time(level,t,x,y)
        oled.fill_rect(0,0,128,15,0)
        oled.text("Lvl: ", 0, 0)
        oled.text(str(round(level,1)), 32, 0)
        oled.show()
        
        #Aplica el PWM al motor
        velocidad = int(potenciometro.read_u16())
        pwm.duty_u16(velocidad)
            
        sleep_ms(100)
    

if __name__ == '__main__':
    main()