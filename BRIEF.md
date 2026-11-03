# Vietnam Wall project (lkn-law.com) — brief
Decisions (Chris, 2026-11-02):
- Host interactive Wall + 58,281 name profiles at wall.lkn-law.com (static site), linked both ways with WP hub 924111.
- Facts from official DoD data; every profile deep-links to VVMF Wall of Faces; do NOT copy VVMF photos/remembrances.
- Photos only when rights-cleared: public-domain official portraits, or family submissions with consent checkbox + Chris approval before display.
- Remembrance: candles + "share a photo or memory" form, moderated by Chris.
- Design: scrollable panorama of the whole black-granite wall (1E apex -> 70E, 70W -> 1W apex), names glow gold on hover, click -> profile.
- Never invent stories; "Service record" vs "Story" labels. Written stories later (MoH, NC/LKN, 8 women).
- No VVMF permission letter for now.
Data source: NARA NAID 2240992 "Vietnam Conflict Extract Data File, as of April 29, 2008"
  https://catalog.archives.gov/medialz/electronic-records/rg-330/dcase/DCAS.VN.EXT08.DAT (24.4 MB, pipe-delimited, 55 fields, 58,220 rows, Use: Unrestricted)
  docs: DCAS.VN08.DOC.PDF, 103.2DP.pdf (same folder)
  Field idx: 0 SSN (NEVER publish) | 3 component (SELECTED SERVICE = draftee) | 4 name | 6 service | 7 rank | 8 paygrade | 9 MOS | 10 MOS desc | 11 birth yyyymmdd | 12 sex | 13 city | 14 county | 16 state | 18 marital | 19 religion | 21/23 race (exclude 18-24) | 26 province | 30 country | 31 unit | 33 incident date | 34 death date | 42 H/NH | 44 category | 45 reason | 47 body recovered | 49 panel/line e.g. "63W 014"
  Stats: KIA 40,934; DOW 5,299; accident 9,107; declared dead 1,201; presumed dead 123; illness 938; self-inflicted 382; homicide 236. Army 38,224, USMC 14,844, USAF 2,586, USN 2,559, USCG 7. Women 8. NC 1,613. Body not recovered 1,741.
  Panel/line present on 58,188; 9 malformed (e.g. "5E  002", "48W"), ~23 blank -> fix by hand. 140 panels; 1E 132 lines (prologue on top), 2E/2W 137 lines max, 70E/70W 1 line (5 names).
  Gap: 58,281 on Wall in 2026 vs 58,220 in 2008 file -> add later additions from VVMF annual name-addition lists.
Blocker: cloud sandbox cannot reach archives.gov (proxy 403); browser can, but tool output can't carry 24 MB.
