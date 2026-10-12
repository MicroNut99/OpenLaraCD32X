# Tomb Raider for Sega CD + 32X (OpenLara CD32X)

Tomb Raider (1996) on the **Sega CD32X**, built on XProger's **OpenLara** 32X engine. **Version 1.2.**
The whole game runs from one CD: each level is loaded from the disc into a 4 MB RAM cart, with
CD music, PCM sound effects and saving.

> **No game data is included.** You need your own copy of Tomb Raider 1 (PC) – the build converts
> it. The music and the loading picture are also yours to supply. See *What you need*.

## Hardware
- Sega Genesis / Mega Drive
- Sega CD / Mega-CD
- Sega 32X
- **A 4MB RAM cart** (battery-backed), in the 32X cartridge slot – required
- a **6-button pad** (recommended; with a 3-button pad Start still opens the inventory, but walk,
  roll and look are missing)

Emulators: Kega Fusion cannot emulate the 4MB RAM cart, so the game does not run there.

## What you need
| What | Where it goes |
|---|---|
| Tomb Raider 1 **PC** data (Steam/GOG: the `DATA` folder with `LEVEL1.PHD` …) | `OpenLaraCD32X/DATA/` → converted by the packer |
| Music: WAV files (44.1 kHz, 16-bit, stereo) | `OpenLaraCD32X/soundtrack_wav/`, assigned in `music_map.txt` |
| A loading picture (any size, 16:9 works best) | `OpenLaraCD32X/splash.jpg` |
| Chilly Willy's Sega toolchain (`/opt/toolchains/sega`), Python 3 with Pillow, MinGW (for the packer) | your build machine (Linux / WSL) |

## Building
Full instructions: `docs/OPENLARA_CD32X_HANDOFF.md`. In short:
1. Get the engine: clone upstream OpenLara next to `OpenLaraCD32X/` and apply `engine/openlara-cd32x.patch`.
2. Build the packer (`OpenLaraCD32X/gba/packer`) and convert your levels: `packer.exe 32x out32x`.
3. `cd OpenLaraCD32X && bash build.sh`
4. **Burn `OpenLaraCD32X/subcpu/CDROMPlayer_music.cue`** (with its `.bin`). The `.iso` alone has no music.

## Starting the game
Put the RAM cart in the 32X, the disc in the Sega CD, and switch on. The picture appears while
OpenLara is copied into the cart; then each level shows the picture with a **red loading bar**
along the bottom while it loads from the disc.

## Fast start
Caves (Level 1) is also the title menu, so it is needed every time the game starts. It now has
its own place in the RAM cart and stays there – the cart keeps its contents without power.

- **First start:** Caves loads from the CD as usual (red bar). Afterwards a record in the cart
  says it is there: its length and a checksum, written only after a complete copy.
- **Every start after that:** the game checks the record against what is really in the cart
  (same length as Caves on this disc, checksum matches). If it is all there, nothing is loaded
  and the menu comes up almost at once.
- **Back to the menu, or playing Caves:** never loads Caves again.
- **Something wrong?** Hold **A + B + C** while the game starts: Caves is always reloaded
  from the CD. (Also use this after rebuilding the disc with a changed Caves of exactly the
  same size – the only change the check can't see.)

Cart layout: game 0–0.5 MB, Caves 0.5–2 MB, the level being played 2–3.94 MB, settings and
saves in the last 64 KB. `build.sh` refuses to build if the game or Caves would overlap.

## Controls (6-button pad)
| Button | Action |
|---|---|
| D-pad | move / turn |
| **A** | action – grab, climb, pull switches, pick up |
| **B** | jump |
| **C** | draw / holster weapons |
| **X** | walk (hold) |
| **Y** | roll |
| **Z** | look around (hold) |
| **Start** or **Mode** | inventory (open / close) |

**In the inventory:** left/right turns the ring, up/down changes ring, A selects, B or Start goes back.

**Passport** (in the inventory): **Load Game** (all levels, or your saved position), **Save Game**,
**Exit to Title** – flip pages with left/right.

## Saving
Saves and settings are stored in the RAM cart (battery-backed), one saved position. Save from the
passport; load it again from the passport's Load Game page ("Current position").
Saving is not available in Lara's Home.

## What is in this version
- All 15 levels from Caves to the Great Pyramid, plus Lara's Home, chosen from the passport or
  played straight through.
- CD music: one piece per level (your choice, in `music_map.txt`) and the secret chime.
- Sound effects on the Sega CD's PCM chip, a set for each level.
- Every enemy except Lara's double: wolves, bears, bats, raptors, T-Rex, lions, pumas, gorillas,
  rats, crocodiles, mutants, centaurs, mummies, Larson, Pierre, the skater, the cowboy, Mr. T,
  Natla and the Torso.
- Saving and loading, options (sound, music, controls) remembered.

## Known limitations
- **Lara's double** (Atlantis) does not move.
- **Gorillas** do not climb ledges; **water rats** do not dive.
- Enemy darts, bolts and bullets hit instantly (no visible projectile); an enemy may occasionally
  shoot through a thin wall.
- Sound effects: one per frame, fixed volume (no fading with distance), the 31 most important per level.
- The original game's short story cues and the cut-scene dialogue are not played (not on the album).
- The cut-scenes between levels have not been tested on hardware yet.
- No FMVs; *Unfinished Business* is not included.
- About 9–15 frames per second (9–10 in fights) – see **Frame rate** below.

## Frame rate
**Status:** **9–15 frames per second while exploring, 9–10 in fights with raptors** – measured
on real hardware with the profiler build (Caves, Lost Valley, raptors, the T-rex). When this
work started it was 7–9 fps everywhere.

| Part of a frame | Before the split | With the split |
|---|---|---|
| Reading the pad (Sega CD) | 0 ms | 0 ms |
| Waiting for the screen | 0 ms | 0 ms |
| Game logic (main SH2) | 10–36 ms | 7–26 ms |
| Preparing the scene (main SH2) | 19–27 ms | 9–34 ms |
| Drawing (both SH2s) | 58–111 ms | 43–103 ms |
| … main SH2 waiting for the second one | 16–30 ms | 0–5 ms |
| **Whole frame** | **110–145 ms** | **69–111 ms exploring, 120–166 ms in fights** |

With the overlap (below) on top of the split, fights with raptors take 100–114 ms per frame
(9–10 fps, was 116–166 ms) and exploring 64–110 ms.

### What was done
- **Screen split (the big one).** OpenLara's two SH2s used to draw every other polygon and stop
  after every depth layer to wait for each other, so the picture stayed in the right order.
  Now the main SH2 draws the top of the screen and the second SH2 the bottom. Each one goes
  through the whole scene far-to-near and draws only its own rows, so neither ever waits for
  the other while drawing. Polygons crossing the line between the halves are cut in two.
- **The line between the halves stays still.** The first version moved it a few rows every
  frame to balance the work – and a still picture then flashed: a cut polygon places its
  texture pixels very slightly differently, so pixels near the line changed back and forth.
  Now the line only moves when one SH2 has been clearly behind for 8 frames in a row.
- **Game logic overlaps the drawing.** The main SH2 draws its rows, then goes straight on to
  the next frame's pad reading and game logic while the second SH2 is still drawing. The
  second SH2 puts the finished frame on screen itself – but only once both halves are done,
  so the picture never tears. The inventory stays at a solid 30 fps.
- **No waiting for the screen refresh before preparing the next frame.** A finished frame
  only appears at the next refresh (every 16.7 ms). The main SH2 used to wait for that before
  starting the next frame (3–14 ms per frame once the logic overlapped). Preparing the scene
  doesn't need the screen, so now only clearing and drawing wait for it.
- **Why the line is usually not in the middle:** the 32X SH2s are *master and slave* on one
  shared bus. The master owns the bus; the slave has to ask for it for every memory access,
  so while both draw, the slave stalls and gets less done. The balancing gives the slave fewer
  rows when it falls behind.
- **The game runs from the RAM cart, exactly like a cartridge.** The CD drive is only used to
  load a level and to play music – never while drawing a frame.
- **Nothing else competes during play.** Once the game loop runs, the Sega CD side goes quiet;
  the 68000 "heartbeat" that stalled the renderer was removed; the diagnostic text is off.
- **No reload on a restart.** Dying, choosing Restart or loading a save from the same level
  reuses the level already in the cart (less waiting, not more frames).
- **Profiler build:** `PROF=1 bash build.sh` shows the numbers above on screen (F fps,
  T frame, I input, L logic, W screen wait, X prepare, D draw, S wait for the second SH2;
  times in ms). It uses the master's watchdog timer – the SH2 free-running timer is taken by
  OpenLara's start-up code and can't be used for timing.

### Files changed for the frame rate
All engine changes are in `engine/openlara-cd32x.patch` (apply it to OpenLara `3b268ca`) and
only take effect in the CD build (`make CD32X=1`); the cartridge build is unchanged.

| File | Change | Switch |
|---|---|---|
| `OpenLara-src/src/platform/32x/render.cpp` | **Screen split:** `flush_ot()` – each SH2 walks the whole scene and draws only its own rows; `drawPolyY()` – cuts polygons at the line between the halves; `flush_c()` – passes the line to the second SH2 and moves it only when one SH2 is clearly behind. **Overlap:** `flush_c()` returns after the main SH2's rows; `renderFinish()` waits for the second SH2, balances the line and clears the draw list; the second SH2 puts the finished frame on screen when both halves are done. Explained in the comment blocks at the top of the file. | `CD32X_SPLIT`, `CD32X_OVERLAP` (off: `-DCD32X_NO_SPLIT`, `-DCD32X_NO_OVERLAP`) |
| `OpenLara-src/src/platform/32x/rasterizer.h` | `rasterizeSprite_c()` – sprites clip to the drawing SH2's own rows. | `CD32X_SPLIT` |
| `OpenLara-src/src/platform/32x/main.cpp` | Game loop for the overlap (pad + game logic while the second SH2 draws, no wait for the screen refresh before preparing); the second SH2's clear job waits for the screen swap; the profiler (timer, on-screen numbers). | `CD32X_OVERLAP`, `CD32X_PROF` |
| `OpenLara-src/src/platform/32x/Makefile` | `make CD32X=1 PROF=1` builds the profiler. | `PROF=1` |
| `OpenLaraCD32X/build.sh` | `PROF=1 bash build.sh` makes the profiler disc. | `PROF=1` |

### Checked and ruled out
- **32-bit cart reads.** The cart slot is 16 bits wide and the 32X sets the wait time for every
  cart access, so a cart that can answer 32-bit reads can't make the console read it faster.
  The game already reads 32 bits at a time where it can.
- **The controller read.** The profiler shows it costs nothing.

### What's left
Preparing the scene (9–34 ms) still runs on the main SH2 while the second SH2 waits. Letting
the second SH2 draw one frame while the main SH2 prepares the next would need the scene lists
twice (about 72 KB); only about 30 KB of the 32X's fast RAM is free, so it doesn't fit as is.

## Versions
The version is in the file `VERSION` and is shown small in the corner of the loading picture.

| Version | What changed |
|---|---|
| 1.0 | The whole game from CD: all levels, CD music, PCM sound effects, saving in the RAM cart, all enemies, full passport, loading screen. |
| 1.2 | Fast start: Caves (the title menu) stays in the RAM cart and is not loaded again – hold A+B+C at start to reload it. |
| 1.1 | Faster: the two SH2s draw separate halves of the screen, game logic runs while the second SH2 is still drawing, and the next frame is prepared without waiting for the screen refresh (fights 7–8 → 9–10 fps, exploring 9–15 fps). Profiler build (`PROF=1`). Version shown on the loading picture. |

## Credits
- **OpenLara** – XProger and contributors: https://github.com/XProger/OpenLara
- **Doom 32X: Resurrection** Victor Luchits (viciious) 
- **Sega CD / 32X boot and command framework** – from the Kobo Deluxe CD32X project, built on
  Chilly Willy's Sega CD and 32X examples and toolchain – the CD32X loader started as its CD-boot loader
- **4MB 32X RAM cart** Victor Luchits, Joseph Fenton, Leo Oliveira, Tiido priimägi and Eric Witt. 
- OpenLara port – MicroNut99
- **Tomb Raider** – Core Design / Eidos (now Crystal Dynamics / Embracer). Tomb Raider is their
  trademark; this project contains none of their data and is not affiliated with them.

Licences: see `licenses/` and each upstream project's own licence.
