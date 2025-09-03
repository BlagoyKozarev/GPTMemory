import json
from pathlib import Path
import pandas as pd
from tools import format_file_size

# Константи
OUT = Path('out')
OUT.mkdir(parents=True, exist_ok=True)
db_path = OUT / 'MANIFEST.json'
csv_path = OUT / 'MANIFEST.csv'

def main():
    """Конвертира MANIFEST.json в CSV формат с подредени данни."""
    
    if not db_path.exists():
        print("❌ Няма MANIFEST.json файл.")
        print("🔄 Изпълнете първо: python ingest_folder.py archives")
        return

    try:
        # Зареждане на данните
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("⚠️  MANIFEST.json е празен.")
            return

        print(f"📊 Зареждам {len(data)} записа от MANIFEST.json...")

        # Сортиране по категория и заглавие
        data = sorted(data, key=lambda r: (r.get('category', ''), r.get('title', '')))

        # Подготовка на данните за DataFrame
        processed_data = []
        for record in data:
            # Обработка на тагове - конвертиране в string
            tags = record.get('tags', [])
            if isinstance(tags, list):
                tags_str = ','.join(tags) if tags else ''
            else:
                tags_str = str(tags)

            processed_record = {
                "id": record.get('id', ''),
                "title": record.get('title', ''),
                "category": record.get('category', ''),
                "tags": tags_str,
                "date": record.get('date', ''),
                "uri": record.get('uri', ''),
                "size": record.get('size', 0),
                "size_formatted": format_file_size(record.get('size', 0)),
                "sha256": record.get('sha256', ''),
                "summary_short": record.get('summary_short', '')
            }
            processed_data.append(processed_record)

        # Създаване на DataFrame
        df = pd.DataFrame(processed_data, columns=[
            "id", "title", "category", "tags", "date", "uri", 
            "size", "size_formatted", "sha256", "summary_short"
        ])

        # Запазване в CSV с правилно кодиране
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')

        # Статистики по категории
        category_stats = df['category'].value_counts()
        total_size = df['size'].sum()

        print(f"✅ CSV файлът е генериран успешно: {csv_path}")
        print(f"📁 Общо записи: {len(df)}")
        print(f"💾 Общ размер: {format_file_size(total_size)}")
        
        print(f"\n📊 Разпределение по категории:")
        for category, count in category_stats.items():
            category_size = df[df['category'] == category]['size'].sum()
            print(f"  • {category}: {count} файла ({format_file_size(category_size)})")

        print(f"\n📄 CSV файл с колони: {', '.join(df.columns)}")
        
    except Exception as e:
        print(f"❌ Грешка при генериране на CSV: {e}")
        return

if __name__ == '__main__':
    main()
