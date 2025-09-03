import os
import hashlib
import json
import re
from pathlib import Path

# Разрешени файлови разширения
ALLOWED_EXT = {
    '.txt','.md','.pdf','.doc','.docx','.xlsx','.xls','.csv','.json','.ppt','.pptx',
    '.zip','.png','.jpg','.jpeg','.webp',
    '.js','.ts','.tsx','.jsx','.css','.scss','.yml','.yaml','.toml','.env','.sh'
}

def norm_title(name: str) -> str:
    """Нормализира заглавието на файл - премахва разширението и подобрява форматирането."""
    return re.sub(r'\s+', ' ', re.sub(r'[_-]+', ' ', Path(name).stem)).strip()

def sha256_of_file(path: Path) -> str:
    """Изчислява SHA256 хеш на файл."""
    h = hashlib.sha256()
    try:
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(1024*1024), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"Грешка при четене на файл {path}: {e}")
        return ""

def short_id(sha256: str) -> str:
    """Генерира кратко ID от SHA256 хеш (първите 12 символа)."""
    return sha256[:12]

def guess_category(p: Path) -> str:
    """Автоматично определя категорията на файл въз основа на пътя и името."""
    s = str(p).lower()
    
    if 'veganmap' in s or 'vegan' in s:
        return 'veganmapai'
    if 'health' in s or 'здрав' in s:
        return 'health'
    if 'market' in s or 'business' in s or 'бизнес' in s:
        return 'marketing'
    if 'screen' in s or 'screenshot' in s:
        return 'screens'
    if 'log' in s or 'oauth' in s:
        return 'logs'
    
    return 'general'

def file_iter(root: Path):
    """Итерира през всички разрешени файлове в дадена директория."""
    try:
        for p in root.rglob('*'):
            if p.is_file() and p.suffix.lower() in ALLOWED_EXT:
                yield p
    except Exception as e:
        print(f"Грешка при обхождане на директория {root}: {e}")

def summarize_placeholder(path: Path, max_chars=600):
    """Генерира автоматично резюме за файл."""
    try:
        size = path.stat().st_size
        return f"Автоматично резюме: {norm_title(path.name)} ({path.suffix.lower()}) — размер {size} B."
    except Exception as e:
        return f"Грешка при достъп до файл: {e}"

def format_file_size(size_bytes: int) -> str:
    """Форматира размера на файл в четим вид."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def validate_file_path(path: Path) -> bool:
    """Проверява дали файловият път е валиден и достъпен."""
    try:
        return path.exists() and path.is_file()
    except Exception:
        return False
