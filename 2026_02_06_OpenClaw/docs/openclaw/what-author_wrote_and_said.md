# Что автор OpenClaw сам писал и проговаривал (короткая выжимка)

Ниже — конспект **первичных тезисов** из материалов, где автор (Peter Steinberger) и команда OpenClaw прямо формулируют позицию.

## 1) Проект родился как “weekend hack”, но быстро стал большим

Из поста “Introducing OpenClaw” видно, что автор позиционирует старт как эксперимент/прототип, который очень быстро вырос до масштаба “нужны мейнтейнеры, процессы, безопасность”.

Источник: `https://openclaw.ai/blog/introducing-openclaw`

## 2) “Local-first” и контроль над данными — центральная идея

Автор явно противопоставляет OpenClaw SaaS‑ассистентам:

- ассистент работает там, где вы решите (локально/домашний сервер/VPS),
- контроль над ключами/инфраструктурой/данными остаётся у пользователя.

Источник: `https://openclaw.ai/blog/introducing-openclaw`  
Доп. первоисточник (публичное позиционирование в README): `https://github.com/openclaw/openclaw`

## 3) Prompt injection не “решили” — поэтому безопасность должна быть инженерной

Автор пишет, что prompt injection — нерешённая проблема индустрии, поэтому ставка делается на:

- строгие политики доступа (кто может триггерить агента),
- снижение blast radius (sandbox, deny/allowlist),
- процессы: аудит, threat model, публичный roadmap.

Источники:

- `https://openclaw.ai/blog/introducing-openclaw`
- `https://docs.openclaw.ai/gateway/security`
- `https://trust.openclaw.ai/`

## 4) Skills/marketplace — главный мультипликатор пользы и риска

Ключевая мысль команды: skills — это код в контексте вашего агента (с доступом к данным/инструментам), поэтому supply chain становится критичной.

Источник: `https://openclaw.ai/blog/virustotal-partnership`

## 5) “Defense in depth”, а не “серебряная пуля”

В анонсе интеграции с VirusTotal отдельно зафиксировано: сканирование — это один из слоёв защиты, но не гарантия безопасности.

Источник: `https://openclaw.ai/blog/virustotal-partnership`

