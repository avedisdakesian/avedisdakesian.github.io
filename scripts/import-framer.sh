#!/usr/bin/env bash
# One-time import: saves the live Framer pages and every file they use
# (images, videos, fonts) into framer-export/, so the rebuild doesn't depend on Framer.
set -euo pipefail

OUT="framer-export"
mkdir -p "$OUT/pages" "$OUT/assets"

declare -A PAGES=(
  [home]="https://avedisdakesian-home.framer.website/"
  [second-caller]="https://secondcaller-avedisdakesian.framer.website/"
  [woods-center]="https://avedisdakesian-woodscenter.framer.website/"
)

for name in "${!PAGES[@]}"; do
  echo "Fetching $name"
  curl -fsSL "${PAGES[$name]}" -o "$OUT/pages/$name.html"
done

# Every framerusercontent file referenced by the pages (query strings dropped).
grep -ohE 'https://framerusercontent\.com/(images|assets|third-party-assets)/[^"'"'"' )?&,\\]+' "$OUT"/pages/*.html \
  | sort -u > "$OUT/asset-urls.txt"

while read -r url; do
  file="$OUT/assets/$(basename "$url")"
  [ -f "$file" ] || curl -fsSL "$url" -o "$file" || echo "failed: $url"
done < "$OUT/asset-urls.txt"

echo "Saved $(ls "$OUT/assets" | wc -l) files"
