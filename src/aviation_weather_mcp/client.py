import httpx
import logging
from typing import Dict, List, Optional, Any
from .exceptions import APIError, NetworkError, ValidationError

logger = logging.getLogger(__name__)

class AviationWeatherClient:
    """Client for aviationweather.gov API"""
    
    BASE_URL = "https://aviationweather.gov/api/data"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Any:
        """Make an HTTP request to the API"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Remove None values from params
        clean_params = {k: v for k, v in params.items() if v is not None}
        
        try:
            logger.info(f"Making request to {url} with params: {clean_params}")
            response = await self.client.get(url, params=clean_params)
            response.raise_for_status()
            
            # Return based on format
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                return response.text
                
        except httpx.TimeoutException:
            raise NetworkError(f"Request to {url} timed out")
        except httpx.HTTPStatusError as e:
            raise APIError(f"API request failed with status {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    async def get_metar(self, 
                       ids: Optional[str] = None,
                       format: str = "json",
                       taf: bool = False,
                       hours: Optional[int] = None,
                       bbox: Optional[str] = None,
                       date: Optional[str] = None) -> Any:
        """Get METAR weather observations"""
        params = {
            "ids": ids,
            "format": format,
            "taf": taf,
            "hours": hours,
            "bbox": bbox,
            "date": date
        }
        return await self._make_request("metar", params)
    
    async def get_taf(self,
                     ids: Optional[str] = None,
                     format: str = "json",
                     metar: bool = False,
                     bbox: Optional[str] = None,
                     time: Optional[str] = None,
                     date: Optional[str] = None) -> Any:
        """Get Terminal Aerodrome Forecasts"""
        params = {
            "ids": ids,
            "format": format,
            "metar": metar,
            "bbox": bbox,
            "time": time,
            "date": date
        }
        return await self._make_request("taf", params)
    
    async def get_pirep(self,
                       id: Optional[str] = None,
                       format: str = "json",
                       age: Optional[int] = None,
                       distance: Optional[int] = None,
                       level: Optional[int] = None,
                       inten: Optional[str] = None,
                       date: Optional[str] = None) -> Any:
        """Get pilot reports (PIREPs)"""
        params = {
            "id": id,
            "format": format,
            "age": age,
            "distance": distance,
            "level": level,
            "inten": inten,
            "date": date
        }
        return await self._make_request("pirep", params)
    
    async def get_sigmet(self,
                        format: str = "json",
                        hazard: Optional[str] = None,
                        level: Optional[int] = None,
                        date: Optional[str] = None) -> Any:
        """Get domestic SIGMETs"""
        params = {
            "format": format,
            "hazard": hazard,
            "level": level,
            "date": date
        }
        return await self._make_request("airsigmet", params)
    
    async def get_isigmet(self,
                         format: str = "json",
                         hazard: Optional[str] = None,
                         level: Optional[int] = None,
                         date: Optional[str] = None) -> Any:
        """Get international SIGMETs"""
        params = {
            "format": format,
            "hazard": hazard,
            "level": level,
            "date": date
        }
        return await self._make_request("isigmet", params)
    
    async def get_gairmet(self,
                         type: Optional[str] = None,
                         format: str = "json",
                         hazard: Optional[str] = None,
                         date: Optional[str] = None) -> Any:
        """Get Graphical AIRMETs"""
        params = {
            "type": type,
            "format": format,
            "hazard": hazard,
            "date": date
        }
        return await self._make_request("gairmet", params)
    
    async def get_cwa(self,
                     hazard: Optional[str] = None,
                     date: Optional[str] = None) -> Any:
        """Get Center Weather Advisories"""
        params = {
            "hazard": hazard,
            "date": date
        }
        return await self._make_request("cwa", params)
    
    async def get_wind_temp(self,
                           region: Optional[str] = None,
                           level: Optional[str] = None,
                           fcst: Optional[str] = None) -> Any:
        """Get wind and temperature data"""
        params = {
            "region": region,
            "level": level,
            "fcst": fcst
        }
        return await self._make_request("windtemp", params)
    
    async def get_station_info(self,
                              ids: Optional[str] = None,
                              bbox: Optional[str] = None,
                              format: str = "json") -> Any:
        """Get weather station information"""
        params = {
            "ids": ids,
            "bbox": bbox,
            "format": format
        }
        return await self._make_request("stationinfo", params)
    
    async def get_airport_info(self,
                              ids: Optional[str] = None,
                              bbox: Optional[str] = None,
                              format: str = "json") -> Any:
        """Get airport information"""
        params = {
            "ids": ids,
            "bbox": bbox,
            "format": format
        }
        return await self._make_request("airport", params)
    
    async def get_navaid_info(self,
                             ids: Optional[str] = None,
                             bbox: Optional[str] = None,
                             format: str = "json") -> Any:
        """Get navigational aid information"""
        params = {
            "ids": ids,
            "bbox": bbox,
            "format": format
        }
        return await self._make_request("navaid", params)
    
    async def get_fix_info(self,
                          ids: Optional[str] = None,
                          bbox: Optional[str] = None,
                          format: str = "json") -> Any:
        """Get navigational fix information"""
        params = {
            "ids": ids,
            "bbox": bbox,
            "format": format
        }
        return await self._make_request("fix", params)
