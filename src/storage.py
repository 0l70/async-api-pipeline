# ----------------------------------------------
# 파이썬 실습 코드
# 작성일 : 2026-07-15
# 작성자 : 이경민
# 설명 : 1) 검증된 Pydantic 레코드를 DataFrame으로 변환
#       2) CSV/Parquet 저장·재로딩 시간 측정 및 비교
#       3) 파일 크기(KB) 비교 결과 포함
#
# 변경일 : 2026-07-15 최초 작성
#
# All Rights Reserved by 이경민
# ----------------------------------------------

import time
from pathlib import Path

import pandas as pd
from pydantic import BaseModel

OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def to_dataframe(records: list[BaseModel]) -> pd.DataFrame:
    return pd.DataFrame([r.model_dump() for r in records])


def benchmark_save(df: pd.DataFrame, name: str) -> dict:
    csv_path = OUT_DIR / f"{name}.csv"
    parquet_path = OUT_DIR / f"{name}.parquet"

    t0 = time.perf_counter()
    df.to_csv(csv_path, index=False)
    csv_write = time.perf_counter() - t0

    t0 = time.perf_counter()
    df.to_parquet(parquet_path, index=False)
    parquet_write = time.perf_counter() - t0

    t0 = time.perf_counter()
    pd.read_csv(csv_path)
    csv_read = time.perf_counter() - t0

    t0 = time.perf_counter()
    pd.read_parquet(parquet_path)
    parquet_read = time.perf_counter() - t0

    return {
        "name": name,
        "rows": len(df),
        "csv_write_s": round(csv_write, 5),
        "parquet_write_s": round(parquet_write, 5),
        "csv_read_s": round(csv_read, 5),
        "parquet_read_s": round(parquet_read, 5),
        "csv_size_kb": round(csv_path.stat().st_size / 1024, 2),
        "parquet_size_kb": round(parquet_path.stat().st_size / 1024, 2),
    }
