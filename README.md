# Spyro: A Hero's Tail — PC port

A native Windows version of the original Xbox game, made by static
recompilation with [xboxrecomp](https://github.com/sp00nznet/xboxrecomp): the
Xbox program is translated to C ahead of time and runs directly, not in an
emulator.

**This repository contains none of the game.** You need your own copy of
Spyro: A Hero's Tail for the original Xbox (USA, title VU-052, version 1).
Setup copies the game's files from a folder, a disc drive, or an Xbox disc
image (.iso, full or trimmed) and checks the version first.

> **Early release.** The opening and Dragon Village have been played. Expect
> bugs later in the game; reports are welcome in Issues (set `Log = 1` in
> `spyro.ini` and attach `spyro.log`, or `crash.txt` if it crashed).

## Playing

Download `SpyroAHT-PC-<version>-Setup.exe` from
[Releases](../../releases), run it, and point it at your copy of the game.
Windows 10 or 11 (64-bit) with a DirectX 11 graphics card.

- Keyboard and mouse or any XInput controller. Keys can be changed in
  `mkb.ini`; the on-screen prompts always show the controller's buttons.
- The launcher sets fullscreen, window size, render scale, widescreen, VSync
  and skipping the logo movies.

See [installer/README.txt](installer/README.txt) for the full player notes,
including the key for each controller button.

## Building

Needs Visual Studio 2022 (C, x64 tools), CMake 3.20+, Python 3 with Capstone,
and your own copy of the game.

1. Clone the runtime branch beside this repository:
   `git clone -b spyro-aht-1.0.0 https://github.com/Starkka15/xboxrecomp ../xboxrecomp`
2. Put the game's files in `game_files/` (with `default.xbe`).
   `tools/xiso_x.py` extracts them from a disc image.
3. Generate the code from your XBE, from the xboxrecomp folder:

   ```
   py -3 -m tools.disasm   <port>/game_files/default.xbe --seed-functions <port>/tools/seeds.json --force
   py -3 -m tools.func_id  <port>/game_files/default.xbe
   py -3 -m tools.abi_analysis <port>/game_files/default.xbe
   py -3 -m tools.recomp   <port>/game_files/default.xbe --all --split 250 --gen-dir <port>/src/recomp/gen
   ```

4. `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo` then
   `cmake --build build`.
5. Optional: `ISCC installer\spyro.iss` (Inno Setup 6) builds Setup.

The generated code is the game's code translated, so it is never committed:
`src/recomp/gen/` stays local.

## Credits and licenses

Spyro: A Hero's Tail was developed by Eurocom and published by Vivendi
Universal Games; Spyro is a trademark of its owner. This port is not
affiliated with or endorsed by any of them.

The port's own code is GPL-3.0 (see LICENSE). The xboxrecomp runtime is MIT
and includes components from xemu under the LGPL 2.1; see
[installer/LICENSES.txt](installer/LICENSES.txt).
