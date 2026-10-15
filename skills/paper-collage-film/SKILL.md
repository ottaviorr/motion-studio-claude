---
name: paper-collage-film
description: Torn-paper COLLAGE motion film, 5–30 s (YouTube intro or channel trailer, brand or shop promo, 16:9), stop-motion on twos, built in code; AI only for photo cut-outs. Use for collage / scrapbook / cut-out / magazine-cutout / ripped-paper / mixed-media / zine-style videos, or when someone sends a paper-collage reference and says "make it like this ref" (RU: коллаж, рваная бумага, вырезки, аппликация, журнальные вырезки, заставка, интро, «сделай как на рефе», «как San Diego Zoo»). Not for static photo collages, moodboards, split-screen clip grids or a single transition. San Diego Zoo "Africa Rocks" technique: layered torn paper with white fibrous edges, halftone, watercolour sky, photo cut-outs dropping in, push into a lens → paper iris → kaleidoscope, strip rocket, title drop, page tear to the logo, logo flicker. Ships a working canvas engine, 10 s and 30 s example edits (kaye.creatives), a synthesised score with paper foley, palette remap, font and palette choice sheets, green-screen keying and render tools.
---

# paper-collage-film

A collage film = **one continuous stop-motion camera journey through torn paper**, cut to the music, ending on a title, a page tear to the logo and a call to action. Everything is code except photographic cut-outs. `assets/template/` is a complete 10 s film (kaye.creatives YouTube launch) that renders as shipped — adapt it, don't start from zero.

## What users of this skill expect (references/lessons.md has the story)
- **Look at the reference first.** Open every link sent, extract frames at 12 fps, read the sheets. Several refs → find the one they love most.
- **Technique from the ref, story from the brand.** Copy the motion grammar, never the plot (no meerkat-for-meerkat mapping).
- **Code first; generate only photo cut-outs.** No generated backgrounds, no people or AI characters unless asked, no video generation.
- **Choices as rendered sheets, not guesses**: title font → `tools/font_sheet.sh`, colours → `tools/palette_sheet.sh`; the user answers with a number.
- **Fast and visible**: send the beat table, the cut-out sheet and a draft early, give clock-time ETAs, use parallel agents (references/agent_workflow.md).
- Talk in the user's language; on-screen copy in English unless asked. No full-frame flashing (photosensitivity).

## 0 · Intake (ask once, in one message, only what you can't infer)
Exact brand/handle spelling and every on-screen word · duration · format (see below) · language of the copy (Cyrillic changes fonts) · CTA (subscribe / follow / visit) · logo file or text logo · music: synthesised or their own track · OK to spend ≈ N×2 credits on cut-outs.

**Format.** The collage layouts are drawn for **1920×1080 only** (collage.js and scenes.js use absolute coordinates). For a 9:16 Reel without a re-layout: render the 16:9 film and place it full-width (1080×608) on a 1080×1920 page between torn-paper bands that carry the title, handle and CTA. A true vertical film means re-placing every coordinate — quote it as extra time.

## 1 · Project (1 min)
```bash
<skill>/scripts/new_project.sh <output_root> <slug>             # new brand: palette off (original paper colours)
<skill>/scripts/new_project.sh <output_root> <slug> --example   # reproduce the shipped kaye.creatives film (night palette)
cd <project>                                                    # run every command below from the project (agents: prefix each call with `cd <project> &&`)
```
Creates comp/, audio/score.html, tools/ (compiled extract/encode/mux/greenkey), cutouts/, refs/, review/. Needs macOS (Swift, AVFoundation, afconvert), Chrome/Brave, Node ≥ 22 (`NODE_BIN=/path/to/node` forces one; if a fallback was linked, `export PATH="<project>/tools/bin:$PATH"` for direct `node` calls — tools/*.sh do it themselves), internet for Google Fonts.
**Missing cut-outs render as labelled grey cards**, so a draft works before any generation. The example loads: cam_side cam_front car helmet phone plane_front plane_side clap reel laptop headphones midi phone_gimbal cassette cloud_1..4 rocks_a/b/c tree_a/b grass_strip.

## 2 · Reference (10–15 min)
Download the ref (Pinterest: resolve pin.it → pin page → the `v1.pinimg.com/videos/…/720w.mp4` or `/mc/720p/` H.264 URL; GIF: split frames with ImageIO/Swift — no ffmpeg). `tools/extract ref.mp4 refs/f 12 960 0.85`, then contact sheets with `tools/sheet.mjs` (captions = frame/12 s; `tools/strip.sh` assumes 24 fps, so its labels are half the real time on 12 fps frames). LOOK. Write `refs/analysis.md` with the headings of references/reference_san_diego.md: cut times, motion curves, palette hexes, font look-alikes, must-copy list — and map every ref device to a CL/CLX device or mark it "new device"; list the San Diego devices to drop. **The user's ref overrides the San Diego numbers below.**

## Motion grammar (San Diego measurements — references/reference_san_diego.md)
- Everything **on twos** (12 drawings/s): motion time `q(t) = floor(t*12)/12`, 1–2 px layer boil per drawing.
- **No hard cuts until the logo**: zoom-throughs, page rip, torn wipe, hexagon hole in the kaleidoscope, tilt-up behind a strip rocket.
- Drop-in 3 drawings (edge enters → mid-air −8° → lands) + 1 settle drawing (1.03→1); pop-ups in 1–2 drawings.
- Push into a detail: exponential zoom ~1→6× over ~1 s, zoom centre lerps onto the detail.
- Kaleidoscope: mirrored rings, **no rotation**, scale doubles every ~0.35–0.38 s; a repeated sticker only as one ring.
- Title lands from above, expo-out over 9 drawings, no overshoot, white paper outline + perspective extrusion.
- Page tear ~0.42 s with a dark curling back → torn band with the wordmark; alt-style flicker held 2-1-2-3-2-2 frames, inside the band.

## 3 · Story + beat table (send within ~15 min)
Write `script.md`: `time | music | what we see | on-screen text (verbatim)`, 120 BPM grid (beat 0.5 s, 24 fps). Pick the length:

**10 s (the shipped example)**
| t | beat |
|---|---|
| 0–1.0 | collage page; ▶ drops (lands 0.5); channel tag; cursor presses ▶ 0.875 |
| 1.0 | page rips from the centre → world 1 (F1 car through diagonal bands, centre 1.75; helmet slaps 2.0; tag) |
| 2.5 | torn wipe → film camera, accelerating push into the lens, paper iris 2.9–3.4 (tag) |
| 3.5–4.5 | kaleidoscope rings, flyers 4.2/4.3/4.4, hexagon hole → desk |
| 4.5–5.5 | desk: laptop 4.5, gear 4.75/5.0/5.25, prompt types, "generate ✦" 5.15 → result |
| 5.5–5.95 | tilt-up, strip rocket carries ▶ away |
| 6.0 | title "KAYE / CREATIVES" (Fraunces Black Italic), radial burst, biplane crosses |
| 7.5–7.92 | page tear → logo band |
| 8.0–8.5 | logo flicker inside the band |
| 8.5–10 | SUBSCRIBE slaps, click 9.0 → SUBSCRIBED ✓, bell 9.15, slow push |

**6 s intro** (plays before every video: no rip, no desk, no CTA): 0–0.5 hero drops · 0.75–1.5 push into a detail, iris 1.0–1.42 · 1.5–2.5 kaleidoscope, flyers 2.17/2.33, hole 2.33–2.5 · 2.5–2.96 rocket tilt-up · 3.0 title (lands 3.75) + burst · 4.5–4.92 tear · 5.0–5.5 band flicker · 5.5–6 final hit + hold. Score: dur 6, drop 0.5, mid 1.5, build 2.5, vac 2.95, lift 3.0, end 5.5. Logo ≥ 1.0 s on screen.

**15 s promo** (mirrors the 15 s ref): 0–0.5 hero drop · 0.5–2.5 pop-ups · 2.5–3.5 push + iris · 3.5–5.5 kaleidoscope, hole 5.33 · 5.5–7.5 world 2, burst led by a flyer · 7.5–9.5 world 3 / product moments · 9.5–10.5 rocket · 10.5 title (lands 11.25) · 12.5–12.92 tear · 13.0–13.5 flicker · 13.5–15 CTA.

**30 s**: assets/examples/kaye_30s_scenes.js + kaye_30s_score.html (phone ad, ransom letters, thumbnail wall).

### Re-skinning for another brand
| device | kaye (YouTube) | e.g. coffee shop |
|---|---|---|
| hero drop | ▶ play button | cup / bag of beans (`CL.sprite` + `CL.drop`) |
| pop-ups | camera props | croissant, beans |
| rip → world 1 | F1 car through bands | roaster drum, farm |
| push + iris | camera lens (cam_front) | crema in the cup (measure centre + radius in sprite px; iris formula in api.md) |
| kaleidoscope rings | cars, reels | beans, cups (one ring per sticker) |
| desk + screen | prompt UI | counter + order ticket (`CLX.tag` / `CLX.ransom`) — or drop it |
| rocket | ▶ on strips | cup on a plume of strips |
| title / band | channel name / `kaye.creatives` | shop name / logo or @handle |
| CTA | SUBSCRIBE + bell + cursor | handle + address chip (`CLX.tag`), hours star (`CLX.star`) |
`CLX.play`, `subscribe`, `thumb`, `screen` and `cursor` are YouTube devices. Backgrounds in collage.js use fixed cut-out names (`CL.page`: grass_strip + rocks_*; `CL.diag`: rocks_* + cassette; `CL.cloudsky`: cloud_1..4): the zero-code re-skin is to generate stand-ins under the same names (grass_strip = a torn strip of coffee beans, rocks_* = b/w halftone sacks); otherwise copy `pageLayers` into scenes.js. Update `warm()`'s `cuts:` list for new names.

## 4 · Cut-outs (5 min, ~2 credits each)
Only what code can't draw — prompt template, the example set and keying in references/cutouts.md. `tools/greenkey keyframes/raw/x.png cutouts/x` → alpha PNG(s), multi-object sheets split automatically. Render a check sheet on a coloured background and send it.
A real **logo file** → `cutouts/logo.png`, drawn with `CL.sprite` inside the tear's `drawUnder`; flicker looks = the `logoBand` style backgrounds + that sprite. For a text logo size it `min(190, 0.78·W / measured width)`.

## 5 · Edit in code
`comp/scenes.js` is the film: `COPY` (on-screen words), scene functions (`pageScene`, `f1Scene`, `camScene`, `kalDraw`, `deskScene`, `titleBg`, `titleScene`, `endScene`), transitions (`wipe`, `ripDraw`, `tearDone`), `K.setup({bars})` punch zooms. Words outside COPY: the prompt UI's "PROMPT"/title (`CLX.screen` o.title), the 'posters' flicker look's poster glyphs (collage_fx.js) — check them. API: references/api.md; as-built timings and gotchas of the example: references/edit_notes_10s.md.
**Re-time by remapping time, not by editing literals**: `Cut(a, b, (ctx, t) => titleScene(ctx, t + (6.0 - a)))`. Keep offsets multiples of 1/12 s. Scenes that draw a neighbour move as one block (kalDraw→deskScene via drawNext, titleBg→deskScene before 71/12, endScene→titleScene/titleBg). Then update `K.setup({bars})`, the score cues and the still times. Times past the duration clamp to the last frame.
**Title font** lives in 4 places: the `<link>` in comp/index.html (load ONE face of the family), the `fonts()` list in comp/film.js (else sprites bake with a fallback), `COPY.titleFont`, and comp/font_sheet.html's `<link>` for candidates. **Cyrillic copy**: Ultra, Fraunces, Cinzel, Bevan, Abril Fatface, Shrikhand, Chango, Rye, Lilita One, Bungee, Chewy and Gluten have no Cyrillic — use Rubik / Rubik Spray Paint, Unbounded, Yeseva One, Lobster, Playfair Display, Russo One for the title and `logoBand o.font`, and check the ransom chips.
Stills: `node tools/capture.mjs comp/index.html review/st --stills 0.5,1.75,…`.

## 6 · Music
`audio/score.html` synthesises the score in the browser (no samples): funk groove + paper foley (slaps, rips, whooshes, pops, typing, clicks, bell), limiter. Set `window.SCORE_CONFIG` {dur, drop, mid, build, vac, lift, end} in its first `<script>` from the beat table and move cues with `window.SCORE_CUES = {…}`; delete the lines in `paper()` for events the film doesn't have (search `CUE.car`, `CUE.plane`, `CUE.type`, `CUE.gen`, `CUE.subClick`, `CUE.ding`) — nulling a cue throws. Mute layers with `?lv_<name>=0`.
```bash
node tools/render_audio.mjs "<project>/audio/score.html" audio/score.wav
afconvert -f m4af -d aac -b 256000 audio/score.wav audio/score.m4a
python3 tools/music_window.py audio/score.wav --hits 0.5:0.35,1.0:1.0,6.0:1.0,7.5:0.45,8.5:1.0   # each big hit loudest in its window
python3 tools/music_window.py audio/score.wav --timeline 0.25
```
Their own track instead: `python3 tools/music_window.py track.mp3 --len <dur>` → pick a window → `python3 tools/cut_audio.py track.mp3 <start> <dur> audio/score.m4a` → re-time the picture to its drops (grid = the track's BPM). You cannot hear audio — verify by numbers (references/music_notes_10s.md) and say so.

## 7 · Draft → choices → final
```bash
tools/render_film.sh draft                       # ~30 s for 10 s → <slug>_draft.mp4 (+ .frames_draft)
tools/strip.sh .frames_draft review/strip.png 1
tools/font_sheet.sh "LINE1|LINE2"                # numbered title fonts in the real treatment and the film's palette
tools/palette_sheet.sh 0.75 3.75 6.9 8.75        # every palette of comp/grade.js on key frames (0 = original)
tools/render_film.sh final audio/score.m4a <slug>_final.mp4   # PNG frames, 30 Mbps
```
Bake the chosen palette with `window.PALETTE = '<name>'` in comp/index.html (`null` = original colours). grade.js recolours every pixel, photos and logo included: for brand colours add a `PALS` entry with the brand hexes in the roles (red → primary) and check that product photos and the logo still read true — or set `null` and edit `CL.C` / `CLX.PAL` directly.

## QA before sending (look at frames yourself)
- Sync: picture events vs `--hits` / `--timeline` peaks, ≤ 1 frame.
- On twos: frame-pair hashes differ only at deliberate 1-frame events.
- Joins: no empty/jumping frames; nothing static > ~1 s except title/logo holds.
- Nothing covers the hero object, the title, the button label, the URL (cursor paths!).
- Tags ≥ 36 px on paper chips, each ≥ 0.8 s; title ≥ 1.5 s; logo ≥ 1.5 s (≥ 1.0 s for films ≤ 8 s).
- No full-frame flicker; band flicker brightness steps one way. No grey "cut-out missing" cards left.
- Duration exact (afinfo), audio present, peak ≤ −1 dBFS.
- Only one render at a time per project (`render_film.sh` wipes its frames folder).

## Files
| need | where |
|---|---|
| measured San Diego grammar, shots, palette, fonts | references/reference_san_diego.md |
| CL / CLX API | references/api.md (+ header comments of collage.js / collage_fx.js) |
| cut-out prompts, example set, keying | references/cutouts.md |
| score cue map + measurements | references/music_notes_10s.md |
| as-built picture timings, edit gotchas | references/edit_notes_10s.md |
| parallel agent recipe | references/agent_workflow.md |
| why the defaults are what they are | references/lessons.md |
| device test scenes (for new devices) | assets/examples/test_collage_scenes.js, test_fx_scenes.js |
