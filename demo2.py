import smbus2
import time
import RPi.GPIO as GPIO

# Địa chỉ I2C của LCD
I2C_ADDR = 0x27
LCD_WIDTH = 16  # Kích thước màn hình LCD 16x2

# Một số hằng số điều khiển LCD
LCD_CHR = 1  # Chế độ ký tự
LCD_CMD = 0  # Chế độ lệnh

LCD_LINE_1 = 0x80  # Địa chỉ của dòng 1 trên LCD
LCD_LINE_2 = 0xC0  # Địa chỉ của dòng 2 trên LCD

# Định nghĩa các chân nút bấm
BUTTON_UP_PIN = 17  # Chân GPIO nút lên
BUTTON_DOWN_PIN = 27  # Chân GPIO nút xuống

# Khởi tạo giao tiếp I2C
bus = smbus2.SMBus(1)

# Thiết lập GPIO cho các nút bấm
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Hàm gửi dữ liệu đến LCD
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08

    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

# Bật tín hiệu cho LCD
def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~0x04))
    time.sleep(0.0005)

# Khởi tạo LCD
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.0005)

# Viết chuỗi lên màn hình LCD
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Hiển thị chướng ngại vật tại vị trí cụ thể
def display_obstacle(position):
    lcd_string(" " * position + "O", LCD_LINE_1)

# Hàm chính điều khiển chướng ngại vật di chuyển
def main():
    lcd_init()

    # Vị trí khởi tạo và tốc độ di chuyển chướng ngại vật
    obstacle_position = 0
    speed = 0.5  # Tốc độ di chuyển (thời gian dừng giữa các lần di chuyển)

    display_obstacle(obstacle_position)

    while True:
        # Di chuyển chướng ngại vật
        obstacle_position += 1
        if obstacle_position >= LCD_WIDTH:
            obstacle_position = 0
        display_obstacle(obstacle_position)

        # Điều chỉnh tốc độ bằng nút bấm
        if GPIO.input(BUTTON_UP_PIN) == GPIO.LOW:
            speed = max(0.1, speed - 0.1)  # Giảm thời gian dừng, tăng tốc độ
            time.sleep(0.2)  # Debounce

        if GPIO.input(BUTTON_DOWN_PIN) == GPIO.LOW:
            speed = min(1, speed + 0.1)  # Tăng thời gian dừng, giảm tốc độ
            time.sleep(0.2)  # Debounce

        time.sleep(speed)  # Tốc độ di chuyển của chướng ngại vật

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)  # Xóa màn hình LCD
        GPIO.cleanup()  # Dọn dẹp GPIO
