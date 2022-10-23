from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import glob

sense=SenseHat()
sense.clear()
sense.set_rotation(180)


red = [255,0,0]
blue = [0,255,0]
green = [0,0,255]

global Connected 
topics_path = './subscriptions'
Topics = []


# sense.show_message("Starting", text_colour=blue)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected with code {rc}")
        # sense.show_message("Connected", text_colour=green)

                      
        Connected = True 
        

    else:
        print(f"Error code {rc}")
        Connected = False 

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    sense.show_message(f"{msg.topic} {msg.payload}", text_colour=red)

def subscription_file_exists():
    filepath = glob.glob(topics_path)
    print(filepath)
    if (filepath):
        print(filepath, "Filepath Exists")
        return True
    else:
        print(filepath, "Filepath doesn't exist")
        False



def topic_exists(topic):
    print("topic_exists", Topics)
    
    if len(Topics) > 0:
        try:
            i = Topics.index(str(topic)+"\n")
            if (i):
                print(topic + " exists")
                return True
        except:
            return False
        
    else:
        print(topic + " is new")
        return False

def write_subscription_topic(topic):
    
    if(subscription_file_exists()):
        f = open(topics_path, "a")
    else: 
        f = open(topics_path, "x")
    if topic_exists(topic):
        return
    else:
        print("writing topic", topic)
        f.write(str(topic)+"\n")
        f.close()

def get_subscription_topics():
    if (subscription_file_exists()):
        f = open(topics_path, "r")
        lines = f.readlines()
        print("Getting topics")
        for line in lines:
            print(line)
            if (topic_exists(line)):
                return
            else:
                Topics.append(line)
        f.close()
        print(Topics)
    else:
        print("No Subscritpions")


def on_add_subscription(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    write_subscription_topic(msg.payload.decode())
    get_subscription_topics()

    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", password="IjW2MQTT!")
client.connect("homeassistant.local", 1883, 60)
client.subscribe("add-subscription", qos=1)
client.message_callback_add("add-subscription", on_add_subscription)
get_subscription_topics()
client.loop_forever()