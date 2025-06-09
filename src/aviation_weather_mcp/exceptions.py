class AviationWeatherError(Exception):
    """Base exception for Aviation Weather operations"""
    pass

class APIError(AviationWeatherError):
    """Error when calling the aviationweather.gov API"""
    pass

class ValidationError(AviationWeatherError):
    """Error when validating parameters"""
    pass

class NetworkError(AviationWeatherError):
    """Error when network request fails"""
    pass
