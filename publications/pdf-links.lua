-- Show links to PDF files in the bibliography as "PDF" instead of the full URL.
-- Must run after citeproc (see the filters list in index.qmd).
function Link(el)
  if el.target:match("%.pdf$") then
    el.content = { pandoc.Str("PDF") }
  end
  return el
end
