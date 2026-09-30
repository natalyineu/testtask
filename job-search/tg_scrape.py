"""Scrape public Telegram channels via t.me/s/<channel> and keep job posts matching keywords.

Usage: python3 tg_scrape.py --since 2026-09-16 --out tg.json evacuatejobs igaming_work call_rabota ...
"""
import argparse, datetime, html, json, re, sys, urllib.request

KW = re.compile(
    r'support|саппорт|поддержк|customer success|customer experience|customer care|client success|'
    r'account manager|аккаунт|helpdesk|оператор|клиентск|KYC|AML|fraud|фрод|риск|risk|compliance|'
    r'комплаенс|операцион|operations|verification|верификац|payment|платеж|back.?office|бэк.?офис|chargeback',
    re.I)


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')


def scrape(channel, cut, max_pages=15):
    out, before = [], None
    for _ in range(max_pages):
        url = f'https://t.me/s/{channel}' + (f'?before={before}' if before else '')
        try:
            page = get(url)
        except Exception as e:
            print(channel, 'ERR', e, file=sys.stderr)
            break
        blocks = re.split(r'(?=<div class="tgme_widget_message_wrap)', page)[1:]
        ids = []
        for b in blocks:
            m = re.search(r'data-post="[^/]+/(\d+)"', b)
            if not m:
                continue
            pid = int(m.group(1))
            ids.append(pid)
            t = re.search(r'datetime="([^"]+)"', b)
            dt = datetime.datetime.fromisoformat(t.group(1)) if t else None
            tx = re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', b, re.S)
            raw = tx.group(1) if tx else ''
            text = re.sub(r'<[^>]+>', '', html.unescape(re.sub(r'<br\s*/?>', '\n', raw)))
            links = [l for l in re.findall(r'href="(https?://[^"]+)"', raw) if 't.me/' not in l]
            if dt and dt >= cut and KW.search(text):
                out.append(dict(ch=channel, id=pid, date=dt.date().isoformat(),
                                url=f'https://t.me/{channel}/{pid}', text=text[:1500], links=links[:5]))
        if not ids:
            break
        dates = re.findall(r'datetime="([^"]+)"', page)
        if dates and datetime.datetime.fromisoformat(dates[0]) < cut:
            break
        before = min(ids)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--since', required=True, help='YYYY-MM-DD')
    ap.add_argument('--out', default='tg.json')
    ap.add_argument('channels', nargs='+')
    a = ap.parse_args()
    cut = datetime.datetime.fromisoformat(a.since).replace(tzinfo=datetime.timezone.utc)
    res = [p for ch in a.channels for p in scrape(ch, cut)]
    json.dump(res, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(len(res), 'posts ->', a.out)
