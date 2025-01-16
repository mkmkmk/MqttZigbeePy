
# Example of Python Integration with Zigbee Devices via MQTT

## Source
This installation guide is based on the official Zigbee2MQTT documentation:

https://www.zigbee2mqtt.io/guide/installation/01_linux.html

The steps have been adapted for a Linux/Debian PC environment instead of the original Raspberry Pi setup.

## Prerequisites
- A Linux/Debian-based system
- Administrator (sudo) privileges
- USB Zigbee adapter connected to your PC
- virtual python environment (venv)

## Tested Hardware
This installation has been verified to work with the following Zigbee devices:
- SONOFF Zigbee 3.0 USB Dongle Plus
- SONOFF SNZB-02P Temperature and Humidity Sensor
- Aqara SP-EUC01 Smart Plug EU


## Installation Steps for Linux/Debian

### 1. Install MQTT Broker
First, install and configure the Mosquitto MQTT broker:
```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### 2. Install Node.js
Install Node.js version 18.x or later:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Verify the installation:
```bash
node --version  # Should show V18.x, V20.x, or V21.x
npm --version   # Should show 9.x or 10.x
```

### 3. Install Zigbee2MQTT
Create and configure the installation directory:
```bash
sudo mkdir /opt/zigbee2mqtt
sudo chown -R ${USER}: /opt/zigbee2mqtt
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
```

Build the application:
```bash
cd /opt/zigbee2mqtt
npm install
npm run build
```

### 4. Configure USB Permissions
Set up proper permissions for the USB device:
```bash
sudo usermod -a -G tty $USER
sudo chmod 666 /dev/ttyUSB0
```

### 5. Configure Zigbee2MQTT
Edit the configuration file:
```bash
gedit /opt/zigbee2mqtt/data/configuration.yaml
```
Adjust the settings according to your setup.
An example configuration.yaml file is included in the project repo.


### 6. Check Zigbee2MQTT in command line
```bash
npm start
```

### 7. Set Up Zigbee2MQTT as System Service
Create and start the Zigbee2MQTT service:
```bash
sudo gedit /etc/systemd/system/zigbee2mqtt.service
sudo systemctl daemon-reload
sudo systemctl start zigbee2mqtt
sudo systemctl enable zigbee2mqtt
```
Adjust the settings according to your setup.
An example zigbee2mqtt.service file is included in the project repo.

### 8. Verify Installation
Check the service status and logs:
```bash
sudo systemctl status zigbee2mqtt
sudo journalctl -xe -u zigbee2mqtt.service -f
```

## Examples

### Simple MQTT listener
```bash
python mqtt_listen.py
```

### Switch on/off
These scripts assume that the directory where they are run contains a .env file with the switch id. Example .env file:

```
SWITCH_ID=<your_switch_id>
```

```bash
python mqtt_switch_on.py 
python mqtt_switch_off.py 
```

### Simple MQTT listen and control

```bash
python mqtt_listen_and_ctrl.py
```

### MQTT listen and log to a .csv files
```bash
python mqtt_listen_and_log.py
```

## Notes
- Make sure your USB Zigbee adapter is properly connected before starting the service
- Check the logs if you encounter any issues
- The system might need a reboot after USB permission change