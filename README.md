# Acond Heat Pump - Home Assistant Integration

Custom Home Assistant integration for [Acond](https://www.acond.cz/) heat pumps via Modbus TCP.

## Features

- **Climate control** — Circuit I and Circuit II with temperature setpoints and HVAC mode control
- **Water heater** — Domestic hot water (boiler) temperature monitoring and control
- **Temperature sensors** — Outdoor, return water, brine, solar, pool, water outlet, and indoor circuit II
- **Power sensors** — Compressor power and max capacity (PRO units)
- **Binary sensors** — Running, fault, defrost, DHW heating, pump status, cooling, bivalence, and more
- **Controls** — Regime, regulation mode, operation mode selects; water back, pool, and cooling temperature setpoints
- **Diagnostics** — Error codes, pump statuses, compressor data

**37 entities** covering ~100% of the data exposed by the heat pump.

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** > three-dot menu > **Custom repositories**
3. Add this repository URL with category **Integration**
4. Download **Acond Heat Pump**
5. Restart Home Assistant

### Manual

1. Copy `custom_components/acond_heat_pump/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services** > **Add Integration**
2. Search for **Acond Heat Pump**
3. Enter the IP address of your heat pump (and optionally the Modbus TCP port, default 502)

## Requirements

- Acond heat pump with Modbus TCP connectivity
- Network access from Home Assistant to the heat pump

## Entity Overview

| Platform | Count | Examples |
|----------|-------|---------|
| Climate | 2 | Circuit I, Circuit II |
| Sensor | 15 | Outdoor temp, compressor power, error codes |
| Binary Sensor | 13 | Running, fault, pump statuses |
| Number | 3 | Water back temp, pool temp, cooling temp |
| Select | 3 | Regime, regulation, operation |
| Water Heater | 1 | Boiler (DHW) |
