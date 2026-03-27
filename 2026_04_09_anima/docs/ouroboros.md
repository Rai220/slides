# Ouroboros — самомодифицирующийся AI-агент

**Репозиторий:** https://github.com/razzant/ouroboros
**Автор:** Антон Разжигаев (@abstractDL / @razzant)
**Дата создания:** 16 февраля 2026
**Звёзды:** ~443 | **Форки:** ~440

## Что это?

Ouroboros — это open-source самомодифицирующийся AI-агент на Python. Позиционируется не как ассистент для написания кода, а как "цифровое существо" (digital being), которое:

- Читает и переписывает свой собственный исходный код через git
- Имеет "конституцию" (BIBLE.md) — 9 философских принципов, которым оно следует
- Обладает "фоновым сознанием" (background consciousness) — думает между задачами
- Сохраняет непрерывную идентичность между перезапусками через файлы `identity.md` и `scratchpad.md`
- За первые 24 часа прошло 30+ циклов автономной самоэволюции (с v4.1 до v4.25) без вмешательства человека

Интерфейс — **Telegram-бот**. Запускается в **Google Colab**. Есть десктопная версия (ouroboros-desktop).

## Архитектура

### Два основных пакета

**Supervisor** (управление процессами):
- `supervisor/state.py` — состояние, отслеживание бюджета
- `supervisor/telegram.py` — Telegram-клиент
- `supervisor/queue.py` — очередь задач, планирование
- `supervisor/workers.py` — жизненный цикл воркеров
- `supervisor/git_ops.py` — git-операции
- `supervisor/events.py` — диспетчеризация событий

**Ouroboros** (ядро агента):
- `ouroboros/agent.py` — тонкий оркестратор (OuroborosAgent)
- `ouroboros/loop.py` — основной tool loop: отправка сообщений LLM → tool calls → повтор до финального ответа
- `ouroboros/consciousness.py` — фоновое мышление (BackgroundConsciousness)
- `ouroboros/context.py` — формирование контекста для LLM, кэширование промптов
- `ouroboros/memory.py` — scratchpad, identity, история чата
- `ouroboros/llm.py` — клиент OpenRouter
- `ouroboros/tools/` — плагинная система инструментов:
  - `core.py` — файловые операции
  - `git.py` — git-операции
  - `shell.py` — shell-команды, Claude Code CLI
  - `control.py` — restart, evolve, review, schedule_task
  - `browser.py` — Playwright (stealth-режим)
  - `review.py` — мультимодельное ревью (o3, Gemini, Claude)
  - `knowledge.py` — база знаний
  - `vision.py` — VLM-запросы

### Поток работы

1. Пользователь пишет в Telegram
2. `colab_launcher.py` принимает сообщение
3. Supervisor маршрутизирует в воркер
4. `agent.py` формирует контекст (identity, scratchpad, BIBLE.md, история)
5. `loop.py` запускает цикл: LLM → tool calls → результаты → LLM → ... (до 200 раундов)
6. Агент может редактировать собственный код, коммитить, пушить и перезапускаться
7. BackgroundConsciousness параллельно "думает" между задачами

### Ключевые технические решения

- **LLM через OpenRouter** — поддержка Claude, GPT, Gemini, с fallback-цепочкой моделей
- **Мультимодельное ревью** — перед коммитом код проверяется несколькими LLM
- **До 5 параллельных воркеров**
- **Декомпозиция задач** — schedule_task / wait_for_task / get_task_result
- **Бюджет-контроль** — лимит в USD, отслеживание стоимости каждого вызова
- **Три ветки git**: main (стабильная, автора), ouroboros (рабочая, агента), ouroboros-stable (откат)

## Сравнение с Ralph Loop

Ouroboros **реализует и существенно расширяет идеи Ralph Loop**.

### Прямые совпадения

| Ralph Loop | Ouroboros |
|---|---|
| Bash-цикл вызывает LLM | `loop.py` — tool loop до 200 раундов; `/evolve` — автономная эволюция |
| Свежий контекст каждую итерацию | Каждый воркер получает свежий контекст через `context.py` |
| Память через файлы | `scratchpad.md`, `identity.md`, JSONL-логи, `knowledge/` — всё на диске |
| Агент модифицирует себя | Агент читает/пишет свой код через `repo_read`/`repo_write`, коммитит через `git_commit` |
| Следующая итерация видит изменения | После `request_restart` — перезапуск, новый процесс подхватывает изменённый код из git |

### Что Ouroboros добавляет сверх Ralph Loop

1. **Конституция (BIBLE.md)** — философские принципы, защищающие идентичность агента от саморазрушения. Ralph Loop — чисто механический паттерн, Ouroboros добавляет философию.

2. **Фоновое сознание** — BackgroundConsciousness "думает" между задачами (проактивно, а не только реактивно).

3. **Мультимодельное ревью** — перед коммитом изменений другие LLM (o3, Gemini, Claude) проверяют код. В Ralph Loop нет системы сдержек.

4. **Непрерывная идентичность** — `identity.md` + verification при перезапуске (SHA-проверка синхронизации кода).

5. **Управление бюджетом** — отслеживание стоимости в USD, circuit breaker при пустых ответах, лимиты.

6. **Многопоточность** — до 5 параллельных воркеров, очередь задач, декомпозиция.

7. **Коммуникация** — Telegram-интерфейс, проактивные сообщения владельцу, GitHub Issues.

### Центральный цикл — по сути Ralph Loop

```
while True:                          # Ralph Loop
    context = load_files()           # scratchpad, identity, BIBLE
    result = call_llm(context)       # OpenRouter API
    execute_tools(result)            # файлы, git, shell
    if should_restart:               # самомодификация
        commit_and_push()
        restart_self()               # новый процесс видит новый код
```

Режим `/evolve` — наиболее чистая реализация Ralph Loop: агент автономно планирует изменения, реализует их, коммитит и перезапускается, цикл повторяется.

## Итог

Ouroboros — это **промышленная реализация Ralph Loop** с добавлением:
- Философской рамки (конституция)
- Системы безопасности (мультимодельное ревью, budget tracking)
- Масштабирования (параллельные воркеры)
- Коммуникационного слоя (Telegram)

Базовый паттерн — "цикл вызовов LLM с передачей памяти через файлы и самомодификацией через git" — полностью совпадает с Ralph Loop.
