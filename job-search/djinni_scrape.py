"""Scrape djinni.co remote vacancies by keyword; keeps Worldwide / Europe / Serbia locations.

Usage: python3 djinni_scrape.py --since 2026-09-16 --out djinni.json
"""
import argparse, datetime, html, json, re, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124'}
KEYWORDS = ['customer support', 'customer success', 'support', 'account manager', 'operations', 'KYC', 'AML', 'fraud',
            'risk', 'compliance', 'payments', 'onboarding', 'VIP', 'back office', 'chargeback', 'moderator',
            'customer experience', 'technical support']
OK_LOC = re.compile(r'Worldwide|Countries of Europe|Serbia|Albania', re.I)
SKIP = re.compile(r'develop|engineer|devops|\bqa\b|head|director|lead|sales|senior|designer|marketing|buyer|recruit|'
                  r'architect|product-manager|backend|frontend|seo|smm|affiliate|media|content|writer|cto|cfo|ceo|coo', re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'ignore')


def search(cut):
    res = {}
    for k in KEYWORDS:
        for p in range(1, 5):
            q = urllib.parse.urlencode({'all_keywords': k, 'search_type': 'basic-search', 'employment': 'remote', 'page': p})
            blocks = get('https://djinni.co/jobs/?' + q).split('class="job-item card-link')[1:]
            if not blocks:
                break
            old = 0
            for b in blocks:
                m = re.search(r'href="(/jobs/(\d+)-([^"/]+)/?)"', b)
                d = re.search(r'title="\d\d:\d\d (\d\d)\.(\d\d)\.(\d{4})"', b)
                if not m or not d:
                    continue
                date = datetime.date(int(d.group(3)), int(d.group(2)), int(d.group(1)))
                if date < cut:
                    old += 1
                    continue
                loc = re.search(r'location-text[^>]*>(.*?)</', b, re.S)
                loc = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', loc.group(1))).split()) if loc else ''
                sal = re.search(r'(\$[\d,\s–-]+\d)', html.unescape(b))
                if OK_LOC.search(loc) and not SKIP.search(m.group(3)):
                    res[m.group(2)] = dict(id=m.group(2), url='https://djinni.co' + m.group(1), date=str(date),
                                           loc=loc, salary=sal.group(1).strip() if sal else '')
            if old > len(blocks) / 2:
                break
            time.sleep(0.7)
    return list(res.values())


def add_title(v):
    t = re.search(r'<meta property="og:title" content="([^"]+)"', get(v['url']))
    title, _, company = html.unescape(t.group(1)).rpartition(' at ') if t else ('', '', '')
    v['title'], v['company'] = title.strip(), company.strip()
    return v


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--since', required=True)
    ap.add_argument('--out', default='djinni.json')
    a = ap.parse_args()
    items = search(datetime.date.fromisoformat(a.since))
    with ThreadPoolExecutor(6) as ex:
        items = list(ex.map(add_title, items))
    json.dump(items, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(len(items), 'vacancies ->', a.out)
