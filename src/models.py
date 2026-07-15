"""API 응답을 검증하기 위한 Pydantic v2 스키마 모음.

- WeatherRecord : Open-Meteo 시간대별 기온/강수확률
- CountryInfo   : RestCountries 국가 정보
- IPInfo        : ip-api IP 기반 지역 정보
"""
from datetime import datetime
from pydantic import BaseModel, Field


class WeatherRecord(BaseModel):
    """Open-Meteo 응답의 hourly 배열 한 줄(row)을 표현."""
    time: datetime
    temperature_2m: float = Field(..., ge=-50, le=60, description="섭씨 기온")
    precipitation_probability: int = Field(..., ge=0, le=100, description="강수확률(%)")


class CountryInfo(BaseModel):
    """RestCountries alpha/KR 응답에서 필요한 필드만 추출."""
    name_common: str
    name_official: str
    capital: str | None = None
    region: str
    subregion: str | None = None
    population: int = Field(..., ge=0)
    area: float = Field(..., ge=0)


class IPInfo(BaseModel):
    """ip-api 응답에서 필요한 필드만 추출."""
    query: str
    country: str
    region_name: str
    city: str
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    isp: str
    timezone: str