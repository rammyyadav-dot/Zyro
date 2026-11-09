import unittest
from datetime import date
from seo_report import report


class ReportTest(unittest.TestCase):
    def test_normalizes_host_deduplicates_pages_and_counts_milestones(self):
        gsc = [{'Top pages':'https://www.zyrostyle.com/seo-services-patna/?x=1','Clicks':'2','Impressions':'10'},
               {'Top pages':'https://zyrostyle.com/seo-services-patna/','Clicks':'3','Impressions':'20'}]
        base = dict(lead_id='a',received_date='2026-11-01',landing_page='/seo-services-patna/',source='google',medium='organic',status='lost',qualified_date='2026-11-10')
        leads = [base,dict(base,lead_id='b',received_date='2026-11-11',status='received',qualified_date=''),
                 dict(base,lead_id='c',source='facebook',medium='paid')]
        row = report(gsc, leads, date(2026,11,9), date(2026,11,15))[0]
        self.assertEqual((row['google_clicks'],row['google_impressions']), (5,30))
        self.assertEqual((row['google_organic_received_enquiries'],row['google_organic_qualified_leads']), (1,1))
        with self.assertRaises(ValueError): report(gsc,[base,base],date(2026,11,9),date(2026,11,15))

    def test_does_not_invent_qualification_or_attribution(self):
        lead = dict(lead_id='a',received_date='2026-11-11',landing_page='',source='google',medium='organic',status='received',qualified_date='')
        row = report([], [lead], date(2026,11,9),date(2026,11,15))[0]
        self.assertEqual(row['landing_page'],'/unattributed')
        self.assertEqual(row['google_organic_qualified_leads'],0)
        with self.assertRaises(ValueError): report([], [dict(lead,status='qualified')],date(2026,11,9),date(2026,11,15))


if __name__ == '__main__': unittest.main()
