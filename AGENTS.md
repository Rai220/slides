Здесь собраны презентации созданные с использованием slidev
Используй скилл slidev для работы с презентациями
Для запуска используй bunx slidev

При создании новой презентации всегда добавляй в её папку файл `vite.config.ts` с содержимым:
```ts
import { defineConfig } from 'vite'

export default defineConfig({
  publicDir: '../public',
})
```
Это необходимо для доступа к общим ресурсам из папки `public/` (фото, QR-коды и т.д.).

Для выгрузки в PDF используй:
```bash
bunx slidev export <путь к md> --output <путь к pdf> --timeout 60000 --per-slide
```
Флаг `--per-slide` обязателен — без него фон может обрезаться на последних слайдах.