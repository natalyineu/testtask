# Инструкция для новой сессии — поиск вакансий для Ильи Хаетова

## Цель
Автоматически находить вакансии Customer Support / Customer Success в компаниях с российскими/СНГ корнями и добавлять их в Google Sheet.

---

## Профиль кандидата — Илья Хаетов
- **Роль:** Customer Support / Customer Success Specialist
- **Локация:** Крагуевац, Сербия (волонтёр)
- **Формат:** только полностью удалённая работа (remote), доступная из Сербии
- **LinkedIn:** доступен в Сербии (не заблокирован)
- **Язык:** русский (родной), английский (рабочий)
- **Опыт:** ~3+ лет в поддержке клиентов, работал в B2B/B2C, знает Zendesk/Intercom, Excel

## Ключевой фильтр вакансий
**ТОЛЬКО компании с российскими/СНГ корнями** — Yango, inDrive, Semrush, Xsolla, PandaDoc, Preply, Nebius, airSlate, Social Discovery Group, Mitgo, Sber-спинофы, Genesis Group, и подобные.

**НЕ брать:**
- Компании только для US/Canada (требуют местного присутствия)
- Вакансии типа "Miami", "New York" без глобального remote
- IT-роли (разработчики, QA, DevOps) — только CS/CX/Support

---

## Google Sheet (основной результат)
- **ID:** `1JrxnkkqaG-l004sTcPT6fLyJJ9ndpc18LodpIjt3NXo`
- **Название листа:** `Untitled`
- **sheetId:** `1600143643`
- **Ссылка:** https://docs.google.com/spreadsheets/d/1JrxnkkqaG-l004sTcPT6fLyJJ9ndpc18LodpIjt3NXo

### Структура таблицы (заголовки в строке 1):
```
Date | Title | Company | Type | Salary | Match | Apply Link | Source
```

Данные вносить начиная со строки 2. Перед добавлением делать `get_values` чтобы не дублировать.

---

## Источники поиска

### 1. Telegram каналы (через Apify `automation-lab/telegram-scraper`)
Основные каналы для CS/CX вакансий:
- `evacuatejobs` — вакансии с relocation и remote (remocate.app)
- `digital_hr` — IT и Digital вакансии
- `Remoteit` — удалёнка, есть российские компании
- `relocateme` — релокация и remote
- `jobsearchIT` — IT вакансии
- `remotejobss` — remote jobs

Запуск актора:
```json
{
  "channelUsernames": ["evacuatejobs", "digital_hr", "Remoteit", "relocateme", "jobsearchIT", "remotejobss"],
  "resultsLimit": 50
}
```

### 2. hh.ru (через WebFetch)
URL для поиска:
```
https://hh.ru/search/vacancy?text=customer+support&schedule=remote&search_field=name&area=1&area=2&area=113
```
Фильтровать по: remote, компании с рос. корнями, зарплата в USD/EUR предпочтительно.

### 3. remocate.app (через WebFetch)
```
https://remocate.app/jobs?category=customer-support
```
Фильтровать только компании с российскими корнями.

### 4. JobsPipe MCP (`mcp__347f4b83`)
```json
{
  "query": "customer support remote",
  "job_country_code_not": "US",
  "posted_at_max_age_days": 7
}
```

---

## Правила добавления в таблицу

| Поле | Что писать |
|------|-----------|
| Date | Дата публикации вакансии (YYYY-MM-DD) |
| Title | Название роли |
| Company | Название компании |
| Type | Remote |
| Salary | Зарплата если указана ($X/мес или ₽XX,XXX) |
| Match | ★★★★ (отлично) / ★★★ (хорошо) / ★★ (средне) |
| Apply Link | Прямая ссылка на вакансию |
| Source | hh.ru / Telegram @канал / remocate / JobsPipe |

**Match-рейтинг:**
- ★★★★ — CS/CX роль, зарплата в USD/EUR, реально global remote, рос. компания
- ★★★ — CS/CX роль, remote доступен из Сербии, рос. компания
- ★★ — похожая роль (Account Manager, Technical Support), рос. компания

---

## Известные хорошие компании для поиска
Все нижеперечисленные — с рос./СНГ корнями, нанимают удалённо:
- **Semrush** — SEO-платформа, основана россиянами
- **Xsolla** — платёжная платформа для gamedev
- **PandaDoc** — документооборот
- **Preply** — edtech (основана украинцами, глобальная)
- **Nebius** — AI/cloud (выделен из Яндекса)
- **airSlate** — автоматизация документов
- **inDrive** — райдшеринг (основан в Якутии)
- **Social Discovery Group** — dating apps
- **Mitgo** — affiliate marketing (Admitad)
- **Yango** — Яндекс Go международный
- **Genesis Group AG** — украинский холдинг tech компаний

---

## Что НЕ делать
- Не добавлять вакансии из US/Canada со словами "Miami", "Austin", "San Francisco" без global remote
- Не добавлять IT-вакансии (developer, engineer, QA)
- Не дублировать — проверять Apply Link перед добавлением
- Не брать вакансии старше 2 недель

---

## Подключённые MCP инструменты
- **Google Sheets** — `mcp__1bc9aec0` — запись/чтение таблицы
- **Google Drive** — `mcp__0327e331` — создание файлов
- **Gmail** — `mcp__c1fa05ee` — черновики писем (аккаунт: rumiantsevanatali@gmail.com)
- **Apify** — `mcp__Apify` — скрейпинг Telegram и других сайтов
- **JobsPipe** — `mcp__347f4b83` — поиск вакансий (30+ источников)
- **Indeed** — `mcp__4560d9d1` — поиск вакансий

---

## Типичная ошибка (была в прошлой сессии)
При вставке данных через `append_values` — НЕ включать строку заголовков в массив values, иначе появятся дубли. Только строки с данными.

Перед записью делать `get_spreadsheet` для проверки имени листа (не всегда "Sheet1").
