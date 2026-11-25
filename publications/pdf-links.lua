-- Show links to PDF files in the bibliography as "PDF" instead of the full URL.
-- Runs at "post-render" (see index.qmd), after the bibliography has been built.
function Link(el)
  if el.target:match("%.pdf$") then
    el.content = { pandoc.Str("PDF") }
  end
  return el
end
