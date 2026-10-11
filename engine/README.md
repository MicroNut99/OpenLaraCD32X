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
src/fixed/enemy.h        all enemies active (ENEMIES-1/2)
src/fixed/inventory.h    full passport (15 levels, scrolling)
src/fixed/item.h         sound effects on
src/fixed/lara.h         Start opens the inventory
src/platform/32x/Makefile    make CD32X=1
src/platform/32x/asm/data.s  splash picture instead of built-in levels
src/platform/32x/main.cpp    CD commands, level loading into the cart, splash, cart saves
src/platform/32x/sound.cpp   CD music and PCM sound effects
```
data/SPLASH.BIN is made by build.sh from splash.jpg.
