# The Wall — wall.lkn-law.com

An interactive remembrance of the 58,280 names on the Vietnam Veterans Memorial, published by The Lake Norman Brief (lkn-law.com).

Every push to `main` rebuilds the site with GitHub Actions (`.github/workflows/build.yml`) and publishes it to GitHub Pages.

- `records.json.gz` — cleaned records from the National Archives' Vietnam Conflict Extract Data File (NAID 2240992, as of April 29, 2008). Social Security numbers, race, religion and marital status are excluded. Rebuild it from the NARA file with `clean.py` if needed.
- `additions.json`, `vvmf_adds.tsv`, `adds_src.txt` — names added to the Wall after 2008.
- `panel_fixes.json`, `vvmf_fix.tsv` — panel/line corrections.
- `gen.py`, `ranks.py`, `additions.py` — site generator.
- `style.css`, `wall.js` — site assets.
- `stories/<slug>.html` — optional written story for a name page (marks the page "Story").
- `photos/<slug>.json` — optional rights-cleared photo for a name page.
