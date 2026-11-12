/* The two editions of the game this port is built for. Each is its own
 * recompilation of that edition's default.xbe (the US and European programs
 * differ throughout), so each build carries its edition's addresses.
 *
 *   US      VU-052 version 1, 2004-09-10, English only (src/recomp/gen)
 *   Europe  VU-052 version 2, 2004-09-24, English, French, German, Spanish,
 *           Italian and Dutch (src/recomp/gen_eu; AHT_EU defined)
 *
 * European addresses were found from the US ones with tools/xbe_match.py and
 * byte signatures. */
#ifndef AHT_EDITION_H
#define AHT_EDITION_H

#ifdef AHT_EU
#define AHT_EDITION_NAME        "Europe"
#define AHT_ENTRY_POINT         0x0026E189u     /* XBE entry point */
#define AHT_D3D_DEVICE_PTR      0x002947A8u     /* D3D's device pointer (D3D__pDevice) */
#define AHT_DEV_GAME_DIR        "H:/spyro-aht/game/eu_files"
/* Game language of the Portuguese entry in the XC_LANGUAGE -> game language
 * table (0x34FD60, 8-byte pairs; read by the function at 0x1D0810). */
#define AHT_LANG_TABLE_PT       0x0034FD8Cu
#else
#define AHT_EDITION_NAME        "US"
#define AHT_ENTRY_POINT         0x0026D329u
#define AHT_D3D_DEVICE_PTR      0x00293908u
#define AHT_DEV_GAME_DIR        "H:/spyro-aht/game_files"
#endif

/* SHA-1 of each edition's default.xbe. */
#define AHT_XBE_SHA1_US         "4f1658aac4a644b7b3db3abf31663f38882e9520"
#define AHT_XBE_SHA1_EU         "6497fe791466e1f3ec144f48ff2d026c2ce552df"

/* The game exe of each edition, beside the launcher. */
#define AHT_EXE_US              L"spyro_aht_recomp.exe"
#define AHT_EXE_EU              L"spyro_aht_recomp_eu.exe"

enum { AHT_EDITION_UNKNOWN = -1, AHT_EDITION_US = 0, AHT_EDITION_EU = 1 };

#ifdef _WIN32
#include <windows.h>
#include <string.h>

/* Which edition a default.xbe is, from its certificate's version (1 US,
 * 2 Europe; the setup import has already checked the whole file's SHA-1). */
static __inline int aht_xbe_edition(const wchar_t *xbe)
{
    unsigned char h[0x180], c[0xB0];
    DWORD n = 0;
    unsigned base, cert;
    int ed = AHT_EDITION_UNKNOWN;
    HANDLE f = CreateFileW(xbe, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (f == INVALID_HANDLE_VALUE)
        return ed;
    if (ReadFile(f, h, sizeof h, &n, NULL) && n == sizeof h && !memcmp(h, "XBEH", 4)) {
        memcpy(&base, h + 0x104, 4);
        memcpy(&cert, h + 0x118, 4);
        if (cert > base && SetFilePointer(f, (LONG)(cert - base), NULL, FILE_BEGIN) != INVALID_SET_FILE_POINTER
            && ReadFile(f, c, sizeof c, &n, NULL) && n == sizeof c) {
            unsigned tid, ver;
            memcpy(&tid, c + 8, 4);
            memcpy(&ver, c + 0xAC, 4);
            if (tid == 0x56550034u)
                ed = ver == 2 ? AHT_EDITION_EU : ver == 1 ? AHT_EDITION_US : AHT_EDITION_UNKNOWN;
        }
    }
    CloseHandle(f);
    return ed;
}
#endif

#endif
