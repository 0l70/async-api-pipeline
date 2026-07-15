# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) WeatherRecord/CountryInfo/IPInfo Pydantic 모델 검증 테스트
#       2) 정상 케이스 및 범위(ge/le) 벗어난 비정상 케이스 확인
#
# 변경일 : 2026-07-15 최초 작성
#        2026-07-15 countries.dev 스키마 반영해 test_country_info_valid 수정
#
# All Rights Reserved by 이경민
# ----------------------------------------------

import pytest
from pydantic import ValidationError

from src.models import CountryInfo, IPInfo, WeatherRecord


def test_weather_record_valid():
    r = WeatherRecord(time="2026-07-15T00:00", temperature_2m=25.3, precipitation_probability=30)
    assert r.temperature_2m == 25.3


def test_weather_record_invalid_probability():
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-07-15T00:00", temperature_2m=25.3, precipitation_probability=150)


def test_country_info_valid():
    c = CountryInfo(
        name="Korea (Republic of)", capital="Seoul",
        region="Asia", subregion="Eastern Asia",
        population=51780579, area=100210.0,
    )
    assert c.region == "Asia"


def test_ip_info_valid():
    ip = IPInfo(
        query="8.8.8.8", country="United States", region_name="California",
        city="Mountain View", lat=37.4, lon=-122.07, isp="Google LLC",
        timezone="America/Los_Angeles",
    )
    assert ip.query == "8.8.8.8"