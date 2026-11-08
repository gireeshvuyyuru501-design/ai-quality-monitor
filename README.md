# AI Quality Monitor

A reproducible, offline Python quality-monitoring baseline for recorded AI evaluation traces. Calculates error rate, average latency, nearest-rank p95 latency, average quality score, and threshold-based alerts. Includes unit tests and GitHub Actions CI.

## Quick start

Requires Python 3.9+ and no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python monitor.py --input examples/sample_traces.json --output quality_report.json
```

## Input format

A JSON array of records with unique `id`, nonnegative numeric `latency_ms`, `quality_score` in [0,1], and `status` (`ok` or `error`). Example records are **synthetic demonstration traces**, not production traffic or Gemini responses. Replace them with measured traces to analyze real system performance. The quality score must be produced by a separately documented evaluator; this tool does not judge answers.

## Alerts

- Error rate **greater than** `--error-rate-limit` (default 0.1)
- Nearest-rank p95 latency **greater than** `--latency-limit-ms` (default 1500)
- Any trace with quality below `--quality-floor` (default 0.7)

## Limitations and next steps

This is batch monitoring, not live observability. No database, FastAPI, React, or Gemini integration is included yet. Later connect real evaluation events, persistent storage, trend charts, and the shared AI QA dashboard.
