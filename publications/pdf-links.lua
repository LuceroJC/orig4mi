-- Builds the publication list itself, then shows links to PDF files as "PDF"
-- instead of the full URL.
--
-- Why the filter runs citeproc itself: Quarto runs the citation processor
-- after all user filters, so a filter would never see the finished list.
-- Here we build the list, relabel the links, and then stop the later
-- citeproc pass from rebuilding it (no 'nocite', bibliography suppressed,
-- and the list's div renamed so citeproc doesn't refill it).

local function relabel(el)
  if el.target:match("%.pdf$") then
    el.content = { pandoc.Str("PDF") }
  end
  return el
end

function Pandoc(doc)
  doc = pandoc.utils.citeproc(doc)
  doc = doc:walk({
    Div = function(div)
      if div.identifier == "refs" then
        div.identifier = "publication-list"
        return div:walk({ Link = relabel })
      end
    end
  })
  doc.meta.nocite = nil
  doc.meta["suppress-bibliography"] = true
  return doc
end
