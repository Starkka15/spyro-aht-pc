/* Installing the game files from a folder, disc or Xbox disc image: see
 * import.c. */
#ifndef SPYRO_IMPORT_H
#define SPYRO_IMPORT_H

#include <windows.h>

enum { IMPORT_OK = 0, IMPORT_FAILED = 1, IMPORT_WRONG_VERSION = 2, IMPORT_CANCELLED = 3 };

/* import_game flags. */
enum {
    IMPORT_QUIET = 1,   /* no "installed" message on success */
    IMPORT_SETUP = 2,   /* Setup: may change the release (US or European),
                         * replacing the other one's files. The launcher keeps
                         * to the release that is installed. */
};

/* Copies the game from `src` (a folder, drive or image file) into `dest`,
 * with a progress window. Errors are shown to the player. Returns an
 * IMPORT_ code. */
int import_game(HWND parent, const wchar_t *src, const wchar_t *dest, int flags);

/* Whether `dest` holds the game (its default.xbe). */
int import_installed(const wchar_t *dest);

#endif
