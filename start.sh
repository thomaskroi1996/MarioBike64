#!/bin/bash
# 1. Create the uinput group and add yourself
sudo groupadd -f uinput
sudo usermod -aG input $USER
sudo usermod -aG uinput $USER

# 2. Create the rule so the kernel allows the group to write to uinput
echo 'KERNEL=="uinput", MODE="0660", GROUP="uinput", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/99-uinput.rules

# 3. Apply the changes immediately
sudo modprobe uinput
sudo udevadm control --reload-rules && sudo udevadm trigger
xhost +si:localuser:root
sudo $(which python) main.py
