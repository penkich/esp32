#
# socket を使った簡単なテスト 2017-05-20
# サーバー、クライアントとも、sta_ifでWiFiに接続しておく
# 時間経過により、サーバ、クライアント双方のNeopixelの色が変わる
# タイマーのオーバーフロー問題ありそう
#
from machine import Pin
from neopixel import NeoPixel
import socket
import time

def callback(p): # たぶんこの方法よくない。
    global start
    start = time.ticks_ms()
    print(p)
    time.sleep(0.5)

p5 = Pin(5, Pin.IN, Pin.PULL_UP) # タイマーをリセットするSWをつなぐ。
p5.irq(trigger=Pin.IRQ_FALLING, handler=callback)
pin = Pin(4,Pin.OUT) # NeoPixel の信号線を接続
np = NeoPixel(pin, 1) # NeoPixel は１つ接続
port = 6809 # 適当

addr = socket.getaddrinfo('0.0.0.0',port)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
start = time.ticks_ms()

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
    cl,addr = s.accept()
#    cl_file = cl.makefile('rwb',0)
    delta = time.ticks_diff(time.ticks_ms(), start)
    print('client connected from',addr)
    cl.send(bytes(str(delta),'utf8'))
    print(str(delta))
    led(delta) # クライアントからの接続なければ更新されませんね。
    cl.close()
