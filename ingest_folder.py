import sys
import os
import json
from pathlib import Path
from tqdm import tqdm
from tools import (
    file_iter, sha256_of_file, short_id, guess_category, 
    norm_title, summarize_placeholder, validate_file_path, format_file_size
)

def main():
    """Основна функция за индексация на файлове от дадена папка."""
    if len(sys.argv) < 2:
        print("Употреба: python ingest_folder.py <папка>")
        print("Пример: python ingest_folder.py archives")
        sys.exit(1)

    root_path = sys.argv[1]
    root = Path(root_path).resolve()
    
    if not root.exists():
        print(f"Грешка: Папката '{root}' не съществува.")
        sys.exit(1)
    
    if not root.is_dir():
        print(f"Грешка: '{root}' не е папка.")
        sys.exit(1)

    # Създаване на изходна папка
    out_dir = Path('out')
    out_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = out_dir / 'MANIFEST.json'
    db = []

    # Зареждане на съществуващи данни
    if db_path.exists():
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
            print(f"Заредени {len(db)} съществуващи записа от MANIFEST.json")
        except Exception as e:
            print(f"Грешка при четене на MANIFEST.json: {e}")
            print("Започвам с празна база данни.")
            db = []

    # Създаване на речник за бърз достъп по SHA256
    by_sha = {r.get('sha256'): r for r in db if r.get('sha256')}

    # Събиране на всички файлове за обработка
    all_files = list(file_iter(root))
    print(f"Намерени {len(all_files)} файла за обработка в '{root}'")

    added = 0
    skipped = 0
    errors = 0

    # Обработка на файловете с прогрес бар
    for p in tqdm(all_files, desc="Обработка на файлове"):
        try:
            if not validate_file_path(p):
                errors += 1
                continue
                
            sha = sha256_of_file(p)
            if not sha:  # Грешка при четене на файла
                errors += 1
                continue
                
            if sha in by_sha:
                skipped += 1
                continue

            # Създаване на нов запис
            rec = {
                "id": short_id(sha),
                "title": norm_title(p.name),
                "category": guess_category(p),
                "tags": [],
                "date": None,
                "uri": str(p.as_posix()),
                "size": p.stat().st_size,
                "sha256": sha,
                "summary_short": summarize_placeholder(p)
            }
            
            db.append(rec)
            by_sha[sha] = rec
            added += 1

        except Exception as e:
            print(f"\nГрешка при обработка на '{p}': {e}")
            errors += 1

    # Запазване на обновената база данни
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Индексацията завърши успешно!")
        print(f"📁 Нови файлове: {added}")
        print(f"⏭️  Пропуснати (дубликати): {skipped}")
        print(f"❌ Грешки: {errors}")
        print(f"📊 Общо записи в базата: {len(db)}")
        print(f"💾 MANIFEST.json записан в: {db_path}")
        
        if added > 0:
            print(f"\n🔄 Следваща стъпка: python manifest.py (за генериране на CSV)")
            
    except Exception as e:
        print(f"\n❌ Грешка при запазване на MANIFEST.json: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
