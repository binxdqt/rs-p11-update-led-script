# APT Update LED Indicator Script for 52Pi RS-P11 Expansion Boards
Use the red LED indicator on the 52Pi RS-P11 to notify you about system updates.

![Raspberry Pi indicator light flashing.](https://github.com/binxdqt/rs-p11-update-led-script/blob/main/flash_sample.gif?raw=true)

## Features
- Automatically run the `apt update` command to check the system for software updates.
- Receive a visual notification on your headless Pi setup when an update is available.
- Different flash times for regular & security updates, with priority for security updates if both exist.
- Simple deployment with python3 and cron.

## Script Installation
1. Download the update_cron.py file from this repository.
2. Save the file somewhere on your device, such as `~/Documents/cron/`
3. In terminal, run the command `sudo crontab -e` to create a new cron job.
4. Add the following line to run the script every 24 hours:
```
0 * * * * python3 /home/%user%/Documents/cron/update_cron.py
```

Replace `%user%` with your username. Cron does not use the tilde `~` wildcard.

## Customizations
You can quickly modify the following variables at the top of the script to fit your needs:

**LED_PIN:** [INT] Change the LED that will flash. By default, this script uses the pin specifically for the 52Pi RS-P11.

**security_update_interval:** [FLOAT] ON/OFF state per second when there is a security update. Default is `0.3` seconds.

**regular_update_interval:** [FLOAT] ON/OFF state per second when there is a regular update. Default is `0.6` seconds.

## Simulation Flags
You can use the simulation flags at the top of the script to test the script.

Set either `simulate_regular_updates` or `simulate_security_updates` to `True` if you want to simulate the blinking LED. Default value is `False`.

## About
This is my first GitHub repository! Please let me know how I did in Discussions.

I created this script after I purchased a RackMate T1 and the Geeekpi RS02 2U Raspberry Pi rack. The RS02 comes with these PCIe to NVMe expansion boards which has a red LED at the front. I wanted to use the red LED for something, and since I'm not checking my devices every single day, I thought it would be useful to know when all of my devices need updates and remembered that the red LED indicator is connected to a GPIO pin. I created this script to simply flash the LED at the front, so I know when updates are needed without having to check manually.
