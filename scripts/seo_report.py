#!/usr/bin/env python3
"""Combine same-window GSC page exports and staff-reviewed lead records. No dependencies."""
import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


def page(value):
    u = urlsplit(value.strip())
    if u.netloc and u.hostname not in ('zyrostyle.com', 'www.zyrostyle.com'):
        raise ValueError('Unexpected landing-page host')
    if not u.path.startswith('/'):
        raise ValueError('Landing page must be a site URL or absolute path')
    path = u.path
    if path.endswith('/index.html'):
        path = path[:-10]
    return path if '.' in path.rsplit('/', 1)[-1] else path.rstrip('/') + '/'


def rows(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def report(gsc, leads, start, end):
    if start > end:
        raise ValueError('Start date must precede end date')
    totals = defaultdict(lambda: {'clicks': 0, 'impressions': 0, 'received': 0, 'qualified': 0})
    for row in gsc:
        key = page(row['Top pages'])
        totals[key]['clicks'] += int(row['Clicks'].replace(',', ''))
        totals[key]['impressions'] += int(row['Impressions'].replace(',', ''))
    seen = set()
    for row in leads:
        lead_id = row['lead_id'].strip()
        if not lead_id or lead_id in seen:
            raise ValueError('Lead records require unique, nonempty lead_id values')
        seen.add(lead_id)
        if row['source'].lower() != 'google' or row['medium'].lower() != 'organic':
            continue
        received = date.fromisoformat(row['received_date'])
        qualified = date.fromisoformat(row['qualified_date']) if row['qualified_date'] else None
        if qualified and qualified < received:
            raise ValueError('Qualification cannot predate receipt')
        if row['status'] not in ('received', 'qualified', 'won', 'unqualified', 'lost'):
            raise ValueError('Unknown reviewed lead status')
        if row['status'] in ('qualified', 'won') and not qualified:
            raise ValueError('Qualified and won leads require qualified_date')
        key = page(row['landing_page']) if row['landing_page'].strip() else '/unattributed'
        if start <= received <= end:
            totals[key]['received'] += 1
        # Count the recorded qualification milestone, even if a qualified lead was later lost.
        if qualified and start <= qualified <= end:
            totals[key]['qualified'] += 1
    return [dict(landing_page=k, google_clicks=v['clicks'], google_impressions=v['impressions'],
                 search_ctr=round(v['clicks'] / v['impressions'], 4) if v['impressions'] else '',
                 google_organic_received_enquiries=v['received'], google_organic_qualified_leads=v['qualified'])
            for k, v in sorted(totals.items())]


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--gsc', required=True, help='GSC Pages.csv, filtered to the reporting period')
    ap.add_argument('--leads', required=True, help='Reviewed lead CSV; never use click events here')
    ap.add_argument('--start', type=date.fromisoformat, required=True)
    ap.add_argument('--end', type=date.fromisoformat, required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    result = report(rows(a.gsc), rows(a.leads), a.start, a.end)
    fields = ['landing_page', 'google_clicks', 'google_impressions', 'search_ctr', 'google_organic_received_enquiries', 'google_organic_qualified_leads']
    with open(a.out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(result)
    print(f'Wrote {len(result)} page rows for {a.start} through {a.end}; GSC export must use this exact period.')
