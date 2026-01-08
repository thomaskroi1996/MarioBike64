import requests
import time
from evdev import UInput, ecodes as e

ui = UInput()

# URL from phyphox app
PHYPHOX_URL = "http://192.168.1.15:8080"
TILT_THRESHOLD = 3.0

def get_tilt():
    try:
        # 'accX' is the internal name for the X-axis in the "Acceleration with g" experiment
        response = requests.get(f"{PHYPHOX_URL}/get?accX=val", timeout=0.1)
        data = response.json()

        acc_x = data['buffer']['accX']['value'][0]
        return acc_x
    except Exception as e:
        print(f"Error connecting to Phyphox: {e}")
        return 0

print("Steering Active! Tilt your phone to steer.")

try:
    while True:
        tilt = get_tilt()

        if tilt > TILT_THRESHOLD:
            ui.write(e.EV_KEY, e.KEY_LEFTARROW, 1)
            ui.write(e.EV_KEY, e.KEY_RIGHTARROW, 0)
            print(f"Left  ({tilt:.2f})")
        elif tilt < -TILT_THRESHOLD:
            ui.write(e.EV_KEY, e.KEY_RIGHTARROW, 1)
            ui.write(e.EV_KEY, e.KEY_LEFTARROW, 0)
            print(f"Right ({tilt:.2f})")
        else:
            ui.write(e.EV_KEY, e.KEY_RIGHTARROW, 1)
            ui.write(e.EV_KEY, e.KEY_LEFTARROW, 0)
            
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("Stopping...")
