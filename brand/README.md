# Scoo — brand and homepage prototype

Working files for the Scoo consumer brand: the logo and its history, and the
single-screen homepage prototype. Nothing here is wired to the router; it is
design source, kept so later changes start from what was decided.

## Logo

`logo/final/` holds the current mark as standalone SVGs:

| file | use |
| --- | --- |
| `mark-light.svg` | ink lines, coral smile, for light backgrounds |
| `mark-dark.svg` | light lines, coral smile, for dark backgrounds |
| `mark-mono-black.svg`, `mark-mono-coral.svg` | single colour |
| `app-icon.svg` | white mark on a coral rounded square |
| `favicon.svg` | heavier lines so it reads at tab size |

The mark spells the name as a face: the two round lenses are the **o o**, a
short bridge joins them, and one stroke between them is the **s** — it curls
right at the top, crosses the bridge, and its tail sweeps left into the coral
smile, the **c**. Colours: ink `#111111`, coral `#FF6B4A` (`#FF7A5C` on dark).

`logo/versions/` keeps every round, each as a sheet (`.html`, open in a browser)
and a rendered `.png`, so an earlier idea can be picked back up:

| version | idea |
| --- | --- |
| v01 heavy face | first take: thick lines, letters as a face |
| v02 light sketch | the hand sketch, redrawn in light single-weight lines |
| v03 proper s and c | real letterforms for the s nose and c mouth |
| v04 round ƒ bridge | round lenses, the stroke read as ƒ ("function of"), long bridge |
| v05 seamless oso | one unbroken line: o, s-curve, o |
| v06 ƒ stroke = nose + smile | one stroke is hook, nose and smile; squircle lenses |
| v07–v09 | round lenses, hook right, smile curling left; then short bridge; then bigger smile |
| v10 wide gap, full s | **current** — wider lens spacing so the s can curve fully |

## Homepage stills

`homepage/` keeps screenshots of the early homepage prototype (the street, the
falling pros and the agent conversation). The live homepage is
`src/routes/+page.svelte`.
