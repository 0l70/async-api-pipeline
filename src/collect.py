# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) Open-Meteo, countries.dev, ip-api 3개 API 동시 호출
#       2) asyncio.gather()를 이용한 비동기 병렬 수집 파이프라인
#       3) 개별 API 실패 시에도 전체 파이프라인이 중단되지 않도록 예외 처리
#
# 변경일 : 2026-07-15 최초 작성
#        2026-07-15 예외 처리 추가 (실패 시 error 필드로 반환)
#        2026-07-15 RestCountries 유료화로 countries.dev API로 교체
#
# All Rights Reserved by 이경민
# ----------------------------------------------

import asyncio

import httpx

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665&longitude=126.9780"
    "&hourly=temperature_2m,precipitation_probability"
    "&forecast_days=3&timezone=Asia/Seoul"
)
COUNTRY_URL = "https://countries.dev/alpha/KR"
IP_URL = "http://ip-api.com/json/8.8.8.8"


async def fetch_json(client: httpx.AsyncClient, url: str, name: str) -> dict:
    """단일 API 호출. 실패해도 예외를 던지지 않고 결과 dict에 담아 반환."""
    try:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        return {"name": name, "data": r.json(), "error": None}
    except Exception as e:  # noqa: BLE001 - 원인 상관없이 파이프라인은 계속 진행
        return {"name": name, "data": None, "error": str(e)}


async def collect_all() -> dict[str, dict]:
    """3개 API를 동시에 호출하고 이름을 키로 하는 dict로 반환."""
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_json(client, WEATHER_URL, "weather"),
            fetch_json(client, COUNTRY_URL, "country"),
            fetch_json(client, IP_URL, "ip"),
        ]
        results = await asyncio.gather(*tasks)
    return {r["name"]: r for r in results}


if __name__ == "__main__":
    raw = asyncio.run(collect_all())
    for name, r in raw.items():
        status = "OK" if r["error"] is None else f"FAIL: {r['error']}"
        print(f"{name}: {status}")
