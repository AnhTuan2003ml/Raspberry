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

# Hiển thị vật thể và chướng ngại vật trên màn hình LCD
def display_objects(player_pos, obstacle_pos, obstacle_line):
    lcd_byte(0x01, LCD_CMD)  # Xóa màn hình

    if obstacle_line == 1:
        lcd_string(" " * obstacle_pos + "O", LCD_LINE_1)
    else:
        lcd_string(" " * obstacle_pos + "O", LCD_LINE_2)

    if player_pos == 1:
        lcd_string("P", LCD_LINE_1)
    else:
        lcd_string("P", LCD_LINE_2)

# Hàm chính điều khiển trò chơi
def main():
    lcd_init()

    # Vị trí khởi tạo
    player_position = 1  # Người chơi ban đầu ở dòng 1
    obstacle_position = LCD_WIDTH - 1  # Chướng ngại vật bắt đầu từ bên phải
    obstacle_line = 1  # Chướng ngại vật bắt đầu từ dòng 1
    speed = 0.5  # Tốc độ di chuyển chướng ngại vật

    while True:
        # Hiển thị vật thể và chướng ngại vật
        display_objects(player_position, obstacle_position, obstacle_line)

        # Di chuyển chướng ngại vật sang trái
        obstacle_position -= 1
        if obstacle_position < 0:
            obstacle_position = LCD_WIDTH - 1  # Chướng ngại vật quay lại từ phải
            obstacle_line = 2 if obstacle_line == 1 else 1  # Thay đổi dòng của chướng ngại vật

        # Điều khiển người chơi di chuyển lên hoặc xuống
        if GPIO.input(BUTTON_UP_PIN) == GPIO.LOW:
            player_position = 1  # Di chuyển người chơi lên dòng 1
            time.sleep(0.2)  # Debounce

        if GPIO.input(BUTTON_DOWN_PIN) == GPIO.LOW:
            player_position = 2  # Di chuyển người chơi xuống dòng 2
            time.sleep(0.2)  # Debounce

        # Kiểm tra va chạm
        if obstacle_position == 0 and player_position == obstacle_line:
            lcd_string("GAME OVER", LCD_LINE_1)
            break

        time.sleep(speed)  # Tốc độ di chuyển của chướng ngại vật

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)  # Xóa màn hình LCD
        GPIO.cleanup()  # Dọn dẹp GPIO
