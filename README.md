# ESP32-Based IoT Smart Energy Meter Monitoring System

An IoT-based smart energy meter monitoring project using ESP32, Embedded C++, Wi-Fi, MQTT, and JSON for periodic energy telemetry and remote monitoring simulation.

## 📌 Project Overview

This project demonstrates an IoT-based smart energy meter monitoring system that publishes simulated electrical readings, such as voltage, current, and energy consumption, over MQTT.

The ESP32 firmware connects to Wi-Fi, synchronizes time using NTP, and periodically publishes JSON-formatted telemetry to an MQTT broker. The repository also includes supporting components for simulation, API integration, dashboard visualization, and Home Energy Management System (HEMS/HES) experimentation.

**Note:** This project uses simulated or prepared readings for demonstration. It should not be considered a physical energy meter measurement or a certified electricity-metering system.

## 🎯 Objectives

- Develop ESP32 firmware using Embedded C++.
- Establish Wi-Fi connectivity for IoT communication.
- Publish telemetry using the MQTT protocol.
- Format readings in JSON for easy integration.
- Demonstrate periodic data transmission and remote monitoring.
- Explore integration with a dashboard, API, and supporting energy-monitoring tools.

## ✨ Key Features

- ESP32-based IoT firmware.
- Wi-Fi connectivity using the Wokwi guest network configuration.
- MQTT-based telemetry publishing.
- JSON-formatted energy readings.
- NTP-based time synchronization.
- Periodic publishing at a configurable interval.
- Supporting Python scripts, API, dashboard, and simulation components.
- Sample data for testing and demonstration.

## 🏗️ System Architecture

1. **ESP32 firmware:** Reads prepared or simulated electrical values.
2. **Wi-Fi:** Connects the ESP32 to the configured network.
3. **NTP:** Synchronizes the system time.
4. **MQTT broker:** Receives published telemetry messages.
5. **API and dashboard:** Supporting components for data access and visualization.
6. **HES tools:** Additional scripts for experimenting with energy-monitoring workflows.

### Data Flow

`Simulated Readings → ESP32 → Wi-Fi → MQTT Broker → Monitoring / Dashboard Components`

The exact data flow between the broker, API, and dashboard depends on the configuration of the supporting components.

## 🛠️ Technologies Used

- **Programming:** Embedded C++, Python
- **Microcontroller:** ESP32
- **Communication:** Wi-Fi, MQTT
- **Data format:** JSON
- **Time synchronization:** NTP
- **Supporting tools:** PlatformIO, Wokwi, MQTT broker
- **Web components:** HTML and API integration

## 📂 Repository Structure

- `src/main.cpp` — Main application source
- `src/readings.h` — Reading data definitions
- `sketch.ino` — Arduino-style firmware entry point or supporting sketch
- `platformio.ini` — PlatformIO project configuration
- `diagram.json` — Wokwi circuit configuration
- `wokwi.toml` — Wokwi project configuration
- `api/` — API implementation
- `dashboard/` — Dashboard interface
- `simulator/` — Simulation utilities
- `hes/` — Home Energy System supporting scripts
- `tools/` — Data preparation and database utilities
- `data/sample.csv` — Sample dataset for testing
- `mosquitto.conf` — MQTT broker configuration
- `include/`, `lib/`, `test/` — Supporting project directories and documentation

## 📊 Dataset and Database Information


- **`data/household_power_consumption.txt`** — The full household power consumption dataset is not included because it exceeds GitHub's 100 MB limit for a regular Git file.
- **`data/mdms.db`** — The local database is excluded because it is a generated or local data artifact and may be recreated or configured separately.
- **Python cache files** — Files such as `__pycache__` and `.pyc` are excluded because they are generated automatically.

The repository includes `data/sample.csv` for sample-data testing.

`data/household_power_consumption.txt`

## ⚙️ Setup and Execution

### Prerequisites

- Visual Studio Code
- PlatformIO extension
- ESP32 development environment or Wokwi simulation
- A reachable MQTT broker
- Python, if using the supporting API, simulator, or HES scripts

### Firmware Setup

1. Clone or download this repository.
2. Open the project in Visual Studio Code.
3. Check `platformio.ini` for the configured board and build environment.
4. Review `src/main.cpp`, `src/readings.h`, and the firmware entry-point files.
5. Configure the Wi-Fi credentials, MQTT broker address, client ID, and topic as required.
6. Build and run the firmware using PlatformIO or the configured simulation environment.
7. Verify that the MQTT broker receives the published telemetry messages.

### MQTT Configuration

The firmware uses configurable values for the Wi-Fi network, MQTT host and port, client ID, meter ID, topic prefix, and publishing interval.

Make sure the configured MQTT broker address is reachable from the environment where the ESP32 is running. An IP address from a local network may not work outside that network or simulation setup.

### Supporting Components

Before running the API, dashboard, or Python utilities, review their individual files for dependencies, environment variables, database configuration, and execution instructions.

The full dataset and local database are not automatically available from a fresh clone of this repository.

## 🧪 Testing and Validation

The project can be evaluated by checking:

- ESP32 Wi-Fi connection status.
- MQTT broker connectivity.
- Successful periodic telemetry publishing.
- JSON message structure and reading values.
- Correct meter ID and MQTT topic.
- Time synchronization behavior.
- Compatibility with the configured simulation and monitoring components.

## 🔒 Configuration and Security

- Do not commit real Wi-Fi passwords, private broker credentials, API keys, or tokens.
- Use placeholders or environment variables for sensitive configuration.
- Restrict MQTT broker access when using a real deployment.
- Do not publish private databases or large datasets unless necessary and appropriately licensed.

## 🚀 Future Improvements

- Integrate a physical energy-metering sensor or calibrated measurement module.
- Store incoming telemetry in a database.
- Add real-time dashboard updates and historical charts.
- Implement device authentication and encrypted MQTT communication using TLS.
- Add alerts for abnormal voltage, current, or energy readings.
- Introduce automated testing and robust Wi-Fi/MQTT reconnection handling.
- Deploy the monitoring stack on a cloud or local server.



*This project is intended for educational purposes, embedded firmware development, IoT communication experiments, and energy-monitoring simulation.*
