---
theme: penguin
colorSchema: dark
title: "OpenClaw: вебинар, часть 2"
fonts:
  sans: 'Open Sans'
  provider: google
class: text-left
mdc: true
transition: slide-left
---

# OpenClaw

## Вебинар, часть 2

### Практические кейсы использования

<div class="mt-8 text-sm text-gray-400">
Формат: короткие слайды + живые демо
</div>

<div class="mt-2 text-sm text-gray-500">
Константин Крестников
</div>

---

# Важное замечание перед демо

<div class="mt-3 grid grid-cols-[1.1fr_0.9fr] gap-6 items-start">

<div>

<v-clicks>

- Сегодня в демо используем бота в режиме `low` или `off` reasoning - так ответы приходят быстрее
- Из-за этого часть кейсов может сработать неидеально или не сработать с первого раза
- В обычной работе я чаще выбираю `high`, `xhigh` или `auto`
- В этих режимах ответы занимают больше времени, но агент рассуждает лучше и обычно надежнее доводит задачу до результата

</v-clicks>

</div>

<img src="think_level.jpg" class="rounded-lg border border-white/10 max-h-96 mx-auto" />

</div>

---

# План второй части

<v-clicks>

- **Шаг 0: UI и потребление токенов** - знакомство с интерфейсом OpenClaw
- Кейс 1: туризм и командировки
- Кейс 2: работа с презентациями
- Кейс 3: заполнение и подписание документов
- Кейс 4: работа с почтой и правила коммуникации
- Кейс 5: веб-автоматизация личных кабинетов
- Кейс 6: контент-пайплайн для Telegram и сообществ
- Быстрые кейсы: домены для роутера, генерация медиа

</v-clicks>

---

# Подключаемся к OpenClaw

<div class="mt-4 text-gray-300">
Первым делом заходим в веб-интерфейс:
</div>

**1. Поднимаем SSH-тоннель:**

```bash
ssh \
  -L 18789:127.0.0.1:80 \
  -L 18792:127.0.0.1:18792 \
  -L 3035:127.0.0.1:3035 \
  root@89.167.76.6
```

**2. Открываем в браузере:**

`http://localhost:18789/usage`

---

# Шаг 0: смотрим UI OpenClaw

<div class="mt-4 text-gray-300">
Что видим в интерфейсе:
</div>

<v-clicks>

- веб-интерфейс OpenClaw: чаты, задачи, файлы
- как устроена работа с агентом через UI
- где смотреть историю запросов и статусы выполнения
- настройки: модели, инструменты, правила

</v-clicks>

<div class="mt-6 text-sm text-gray-500">
Живое демо - <a href="http://localhost:18789/usage" target="_blank">http://localhost:18789/usage</a>
</div>

---

# Потребление токенов

<div class="mt-4 text-gray-300">
Что важно понимать про расход:
</div>

<v-clicks>

- каждый запрос к LLM тратит токены (input + output)
- контекст агента (файлы, правила, инструменты) - тоже токены
- длинные чаты накапливают контекст и растут в цене
- разные модели - разная стоимость за токен

</v-clicks>

---

# Недельное потребление OpenClaw

<img src="usage_1.png" class="rounded-lg border border-white/10" />

<div class="mt-3 text-sm text-gray-400">
125.7 млн токенов за неделю - активность по дням, разбивка по типам (input/output/cache), список сессий
</div>

---

# Простой чат с агентом

<img src="simple_chat.png" class="mx-auto rounded-lg border border-white/10 h-96" />

---

# Потребление на простой чат

<img src="usage_2.png" class="rounded-lg border border-white/10" />

<div class="mt-3 text-sm text-gray-400">
247.9K токенов на 14 сообщений - system prompt ~31.6K, 21 скилл, 23 инструмента, 8 файлов
</div>

---

# Codex CLI: токены через подписку ChatGPT

<div class="mt-2 grid grid-cols-[1fr_1.2fr] gap-6 items-start">

<div class="text-sm">

<v-clicks>

- **ChatGPT Pro ($200/мес)** - Codex CLI входит в подписку, лимиты на скриншоте
- **ChatGPT Plus ($20/мес)** - достаточно чтобы начать, но при активном использовании расходуется быстро
- Лимиты: 5-часовой и недельный, отдельно для Codex-Spark
- Credits = 0 - все в рамках подписки, докупать не нужно

</v-clicks>

</div>

<img src="codex_usage.png" class="rounded-lg border border-white/10" />

</div>

---

# Как отслеживать расход

<div class="mt-4 grid grid-cols-2 gap-6 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Что смотрим

- дашборд потребления в OpenClaw
- расход по моделям и по задачам
- пиковые запросы и аномалии
- динамика за период

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### На что обращать внимание

- большие контексты = дорогие вызовы
- повторные запросы без результата
- баланс между качеством ответа и стоимостью
- выбор модели под задачу

</div>

</div>

<div class="mt-4 text-sm text-gray-500">
Живое демо: смотрим реальные цифры
</div>

---

# Общий подход к работе

<div class="mt-4 text-gray-300">
Как обычно выстраивается практический процесс:
</div>

<v-clicks>

- работа идет в репозиториях на GitHub
- под задачу создается структура файлов, куда можно регулярно делать context offloading
- в Cursor IDE и Claude Code выполняются сложные задачи
- через OpenClaw удобно вносить небольшие правки на бегу и запрашивать информацию

</v-clicks>

<div class="mt-5 text-sm text-gray-500">
Идея: тяжелую работу делаем в полноценных IDE, а OpenClaw используем как быстрый рабочий интерфейс.
</div>

---

# Кейс 1: туризм и поездки

<div class="mt-4 text-gray-300">
Что автоматизируем:
</div>

<v-clicks>

- сбор вводных по поездке (даты, участники, ограничения)
- чтение структурированных файлов маршрута и документов
- подготовка данных для форм и анкет
- контроль чеклистов по документам и бронированиям
- фиксация изменений в git-репозитории поездок

</v-clicks>

---

# Кейс 1: рабочий сценарий

<div class="mt-4 grid grid-cols-2 gap-6 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Вход

- "Нужно собрать поездку в N"
- "Подготовь данные для формы"
- "Проверь, что не забыли"

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### Действия агента

1. git pull в репозитории поездок
2. чтение AGENTS.md, PERSONS.md и файлов поездки
3. сбор ответа в нужном формате
4. при правках - commit + push

</div>

</div>

<div class="mt-4 text-gray-400 text-sm">
Результат: меньше ручной рутины и ниже риск пропустить важные детали.
</div>

---

# Кейс 1: пример репозитория

<div class="grid grid-cols-[1.6fr_0.9fr] gap-8 items-center mt-6">

<div>

<div class="text-gray-300 text-sm mb-3">
Пример репозитория для планирования поездок и командировок:
</div>

<div class="text-lg leading-snug">
<a
  href="https://github.com/Rai220/my_travel_demo"
  target="_blank"
  class="text-cyan-400 hover:text-cyan-300 underline"
>
  github.com/Rai220/my_travel_demo
</a>
</div>

<div class="mt-5 rounded-lg border border-amber-500/30 bg-amber-900/20 p-4 text-sm text-amber-100">
Все данные в этом репозитории тестовые и не настоящие. Имена, документы, даты, маршруты и бронирования приведены только для демонстрации.
</div>

</div>

<div class="flex flex-col items-center">

<img
  src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https%3A%2F%2Fgithub.com%2FRai220%2Fmy_travel_demo"
  alt="QR-код на репозиторий с примером планирования поездок"
  class="w-44 h-44 rounded-lg bg-white p-2"
/>

<div class="mt-3 text-xs text-gray-400 text-center">
QR-код на пример репозитория
</div>

</div>

</div>

---

# Кейс 1: структура репозитория

<div class="grid grid-cols-2 gap-6 mt-4 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Что лежит в корне

```text
my_travel_demo/
├─ AGENTS.md
├─ PERSONS.md
├─ signatures/
├─ TEMPLATE/
├─ 2026_03_Командировка_Сочи_SnowBase/
├─ 2026_06_Армения/
└─ 2026_10_Португалия_Солнечное_затмение/
```

- `AGENTS.md` - правила и порядок работы с поездками
- `PERSONS.md` - участники, документы, контакты
- `signatures/` - подписи для документов
- отдельные папки - конкретные поездки

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### Из чего состоит шаблон поездки

```text
TEMPLATE/
├─ CORE.md
├─ BOOKINGS.md
├─ CHECKLIST.md
├─ MOVEMENTS.md
├─ PROGRAM.md
└─ docs/
```

- `CORE.md` - вводные, даты, состав, ограничения
- `BOOKINGS.md` - брони, оплаты, статусы, ссылки
- `CHECKLIST.md` - задачи подготовки
- `MOVEMENTS.md` - сегменты маршрута и билеты
- `PROGRAM.md` - план по дням или программа события
- `docs/` - сканы, билеты, ваучеры, подтверждения

</div>

</div>

<div class="mt-4 text-sm text-gray-400">
Шаблон копируется под новую поездку и превращается в отдельную папку-источник правды по маршруту, документам и бронированиям.
</div>

---

# Кейс 1: пример - подпись туристических документов

<div class="grid grid-cols-2 gap-6 mt-4 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Что просим у агента

- "К каким поездкам подойдет моя страховка"
- "Подготовь согласие на выезд"
- "Подставь данные туриста и маршрута"
- "Подпиши PDF эталонной подписью"
- Что осталось сделать по поездке?

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### Что использует агент

```text
PERSONS.md
2026_06_Армения/docs/
signatures/
```

- данные туриста и контакты из `PERSONS.md`
- шаблон документа из папки конкретной поездки
- файл подписи из `signatures/`
- сохранение результата рядом с исходными документами

</div>

</div>

<div class="mt-4 rounded-lg border border-cyan-500/30 bg-cyan-900/15 p-4 text-sm text-cyan-100">
Пример результата: заполненное согласие, анкета на визу или ваучер собираются из данных поездки и подписываются без ручного копирования реквизитов.
</div>

---

# Кейс 2: работа с презентациями

<div class="mt-4 text-gray-300">
Что автоматизируем в Slidev-цикле:
</div>

<v-clicks>

- создание новой презентации по задаче
- синхронизация репозитория перед правками
- правка структуры и содержания слайдов
- экспорт в PDF с корректными фонами
- подготовка коммита и push после подтверждения

</v-clicks>

---

# Кейс 2: что такое Slidev

<div class="mt-6 grid grid-cols-[1.6fr_0.9fr] gap-8 items-start">

<div>

<div class="text-2xl font-semibold text-emerald-300">
Использую <a href="https://sli.dev/" target="_blank">Slidev</a>
</div>

<div class="mt-4 text-gray-300 leading-relaxed">
Slidev - это инструмент для создания презентаций для разработчиков на базе Markdown, Vite и Vue. Слайды удобно хранить в репозитории, быстро править как код, дополнять компонентами и экспортировать в PDF.
</div>

<div class="mt-4 text-sm text-gray-400">
Сайт: <a href="https://sli.dev/" target="_blank">https://sli.dev/</a>
</div>

</div>

<div class="flex flex-col items-center">

<img
  src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https%3A%2F%2Fsli.dev%2F"
  alt="QR-код на сайт Slidev"
  class="w-44 h-44 rounded-lg bg-white p-2"
/>

<div class="mt-3 text-xs text-gray-400 text-center">
QR-код на Slidev
</div>

</div>

</div>

---

# Кейс 2: репозитарий

```bash
cd /root/.openclaw/workspace/slides
git pull --rebase origin "$(git branch --show-current)"
# правки в .md + assets
bunx slidev export <deck.md> --output <deck.pdf> --timeout 60000 --per-slide
git add -A && git commit -m "slides: update deck" && git push
```

<div class="mt-4 text-sm text-gray-400">
Важный принцип: сначала согласование с автором, потом фиксация изменений в git.
</div>

---

# Кейс 2: ценность

<v-clicks>

- быстрее делается черновик и итерации по слайдам
- ниже риск сломать структуру при массовых правках
- прозрачная история изменений для командной работы
- удобно масштабировать на серию вебинаров

</v-clicks>

---

# Кейс 3: документы и подпись

<div class="mt-4 text-gray-300">
Что автоматизируем:
</div>

<v-clicks>

- извлечение данных из репозитория и карточек поездок/объектов
- заполнение шаблонов документов по структуре формы
- подстановка реквизитов и проверка обязательных полей
- автоматическое подписание PDF эталонной подписью
- сохранение финальной версии и фиксация изменений в git

</v-clicks>

---

# Кейс 3: пример потока

<div class="mt-4 grid grid-cols-2 gap-6 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Вход

- "Заполни форму командировки"
- "Собери PDF и подпиши"
- "Проверь, что поля корректны"

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### Действия агента

1. синхронизация репозитория с данными
2. чтение нужных реквизитов и проверка ограничений
3. заполнение шаблона и генерация PDF
4. подписание PDF и сохранение результата
5. commit + push после подтверждения

</div>

</div>

<div class="mt-4 text-gray-400 text-sm">
Результат: меньше ручных ошибок и быстрее подготовка документов к отправке.
</div>

---

# Кейс 3: ценность и контроль

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">

<div class="p-4 rounded-lg bg-blue-900/25 border border-blue-500/30">

### Скорость

Рутинное заполнение и подпись уходят в минуты, а не в долгую ручную сборку.

</div>

<div class="p-4 rounded-lg bg-emerald-900/25 border border-emerald-500/30">

### Точность

Данные берутся из структурированных источников, снижается риск опечаток.

</div>

<div class="p-4 rounded-lg bg-amber-900/25 border border-amber-500/30">

### Аудит

Версионирование и понятный журнал изменений упрощают проверку и откат.

</div>

</div>

---

# Кейс 4: работа с почтой

<div class="mt-4 text-gray-300">
Что уже делается в рабочем контуре:
</div>

<v-clicks>

- мониторинг Gmail по cron каждые 30 минут
- апдейты только по важным письмам, без лишнего шума
- правила коммуникации по отправителям и типам запросов
- обработка вложений (текст, аудио) и подготовка ответа
- контроль статусов писем, чтобы не дублировать действия

</v-clicks>

---

# Кейс 4: пример потока

<div class="mt-4 grid grid-cols-2 gap-6 text-sm">

<div class="p-4 rounded-lg bg-gray-800/60">

### Вход

- "Что важного в почте?"
- "Обработай это письмо и подготовь ответ"
- "Ответь по правилам, но без лишних данных"

</div>

<div class="p-4 rounded-lg bg-gray-800/60">

### Действия агента

1. проверка новых писем по приоритету
2. извлечение сути и вложений
3. черновик или отправка по заданным правилам
4. логирование и обновление статуса треда

</div>

</div>

<div class="mt-4 text-gray-400 text-sm">
Результат: коммуникация быстрее, при этом сохраняются приватность и контроль.
</div>

---

# Кейс 5: веб-автоматизация личных кабинетов

<v-clicks>

- заполнение сложных веб-форм (например, визовые анкеты)
- проверка отпусков и сверка с датами поездок в HR-системах
- поиск данных в кабинетах и перенос в структурированный репозиторий
- работа через Browser Relay с продолжением с места остановки

</v-clicks>

<div class="mt-6 text-sm text-gray-400">
Польза: меньше ручных кликов и ниже риск пропустить обязательные поля.
</div>

---

# Быстрые кейсы, которые не успели показать

<div class="grid grid-cols-2 gap-4 mt-5 text-sm">

<div class="p-4 rounded-lg bg-blue-900/25 border border-blue-500/30">

### Сети и роутер

Подбор доменов сервисов под правила обхода блокировок.

</div>

<div class="p-4 rounded-lg bg-emerald-900/25 border border-emerald-500/30">

### Медиа

Генерация изображений и быстрые креативы для задач и постов.

</div>

<div class="p-4 rounded-lg bg-purple-900/25 border border-purple-500/30">

### Документы

Конвертация файлов и подготовка PDF для отправки.

</div>

<div class="p-4 rounded-lg bg-amber-900/25 border border-amber-500/30">

### Оперативные сводки

Короткие апдейты по почте, задачам и открытым хвостам.

</div>

</div>

---

# Заготовка под новые кейсы

<div class="mt-4 p-5 rounded-lg bg-gray-800/60 border border-white/10">

- Кейс 7: ____________________
- Кейс 8: ____________________
- Кейс 9: ____________________

</div>

---

# Финал

## Что важно унести из части 2

<v-clicks>

- OpenClaw дает практическую пользу на рутинных процессах
- ключ к качеству: правила, память и воспроизводимый workflow
- ценность растет от регулярного использования, а не от одиночного запроса

</v-clicks>

<div class="mt-8 text-sm text-gray-400">
Дальше можно расширять библиотеку кейсов под вашу реальную работу.
</div>
