# Render the website, then each book into _site/books/<slug>/.  Run from the website folder in PowerShell.
# Requires Quarto (https://quarto.org/docs/get-started/) and, for the book's Python chunks, Python with numpy + jupyter.
$ErrorActionPreference = "Stop"
quarto render
Get-ChildItem -Directory books-src | ForEach-Object {
    Write-Host "Rendering book: $($_.Name)"
    quarto render $_.FullName --to html
    quarto render $_.FullName --to pdf      # comment out if no LaTeX installed (quarto install tinytex gives you one)
}
Write-Host "Done. Preview with:  quarto preview   (website)   or open _site/index.html"
