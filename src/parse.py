# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) 수집한 원본 JSON을 Pydantic 모델 기준으로 파싱·검증
#       2) weather는 hourly 배열을 시간 단위 레코드로 펼쳐서 검증
#       3) country/ip는 단일 레코드 검증, 실패 시 None 반환
#
# 변경일 : 2026-07-15 최초 작성
#        2026-07-15 ValidationError 예외 처리 추가
#        2026-07-15 countries.dev 단일 dict 응답 구조에 맞게 parse_country 수정
#
# All Rights Reserved by 이경민
# ----------------------------------------------

from pydantic import ValidationError

from src.models import CountryInfo, IPInfo, WeatherRecord


def parse_weather(raw: dict) -> tuple[list[WeatherRecord], list[dict]]:
    hourly = raw["hourly"]
    records, errors = [], []
    for t, temp, precip in zip(
        hourly["time"], hourly["temperature_2m"], hourly["precipitation_probability"]
    ):
        try:
            records.append(
                WeatherRecord(time=t, temperature_2m=temp, precipitation_probability=precip)
            )
        except ValidationError as e:
            errors.append({"time": t, "error": str(e)})
    return records, errors


def parse_country(raw: dict) -> CountryInfo | None:
    """countries.dev는 리스트가 아닌 단일 dict로 응답한다."""
    try:
        return CountryInfo(
            name=raw["name"],
            capital=raw.get("capital"),
            region=raw["region"],
            subregion=raw.get("subregion"),
            population=raw["population"],
            area=raw["area"],
        )
    except ValidationError as e:
        print(f"country 검증 실패: {e}")
        return None


def parse_ip(raw: dict) -> IPInfo | None:
    try:
        return IPInfo(
            query=raw["query"],
            country=raw["country"],
            region_name=raw["regionName"],
            city=raw["city"],
            lat=raw["lat"],
            lon=raw["lon"],
            isp=raw["isp"],
            timezone=raw["timezone"],
        )
    except ValidationError as e:
        print(f"ip 검증 실패: {e}")
        return None
