import RPi.GPIO as GPIO
import time
import subprocess

# Define the LED pin
LED_PIN = 4

# Flash Speed
security_update_interval = 0.3
regular_update_interval = 0.6

# Simulation flags (set to True to simulate updates)
simulate_regular_updates = False
simulate_security_updates = False

# Setup Raspberry Pi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def run_apt_update():
    """Run 'apt update' to refresh the package lists."""
    subprocess.run(["apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_updates():
    """Check for upgradeable packages and determine if any are security updates."""
    if simulate_regular_updates or simulate_security_updates:
        return simulate_regular_updates, simulate_security_updates  # Use simulation flags

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
    try:
        while True:
            run_apt_update()  # Refresh package lists before checking updates
            regular, security = check_updates()
            if security:
                delay = security_update_interval  # Flash faster for security updates
            elif regular:
                delay = regular_update_interval  # Flash slower for regular updates
            else:
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
