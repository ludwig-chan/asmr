爱声美柔
asmr

## 日期转换工具

新增 `date_converter.py`，支持：

- 常见日期格式自动识别（如 `2026-02-09`、`2026/02/09 14:30:00`）
- Unix 时间戳（秒/毫秒）转换
- 输入/输出时区转换（如 `UTC` -> `Asia/Shanghai`）
- 自定义输出格式

### 使用示例

```bash
# 自动识别日期并转为 UTC 输出
python3 date_converter.py "2026-02-09 14:30:00"

# 指定输入时区为上海，输出为纽约
python3 date_converter.py "2026-02-09 14:30:00" --input-tz Asia/Shanghai --output-tz America/New_York

# 转换 Unix 秒级时间戳
python3 date_converter.py 1760000000 --output-tz Asia/Shanghai

# 指定输入格式与输出格式
python3 date_converter.py "09-02-2026 14:30" -i "%d-%m-%Y %H:%M" -o "%Y/%m/%d %H:%M"
```
