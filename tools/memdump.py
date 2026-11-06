"""Dumps words of a running game's guest memory: memdump.py <pid> <hex addr> [words=64]"""
import ctypes as C, struct, sys
from ctypes import wintypes as W

k = C.WinDLL('kernel32')
k.OpenProcess.restype = W.HANDLE
k.ReadProcessMemory.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, C.c_size_t, C.POINTER(C.c_size_t)]
h = k.OpenProcess(0x0410, False, int(sys.argv[1]))
a = int(sys.argv[2], 16)
n = int(sys.argv[3]) if len(sys.argv) > 3 else 64
buf = C.create_string_buffer(n * 4)
got = C.c_size_t()
k.ReadProcessMemory(h, a, buf, n * 4, C.byref(got))
for i in range(0, got.value // 4, 4):
    ws = struct.unpack_from('<4I', buf.raw, i * 4)
    txt = ''.join(chr(b) if 32 <= b < 127 else '.' for b in buf.raw[i * 4:i * 4 + 16])
    print(f'{a + i * 4:08X}: ' + ' '.join(f'{w:08X}' for w in ws) + '  ' + txt)
