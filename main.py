from machine import Pin, I2C
import utime
from machine import ADC
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=200000)
display = SSD1306_I2C(128, 64, i2c)
display.fill(0)

adc = ADC(28)
while True:
    adc_reading = round(adc.read_u16())
    print(adc_reading)
    display.text(str(adc_reading),0,14)
    display.show()
    display.fill(0)
    utime.sleep(0.04)