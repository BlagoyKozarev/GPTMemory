import argparse
import json
from pathlib import Path
from datetime import datetime
import re

# Константи
db_path = Path('out/MANIFEST.json')

def validate_date(date_string):
    """Валидира формата на датата (YYYY-MM-DD)."""
    if not date_string:
        return True
    
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_tags(tags_string):
    """Валидира и нормализира тагове."""
    if not tags_string:
        return []
    
    # Разделяне по запетая и почистване
    tags = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
    
    # Валидация - само букви, цифри, тире и долни черти
    valid_tags = []
    for tag in tags:
        if re.match(r'^[a-zA-Z0-9_-]+$', tag):
            valid_tags.append(tag.lower())
        else:
            print(f"⚠️  Невалиден таг '{tag}' - разрешени са само букви, цифри, тире и долни черти")
    
    return valid_tags

def main():
    """Основна функция за обновяване на метаданни на документ."""
    
    # Настройка на аргументи
    ap = argparse.ArgumentParser(
        description='Обновява метаданните на документ в MANIFEST.json',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примери за употреба:
  python update_summary.py --id abc123def456 --summary "Обновено резюме"
  python update_summary.py --id abc123def456 --category marketing --tags "план,Q3,бизнес"
  python update_summary.py --id abc123def456 --date "2024-03-15"
  python update_summary.py --id abc123def456 --summary "Пълно резюме" --category health --tags "здраве,данни" --date "2024-03-15"
        """
    )
    
    ap.add_argument('--id', required=True, 
                   help='ID на документа за обновяване (12-символен префикс от SHA256)')
    ap.add_argument('--summary', required=False, default=None,
                   help='Ново кратко резюме на документа')
    ap.add_argument('--category', required=False, default=None,
                   choices=['veganmapai', 'health', 'marketing', 'screens', 'logs', 'general'],
                   help='Нова категория на документа')
    ap.add_argument('--tags', required=False, default=None,
                   help='Тагове разделени със запетая (например: "plan,Q3,business")')
    ap.add_argument('--date', required=False, default=None,
                   help='Дата във формат YYYY-MM-DD (например: "2024-03-15")')
    
    args = ap.parse_args()

    # Проверка дали MANIFEST.json съществува
    if not db_path.exists():
        print("❌ MANIFEST.json не е намерен.")
        print("🔄 Изпълнете първо: python ingest_folder.py archives")
        return

    # Валидация на входните данни
    if args.date and not validate_date(args.date):
        print("❌ Невалиден формат на дата. Използвайте YYYY-MM-DD (например: 2024-03-15)")
        return

    try:
        # Зареждане на базата данни
        with open(db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)

        # Търсене на документа по ID
        hit = None
        for r in db:
            if r.get('id') == args.id:
                hit = r
                break

        if not hit:
            print(f"❌ Документ с ID '{args.id}' не е намерен.")
            print(f"💡 Съвет: Проверете списъка с ID-та в MANIFEST.csv или използвайте:")
            print(f"   python manifest.py")
            return

        # Показване на текущите данни
        print(f"📄 Намерен документ: {hit.get('title', 'Без заглавие')}")
        print(f"📁 Текуща категория: {hit.get('category', 'Няма')}")
        print(f"🏷️  Текущи тагове: {', '.join(hit.get('tags', [])) or 'Няма'}")
        print(f"📅 Текуща дата: {hit.get('date', 'Няма')}")
        print(f"📝 Текущо резюме: {hit.get('summary_short', 'Няма')[:100]}...")

        # Обновяване на данните
        changes_made = []
        
        if args.summary is not None:
            old_summary = hit.get('summary_short', '')
            hit['summary_short'] = args.summary
            changes_made.append(f"резюме обновено ({len(old_summary)} → {len(args.summary)} символа)")

        if args.category is not None:
            old_category = hit.get('category', 'няма')
            hit['category'] = args.category
            changes_made.append(f"категория: {old_category} → {args.category}")

        if args.tags is not None:
            old_tags = hit.get('tags', [])
            new_tags = validate_tags(args.tags)
            hit['tags'] = new_tags
            changes_made.append(f"тагове: {old_tags} → {new_tags}")

        if args.date is not None:
            old_date = hit.get('date', 'няма')
            hit['date'] = args.date
            changes_made.append(f"дата: {old_date} → {args.date}")

        if not changes_made:
            print("⚠️  Няма промени за прилагане.")
            return

        # Запазване на обновената база данни
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Документ '{args.id}' е обновен успешно!")
        print("🔄 Промени:")
        for change in changes_made:
            print(f"  • {change}")
        
        print(f"\n💡 Съвет: Изпълнете 'python manifest.py' за обновяване на CSV файла")

    except Exception as e:
        print(f"❌ Грешка при обновяване: {e}")
        return

if __name__ == '__main__':
    main()
