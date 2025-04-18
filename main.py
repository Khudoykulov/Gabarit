import serial
import time
import pickle

# COM port va baud rate ni sozlash
com_port = 'COM6'
baud_rate = 9600

ser = serial.Serial(com_port, baud_rate)
print(f"{com_port} portiga ulandim, jism aniqlashni boshlayman...")

# Doimiy devorga qadar masofani max deb olamiz
H_MAX = 29
X_MAX = 17
Y_MAX = 17

# Jism aniqlanish flagi
object_detected = False

# Har bir yo'nalishdagi minimal qiymat (jism o‘tayotganda)
h_min = H_MAX
x_min = X_MAX
y_min = Y_MAX

try:
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
            raw_data = raw_data.replace('см', '').replace('=', '').lower()

            try:
                parts = raw_data.split()
                if len(parts) < 6:
                    continue  # to‘liq 3 ta qiymat bo‘lmasa

                data_dict = {
                    parts[i]: int(parts[i + 1])
                    for i in range(0, len(parts), 2)
                }

                if not all(k in data_dict for k in ['h', 'x', 'y']):
                    continue

                h = data_dict['h']
                x = data_dict['x']
                y = data_dict['y']

                # Jism yaqinlashmoqda (ya'ni masofa kamaymoqda)
                if h < H_MAX-2 or x < X_MAX-2 or y < Y_MAX-2:
                    object_detected = True
                    h_min = min(h_min, h)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)

                # Jism o‘tib ketdi, masofalar qayta maksimalga teng bo‘ldi
                elif object_detected:
                    timestamp = time.strftime("%H:%M:%S")
                    h_size = H_MAX - h_min
                    x_size = X_MAX - x_min - y_min

                    print(f"\n[{timestamp}] Jism aniqlandi:")
                    try:
                        # Oldindan mavjud ma'lumotlarni yuklash
                        with open('object_sizes.pkl', 'rb') as f:
                            saved_data = pickle.load(f)
                    except (FileNotFoundError, EOFError):
                        saved_data = []

                    # Yangi o'lchamlarni qo'shish
                    if h_size >= 1 or x_size >= 1:
                        new_entry = {'timestamp': timestamp, 'h_size': h_size, 'x_size': x_size}
                        saved_data.append(new_entry)

                        # Yangilangan ma'lumotlarni saqlash
                        with open('object_sizes.pkl', 'wb') as f:
                            pickle.dump(saved_data, f)

                    # Natijalarni konsolga chiqarish
                    if h_size >= 1:
                        print(f"  H (balandlik): {h_size} sm")
                    if x_size >= 1:
                        print(f"  X (eni):       {x_size} sm")

                    # Reset qilish
                    object_detected = False
                    h_min = H_MAX
                    x_min = X_MAX
                    y_min = Y_MAX

            except (ValueError, IndexError):
                print("⚠️ Xatolik: noto‘g‘ri format:", raw_data)

except KeyboardInterrupt:
    print("\nDastur to‘xtatildi foydalanuvchi tomonidan.")

finally:
    ser.close()
    print("Serial port yopildi. Dastur tugadi.")
