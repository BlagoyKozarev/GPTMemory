#!/bin/bash
# === GPT-Memory TOP5 Context Generator ===
# Активира top5 контексти за ZeroAPI, VeganMapAI и Health
# Употреба: bash update_top5.sh

set -euo pipefail

echo "=== GPT-Memory TOP5 Context Generator ==="

# Гарантирай canonical локация за ZeroAPI
mkdir -p archives/zeroapi

# 1) Проверка
test -f out/MANIFEST.json || { echo "❌ Липсва out/MANIFEST.json. Пусни: python ingest_folder.py archives && python manifest.py"; exit 1; }

# 2) Създаване на изходна папка
mkdir -p out/top5

echo "📊 Генериране на TOP5 контексти..."

# 3) ZeroAPI контекст с fallback филтри
echo "🔍 ZeroAPI контекст..."
jq -r '
# Филтрираме по категория, path/title pattern и разширения
[.[] | select(
  (.category == "zeroapi") or
  (.uri | test("zero|api"; "i")) or
  (.title | test("zero|api"; "i")) or
  (.tags[]? | test("zero|api"; "i")) or
  (.uri | test("\\.(ts|tsx|js|jsx|md|json|yml|yaml|txt)$"; "i"))
)] |
# Сортираме по категория (zeroapi първо), после по размер
sort_by(if .category == "zeroapi" then 0 else 1 end, -.size) |
# Взимаме първите 5
.[0:5] |
# Форматираме изхода
if length > 0 then
  "=== TOP 5 ZeroAPI Files ===\n" + 
  (to_entries | map(
    "\(.key + 1). \(.value.title) [\(.value.category)] - \(.value.size) bytes\n" +
    "   ID: \(.value.id)\n" +
    "   Path: \(.value.uri)\n" +
    "   Summary: \(.value.summary_short // "No summary")\n"
  ) | join("\n"))
else
  "=== TOP 5 ZeroAPI Files ===\nNo ZeroAPI entries found.\nConsider adding files to archives/zeroapi/ with .ts, .tsx, .js, .jsx, .md, .json, .yml, .yaml, .txt extensions."
end
' out/MANIFEST.json > out/top5/zeroapi.txt

# 4) VeganMapAI контекст
echo "🔍 VeganMapAI контекст..."
jq -r '
[ .[] | select(
    (.category=="veganmapai") or
    (.uri   //"" | test("veganmapai";"i")) or
    (.title //"" | test("veganmapai";"i")) or
    ((.tags //[]) | map(tostring) | join(",") | test("veganmapai";"i"))
  )
]
| sort_by((.updated_at//0), (.size//0)) | reverse | .[:5]
| if length>0 then
    "=== TOP 5 VeganMapAI Files ===\n" +
    ( to_entries | map(
        "\(.key+1). \(.value.title//"untitled") [\(.value.category//"n/a")] - \(.value.size//0) bytes\n" +
        "   ID: \(.value.id//"n/a")\n" +
        "   Path: \(.value.uri//"n/a")\n" +
        "   Summary: \(.value.summary_short // "No summary")\n"
      ) | join("\n") )
  else
    "=== TOP 5 VeganMapAI Files ===\nNo VeganMapAI entries found."
  end
' out/MANIFEST.json > out/top5/veganmapai.txt

# 5) Health контекст
echo "🔍 Health контекст..."
jq -r '
[ .[] | select(
    (.category=="health") or
    (.uri   //"" | test("health";"i")) or
    (.title //"" | test("health";"i")) or
    ((.tags //[]) | map(tostring) | join(",") | test("health";"i"))
  )
]
| sort_by((.updated_at//0), (.size//0)) | reverse | .[:5]
| if length>0 then
    "=== TOP 5 Health Files ===\n" +
    ( to_entries | map(
        "\(.key+1). \(.value.title//"untitled") [\(.value.category//"n/a")] - \(.value.size//0) bytes\n" +
        "   ID: \(.value.id//"n/a")\n" +
        "   Path: \(.value.uri//"n/a")\n" +
        "   Summary: \(.value.summary_short // "No summary")\n"
      ) | join("\n") )
  else
    "=== TOP 5 Health Files ===\nNo Health entries found."
  end
' out/MANIFEST.json > out/top5/health.txt

# 6) Показваме резултатите
echo ""
echo "✅ Генериране завършено!"
echo "📁 Файлове създадени в out/top5/:"
ls -la out/top5/

echo ""
echo "📊 Статистика:"
echo "ZeroAPI записи: $(grep -c "^[0-9]\." out/top5/zeroapi.txt 2>/dev/null || echo "0")"
echo "VeganMapAI записи: $(grep -c "^[0-9]\." out/top5/veganmapai.txt 2>/dev/null || echo "0")"
echo "Health записи: $(grep -c "^[0-9]\." out/top5/health.txt 2>/dev/null || echo "0")"

echo ""
echo "💡 Ръчно използване: bash update_top5.sh"
echo "📄 Прегледай файловете: cat out/top5/zeroapi.txt"