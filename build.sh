#!/usr/bin/env bash
# Render the website, then each book into _site/books/<slug>/.
set -euo pipefail
cd "$(dirname "$0")"
quarto render
for b in books-src/*/; do
  echo "Rendering book: $b"
  quarto render "$b" --to html
  quarto render "$b" --to pdf   # comment out if no LaTeX installed (quarto install tinytex)
done
bash ./fix-urls.sh _site
echo "Done. Open _site/index.html or run: quarto preview"
