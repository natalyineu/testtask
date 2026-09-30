"""Read Telegram groups/chats (e.g. Pol_relocation, cyprusithr) via your own account using Telethon.
Web preview (tg_scrape.py) only works for channels; groups need a logged-in account.

Setup (once):
  pip install telethon
  1. https://my.telegram.org -> API development tools -> create app -> copy api_id and api_hash
  2. export TG_API_ID=...  TG_API_HASH=...   (never commit them)
  3. First run asks for your phone number and the login code from Telegram; a session file is saved locally.
     Do not share or commit the *.session file - it gives access to your account.

Usage: python3 tg_groups.py --since 2026-09-16 --out groups.json Pol_relocation cyprusithr
"""
import argparse, asyncio, datetime, json, os, re

from telethon import TelegramClient

from tg_scrape import KW


async def main(a):
    cut = datetime.datetime.fromisoformat(a.since).replace(tzinfo=datetime.timezone.utc)
    out = []
    async with TelegramClient('job_search', int(os.environ['TG_API_ID']), os.environ['TG_API_HASH']) as client:
        for chat in a.chats:
            async for m in client.iter_messages(chat, offset_date=None):
                if m.date < cut:
                    break
                text = m.message or ''
                if KW.search(text):
                    out.append(dict(ch=chat, id=m.id, date=m.date.date().isoformat(),
                                    url=f'https://t.me/{chat}/{m.id}', text=text[:1500],
                                    links=re.findall(r'https?://\S+', text)[:5]))
            print(chat, 'done')
    json.dump(out, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(len(out), 'posts ->', a.out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--since', required=True)
    ap.add_argument('--out', default='groups.json')
    ap.add_argument('chats', nargs='+')
    asyncio.run(main(ap.parse_args()))
