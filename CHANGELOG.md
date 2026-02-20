# Changelog

## [1.1.0] - 2026-02-20

### Added
- Czech (cs) translations using official Acond Modbus documentation terminology
- DHW temperature sensor (`dhw_temperature`)
- DHW temperature setpoint number entity (`dhw_temperature_setpoint`)

### Changed
- Replace water_heater entity with number + sensor entities for DHW control
- Select options (regime, regulation, operation) now use translatable state keys
- Fix DHW heating binary sensor device class from `HEAT` to `RUNNING`

### Removed
- Water heater platform (`water_heater.py`)

## [1.0.4] - 2026-02-19

### Added
- Custom MDI icons for all entities (climate, water heater, sensors, binary sensors, number controls, selects)

## [1.0.3] - 2026-02-18

### Changed
- Temperature step from 0.5°C to 0.1°C for Circuit I, Circuit II, and Boiler entities

## [1.0.2] - 2026-02-17

### Fixed
- Boiler (DHW) temperature range corrected to 10–50°C (was 10–46°C)
- Bump `acond-heat-pump` to v1.2.2

## [1.0.1] - 2026-02-17

### Changed
- Bump `acond-heat-pump` to v1.2.1 (pymodbus 3.8 compatibility)

## [1.0.0] - 2026-02-17

### Added
- Initial release with 37 entities
- Climate control for Circuit I and Circuit II
- Water heater (Boiler/DHW) temperature control
- 15 sensors: outdoor, return water, brine, solar, pool, water outlet, indoor circuit II, compressor power/max, error codes
- 13 binary sensors: power, running, fault, defrost, DHW heating, pump statuses, cooling, bivalence, summer mode
- 3 number controls: water back, pool, and cooling temperature setpoints
- 3 selects: regime, regulation mode, operation mode
- Config flow with optional port field (default 502)
- `ConfigEntryNotReady` for automatic retry on connection failure
