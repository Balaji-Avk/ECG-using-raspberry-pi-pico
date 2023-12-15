from machine import Pin, I2C
import utime
from machine import ADC
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=200000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.fill(0)

adc = ADC(28)
history = []  # List to store ADC readings
peak_detected = False
peak_count = 0
last_peak_time = utime.ticks_ms()
bpm=0
while True:
    adc_reading = round(adc.read_u16() / 64)
    print(adc_reading)
    # Add the ADC reading to the history
    history.append(adc_reading)

    # Keep the history length within the width of the display
    max_history_length = WIDTH // 2

    if len(history) > max_history_length:
        history.pop(0)

    # Calculate the scaling factors for the graph
    max_value = max(history, default=0)
    scale_x = WIDTH / (max_history_length - 1)
    scale_y = (HEIGHT - 50) / max_value  # Adjusted for y = 35

    display.fill(0)
    display.text("ECG:", 10, 0)

    # Draw the line graph
    prev_x, prev_y = None, None
    for i, value in enumerate(history):
        x = int(i * scale_x)
        x2 = int((i + 1) * scale_x) if i < len(history) - 1 else int(i * scale_x)
        y = HEIGHT - 35 - int(value * scale_y)  # Adjusted for y = 35

        if prev_x is not None and prev_y is not None:
            display.line(prev_x, prev_y, x2, y, 1)

        prev_x, prev_y = x, y

    display.show()
    display.text("BPM:", 0, 55)
    display.text(str(bpm), 35, 55)
    display.show()
    # Check for peaks in the ECG signal
    if len(history) > 2 and history[-2] < history[-1] > history[-3]:
        if not peak_detected:
            peak_detected = True
            peak_count += 1
            current_time = utime.ticks_ms()
            elapsed_time = utime.ticks_diff(current_time, last_peak_time)
            last_peak_time = current_time
            bpm = int(60000 / elapsed_time)

            # Adjust BPM to be within the desired range
            bpm = max(60, min(bpm, 95))
            print(f"BPM: {bpm}")

    utime.sleep(0.04)