"""Offline monitoring of recorded AI evaluation traces (standard library only)."""
import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path


def analyze(records, latency_limit_ms=1500, quality_floor=0.7, error_rate_limit=0.1):
    if not isinstance(records, list) or not records:
        raise ValueError('records must be a nonempty list')
    ids = set()
    for i, r in enumerate(records):
        if not isinstance(r, dict) or not all(k in r for k in ('id', 'latency_ms', 'quality_score', 'status')):
            raise ValueError(f'invalid record at index {i}')
        if r['id'] in ids:
            raise ValueError('duplicate trace id')
        ids.add(r['id'])
        if type(r['latency_ms']) not in (int, float) or r['latency_ms'] < 0:
            raise ValueError('latency_ms must be nonnegative')
        if type(r['quality_score']) not in (int, float) or not 0 <= r['quality_score'] <= 1:
            raise ValueError('quality_score must be between 0 and 1')
        if r['status'] not in ('ok', 'error'):
            raise ValueError('status must be ok or error')
    n = len(records)
    latencies = sorted(r['latency_ms'] for r in records)
    errors = sum(r['status'] == 'error' for r in records)
    low_quality = sum(r['quality_score'] < quality_floor for r in records)
    slow = sum(r['latency_ms'] > latency_limit_ms for r in records)
    p95 = latencies[max(0, __import__('math').ceil(.95*n)-1)]
    error_rate = errors/n
    alerts = []
    if error_rate > error_rate_limit:
        alerts.append({'type':'error_rate','observed':round(error_rate,4),'limit':error_rate_limit})
    if p95 > latency_limit_ms:
        alerts.append({'type':'p95_latency','observed':p95,'limit':latency_limit_ms})
    if low_quality:
        alerts.append({'type':'low_quality_records','count':low_quality,'floor':quality_floor})
    return {'total_traces':n,'error_count':errors,'error_rate':round(error_rate,4),
            'mean_latency_ms':round(statistics.mean(latencies),2),'p95_latency_ms':p95,
            'mean_quality_score':round(statistics.mean(r['quality_score'] for r in records),4),
            'slow_trace_count':slow,'low_quality_count':low_quality,'alerts':alerts,
            'source':'recorded input traces; no live model inference'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input', default='examples/sample_traces.json')
    p.add_argument('--output', default='quality_report.json')
    p.add_argument('--latency-limit-ms', type=float, default=1500)
    p.add_argument('--quality-floor', type=float, default=.7)
    p.add_argument('--error-rate-limit', type=float, default=.1)
    args=p.parse_args()
    records=json.loads(Path(args.input).read_text(encoding='utf-8'))
    report=analyze(records,args.latency_limit_ms,args.quality_floor,args.error_rate_limit)
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
