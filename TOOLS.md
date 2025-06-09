# Aviation Weather MCP Server Tools

This document describes the available tools in the Aviation Weather MCP Server.

## Weather Observations

### get_metar
Get METAR weather observations from aviation weather stations.

**Parameters:**
- `ids` (string): Station ID(s) - single ICAO ID (e.g. 'KMCI') or comma/space separated list (e.g. 'KMCI,KORD,KBOS') or state (@WA)
- `format` (string): Output format - 'json', 'xml', 'raw', 'geojson', 'html' (default: 'json')
- `taf` (boolean): Include TAF with METAR (default: false)
- `hours` (integer): Hours back to search
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

**Example:**
```
get_metar(ids="KJFK,KLGA", format="json", hours=2)
```

### get_taf
Get Terminal Aerodrome Forecasts (TAF) for aviation weather stations.

**Parameters:**
- `ids` (string): Station ID(s) - single ICAO ID (e.g. 'KMCI') or comma/space separated list
- `format` (string): Output format - 'json', 'xml', 'raw', 'geojson', 'html' (default: 'json')
- `metar` (boolean): Include METAR with TAF (default: false)
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1'
- `time` (string): Process time - 'valid' (default) or 'issue'
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

## Pilot Reports

### get_pirep
Get pilot reports (PIREPs) from aviation weather.

**Parameters:**
- `id` (string): Station ID to search around
- `format` (string): Output format - 'json', 'xml', 'raw', 'geojson' (default: 'json')
- `age` (integer): Hours back to search
- `distance` (integer): Distance from station to search
- `level` (integer): Flight level +-3000' to search
- `inten` (string): Minimum intensity - 'lgt', 'mod', 'sev'
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

## Weather Warnings

### get_sigmet
Get domestic SIGMETs (Significant Meteorological Information).

**Parameters:**
- `format` (string): Output format - 'json', 'xml', 'raw' (default: 'json')
- `hazard` (string): Hazard type - 'conv', 'turb', 'ice', 'ifr'
- `level` (integer): Level +-3000' to search
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

### get_isigmet
Get international SIGMETs (Significant Meteorological Information).

**Parameters:**
- `format` (string): Output format - 'json', 'xml', 'raw' (default: 'json')
- `hazard` (string): Hazard type - 'turb', 'ice'
- `level` (integer): Level +-3000' to search
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

### get_gairmet
Get US Graphical AIRMETs (G-AIRMETs).

**Parameters:**
- `type` (string): Product type - 'sierra', 'tango', 'zulu'
- `format` (string): Output format - 'decoded', 'json', 'geojson', 'xml' (default: 'json')
- `hazard` (string): Hazard type - 'turb-hi', 'turb-lo', 'llws', 'sfc_wind', 'ifr', 'mtn_obs', 'ice', 'fzlvl'
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

### get_cwa
Get CWSU Center Weather Advisories.

**Parameters:**
- `hazard` (string): Hazard type - 'ts', 'turb', 'ice', 'ifr', 'pcpn', 'unk'
- `date` (string): Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'

## Upper Air Data

### get_wind_temp
Get wind and temperature data from upper air observations.

**Parameters:**
- `region` (string): Region - 'us', 'bos', 'mia', 'chi', 'dfw', 'slc', 'sfo', 'alaska', 'hawaii', 'other_pac'
- `level` (string): Level - 'low', 'high'
- `fcst` (string): Forecast cycle - '06', '12', '24'

## Station and Navigation Information

### get_station_info
Get weather station information.

**Parameters:**
- `ids` (string): Station ID(s) - comma/space separated list (e.g. 'KORD,KJFK,KDEN')
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '35,-90,45,-80')
- `format` (string): Output format - 'json', 'xml', 'raw', 'geojson' (default: 'json')

### get_airport_info
Get airport information.

**Parameters:**
- `ids` (string): Airport ID(s) - single ICAO ID or comma/space separated list or state (@WA)
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1'
- `format` (string): Output format - 'decoded', 'json', 'geojson' (default: 'json')

### get_navaid_info
Get navigational aid information.

**Parameters:**
- `ids` (string): Navaid ID(s) - 5 letter Fix ID (e.g. 'MCI')
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1'
- `format` (string): Output format - 'json', 'geojson', 'raw' (default: 'json')

### get_fix_info
Get navigational fix information.

**Parameters:**
- `ids` (string): Fix ID(s) - 5 letter Fix ID (e.g. 'BARBQ')
- `bbox` (string): Geographic bounding box as 'lat0,lon0,lat1,lon1'
- `format` (string): Output format - 'json', 'geojson', 'raw' (default: 'json')

## Common Parameters

### Date Formats
- `yyyymmdd_hhmm` - e.g., '20231220_1200'
- `yyyy-mm-ddThh:mm:ssZ` - e.g., '2023-12-20T12:00:00Z'

### Bounding Box Format
Geographic bounding box: 'lat0,lon0,lat1,lon1'
- Example: '40,-90,45,-85' (box around Chicago area)

### Station ID Formats
- Single ICAO ID: 'KMCI'
- Multiple IDs: 'KMCI,KORD,KBOS' or 'KMCI KORD KBOS'
- State: '@WA' (all stations in Washington state)

## Usage Examples

### Get current weather for JFK and LaGuardia airports:
```
get_metar(ids="KJFK,KLGA", format="json")
```

### Get TAF forecast for Denver:
```
get_taf(ids="KDEN", format="json", metar=true)
```

### Get pilot reports around Chicago in the last 3 hours:
```
get_pirep(id="KORD", format="json", age=3, distance=100)
```

### Get current SIGMETs for turbulence:
```
get_sigmet(format="json", hazard="turb")
```

### Get G-AIRMETs for icing conditions:
```
get_gairmet(format="json", hazard="ice")
```
