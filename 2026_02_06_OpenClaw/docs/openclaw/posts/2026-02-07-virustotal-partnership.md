# OpenClaw × VirusTotal (2026‑02‑07) — конспект

- **Источник**: `https://openclaw.ai/blog/virustotal-partnership`
- **Авторы**: Peter Steinberger (`@steipete`), Jamieson O'Reilly (`@theonejvo`), Bernardo Quintero (`@bquintero`)
- **Зачем читать**: это программное заявление по безопасности экосистемы skills/marketplace (ClawHub) и конкретная интеграция со сканированием.

## Ключевые тезисы авторов

### 1) “AI agents are a fundamental shift”

Пост объясняет, что агент отличается от “обычного софта”: он интерпретирует естественный язык и сам принимает решения об экшенах. Это сдвигает границы безопасности (уязвимость может быть “в языке”, не только в коде).

### 2) Skills — расширение возможностей и поверхности атаки

Навыки (skills) выполняются в контексте агента и потенциально имеют доступ к инструментам/данным. В посте перечислены риски: эксфильтрация, несанкционированные команды, отправка сообщений от имени пользователя, загрузка payload.

### 3) Механика сканирования при публикации в ClawHub

В посте описан конвейер:

- детерминированная упаковка skill в ZIP + метаданные,
- SHA‑256 хэш,
- lookup/аплоад в VirusTotal,
- **Code Insight** (LLM‑анализ поведения кода/инструкций),
- авто‑аппрув “benign”, маркировка “suspicious”, блок “malicious”,
- ежедневные ресканы.

### 4) “Not a silver bullet”

Авторы подчёркивают, что это слой защиты, а не “решение всего”: prompt injection и социальная инженерия по‑прежнему остаются риском, поэтому нужен defense‑in‑depth.

## Цитаты (короткие)

> “Unlike traditional software that does exactly what code tells it to do, AI agents interpret natural language and make decisions about actions.”

> “Skills are code that runs in your agent’s context, with access to your tools and your data.”

> “Let’s be clear: this is not a silver bullet.”

## Связанные материалы

- Trust / security program: `https://trust.openclaw.ai/`
- Security guide (Gateway): `https://docs.openclaw.ai/gateway/security`
- Контекст со стороны VT (упоминается в посте как “documented cases”):  
  `https://blog.virustotal.com/2026/02/from-automation-to-infection-how.html`

