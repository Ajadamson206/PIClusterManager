import network
import socket
from machine import Pin, I2C
import time

# -------- I2C SETUP --------
# Pico 2 W I2C0: SDA=GP8, SCL=GP9
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)

# -------- SI7021 ADDRESS --------
SI7021_ADDR = 0x40

# -------- HELPER FUNCTIONS --------
def read_temperature():
    # Command 0xF3: measure temperature, no  hold master
    i2c.writeto(SI7021_ADDR, bytes([0xF3]))
    time.sleep(0.05)
    data = i2c.readfrom(SI7021_ADDR, 2)
    raw = (data[0] << 8) | data[1]
    temp_c = ((175.72 * raw) / 65536) - 46.85
    return temp_c

def read_humidity():
    # Command 0xF5: measure humidity, no hold master
    i2c.writeto(SI7021_ADDR, bytes([0xF5]))
    time.sleep(0.05)
    data = i2c.readfrom(SI7021_ADDR, 2)
    raw = (data[0] << 8) | data[1]
    humidity = ((125 * raw) / 65536) - 6
    return max(0, min(100, humidity))

def convert_the_damn_commie_units_to_freedom_units(temperature):
    return temperature * (9/5) + 32
def format_sensor_response():
    try:
        commie_temp = read_temperature()
        hum = read_humidity()
        real_temp = convert_the_damn_commie_units_to_freedom_units(commie_temp)
        return "{:.4f},{:.4f}".format(real_temp, hum)
    except Exception as e:
        return "Error Reading Sensor!"
    time.sleep(1)
# -------- MAIN LOOP --------
print("Starting Si7021 sensor readout...")

SSID = "PI3GEAR"
PASSWORD = "123456789"

PI_IP = "192.168.50.1"    # replace with your Pi’s IP
PI_PORT = "1"

# --- connect WiFi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("Connected! IP:", wlan.ifconfig()[0])

# -------- TCP SERVER --------
port = 5000

# Create socket
server = socket.socket()
server.bind(('', port))
server.listen(1)

print(f"Listening on port {port}...")

while True:
    conn, addr = server.accept()
    print("Client connected:", addr)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            print("Received:", data.decode())
            # Echo back
            response_data = format_sensor_response()
            conn.send(b"ACK: " + response_data)

    except Exception as e:
        print("Error:", e)

    print("Client disconnected")
    conn.close()

