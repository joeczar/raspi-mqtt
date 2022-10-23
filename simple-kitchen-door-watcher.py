from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import time

sense = SenseHat()
sense.clear()
sense.set_rotation(180)

val = 50

red = [val, 0, 0]
blue = [0, val, 0]
green = [0, 0, val]

Message = ""


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global Connected
        Connected = True
        print(f"Connected with code {rc}")
        # sense.show_message("Connected", text_colour=green)

    else:
        print(f"Error code {rc}")


Connected = False


def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    sense.set_pixel(1, 0, 0, 0, val)
    global Message
    Message = msg.payload.decode()
    # time.sleep(0.5)
    sense.clear()


def on_open():
    sense.show_message("Kitchen door is open!", text_colour=red)
    sense.clear()


def on_close():
    sense.show_message("Kitchen door is closed", text_colour=green)
    sense.clear()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", password="IjW2MQTT!")
client.connect("homeassistant.local", 1883, 60)
client.subscribe("kitchen-door", qos=1)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

try:

    while True:

        sense.set_pixel(0, 0, val, 0, 0)

        try:
            while Message == "open":
                on_open()

        except Message == "closed":
            on_close()
            sense.clear()

except KeyboardInterrupt:

    client.disconnect()
    client.loop_stop()
