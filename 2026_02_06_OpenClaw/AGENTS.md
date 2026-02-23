Это презентация к вебинару. Основная часть вебинара — живое демо, слайды служат опорой.

## Структура презентации

1. **Что такое OpenClaw** — факты, сравнение с ChatGPT, три столпа (UX, проактивность, самомодификация), спектр автономности
2. **Архитектура** — простой agentic loop (НЕ ReAct), самомодифицирующийся агент, системный промпт и тулы, память (файлы), Skills vs MCP
3. **Философия автора** — почему «взлетел», Soul.md и Heartbeat, безопасность (defense in depth), будущее (агент → OS)
4. **Запуск на GigaChat / Ollama** — конфигурация, mitmproxy-трассировка
5. **Моё видение** — автономность vs совместная работа, конвергенция

## Ключевые источники

- Интервью Peter Steinberger у Lex Fridman (#491): `docs/openclaw/posts/lex491-openclaw-peter-steinberger-en-full-log.md`
- Официальный блог: `https://openclaw.ai/blog`
- Конспекты и ссылки: `docs/openclaw/`

## Ключевые факты

- 180K+ GitHub Stars, MIT License, TypeScript
- Автор: Peter Steinberger (@steipete) — 13 лет PSPDFKit (1B+ устройств)
- Архитектура: простой tool-calling loop, 23 тула, файлы как память
- Философия: fun > serious, простота > оркестрация, human touch
