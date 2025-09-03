# GPT-Memory
Каталог и резюмета за документи от много проекти/чатове.
- Внася zip/папки в `archives/`
- Генерира MANIFEST.json/CSV в `out/`
- Поддържа категории и кратки резюмета

## Бърз старт
1) Качи файлове в `archives/`
2) `python ingest_folder.py archives`
3) `python manifest.py`
4) (по желание) `python update_summary.py --id <doc_id> --summary "..." --category marketing --tags "plan,Q3"`

## ZeroAPI exports
Всички файлове, свързани със ZeroAPI, се съхраняват в `archives/zeroapi/`. Поддържани формати: .ts, .tsx, .js, .jsx, .md, .json, .yml, .yaml, .txt.

## Daily run
Изпълни `bash update_top5.sh` след индексиране, преди да започнеш нов GPT чат. Копирай контекста от `out/top5/zeroapi.txt`, `out/top5/veganmapai.txt`, `out/top5/health.txt`.

## Файлова структура
