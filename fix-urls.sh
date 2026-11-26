#!/usr/bin/env bash
# Post-build SEO fix for Cloudflare's clean URLs.
# Cloudflare serves /about.html as /about and /x/index.html as /x/ (redirecting the
# .html forms), but Quarto writes .html URLs into sitemap.xml and adds no canonical tag.
# This script (1) rewrites every sitemap.xml under _site to the clean URLs and
# (2) adds <link rel="canonical"> with the clean https://orig4mi.com URL to each page.
set -euo pipefail
SITE="${1:-_site}"
BASE="https://orig4mi.com"

find "$SITE" -name sitemap.xml -print0 | while IFS= read -r -d '' f; do
  sed -i -E 's#/index\.html</loc>#/</loc>#g; s#\.html</loc>#</loc>#g' "$f"
done

find "$SITE" -name '*.html' -print0 | while IFS= read -r -d '' f; do
  rel="${f#$SITE/}"
  [ "$rel" = "404.html" ] && continue
  grep -qE 'http-equiv="refresh"|<title>Redirect</title>' "$f" && continue   # alias/redirect stubs
  grep -q 'rel="canonical"' "$f" && continue
  case "$rel" in
    index.html) clean="/";;
    */index.html) clean="/${rel%index.html}";;
    *.html) clean="/${rel%.html}";;
  esac
  sed -i "0,/<\/head>/s#</head>#<link rel=\"canonical\" href=\"$BASE$clean\">\n</head>#" "$f"
done
echo "Canonical tags and sitemap URLs cleaned in $SITE/"
