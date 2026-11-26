#!/usr/bin/env bash
# Build script for Cloudflare (Workers/Pages Git integration).
# The build image has no Quarto, so fetch the latest release first.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v quarto >/dev/null 2>&1; then
  echo "Installing Quarto..."
  mkdir -p /tmp/quarto
  curl -fsSL https://quarto.org/download/latest/quarto-linux-amd64.tar.gz \
    | tar xz -C /tmp/quarto --strip-components=1
  export PATH="/tmp/quarto/bin:$PATH"
fi
quarto --version

quarto render
# Books: computed chunks must be pre-rendered locally and committed in _freeze/
# (execute: freeze: auto). No Python/Jupyter here, so never execute on the server.
for b in books-src/*/; do
  echo "Rendering book (HTML only): $b"
  quarto render "$b" --to html \
    || { echo "Book $b failed — did you commit its _freeze/ folder?"; exit 1; }
done
bash ./fix-urls.sh _site
echo "Build finished: _site/"
