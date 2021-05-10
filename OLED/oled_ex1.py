from machine import Pin, I2C
from utime import sleep_ms
from ssd1306 import SSD1306_I2C
import framebuf

def open_icon(routh):
    doc = open(routh, "rb")
    doc.readline()
    xy = doc.readline()
    x = int(xy.split()[0])
    y = int(xy.split()[1])
    icon = bytearray(doc.read())
    doc.close()
    return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)

WIDTH = 128
HEIGHT = 64

i2c = I2C(1, scl = Pin(19), sda = Pin(18), freq = 200000)

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)

oled.text("Hello World", 0, 0)

oled.show()

sleep_ms(2000)

oled.blit(open_icon("img/CAE.pbm"),35, 10)
oled.show()


