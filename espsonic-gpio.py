
import time
import mraa

# Define GPIO Pins for HC-SR04 and Trigger (based on your working setup)
TRIG_PIN = 12    # MRAA Pin 12 (for HC-SR04 TRIG)
ECHO_PIN = 13    # MRAA Pin 13 (for HC-SR04 ECHO)
TRIGGER_PIN = 14 # MRAA Pin 14 (for GPIO trigger to ESP32-CAM)

# Initialize MRAA
mraa.init()

# Setup GPIO for HC-SR04
try:
    trigPin = mraa.Gpio(TRIG_PIN)
    print("TRIG pin {} initialized".format(TRIG_PIN))
except ValueError as e:
    print("Error initializing TRIG pin {}: {}".format(TRIG_PIN, e))
    exit(1)

try:
    echoPin = mraa.Gpio(ECHO_PIN)
    print("ECHO pin {} initialized".format(ECHO_PIN))
except ValueError as e:
    print("Error initializing ECHO pin {}: {}".format(ECHO_PIN, e))
    exit(1)

trigPin.dir(mraa.DIR_OUT)
echoPin.dir(mraa.DIR_IN)

# Setup GPIO for Trigger
try:
    triggerPin = mraa.Gpio(TRIGGER_PIN)
    print("TRIGGER pin {} initialized".format(TRIGGER_PIN))
except ValueError as e:
    print("Error initializing TRIGGER pin {}: {}".format(TRIGGER_PIN, e))
    exit(1)

triggerPin.dir(mraa.DIR_OUT)
triggerPin.write(0)  # Start with LOW

def measure_distance():
    # Check initial state of ECHO pin
    initial_state = echoPin.read()
    print("ECHO pin initial state: {}".format(initial_state))
    if initial_state == 1:
        print("Warning: ECHO pin is HIGH before measurement. Check wiring or sensor.")
        return None

    # Ensure trigger pin is LOW
    trigPin.write(0)
    time.sleep(0.00001)  # 10 µs delay
    
    # Send 10 µs pulse to trigger
    trigPin.write(1)
    time.sleep(0.00001)
    trigPin.write(0)
    
    # Measure the echo pulse duration
    start_time = time.time()
    timeout = start_time + 0.02  # 20 ms timeout
    while echoPin.read() == 0:
        start_time = time.time()
        if start_time > timeout:
            print("Echo signal timeout (no response)")
            return None
    
    stop_time = time.time()
    timeout = stop_time + 0.02
    while echoPin.read() == 1:
        stop_time = time.time()
        if stop_time > timeout:
            print("Echo signal timeout (stuck HIGH)")
            return None
    
    # Calculate distance (speed of sound = 343 m/s = 34300 cm/s)
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Divide by 2 since the sound travels to the object and back
    
    return distance

try:
    while True:
        distance = measure_distance()
        if distance is not None:
            print("Distance: {:.2f} cm".format(distance))
            
            if distance < 60:
                print("Object detected! Sending GPIO trigger to ESP32")
                triggerPin.write(1)  # Set HIGH to trigger the interrupt
                time.sleep(0.05)  # 50 ms pulse (enough for ESP32 to detect)
                triggerPin.write(0)  # Set LOW
                time.sleep(2)  # Wait 2 seconds for ESP32-CAM to process the photo
            else:
                triggerPin.write(0)  # Ensure LOW when no object is detected
                
        time.sleep(0.5)  # Check distance every 0.5 seconds

except KeyboardInterrupt:
    print("\nMeasurement stopped")
    triggerPin.write(0)  # Ensure trigger is LOW on exit
