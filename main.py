# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) 데이터 수집 미니 파이프라인 엔트리포인트
#       2) 흐름: 비동기 동시 수집 → Pydantic 검증 → CSV/Parquet 저장 → 성능 비교
#       3) logging으로 각 단계 진행 상황 및 오류 기록
#
# 변경일 : 2026-07-15 최초 작성
#        2026-07-15 API별 실패 처리 및 로깅 추가
#        2026-07-15 CSV vs Parquet 성능 비교 결과를 표 형태로 출력하도록 개선
#
# All Rights Reserved by 이경민
# ----------------------------------------------

import asyncio
import logging

from src.collect import collect_all
from src.parse import parse_country, parse_ip, parse_weather
from src.storage import benchmark_save, to_dataframe

logging.basicConfig(level=logging.INFO, format="%(asctime)s|%(levelname)s|%(message)s")
logger = logging.getLogger("pipeline")


def print_summary(results: list[dict]) -> None:
    """CSV vs Parquet 성능 비교 결과를 정렬된 표 형태로 출력."""
    if not results:
        print("저장된 결과가 없습니다.")
        return

    headers = ["name", "rows", "csv_write_s", "parquet_write_s",
               "csv_read_s", "parquet_read_s", "csv_size_kb", "parquet_size_kb"]
    col_titles = ["데이터", "행수", "CSV write(s)", "Parquet write(s)",
                  "CSV read(s)", "Parquet read(s)", "CSV(KB)", "Parquet(KB)"]

    rows = [[str(r[h]) for h in headers] for r in results]
    widths = [max(len(title), *(len(row[i]) for row in rows)) for i, title in enumerate(col_titles)]

    def fmt_row(cells: list[str]) -> str:
        return " | ".join(cell.rjust(w) for cell, w in zip(cells, widths))

    print("\n=== CSV vs Parquet 성능 비교 ===")
    print(fmt_row(col_titles))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt_row(row))
    print()


def main() -> None:
    logger.info("파이프라인 시작")
    raw = asyncio.run(collect_all())
    results = []

    if raw["weather"]["error"] is None:
        records, errors = parse_weather(raw["weather"]["data"])
        logger.info("weather: 유효 %d건, 오류 %d건", len(records), len(errors))
        results.append(benchmark_save(to_dataframe(records), "weather"))
    else:
        logger.error("weather 수집 실패: %s", raw["weather"]["error"])

    if raw["country"]["error"] is None:
        country = parse_country(raw["country"]["data"])
        if country:
            results.append(benchmark_save(to_dataframe([country]), "country"))
        else:
            logger.error("country 검증 실패")
    else:
        logger.error("country 수집 실패: %s", raw["country"]["error"])

    if raw["ip"]["error"] is None:
        ip = parse_ip(raw["ip"]["data"])
        if ip:
            results.append(benchmark_save(to_dataframe([ip]), "ip"))
        else:
            logger.error("ip 검증 실패")
    else:
        logger.error("ip 수집 실패: %s", raw["ip"]["error"])

    print_summary(results)


if __name__ == "__main__":
    main()