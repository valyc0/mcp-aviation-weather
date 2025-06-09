import logging
import json
import os
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from .client import AviationWeatherClient
from .exceptions import AviationWeatherError, APIError, NetworkError, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("aviation-weather-mcp.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize the MCP server
app = FastMCP("Aviation Weather MCP Server")

# Global client instance
client = None

async def get_client():
    """Get or create the aviation weather client"""
    global client
    if client is None:
        client = AviationWeatherClient()
    return client

@app.tool()
async def get_metar(
    ids: str = "",
    format: str = "json",
    taf: bool = False,
    hours: Optional[int] = None,
    bbox: str = "",
    date: str = ""
) -> str:
    """
    Get METAR weather observations from aviation weather stations.
    
    Args:
        ids: Station ID(s) - single ICAO ID (e.g. 'KMCI') or comma/space separated list (e.g. 'KMCI,KORD,KBOS') or state (@WA)
        format: Output format - 'json', 'xml', 'raw', 'geojson', 'html'
        taf: Include TAF with METAR
        hours: Hours back to search
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        Weather observation data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_metar(
            ids=ids if ids else None,
            format=format,
            taf=taf,
            hours=hours,
            bbox=bbox if bbox else None,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting METAR: {e}")
        raise AviationWeatherError(f"Failed to get METAR data: {e}")

@app.tool()
async def get_taf(
    ids: str = "",
    format: str = "json",
    metar: bool = False,
    bbox: str = "",
    time: str = "",
    date: str = ""
) -> str:
    """
    Get Terminal Aerodrome Forecasts (TAF) for aviation weather stations.
    
    Args:
        ids: Station ID(s) - single ICAO ID (e.g. 'KMCI') or comma/space separated list (e.g. 'KMCI,KORD,KBOS') or state (@WA)
        format: Output format - 'json', 'xml', 'raw', 'geojson', 'html'
        metar: Include METAR with TAF
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
        time: Process time - 'valid' (default) or 'issue'
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        Terminal aerodrome forecast data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_taf(
            ids=ids if ids else None,
            format=format,
            metar=metar,
            bbox=bbox if bbox else None,
            time=time if time else None,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting TAF: {e}")
        raise AviationWeatherError(f"Failed to get TAF data: {e}")

@app.tool()
async def get_pirep(
    id: str = "",
    format: str = "json",
    age: Optional[int] = None,
    distance: Optional[int] = None,
    level: Optional[int] = None,
    inten: str = "",
    date: str = ""
) -> str:
    """
    Get pilot reports (PIREPs) from aviation weather.
    
    Args:
        id: Station ID to search around
        format: Output format - 'json', 'xml', 'raw', 'geojson'
        age: Hours back to search
        distance: Distance from station to search
        level: Flight level +-3000' to search
        inten: Minimum intensity - 'lgt', 'mod', 'sev'
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        Pilot report data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_pirep(
            id=id if id else None,
            format=format,
            age=age,
            distance=distance,
            level=level,
            inten=inten if inten else None,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting PIREP: {e}")
        raise AviationWeatherError(f"Failed to get PIREP data: {e}")

@app.tool()
async def get_sigmet(
    format: str = "json",
    hazard: str = "",
    level: Optional[int] = None,
    date: str = ""
) -> str:
    """
    Get domestic SIGMETs (Significant Meteorological Information).
    
    Args:
        format: Output format - 'json', 'xml', 'raw'
        hazard: Hazard type - 'conv', 'turb', 'ice', 'ifr'
        level: Level +-3000' to search
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        SIGMET data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_sigmet(
            format=format,
            hazard=hazard if hazard else None,
            level=level,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting SIGMET: {e}")
        raise AviationWeatherError(f"Failed to get SIGMET data: {e}")

@app.tool()
async def get_isigmet(
    format: str = "json",
    hazard: str = "",
    level: Optional[int] = None,
    date: str = ""
) -> str:
    """
    Get international SIGMETs (Significant Meteorological Information).
    
    Args:
        format: Output format - 'json', 'xml', 'raw'
        hazard: Hazard type - 'turb', 'ice'
        level: Level +-3000' to search
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        International SIGMET data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_isigmet(
            format=format,
            hazard=hazard if hazard else None,
            level=level,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting International SIGMET: {e}")
        raise AviationWeatherError(f"Failed to get International SIGMET data: {e}")

@app.tool()
async def get_gairmet(
    type: str = "",
    format: str = "json",
    hazard: str = "",
    date: str = ""
) -> str:
    """
    Get US Graphical AIRMETs (G-AIRMETs).
    
    Args:
        type: Product type - 'sierra', 'tango', 'zulu'
        format: Output format - 'decoded', 'json', 'geojson', 'xml'
        hazard: Hazard type - 'turb-hi', 'turb-lo', 'llws', 'sfc_wind', 'ifr', 'mtn_obs', 'ice', 'fzlvl'
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        G-AIRMET data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_gairmet(
            type=type if type else None,
            format=format,
            hazard=hazard if hazard else None,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting G-AIRMET: {e}")
        raise AviationWeatherError(f"Failed to get G-AIRMET data: {e}")

@app.tool()
async def get_cwa(
    hazard: str = "",
    date: str = ""
) -> str:
    """
    Get CWSU Center Weather Advisories.
    
    Args:
        hazard: Hazard type - 'ts', 'turb', 'ice', 'ifr', 'pcpn', 'unk'
        date: Date in format 'yyyymmdd_hhmm' or 'yyyy-mm-ddThh:mm:ssZ'
    
    Returns:
        Center Weather Advisory data
    """
    try:
        client = await get_client()
        result = await client.get_cwa(
            hazard=hazard if hazard else None,
            date=date if date else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting CWA: {e}")
        raise AviationWeatherError(f"Failed to get CWA data: {e}")

@app.tool()
async def get_wind_temp(
    region: str = "",
    level: str = "",
    fcst: str = ""
) -> str:
    """
    Get wind and temperature data from upper air observations.
    
    Args:
        region: Region - 'us', 'bos', 'mia', 'chi', 'dfw', 'slc', 'sfo', 'alaska', 'hawaii', 'other_pac'
        level: Level - 'low', 'high'
        fcst: Forecast cycle - '06', '12', '24'
    
    Returns:
        Wind and temperature data
    """
    try:
        client = await get_client()
        result = await client.get_wind_temp(
            region=region if region else None,
            level=level if level else None,
            fcst=fcst if fcst else None
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting wind/temp data: {e}")
        raise AviationWeatherError(f"Failed to get wind/temp data: {e}")

@app.tool()
async def get_station_info(
    ids: str = "",
    bbox: str = "",
    format: str = "json"
) -> str:
    """
    Get weather station information.
    
    Args:
        ids: Station ID(s) - comma/space separated list (e.g. 'KORD,KJFK,KDEN')
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '35,-90,45,-80')
        format: Output format - 'json', 'xml', 'raw', 'geojson'
    
    Returns:
        Station information data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_station_info(
            ids=ids if ids else None,
            bbox=bbox if bbox else None,
            format=format
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting station info: {e}")
        raise AviationWeatherError(f"Failed to get station info: {e}")

@app.tool()
async def get_airport_info(
    ids: str = "",
    bbox: str = "",
    format: str = "json"
) -> str:
    """
    Get airport information.
    
    Args:
        ids: Airport ID(s) - single ICAO ID (e.g. 'KMCI') or comma/space separated list (e.g. 'KMCI,KORD,KBOS') or state (@WA)
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
        format: Output format - 'decoded', 'json', 'geojson'
    
    Returns:
        Airport information data in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_airport_info(
            ids=ids if ids else None,
            bbox=bbox if bbox else None,
            format=format
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting airport info: {e}")
        raise AviationWeatherError(f"Failed to get airport info: {e}")

@app.tool()
async def get_navaid_info(
    ids: str = "",
    bbox: str = "",
    format: str = "json"
) -> str:
    """
    Get navigational aid information.
    
    Args:
        ids: Navaid ID(s) - 5 letter Fix ID (e.g. 'MCI')
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
        format: Output format - 'json', 'geojson', 'raw'
    
    Returns:
        Navigational aid information in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_navaid_info(
            ids=ids if ids else None,
            bbox=bbox if bbox else None,
            format=format
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting navaid info: {e}")
        raise AviationWeatherError(f"Failed to get navaid info: {e}")

@app.tool()
async def get_fix_info(
    ids: str = "",
    bbox: str = "",
    format: str = "json"
) -> str:
    """
    Get navigational fix information.
    
    Args:
        ids: Fix ID(s) - 5 letter Fix ID (e.g. 'BARBQ')
        bbox: Geographic bounding box as 'lat0,lon0,lat1,lon1' (e.g. '40,-90,45,-85')
        format: Output format - 'json', 'geojson', 'raw'
    
    Returns:
        Navigational fix information in the requested format
    """
    try:
        client = await get_client()
        result = await client.get_fix_info(
            ids=ids if ids else None,
            bbox=bbox if bbox else None,
            format=format
        )
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting fix info: {e}")
        raise AviationWeatherError(f"Failed to get fix info: {e}")

async def run_sse():
    """Run the server in SSE mode"""
    # Get configuration from environment variables
    host = os.getenv("FASTMCP_HOST", "127.0.0.1")
    port = int(os.getenv("FASTMCP_PORT", "8000"))
    
    # Set environment variables for FastMCP
    os.environ["FASTMCP_HOST"] = host
    os.environ["FASTMCP_PORT"] = str(port)
    
    try:
        logger.info(f"Starting Aviation Weather MCP Server in SSE mode on {host}:{port}")
        await app.run_sse_async()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        await app.shutdown()
    except Exception as e:
        logger.error(f"Server failed: {e}")
        raise
    finally:
        logger.info("Server shutdown complete")

def run_stdio():
    """Run the server in stdio mode"""
    try:
        logger.info("Starting Aviation Weather MCP Server in stdio mode")
        app.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {e}")
        raise
    finally:
        logger.info("Server shutdown complete")

# Cleanup function for the client
async def cleanup():
    """Cleanup resources"""
    global client
    if client:
        await client.close()
        client = None
