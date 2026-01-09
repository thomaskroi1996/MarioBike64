import asyncio
from bleak import BleakScanner, BleakClient
import struct
from evdev import UInput, ecodes as e
import tkinter as tk
import gui

ui = UInput()


class HRLogic:
    def __init__(self):
        # Standard Cycling Power Measurement Characteristic UUID
        self.HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        self.HR_THRESHOLD = 100
        self.current_hr = 0

    def get_target_address(self, devices):
        root = tk.Tk()
        app = gui.BluetoothSelectionGUI(root, devices)
        root.mainloop()
        return app.target_address

    def callback(self, sender, data):
        # data[0]: Flags
        # data[1]: HR Value (UINT8)

        hr_value = data[1]
        self.current_hr = hr_value
        print(f"\rHeart Rate: {hr_value} BPM")

    async def hr_acc(self):
        while True:
            if self.current_hr < self.HR_THRESHOLD:
                await asyncio.sleep(0.1)
                continue

            # delay of repeated presses is linear with hr 
            delay = max(0, 0.2 * (1 - (self.current_hr / 190)))

            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.write(e.EV_KEY, e.KEY_X, 1)
            ui.syn()
            await asyncio.sleep(0.05)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
            ui.write(e.EV_KEY, e.KEY_X, 0)
            ui.syn()

            await asyncio.sleep(delay)

    # handles bluetooth connection
    async def hr_ble(self):
        print("Scanning for HR Sensors...")
        devices = await BleakScanner.discover()

        target_address = self.get_target_address(devices)

        if not target_address:
            print("HR Sensor not found. Make sure it is awake.")
            return

        async with BleakClient(target_address) as client:
            print(f"Connected: {client.is_connected}")

            await client.start_notify(self.HR_MEASUREMENT_UUID, self.callback)

            print("Reading raw data (Press Ctrl+C to stop)...")
            while True:
                await asyncio.sleep(1)
