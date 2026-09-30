"""Scrape hh.ru search pages (remote vacancies, last N days). The hh API returns 403, so HTML is parsed.

Usage:
  python3 hh_scrape.py --out hh.json                      # all regions
  python3 hh_scrape.py --non-ru --out hh_nonru.json       # BY, KZ, GE, UZ, KG + other countries
  python3 hh_scrape.py --details hh.json --out hh_det.json  # add date/salary/employer from vacancy pages
"""
import argparse, html, json, re, time, urllib.parse, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124'}
QUERIES = [
    'customer support', 'customer success', 'support specialist', 'поддержка клиентов', 'специалист поддержки',
    'менеджер поддержки', 'саппорт', 'чат поддержки', 'клиентский сервис', 'customer experience', 'account manager',
    'technical support', 'риск аналитик', 'risk analyst', 'операционный специалист', 'operations specialist', 'KYC',
    'AML', 'антифрод', 'fraud analyst', 'payment operations', 'платежн', 'back office', 'бэк-офис', 'compliance',
    'верификац', 'chargeback', 'мониторинг транзакций', 'onboarding specialist', 'crypto', 'крипто', 'web3', 'p2p',
]
NON_RU_AREAS = [16, 40, 28, 97, 48, 1001]  # Belarus, Kazakhstan, Georgia, Uzbekistan, Kyrgyzstan, other countries
SKIP = re.compile(r'develop|разработ|инженер|engineer|devops|\bQA\b|тестиров|руководител|head|директор|lead|'
                  r'sales|продаж|senior|designer|дизайн|маркетолог|buyer|байер|бухгалт|юрист|recruit|рекрут', re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'ignore')


def txt(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace(' ', ' ').replace('\xa0', ' ').strip()


def search(non_ru, days):
    res = {}
    for q in QUERIES:
        for p in range(3):
            params = [('text', q), ('search_field', 'name'), ('schedule', 'remote'), ('search_period', days),
                      ('items_on_page', 100), ('page', p)]
            if non_ru:
                params += [('area', a) for a in NON_RU_AREAS]
            h = get('https://hh.ru/search/vacancy?' + urllib.parse.urlencode(params))
            blocks = h.split('data-qa="vacancy-serp__vacancy"')[1:]
            for b in blocks:
                m = re.search(r'href="https://hh\.ru/vacancy/(\d+)', b)
                if not m:
                    continue
                t = re.search(r'serp-item__title-text"[^>]*>(.*?)</', b, re.S)
                e = re.search(r'vacancy-serp__vacancy-employer-text"[^>]*>(.*?)</(?:span|a)>', b, re.S)
                a = re.search(r'vacancy-serp__vacancy-address"[^>]*>(.*?)</', b, re.S)
                title = txt(t.group(1)) if t else ''
                if SKIP.search(title):
                    continue
                res[m.group(1)] = dict(id=m.group(1), title=title, emp=txt(e.group(1)) if e else '',
                                       area=txt(a.group(1)) if a else '', url=f'https://hh.ru/vacancy/{m.group(1)}')
            if len(blocks) < 100:
                break
            time.sleep(0.7)
    return list(res.values())


def details(items):
    for v in items:
        h = get(v['url'])
        d = re.search(r'"datePosted"\s*:\s*"([^"]+)"', h)
        s = re.search(r'data-qa="vacancy-salary"[^>]*>(.*?)</div>', h, re.S)
        v['date'] = d.group(1)[:10] if d else ''
        v['salary'] = txt(s.group(1)) if s else ''
        v['tk_rf'] = bool(re.search(r'ТК РФ|гражданств[оа] РФ', h))
        time.sleep(0.5)
    return items


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--non-ru', action='store_true')
    ap.add_argument('--days', type=int, default=14)
    ap.add_argument('--details', help='input json from a previous search run')
    ap.add_argument('--out', default='hh.json')
    a = ap.parse_args()
    data = details(json.load(open(a.details))) if a.details else search(a.non_ru, a.days)
    json.dump(data, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(len(data), 'vacancies ->', a.out)
