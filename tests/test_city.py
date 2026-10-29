import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import urllib.error
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import generate_city as city

class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.snapshot=json.loads((city.ROOT/'data/contributions.json').read_text())

    def test_real_snapshot_has_exactly_one_block_per_day(self):
        root=ET.fromstring(city.render(self.snapshot))
        blocks=[n for n in root.iter() if 'data-date' in n.attrib]
        self.assertEqual(len(blocks),len(self.snapshot['days']))
        self.assertEqual(sum(int(n.attrib['data-count']) for n in blocks),city.metrics(self.snapshot['days'])['total'])
        self.assertEqual({n.attrib['data-date'] for n in blocks},{d['date'] for d in self.snapshot['days']})

    def test_zero_day_has_only_platform(self):
        root=ET.fromstring(city.render(self.snapshot))
        for n in root.iter():
            if n.attrib.get('data-count')=='0':
                self.assertEqual(sum(c.tag.endswith('polygon') for c in n),1)

    def test_invalid_counts_and_missing_dates_fail_closed(self):
        for count in [-1,1.5,True,'3']:
            days=[dict(d) for d in self.snapshot['days']];days[0]['count']=count
            with self.assertRaises(ValueError):city.validate_days(days)
        with self.assertRaises(ValueError):city.validate_days(self.snapshot['days'][:10])
        days=[dict(d) for d in self.snapshot['days']];days[1]['date']=days[0]['date']
        with self.assertRaises(ValueError):city.validate_days(days)

    def test_graphql_errors_and_null_user(self):
        with self.assertRaises(ValueError):city.graphql_days({'errors':[{'message':'denied'}]})
        with self.assertRaises(TypeError):city.graphql_days({'data':{'user':None}})

    def test_public_parser_does_not_infer_counts_from_colors(self):
        p=city.CalendarParser();p.feed('<td data-date="2026-10-01" id="day1" data-level="4"></td><tool-tip for="day1">Unknown</tool-tip>')
        with self.assertRaises(ValueError):p.days()
        p=city.CalendarParser();p.feed('<tool-tip for="a">1,234 contributions on October 1st.</tool-tip><tool-tip for="b">No contributions on October 2nd.</tool-tip>')
        self.assertEqual(p.counts,{'a':1234,'b':0})

    def test_streak_resets_on_zero(self):
        self.assertEqual(city.metrics([{'count':n} for n in [1,2,0,1,1,1,0]])['longest'],3)

    def test_identical_input_never_rewrites_output(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'city.svg';content=city.render(self.snapshot)
            self.assertTrue(city.write_if_changed(p,content));stamp=p.stat().st_mtime_ns
            self.assertFalse(city.write_if_changed(p,city.render(self.snapshot)))
            self.assertEqual(p.stat().st_mtime_ns,stamp)

    def test_failed_refresh_preserves_last_good_files(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'assets').mkdir();p=root/'assets/contribution-city.svg';p.write_text('last good')
            with patch.object(city,'ROOT',root),patch.object(city,'collect',side_effect=urllib.error.URLError('offline')),patch.object(sys,'argv',['generate_city.py']):
                self.assertEqual(city.main(),1)
            self.assertEqual(p.read_text(),'last good')

if __name__=='__main__':unittest.main()
