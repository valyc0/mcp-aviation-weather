#!/usr/bin/env python3
"""Test script for Aviation Weather MCP Server"""

import asyncio
import json
import logging
from aviation_weather_mcp.client import AviationWeatherClient

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_client():
    """Test the aviation weather client"""
    print("Creating client...")
    client = AviationWeatherClient()
    
    try:
        print("Testing METAR for JFK...")
        result = await client.get_metar(ids="KJFK", format="json")
        print("METAR result type:", type(result))
        if isinstance(result, (dict, list)):
            print("METAR result:", json.dumps(result, indent=2)[:1000] + ("..." if len(str(result)) > 1000 else ""))
        else:
            print("METAR result:", str(result)[:1000] + ("..." if len(str(result)) > 1000 else ""))
        
        print("\nTesting station info for JFK...")
        result = await client.get_station_info(ids="KJFK", format="json")
        print("Station info result type:", type(result))
        if isinstance(result, (dict, list)):
            print("Station info result:", json.dumps(result, indent=2)[:1000] + ("..." if len(str(result)) > 1000 else ""))
        else:
            print("Station info result:", str(result)[:1000] + ("..." if len(str(result)) > 1000 else ""))
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing client...")
        await client.close()
        print("Test completed.")

if __name__ == "__main__":
    print("Starting test...")
    asyncio.run(test_client())
