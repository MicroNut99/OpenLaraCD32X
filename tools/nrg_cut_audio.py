#!/usr/bin/env python3
"""nrg_cut_audio.py - the cut-scenes' sound (voices + music) out of a Tomb Raider 1 CD image.

    python3 tools/nrg_cut_audio.py "<your Tomb Raider 1.nrg>" soundtrack_wav

The cut-scene sound is not on the soundtrack album - it is CD audio on the original game CD
(the game's tracks 22-25).  On the PC disc they are its audio tracks 7-10; their lengths match
the cut-scenes (Atlantis 65 s, Qualopec 54 s, Natla's Mines 17 s, Tihocan 33 s of sound).
This writes them as soundtrack_wav/cut22_atlantis.wav ... cut25_tihocan.wav (44.1 kHz,
16-bit stereo); music_map.txt puts them on the disc as CD tracks 22-25.

Reads Nero images (.nrg).  With another image type or a real CD: rip disc tracks 7-10 to WAV
yourself and name them cut22_..., cut23_..., cut24_..., cut25_... (the order above)."""
import os, struct, sys, wave

def die(m): sys.exit("*** " + m)

def nrg_tracks(path):
    """{track: (sector size, start byte, end byte)} from the image's DAOX/DAOI chunk"""
    f = open(path, 'rb')
    f.seek(0, 2); size = f.tell()
    f.seek(size - 12)
    if f.read(4) == b'NER5':
        off = struct.unpack('>Q', f.read(8))[0]; v2 = True
    else:
        f.seek(size - 8)
        if f.read(4) != b'NERO': die("%s: not a Nero image" % path)
        off = struct.unpack('>I', f.read(4))[0]; v2 = False
    f.seek(off)
    tracks = {}
    while True:
        tag = f.read(4)
        if len(tag) < 4: break
        ln = struct.unpack('>I', f.read(4))[0]; data = f.read(ln)
        if tag in (b'DAOX', b'DAOI'):
            first, last = data[20], data[21]
            rec = 42 if tag == b'DAOX' else 30
            for i in range(last - first + 1):
                r = data[22 + i * rec: 22 + (i + 1) * rec]
                secsize = struct.unpack('>H', r[12:14])[0]
                if tag == b'DAOX':
                    idx1, end = struct.unpack('>QQ', r[26:42])
                else:
                    idx1, end = struct.unpack('>II', r[22:30])
                tracks[first + i] = (secsize, idx1, end)
        if tag == b'END!':
            break
    return f, tracks

NAMES = {22: 'cut22_atlantis.wav', 23: 'cut23_qualopec.wav', 24: 'cut24_natlas_mines.wav',
         25: 'cut25_tihocan.wav'}
SECONDS = {22: 70.0, 23: 64.0, 24: 21.7, 25: 35.1}      # disc tracks 7-10, whole length

def main():
    if len(sys.argv) != 3: sys.exit(__doc__)
    nrg, out = sys.argv[1:]
    os.makedirs(out, exist_ok=True)
    f, tracks = nrg_tracks(nrg)
    for game, disc in zip((22, 23, 24, 25), (7, 8, 9, 10)):
        if disc not in tracks: die("the image has no track %d" % disc)
        secsize, a, b = tracks[disc]
        secs = (b - a) / 176400.0
        if secsize != 2352 or abs(secs - SECONDS[game]) > 0.5:
            die("track %d is %.1f s (%d-byte sectors), expected %.1f s of CD audio - "
                "a different Tomb Raider disc?" % (disc, secs, secsize, SECONDS[game]))
        f.seek(a)
        w = wave.open(os.path.join(out, NAMES[game]), 'wb')
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes(f.read(b - a))                # CD audio: 44.1 kHz, 16 bit, stereo
        w.close()
        print("==> %s  (%.1f s, disc track %d)" % (NAMES[game], secs, disc))

if __name__ == '__main__':
    main()
