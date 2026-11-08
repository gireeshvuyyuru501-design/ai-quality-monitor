import unittest
from monitor import analyze

SAMPLE=[{'id':'a','latency_ms':100,'quality_score':.9,'status':'ok'},
        {'id':'b','latency_ms':2000,'quality_score':.4,'status':'error'}]

class MonitorTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(analyze(SAMPLE)['total_traces'],2)
    def test_error_rate(self):
        self.assertEqual(analyze(SAMPLE)['error_rate'],.5)
    def test_p95(self):
        self.assertEqual(analyze(SAMPLE)['p95_latency_ms'],2000)
    def test_alerts(self):
        self.assertEqual(len(analyze(SAMPLE)['alerts']),3)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): analyze([])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): analyze([SAMPLE[0],SAMPLE[0]])
    def test_bad_score_rejected(self):
        with self.assertRaises(ValueError): analyze([dict(SAMPLE[0],quality_score=2)])
    def test_no_alerts(self):
        self.assertEqual(analyze([SAMPLE[0]])['alerts'],[])

if __name__=='__main__': unittest.main()
