# Photo cut-outs — the only generated images

Code draws every paper layer, edge, halftone, sky, strip, transition and letter. Generate an image only when code cannot fake it convincingly: **photographic objects** (cameras, cars, planes, devices, props, animals, plants, rocks, clouds, grass texture). Never generate whole backgrounds/plates, people or AI characters unless the user explicitly asks.

## Generation (Higgsfield connector)
- Tool: `generate_image_batch` (up to 12 per call), model `nano_banana_pro`, `aspect_ratio: "16:9"`, `resolution: "2k"`. ~2 credits each, ~1 min per batch. Poll with `jobs_wait`.
- Download: `curl -sSL --fail --retry 4 -o keyframes/raw/<name>.png <result_url>`.
- Several small objects can share one sheet ("four separate … in a 2x2 grid with generous green space, they do not touch") — the keyer splits them.

### Prompt template (single object)
> Photographic cut-out sticker of **{object, view, details}**, with a rough hand-cut white paper border about 2 percent of the width, slight halftone print texture, isolated on a perfectly flat pure green background (#00FF00), no shadow on the background, nothing else in frame. No text, no letters, no logos.

Add "no numbers" for vehicles; "blank slate (no writing)" for clapperboards; "screen a flat pastel sky gradient, nothing readable" for laptops; "screen completely flat pure black (screen off)" for phones.

### Set used in the kaye.creatives film (names = file names in cutouts/)
| name | object |
|---|---|
| cam_side | vintage silver-and-black Super 8 film camera, 3/4, slightly tilted |
| cam_front | same camera, front 3/4, big round lens prominent (iris lens centre ≈ (400,605) of a 1448×1192 sprite, r ≈ 228) |
| car | sleek pastel-pink open-wheel race car, 3/4 front, diagonal, no logos/numbers |
| helmet | glossy white-and-pink full-face racing helmet, dark visor |
| phone | sleek smartphone straight from the front, flat black glossy screen (came out landscape) |
| plane_front | vintage pastel-blue biplane flying toward camera, 3/4 front, propeller blurred |
| plane_side | same biplane, clean side view flying right |
| clap | open black-and-white clapperboard, blank slate |
| reel | vintage metal film reel with a curl of film strip |
| laptop | open silver laptop 3/4, screen = flat pastel sky with pink clouds |
| headphones, midi, phone_gimbal, cassette | one 2×2 sheet: white/silver headphones · 25-key MIDI keyboard with pads · phone on a black gimbal · cassette with blank pink label |
| rocks_a/b/c, tree_a/b, grass_strip | one sheet: long torn strip of photo savanna grass + 3 b/w rock cut-outs + 2 acacia tree cut-outs |
| cloud_1..4 | one sheet: four b/w halftone cumulus cut-outs |

## Keying → alpha PNGs
`tools/greenkey <in.png> <out_prefix> [minAreaFrac=0.002]`
- alpha from greenness `g − max(r,b)`: > 90 → transparent, 25…90 → ramp; hard cut for g>160 & r,b<110; despill (green pulled down to max(r,b)).
- splits connected components (4× downscaled mask, 8-neighbour), sorts them top→bottom/left→right, writes `<prefix>.png` (one piece) or `<prefix>_1.png, _2.png …`, tight crop + 6 px pad, prints JSON with sizes.
- Then rename pieces to meaningful names and write `cutouts.txt` (`name w h`).
- Check them on a coloured background (red + striped cyan) before use: the white paper border must be clean, no green fringe.

`CL.img(name)` loads `../cutouts/<name>.png`; `CL.preload()` warms all of them (list them in collage.js if you add new names, or load on demand).
