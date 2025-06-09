# Aviation Weather MCP Server

This is a Model Context Protocol (MCP) server that provides access to aviation weather data from aviationweather.gov.

## Features

- **METAR** - Current weather observations from airports
- **TAF** - Terminal Aerodrome Forecasts
- **PIREP** - Pilot reports
- **SIGMET/AIRMET** - Significant meteorological information
- **G-AIRMET** - Graphical AIRMETs
- **Station Info** - Airport and weather station information
- **Wind/Temperature** - Upper air wind and temperature data

## Installation

```bash
pip install -e .
```

## Usage

### SSE Mode (for VS Code)
```bash
# Default port (8003)
aviation-weather-mcp-server sse

# Custom port via command line
aviation-weather-mcp-server sse --port 9000

# Custom host and port
aviation-weather-mcp-server sse --host 0.0.0.0 --port 9000
```

### Environment Variables
You can also configure the server using environment variables:

```bash
# Set port via environment variable
FASTMCP_PORT=9000 aviation-weather-mcp-server sse

# Set both host and port
FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=9000 aviation-weather-mcp-server sse
```

### STDIO Mode
```bash
aviation-weather-mcp-server stdio
```

## Configuration

The server can be configured in VS Code settings. Update the port in the URL if you're using a custom port:

```json
{
  "mcp": {
    "servers": {
      "aviation-weather": {
        "url": "http://localhost:8003/sse"
      }
    }
  }
}
```

For custom port (e.g., 9000):
```json
{
  "mcp": {
    "servers": {
      "aviation-weather": {
        "url": "http://localhost:9000/sse"
      }
    }
  }
}
```

## Available Tools

### Weather Observations
- `get_metar` - Get METAR weather observations
- `get_taf` - Get Terminal Aerodrome Forecasts

### Pilot Reports
- `get_pirep` - Get pilot reports (PIREPs)

### Weather Warnings
- `get_sigmet` - Get domestic SIGMETs
- `get_isigmet` - Get international SIGMETs
- `get_gairmet` - Get Graphical AIRMETs
- `get_cwa` - Get Center Weather Advisories

### Station Information
- `get_station_info` - Get weather station information
- `get_airport_info` - Get airport information

### Navigation
- `get_navaid_info` - Get navigational aid information
- `get_fix_info` - Get navigational fix information

### Upper Air Data
- `get_wind_temp` - Get wind and temperature data

## API Documentation

This server interfaces with the aviationweather.gov Data API. For more information about the underlying API, visit:
https://aviationweather.gov/data/api/
