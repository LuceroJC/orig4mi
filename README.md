# Folded Geometry — site source

A Quarto website (blog, reviews, publications, books hub) plus one Quarto book project per online book.

## Layout
```
_quarto.yml            site configuration (title, navbar, theme)
index.qmd              home page (lists latest posts)
about.qmd  disclosure.qmd
_affiliate-note.qmd    include at the top of any post with affiliate links: {{< include /_affiliate-note.qmd >}}
blog/                  one folder per post: blog/YYYY-MM-DD-slug/index.qmd
reviews/books/         book reviews (table listing with author, rating, level)
reviews/products/      product reviews (grid listing with image and rating)
publications/          index.qmd renders publications.bib; PDFs go in pdfs/<bibkey>.pdf
books/index.qmd        hub page linking the online books
books-src/<slug>/      one Quarto *book* project per book; renders into _site/books/<slug>/
build.ps1  build.sh    render everything in the right order
```

## First run
1. Install Quarto: https://quarto.org/docs/get-started/  (and `quarto install tinytex` for PDF output).
2. For the book's Python chunks: `pip install numpy jupyter` (or disable execution with `execute: enabled: false` in the book's `_quarto.yml`).
3. In this folder: `quarto preview` for the website alone, or `.\build.ps1` for site + books.

## Publishing
- Put the source in a GitHub repository (public or private).
- Host on Cloudflare Pages or Netlify (build command: `./build.sh`, output: `_site`), with a custom domain.
  GitHub Pages works too but its terms discourage commercial (affiliate) sites.
- Set `site-url` in `_quarto.yml` to the real domain so RSS feeds and the sitemap are correct.
- Replace `YOURTAG-20` in affiliate links with your Amazon Associates tag; the disclosure page must match the programmes you join.

## Adding content
- Blog post: copy `blog/2026-11-19-why-this-site/`, rename, edit the YAML and text.
- Review: copy a folder under `reviews/books/` or `reviews/products/`; remove `draft: true` to publish.
- Paper: add a BibTeX entry to `publications/publications.bib` and the PDF as `publications/pdfs/<key>.pdf`.
- Book chapter: add a `.qmd` to `books-src/<slug>/` and list it under `chapters:` in that book's `_quarto.yml`.
