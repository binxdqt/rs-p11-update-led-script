import RPi.GPIO as GPIO
import time
import subprocess
import os

# Define the LED pin
LED_PIN = 4

# Path for running check
CHECK_PATH = "/tmp/update_cron.drop"

# Simulation flags (set to True to simulate updates)
SIMULATE_REGULAR_UPDATES = False
SIMULATE_SECURITY_UPDATES = False

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def detect_running():
    """Check to see if the script is already running. Will drop a file if it is not running for future checking."""

    if not (SIMULATE_REGULAR_UPDATES or SIMULATE_SECURITY_UPDATES):
        if os.path.exists(CHECK_PATH):
            return True
        else:
            open(CHECK_PATH, 'a').close()
    else:
        return False

def run_apt_update():
    """Run 'apt update' to refresh the package lists."""
    subprocess.run(["apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_updates():
    """Check for upgradeable packages and determine if any are security updates."""
    if SIMULATE_REGULAR_UPDATES or SIMULATE_SECURITY_UPDATES:
        return SIMULATE_REGULAR_UPDATES, SIMULATE_SECURITY_UPDATES  # Use simulation flags

    result = subprocess.run(["apt", "list", "--upgradeable"], capture_output=True, text=True)
    lines = result.stdout.split("\n")

    regular_updates = False
    security_updates = False

    for line in lines:
        if "/" in line:
            regular_updates = True  # At least one upgradeable package exists
            if "security" in line:
                security_updates = True  # Found a security update

    return regular_updates, security_updates

def flash_led():
    """Flash the LED at different rates based on update type."""
    if detect_running() == True:
        # Ends the script if the script is already running.
        return
    
    try:
        while True:
            run_apt_update()  # Refresh package lists before checking updates
            regular, security = check_updates()
            if security:
                delay = 0.3  # Flash faster for security updates
            elif regular:
                delay = 0.6  # Flash slower for regular updates
            else:
                os.remove(CHECK_PATH) # Delete the check file if updates do not exist so it can run again.
                break  # No updates, exit the loop
            
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    flash_led()
