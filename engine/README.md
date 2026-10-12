# Engine changes

`openlara-cd32x.patch` holds all CD32X changes to XProger's OpenLara, made against upstream
commit `3b268ca` (https://github.com/XProger/OpenLara). Source files only.

```bash
git clone https://github.com/XProger/OpenLara OpenLara-src
cd OpenLara-src
git checkout -b cd32x 3b268ca
git apply ../OpenLaraCD32X/engine/openlara-cd32x.patch
```

Put `OpenLara-src` next to `OpenLaraCD32X` (build.sh expects `../OpenLara-src`).
Every change is inside `#ifdef CD32X`, so the normal 32X cartridge build is unchanged.

Files changed:
```
src/fixed/camera.h       cut-scenes: start at frame 0, back to the menu when picked in the passport
src/fixed/common.h       passport strings (cut-scenes, movies)
src/fixed/enemy.h        all enemies active (ENEMIES-1/2), Lara's double (DOPPEL-1)
src/fixed/inventory.h    full passport (15 levels, cut-scenes, movies, scrolling)
src/fixed/lang/en.h      their names
src/fixed/item.h         sound effects on
src/fixed/lara.h         Start opens the inventory
src/platform/32x/Makefile      make CD32X=1  (+ PROF=1 for the profiler)
src/platform/32x/asm/data.s    splash picture instead of built-in levels
src/platform/32x/main.cpp      CD commands, level loading into the cart, splash, cart saves,
                               Caves kept in the cart, profiler (CD32X_PROF), game loop for
                               the overlap, the slave's movie-sound job
src/platform/32x/sound.cpp     CD music, PCM sound effects (volume by distance), cut-scene sound
src/platform/32x/fmv.inc       the movie player (included by main.cpp)
src/platform/32x/roq.h         RoQ decoder header  - Victor Luchits, Doom 32X: Resurrection (MIT)
src/platform/32x/roq_read.c    RoQ decoder         - same; decoder by Dr. Tim Ferguson
src/platform/32x/render.cpp    screen split: each SH2 draws its own part of the screen
                               (CD32X_SPLIT) and the game logic overlaps the drawing
                               (CD32X_OVERLAP) - see the comment blocks at the top;
                               renderScratch() lends the face/vertex lists to the movie player
src/platform/32x/rasterizer.h  sprites clip to the SH2's own rows (screen split)
```
data/SPLASH.BIN is made by build.sh from splash.jpg.
