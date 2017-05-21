from machine import Pin
from neopixel import NeoPixel
import socket
import time
pin = Pin(4,Pin.OUT) # NeoPixelの信号線を接続
np = NeoPixel(pin, 1) # NeoPixelを1つ使う

host = '192.168.1.45' # サーバアドレス
port = 6809

def led(t):
    if t < 600000:
        rgb = [0,100,0]
    elif t < 1200000:
        rgb = [30,80,0]
    elif t < 1800000:
        rgb = [50,50,0]
    elif t < 6000000:
        rgb = [80,0,0]
    else:
        rgb = [0,0,0]
    np[0] = rgb
    np.write()

while True:
    try:
        s = socket.socket()
        s.connect([host,port])
        data = s.recv(200)
        led(int(data))
        print(str(data,'utf-8'))
    except:
        pass
    s.close()
    time.sleep(5)
