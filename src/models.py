# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) Open-Meteo 날씨 응답 검증용 WeatherRecord 모델 정의
#       2) countries.dev 국가 정보 검증용 CountryInfo 모델 정의
#       3) ip-api 응답 검증용 IPInfo 모델 정의
#       4) Pydantic v2 Field로 타입·범위(ge/le) 제약 조건 설정
#
# 변경일 : 2026-07-15 최초 작성
#        2026-07-15 RestCountries 유료화로 CountryInfo를 countries.dev 스키마로 수정
#
# All Rights Reserved by 이경민
# ----------------------------------------------

from datetime import datetime

from pydantic import BaseModel, Field


class WeatherRecord(BaseModel):
    """Open-Meteo 응답의 hourly 배열 한 줄(row)을 표현."""

    time: datetime
    temperature_2m: float = Field(..., ge=-50, le=60, description="섭씨 기온")
    precipitation_probability: int = Field(..., ge=0, le=100, description="강수확률(%)")


class CountryInfo(BaseModel):
    """countries.dev alpha/{code} 응답 검증용."""

    name: str
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
