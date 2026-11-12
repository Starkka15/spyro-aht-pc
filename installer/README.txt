Spyro: A Hero's Tail -- PC port
================================

A native Windows version of the original Xbox game, made by static
recompilation: the Xbox program is translated into PC code ahead of time, so
the game runs directly instead of in an emulator.

This port contains none of the game. It needs your own copy of Spyro: A
Hero's Tail for the original Xbox (title VU-052), the US or the European
release. Setup copies the game's files from it: a folder with the game's
files, the disc in a drive that can read it, or an Xbox disc image (.iso, full
or trimmed). The launcher shows which release is installed and starts the
matching program. To change to the other release, run Setup again and choose
that copy; it replaces the installed game files (saves are kept).

This is an early release: the opening of the game and Dragon Village have been
played, so expect bugs further in. Reports are welcome at
https://github.com/Starkka15/spyro-aht-pc/issues


Playing
-------

Start "Spyro - A Hero's Tail" from the Start menu. It opens the launcher,
where the settings are; Play starts the game. "Play (skip launcher)" starts
the game straight away with the settings you saved.

  Alt+Enter     fullscreen on/off (remembered)
  F9            release the mouse (press again to capture it)
  Close window  quit to the desktop

An Xbox-style controller (or any controller Windows sees as one) works, and
can be plugged in or out at any time.


Keyboard and mouse
------------------

Keys stand in for the Xbox controller's buttons. The on-screen prompts always
show the controller's buttons, so here is what each one is on the keyboard:

  Left stick      W A S D
  Right stick     mouse (camera)
  A               Space, Enter      (jump, glide; confirm in menus)
  B               left mouse, Backspace   (back in menus)
  X               right mouse
  Y               E, middle mouse
  Right trigger   Shift
  Left trigger    Ctrl
  Black / White   F / R
  D-pad           arrow keys, 1 2 3 4
  Start           Esc               (pause)
  Back            Tab               (task list)

Every key can be changed in mkb.ini ("Key bindings..." in the launcher). The
file explains itself; delete it to get the defaults back.


Settings
--------

The launcher writes spyro.ini beside the game. You can edit it by hand too:

  Fullscreen, window size     Alt+Enter and resizing the window are remembered
  Widescreen                  the game's own 16:9 mode (1) or 4:3 (0)
  Sharpness (RenderScale)     the game draws at 640x480 times this; Auto
                              matches your monitor
  VSync                       no tearing, slightly more input lag
  Skip intro movies           skips the Eurocom and Vivendi logos
  Language                    European release only: English, French,
                              German, Spanish, Italian or Dutch, for text
                              and voices. Auto follows the Windows display
                              language (English if the game lacks it). The
                              US release is English only.
  Log                         write spyro.log, for bug reports


Saves
-----

Saves are kept in %LOCALAPPDATA%\xboxrecomp (the launcher's "Saves folder"
button opens it). Uninstalling leaves them alone.


If something goes wrong
-----------------------

If the game stops with an error, it writes crash.txt beside the game and says
so. For anything else, set Log = 1 in spyro.ini, reproduce the problem, and
include spyro.log with your report.

The game needs Windows 10 or 11 (64-bit) and a DirectX 11 graphics card. On
"N" editions of Windows, install the Media Feature Pack for the game's movies.


Credits
-------

Spyro: A Hero's Tail was developed by Eurocom and published by Vivendi
Universal Games; Spyro is a trademark of its owner. This port is not
affiliated with or endorsed by any of them.

Built with xboxrecomp (MIT). It includes code from xemu under the LGPL 2.1;
see LICENSES.txt.
