# async-api-pipeline

httpx + asyncio로 API 3종(Open-Meteo, countries.dev, ip-api)을 동시 수집하고,
Pydantic v2로 검증한 뒤 CSV/Parquet 저장 성능을 비교하는 미니 데이터 파이프라인.

> 참고: RestCountries가 유료 전환되어 countries.dev(무료, 키 불필요)로 대체 사용.

## 환경 설정
​```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
​```

## 실행
​```bash
python main.py
​```

## 테스트
​```bash
pytest tests/ -v
ruff check .
​```