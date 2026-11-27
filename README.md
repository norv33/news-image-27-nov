# The World — 27 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261127)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261127-orange)](https://make.fun/bounty/news-image-20261127)
[![make.fun](https://img.shields.io/badge/make.fun-Friday%2027%20November%202026-green)](https://make.fun/bounty/news-image-20261127)

A morning-edition front page summing up the world's news of **Friday, 27 November 2026** in one image: a sunrise masthead, six headline stories from six regions and fields, and an "ALSO TODAY" strip. The image is drawn from scratch with Python (PIL primitives only — no photos, no clipart, no copied artwork) and copied to `/output/entry.png` by a small Node 22 program (`main.ts`, standard library only).

Entry for the make.fun bounty: https://make.fun/bounty/news-image-20261127

## The six stories

1. **Drone strike in Kuwait kills two Italians** — Iran denies responsibility for the attack. *(BBC, The New York Times, NDTV)*
2. **Thanksgiving storm halts Macy's parade** — Flights cancelled; 500,000 homes lose power. *(BBC)*
3. **Zelenskyy: US must push Russia harder** — Warns Moscow may strike Ukraine's power grid again. *(BBC)*
4. **Israel kills 10 in Gaza; Hamas weighs reply** — Ceasefire strained as mediators urge restraint. *(Reuters)*
5. **UK net migration lowest since 1997** — Lowest level outside the pandemic years. *(The New York Times)*
6. **Gukesh–Sindarov draw in marathon Game 3** — Still level after three games in the World Chess Championship final. *(India Today)*

Also today: a diesel tanker capsizes off Ibiza (one dead, BBC); Gérard Depardieu is to stand trial over an alleged 2018 rape (BBC); Black Friday brings bigger discounts (Salesforce); Lille hand Bayern Munich their first defeat of the season.

All stories are events that happened, or were first reported, on 27 November 2026.

## How to run

```sh
python3 draw.py          # redraw entry.png (1024 x 1024, PNG, under 1 MiB)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts   # validate + copy entry.png to out/entry.png
```

`main.ts` checks the PNG signature, the IHDR chunk, the 1024×1024 size, the 1 MiB cap and the IEND chunk, then copies the file atomically (temp file + rename). Running it twice writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
