# Acond Heat Pump — Home Assistant Integration

Custom HA integration for Acond heat pumps. HACS-compatible.

## Project Structure

```
custom_components/acond_heat_pump/
  __init__.py        # Entry setup/unload, AcondConfigEntry type alias
  config_flow.py     # Config flow with host, port (default 502), name
  const.py           # DOMAIN, DEFAULT_PORT, PLATFORMS, mode/regulation name mappings
  coordinator.py     # AcondCoordinator — polls read_data() every 60s
  entity.py          # AcondEntity base class (CoordinatorEntity)
  climate.py         # Circuit I + Circuit II climate entities
  sensor.py          # 16 sensors via description pattern (AcondSensorEntityDescription)
  binary_sensor.py   # 13 binary sensors via description pattern
  number.py          # 4 number entities (water back, pool, cooling, DHW setpoints)
  select.py          # 3 selects (regime, regulation, operation)
  strings.json       # Translation keys for all entities + config flow
  translations/en.json  # Must mirror strings.json exactly
hacs.json            # HACS metadata
```

## Architecture

- **Coordinator pattern**: `AcondCoordinator` fetches `HeatPumpResponse` every 60s via `read_data()`
- **Base entity**: `AcondEntity` sets `_attr_has_entity_name = True` and shared `DeviceInfo`
- **Description pattern**: sensors and binary sensors use frozen dataclass descriptions with `value_fn` lambdas
- **Synchronous library**: all `client.*` calls must be wrapped in `hass.async_add_executor_job()`
- **ConfigEntryNotReady**: raised on connection failure so HA retries automatically

## Entity Counts (38 total)

| Platform | Count | File |
|----------|-------|------|
| Climate | 2 | `climate.py` — Circuit I, Circuit II |
| Sensor | 16 | `sensor.py` — temps, compressor power, error codes, DHW temp |
| Binary Sensor | 13 | `binary_sensor.py` — status bits |
| Number | 4 | `number.py` — water back, pool, cooling, DHW setpoints |
| Select | 3 | `select.py` — regime, regulation, operation |

## Key Patterns

- Every entity needs a `translation_key` with a matching entry in both `strings.json` and `translations/en.json`
- Unique IDs follow `{entry_id}_{platform}_{key}` format
- `EntityCategory.DIAGNOSTIC` is used for pumps, compressor stats, error codes — not for user-facing sensors
- Number entities use the library's setter methods directly; ranges must match the library's write validation
- Climate entities share HVAC mode/action since the pump has one global operating mode

## Dependency

- `acond-heat-pump` library — version pinned in `manifest.json` `requirements`
- When the library version is bumped, update `manifest.json` to match

## Gotchas

- **Read vs write ranges**: the library's `_read_temp_register` can return `None` if a value exceeds the read validation max. If HA gets `None` for `target_temperature`, the UI hides the temperature control entirely. Keep read ranges in the library wider than write ranges.
- **`translations/en.json` must mirror `strings.json`** — forgetting to add a key causes the entity name to show as the translation key string
- **Config entry backwards compatibility**: `entry.data.get(CONF_PORT, DEFAULT_PORT)` handles existing entries that lack the port field

## No Tests

This integration has no test suite. Validation is done by:
1. Checking library field/method names match via `python -c "import acond_heat_pump; ..."`
2. Verifying all translation keys are present in `strings.json`
3. Manual testing on HA with the real heat pump
