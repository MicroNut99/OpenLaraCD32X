# Tomb Raider for Sega CD + 32X (OpenLara CD32X)

Tomb Raider (1996) on the **Sega CD32X**, built on XProger's **OpenLara** 32X engine.
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
- About 7–9 frames per second – see **Frame rate** below.

## Frame rate
**Status:** about **7–9 frames per second**, measured on real hardware with a profiler build
(Caves, Lost Valley, a fight). The drawing code is still OpenLara's own 32X renderer.

Where a frame's ~120 ms go (profiler):

| Part | Time per frame |
|---|---|
| Reading the pad (Sega CD) | 0 ms |
| Waiting for the screen | 0 ms |
| Game logic | 10–36 ms |
| Preparing the scene (transform, sort) | 19–27 ms |
| Drawing (both SH2s) | 58–111 ms – of which the main SH2 waits 16–30 ms for the second one |

**What has been done so the CD version keeps that speed:**
- **The game runs from the RAM cart, exactly like a cartridge.** The CD drive is only used to
  load a level and to play music – never while drawing a frame.
- **Both SH2 processors work on every frame** (OpenLara splits the drawing between them).
- **Nothing else competes during play.** Once the game loop runs, the Sega CD side goes quiet;
  the 68000 "heartbeat" that stalled the renderer was removed; the diagnostic text is off.
- **No reload on a restart.** Dying, choosing Restart or loading a save from the same level
  reuses the level already in the cart (faster restarts – not more frames, but less waiting).

**Checked and ruled out:**
- **32-bit cart reads.** The cart slot is 16 bits wide and the 32X sets the wait time for every
  cart access, so a cart that can answer 32-bit reads can't make the console read it faster.
  The game already reads 32 bits at a time where it can.

- **The controller read.** The profiler shows it costs nothing, so there is nothing to win there.

**In progress:** drawing is the bottleneck. The two SH2s used to take turns layer by layer and
wait for each other; the next build lets each SH2 draw its own half of the screen (top/bottom,
balanced every frame), which removes that waiting. Expected: about 1–2 frames per second more.
A bigger step – letting the second SH2 draw while the first one runs the game logic – would
need a larger rework of the engine.

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
