# Object-and-intrusion-detction

Object and Intrusion Detection Using RuggedBoard A5D2X
This project implements an IoT-based object and intrusion detection system using the RuggedBoard A5D2X, HC-SR04 ultrasonic sensor, ESP32-CAM, and a XAMPP server. The system detects objects within a 60 cm range, captures images of intrusions, and uploads them to a local server for real-time monitoring and logging.
Table of Contents

Project Overview
Prerequisites
Hardware Requirements
Software Requirements
Installation Steps
How It Works
Directory Structure
Troubleshooting
Contributing
License

Project Overview
The system leverages the RuggedBoard A5D2X to process data from an HC-SR04 sensor, which detects objects within a 60 cm threshold. Upon detection, the board triggers the ESP32-CAM to capture an image via GPIO interrupts. The ESP32-CAM uploads the image to a XAMPP server over WiFi, where it’s stored and displayed in a web interface for monitoring. This setup is ideal for surveillance, smart monitoring, or automated security applications.
Prerequisites

Basic knowledge of embedded systems, Python, and PHP.
Access to a computer with a Linux/Windows environment for setup.
WiFi network for ESP32-CAM connectivity.
MicroSD card for RuggedBoard A5D2X (optional for OS installation).

Hardware Requirements

RuggedBoard A5D2X: Microchip SAMA5D2-based single-board computer.
HC-SR04 Ultrasonic Sensor: For distance measurement (2-400 cm range).
ESP32-CAM: Camera module with OV2640 for image capture.
Jumper Wires: For connecting components.
Power Supply: 5V for RuggedBoard and ESP32-CAM.
USB-to-Serial Adapter: For ESP32-CAM programming.

Software Requirements

Embedded Linux: For RuggedBoard A5D2X (e.g., Debian-based image).
Python 3: For RuggedBoard sensor scripts (with RPi.GPIO-compatible library for GPIO).
Arduino IDE: For programming the ESP32-CAM.
XAMPP: For hosting the local server (Apache and PHP).
Git: For cloning this repository.
Web Browser: For accessing the XAMPP server interface.

Installation Steps
Follow these steps to set up the system:
1. Clone the Repository
git clone https://github.com/your-username/object-intrusion-detection.git
cd object-intrusion-detection

2. Set Up the RuggedBoard A5D2X

Install Embedded Linux:
Download a Debian-based image for the RuggedBoard A5D2X from the official site.
Flash the image to a microSD card using a tool like Balena Etcher.
Insert the microSD card into the RuggedBoard and power it on.


Install Dependencies:sudo apt update
sudo apt install python3 python3-pip
pip3 install RPi.GPIO  # Note: Use a compatible GPIO library for SAMA5D2


Copy RuggedBoard Code:
Copy ruggedboard_intrusion.py from the code/ruggedboard directory to the RuggedBoard.

scp code/ruggedboard/ruggedboard_intrusion.py user@<ruggedboard-ip>:/home/user



3. Configure the HC-SR04 Sensor

Connect the Sensor:
Wire the HC-SR04 to the RuggedBoard A5D2X:
VCC → 5V
GND → GND
TRIG → GPIO pin (e.g., PA10)
ECHO → GPIO pin (e.g., PA11)


Update ruggedboard_intrusion.py with the correct GPIO pin numbers if needed.


Test the Sensor:python3 ruggedboard_intrusion.py


Verify distance readings appear in the terminal.



4. Program the ESP32-CAM

Set Up Arduino IDE:
Install the Arduino IDE and add ESP32 board support:
Go to File > Preferences > Additional Boards Manager URLs and add:https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json


Install esp32 by Espressif Systems in Boards Manager.




Upload Code:
Open code/esp32-cam/esp32_cam_capture.ino in Arduino IDE.
Update WiFi credentials and server URL:const char* ssid = "your-wifi-ssid";
const char* password = "your-wifi-password";
const char* serverName = "http://<your-xampp-server-ip>/upload.php";


Connect the ESP32-CAM via a USB-to-Serial adapter.
Select AI Thinker ESP32-CAM as the board and upload the code.


Test the ESP32-CAM:
Open the Serial Monitor (115200 baud) to verify WiFi connection and image capture triggers.



5. Set Up the XAMPP Server

Install XAMPP:
Download and install XAMPP for your OS (Windows/Linux) from apachefriends.org.
Start Apache and ensure PHP is enabled.


Configure the Server:
Copy code/server/upload.php and the captured_images directory to XAMPP’s htdocs folder:cp -r code/server/* /path/to/xampp/htdocs/


Ensure the captured_images directory has write permissions:chmod -R 777 /path/to/xampp/htdocs/captured_images




Access the Interface:
Open a browser and navigate to http://<your-xampp-server-ip>/upload.php.
Verify the gallery displays test images.



6. Run the System

Power on the RuggedBoard and ESP32-CAM.
Run the RuggedBoard script:python3 ruggedboard_intrusion.py


Monitor the XAMPP server interface for uploaded images when objects are detected within 60 cm.

How It Works

Object Detection:

The HC-SR04 sensor, connected to the RuggedBoard A5D2X, measures distances continuously.
If an object is detected within 60 cm, the RuggedBoard generates a GPIO interrupt.


Image Capture:

The interrupt triggers the ESP32-CAM to capture an image using its OV2640 camera module.
The ESP32-CAM connects to the WiFi network and prepares the image for upload.


Image Upload and Storage:

The ESP32-CAM sends the image to the XAMPP server via an HTTP POST request.
The server’s upload.php script saves the image in the captured_images directory with a timestamp.


Monitoring:

The XAMPP server hosts a web interface displaying a gallery of captured images.
Operators can access http://<server-ip>/upload.php to view intrusion events in real-time.



Directory Structure
object-intrusion-detection/
├── code/
│   ├── ruggedboard/
│   │   └── ruggedboard_intrusion.py  # RuggedBoard sensor script
│   ├── esp32-cam/
│   │   └── esp32_cam_capture.ino     # ESP32-CAM Arduino sketch
│   └── server/
│       ├── upload.php                # PHP script for image upload
│       └── captured_images/          # Directory for stored images
├── docs/
│   └── report.pdf                    # Project documentation
├── README.md                         # This file
└── LICENSE                           # License file

Troubleshooting

HC-SR04 Not Detecting:
Check GPIO pin assignments in ruggedboard_intrusion.py.
Ensure proper wiring and 5V power supply.


ESP32-CAM Fails to Connect:
Verify WiFi credentials in esp32_cam_capture.ino.
Check Serial Monitor for error logs.


Images Not Uploading:
Confirm XAMPP server is running and captured_images has write permissions.
Ensure the server IP in esp32_cam_capture.ino matches your setup.


RuggedBoard Script Errors:
Verify Python and GPIO library installations.
Run python3 --version and pip3 show RPi.GPIO to check dependencies.



Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code follows the project’s style and includes relevant documentation.
License
This project is licensed under the MIT License. See the LICENSE file for details.

 
