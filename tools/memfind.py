"""Finds a string in a running game's guest memory (identity-mapped below 4 GB) and the
pointers to it, with the words around each pointer. For locating game structures from text.
usage: memfind.py <pid> <text> [more texts...]
"""
import ctypes as C, struct, sys
from ctypes import wintypes as W

k = C.WinDLL('kernel32', use_last_error=True)
k.OpenProcess.restype = W.HANDLE
k.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
k.ReadProcessMemory.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, C.c_size_t, C.POINTER(C.c_size_t)]


class MBI(C.Structure):
    _fields_ = [('BaseAddress', C.c_ulonglong), ('AllocationBase', C.c_ulonglong), ('AllocationProtect', W.DWORD),
                ('PartitionId', W.WORD), ('RegionSize', C.c_ulonglong), ('State', W.DWORD), ('Protect', W.DWORD), ('Type', W.DWORD)]


k.VirtualQueryEx.argtypes = [W.HANDLE, C.c_void_p, C.POINTER(MBI), C.c_size_t]
h = k.OpenProcess(0x0410, False, int(sys.argv[1]))


def regions():
    a = 0x10000
    m = MBI()
    while a < 0x100000000 and k.VirtualQueryEx(h, a, C.byref(m), C.sizeof(m)):
        if m.State == 0x1000 and not (m.Protect & 0x101):
            buf = C.create_string_buffer(m.RegionSize)
            got = C.c_size_t()
            if k.ReadProcessMemory(h, m.BaseAddress, buf, m.RegionSize, C.byref(got)):
                yield m.BaseAddress, buf.raw[:got.value]
        a = m.BaseAddress + m.RegionSize


mem = list(regions())
for text in sys.argv[2:]:
    hits = []
    for pat in (text.encode('latin1'), text.encode('utf-16-le')):
        for base, data in mem:
            i = -1
            while (i := data.find(pat, i + 1)) >= 0:
                hits.append(base + i)
    print(f'"{text}": {len(hits)} copies:', ' '.join(f'{a:08X}' for a in hits[:20]))
    for a in hits[:20]:
        for t in range(a - 48, a + 4):  # pointer to the text or into its table line
            pat = struct.pack('<I', t)
            for base, data in mem:
                j = -1
                while (j := data.find(pat, j + 1)) >= 0:
                    if j % 4:
                        continue
                    around = struct.unpack_from('<8I', data, max(0, j - 16))
                    print(f'  ptr to {t:08X} at {base + j:08X}:', ' '.join(f'{w:08X}' for w in around))
