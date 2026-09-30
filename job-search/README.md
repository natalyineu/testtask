# Job search: Customer Support / CS / fintech ops (remote from Serbia)

Results go to a Google Sheet (ID kept outside the repo)
(columns: Date | Title | Company | Location | Salary | Match | Apply Link | Source).

Network access needed: `t.me`, `hh.ru` (plus `remocate.app`, `djinni.co` if used).

## Telegram (channel list: channels.txt)
```
python3 tg_scrape.py --since 2026-09-16 --out tg.json \
  evacuatejobs remocate igaming_work call_rabota jobs_support Remoteit remotejobss web3hiring cryptojobslist
```
Most useful: `igaming_work`, `call_rabota`, `evacuatejobs`/`remocate`. `jobsearchIT` returned nothing,
`remotejobss` posts have no links.

## djinni
```
python3 djinni_scrape.py --since 2026-09-16 --out djinni.json
```

## hh.ru
```
python3 hh_scrape.py --non-ru --out hh_nonru.json   # vacancies outside Russia (RF contracts don't work from Serbia)
python3 hh_scrape.py --details hh_nonru.json --out hh_det.json
```
`api.hh.ru` returns 403, so the scripts parse search/vacancy HTML. Drop rows with `tk_rf: true`.

## Filters used
- Remote only, available from Serbia; skip RF labor contracts, US/Canada-only, IT/engineering roles.
- Match: ★★★★ CS/CX + USD/EUR + global remote; ★★★ CS/CX remote; ★★ adjacent (account mgmt, tech support, ops, KYC/AML).
- Check Apply Link against the sheet before adding (no duplicates).
