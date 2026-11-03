# The Wall — wall.lkn-law.com

Every name on the Vietnam Veterans Memorial, published by The Lake Norman Brief (Adkins Law, PLLC).

The site is built automatically by GitHub Actions (`.github/workflows/pages.yml`):
it downloads the Department of Defense Vietnam casualty file from the National Archives
(NAID 2240992), runs `clean.py`, `additions.py` (names added to the Wall since 2008, from
`vvmf_adds.tsv`, and panel/line fixes from `vvmf_fix.tsv`) and `gen.py`, then deploys to GitHub Pages.

Researched stories: add `stories/<slug>.html`. Rights-cleared photos: add `photos/<slug>.json`
(`{"src": "...", "credit": "..."}`). Service numbers, race, religion and marital status from the
federal file are never published.
