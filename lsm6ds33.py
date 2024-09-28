import smbus
import math
import ctypes
import time

i2c = smbus.SMBus(1)
ADDR = 0x6b

gyro_offset = [0, 0, 0]
acc_gravity = 0.0

gyro_scale = 0.0175 / 13
    # 500dps, 17.5mdps/LSB, 13Hz
acc_scale = 0.061 * 0.001
    # 2g, 0.061mg/LSB, 13Hz

def init():
    global gyro_offset
    global acc_gravity
    global degree
    gyro_offset_tmp = [0, 0, 0]

    # 0x0F [WHO_AM_I] has 0x69 = b'01101001', read only
    if(i2c.read_byte_data(ADDR, 0x0F) != 0x69):
        print("error : LSM6DS33 is not connected")
        exit(1)
    
    i2c.write_byte_data(ADDR, 0x10, 0x10)
    i2c.write_byte_data(ADDR, 0x11, 0x14)
#    i2c.write_byte_data(ADDR, 0x16, 0x00)

    # 0x10 [CTRL1_XL] is linear acceleration sensor control register
    # 4-7bit : Output data rate  23bit : scale  01bit : filter
    # 0x11 [CTRL2_XL] is angular rate sensor control register
    # 4-7bit : Output data rate  1-3bit : scale  0bit : 0

    # The average of first 10 data is saved as an offset
    for i in range(10):
        while(not is_available()):
            pass
        gyro_tmp = get_gyro()
        gyro_offset_tmp = [x + y for x, y in zip(gyro_offset_tmp, gyro_tmp)] 

    gyro_offset = [round(x/10) for x in gyro_offset_tmp]
    acc_tmp = get_acc()
    degree[0] = math.degrees(math.asin(acc_tmp[1] * acc_scale))

def get_temp():
    temp = i2c.read_i2c_block_data(ADDR, 0x20, 2)
    temp = temp[1] << 8 | temp[0]
    return ctypes.c_int16(temp).value / 16 + 25

    # read_i2c_block_data returns list of int
    # This register uses big-endian
    # e.g. [0x01, 0x02] -> 0x0201 = 513

    # temperature sensitivity : LSB / Degree Celsius
    # temperature offset      : 25 [Degree Celsius]
    # c_int16 : [unsigned short] changes [signed short]

def get_gyro():
    gyro = i2c.read_i2c_block_data(ADDR, 0x22, 6)
    gyro_x = gyro[1] << 8 | gyro[0]
    gyro_y = gyro[3] << 8 | gyro[2]
    gyro_z = gyro[5] << 8 | gyro[4]
    gyro_x = ctypes.c_int16(gyro_x).value
    gyro_y = ctypes.c_int16(gyro_y).value
    gyro_z = ctypes.c_int16(gyro_z).value
#    return [gyro_x, gyro_y, gyro_z]
    return [gyro_x - gyro_offset[0], gyro_y - gyro_offset[1], gyro_z - gyro_offset[2]]

def get_acc():
    acc = i2c.read_i2c_block_data(ADDR, 0x28, 6)
    acc_x = acc[1] << 8 | acc[0]
    acc_y = acc[3] << 8 | acc[2]
    acc_z = acc[5] << 8 | acc[4]
    acc_x = ctypes.c_int16(acc_x).value
    acc_y = ctypes.c_int16(acc_y).value
    acc_z = ctypes.c_int16(acc_z).value
    return [acc_x, acc_y, acc_z]

def is_available():
    time.sleep(0.01)
    if i2c.read_byte_data(ADDR, 0x1E) == 0x07:
        return True
    return False
    # 0x1E [STATUS_REG] indicates that new sensor data is available
    # bit2 : Temperature  bit1 : Gyroscope  bit0 : Accelerometer

gyro_x = 0
gyro_y = 0
gyro_z = 0

acc_x = 0
acc_y = 0
acc_z = 0

degree = [0.0, 0.0, 0.0]

init()

while(True):
    while not is_available():
        pass
    gyro = get_gyro()
    acc = get_acc()
    gyro_x = gyro[0] * gyro_scale
    gyro_y = gyro[1] * gyro_scale
    gyro_z = gyro[2] * gyro_scale
    acc_x = acc[0] * acc_scale
    acc_y = acc[1] * acc_scale
    acc_z = acc[2] * acc_scale
#    print(f"gyro x : {gyro_x:.4f}, y : {gyro_y:.4f}, z:{gyro_z:.4f}")
#    print(f"acc  x : {acc_x:.4f}, y : {acc_y:.4f}, z:{acc_z:.4f}")
    # Correct the value between -1 and 1
    acc_rate_x = acc_y if abs(acc_y) <= 1 else acc_rate_x
    degree[0] = 0.02 * math.degrees(math.asin(acc_rate_x)) + 0.98 * (degree[0] + gyro_x)
    print(degree[0])