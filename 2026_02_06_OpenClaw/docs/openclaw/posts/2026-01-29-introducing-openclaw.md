# Introducing OpenClaw (2026‑01‑29) — конспект

- **Источник**: `https://openclaw.ai/blog/introducing-openclaw`
- **Автор**: Peter Steinberger (`@steipete`)
- **Зачем читать**: это “origin story” и позиционирование OpenClaw (local‑first, open source, community‑driven), плюс объяснение переименований.

## Ключевые тезисы автора

### 1) “Weekend project” → вирусный рост

Автор описывает проект как быстрый “хак на выходных”, который внезапно вырос до масштаба, требующего процессов и команды.

### 2) Naming journey: Clawd → Moltbot → OpenClaw

Сводка по тексту:

- **Clawd** (ноябрь 2025): игра слов вокруг “Claude” + lobster‑мотив.
- **Moltbot**: выбран комьюнити; “molt” как метафора роста (линька у лобстеров).
- **OpenClaw**: финальное имя после “домашней работы” (trademark search, домены, миграции).

### 3) Что такое OpenClaw по версии автора

OpenClaw — “open agent platform”, который:

- работает на машине пользователя (laptop / homelab / VPS),
- отвечает в привычных чат‑каналах (WhatsApp/Telegram/Discord/Slack/Teams и т.п.),
- делает акцент на “владении инфраструктурой и данными”.

### 4) Безопасность как постоянный фокус

Автор прямо говорит, что prompt injection — “нерешённая” отраслью проблема, и рекомендует изучать best practices и использовать сильные модели (в контексте именно инструментальных агентов).

### 5) Проекту нужна команда

Фиксируется сдвиг от “solo maintainer” к расширению состава мейнтейнеров и настройке процессов/финансирования.

## Цитаты (короткие)

> “Two months ago, I hacked together a weekend project. What started as “WhatsApp Relay” now has over 100,000 GitHub stars and drew 2 million visitors in a single week.”

> “Your assistant. Your machine. Your rules.”

> “Unlike SaaS assistants where your data lives on someone else’s servers, OpenClaw runs where you choose… Your infrastructure. Your keys. Your data.”

> “prompt injection is still an industry-wide unsolved problem”

## Связанные ссылки из поста

- Security best practices: `https://docs.openclaw.ai/gateway/security`
- “Machine-checkable security models”: `https://github.com/vignesh07/clawdbot-formal-models`
- Contributing: `https://github.com/openclaw/openclaw/blob/main/CONTRIBUTING.md`
- Sponsoring: `https://github.com/sponsors/openclaw`

