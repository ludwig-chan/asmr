#!/usr/bin/env python3
"""日期转换工具。

支持以下输入：
1. 常见日期字符串（如 2026-02-09 14:30:00）。
2. Unix 时间戳（秒或毫秒）。

可指定输入/输出时区与输出格式。
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

COMMON_INPUT_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y%m%d",
    "%Y%m%d%H%M%S",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="日期转换工具")
    parser.add_argument("value", help="待转换的日期字符串或 Unix 时间戳")
    parser.add_argument(
        "-i",
        "--input-format",
        default="auto",
        help="输入格式，默认 auto 自动识别，或传入 strptime 格式字符串",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        default="%Y-%m-%d %H:%M:%S%z",
        help="输出格式，默认: %%Y-%%m-%%d %%H:%%M:%%S%%z",
    )
    parser.add_argument(
        "--input-tz",
        default="UTC",
        help="输入时区，默认 UTC，例如 Asia/Shanghai",
    )
    parser.add_argument(
        "--output-tz",
        default="UTC",
        help="输出时区，默认 UTC，例如 Asia/Shanghai",
    )
    return parser.parse_args()


def parse_timestamp(value: str) -> datetime | None:
    if not value.lstrip("-").isdigit():
        return None

    raw = int(value)
    abs_raw = abs(raw)

    if abs_raw > 10**12:
        seconds = raw / 1000
    else:
        seconds = raw

    return datetime.fromtimestamp(seconds, tz=timezone.utc)


def parse_datetime(value: str, input_format: str, input_tz: ZoneInfo) -> datetime:
    ts_dt = parse_timestamp(value)
    if ts_dt is not None:
        return ts_dt.astimezone(input_tz)

    fmts = COMMON_INPUT_FORMATS if input_format == "auto" else [input_format]

    for fmt in fmts:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.replace(tzinfo=input_tz)
        except ValueError:
            continue

    if input_format == "auto":
        raise ValueError(
            "无法自动识别日期格式，请使用 --input-format 指定格式，例如 '%Y-%m-%d %H:%M:%S'"
        )

    raise ValueError(f"输入日期与指定格式不匹配: {input_format}")


def main() -> None:
    args = parse_args()

    try:
        input_tz = ZoneInfo(args.input_tz)
        output_tz = ZoneInfo(args.output_tz)
    except Exception as exc:
        raise SystemExit(f"时区无效: {exc}") from exc

    try:
        dt = parse_datetime(args.value, args.input_format, input_tz)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    converted = dt.astimezone(output_tz)
    print(converted.strftime(args.output_format))


if __name__ == "__main__":
    main()
