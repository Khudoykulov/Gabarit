import serial

# COM port va baud rate ni sozlang
com_port = 'COM3'  # COM port nomini moslang
baud_rate = 9600   # Arduino'dagi baud rate bilan moslang

# Serial portni oching
ser = serial.Serial(com_port, baud_rate)

print(f"{com_port} portiga ulandim, ma'lumotlarni qabul qilishni boshlayman...")

h_max = 0; h_min = 30
x_max = 0; x_min = 30
y_max = 0; y_min = 30
try:
    while True:
        if ser.in_waiting > 0:
            # data = ser.readline().decode('utf-8').strip()
            data = ser.readline().decode('latin-1').strip()
            data = data[:-4].split()
            h, x, y = int(data[1]), int(data[3]), int(data[5])
            h_max = max(h_max, h); h_min = min(h_min, h)
            x_max = max(x_max, x); x_min = min(x_min, x)
            y_max = max(y_max, y); y_min = min(y_min, y)
except KeyboardInterrupt:
    print(f"Qiymatlar: H={h_max - h_min}, X={x_max - x_min}, Y={y_max - y_min}")
    print("Dastur to'xtatildi.")
finally:
    ser.close()
    print("Serial port yopildi.")
