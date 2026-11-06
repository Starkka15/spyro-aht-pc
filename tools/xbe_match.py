"""Finds where a global of one XBE lives in another XBE built with the same library.

Takes each place the reference XBE's code mentions <va> (as a 32-bit absolute), uses the
surrounding code bytes as a signature with every absolute address masked out, finds the same
code in the target XBE, and reads the address at the same spot there.

usage: python -I xbe_match.py <ref.xbe> <target.xbe> <va_hex> [--window 24]
"""
import re, struct, sys
from collections import Counter


def load(path):
    d = open(path, 'rb').read()
    base = struct.unpack_from('<I', d, 0x104)[0]
    nsec, sec_hdr = struct.unpack_from('<II', d, 0x11C)
    secs = []
    for i in range(nsec):
        o = sec_hdr - base + i * 0x38
        flags, va, vsize, raw, rsize = struct.unpack_from('<IIIII', d, o)
        secs.append((va, vsize, raw, rsize))
    img = bytearray(max(va + vs for va, vs, _, _ in secs) - base)
    for va, vs, raw, rs in secs:
        img[va - base:va - base + rs] = d[raw:raw + rs]
    return base, bytes(img), secs


def is_addr(v, secs):
    return any(va <= v < va + vs for va, vs, _, _ in secs)


def masked(img, base, secs, off, n):
    """Bytes img[off:off+n] as a regex, with every word that looks like an in-image VA wildcarded."""
    b = img[off:off + n]
    mask = [False] * n
    for i in range(n - 3):
        if is_addr(struct.unpack_from('<I', b, i)[0], secs):
            for k in range(4):
                mask[i + k] = True
    return b''.join(b'.' if m else re.escape(bytes([c])) for c, m in zip(b, mask))


def main():
    ref, tgt, va = sys.argv[1], sys.argv[2], int(sys.argv[3], 16)
    win = int(sys.argv[sys.argv.index('--window') + 1]) if '--window' in sys.argv else 24
    rb, rimg, rsecs = load(ref)
    tb, timg, tsecs = load(tgt)
    needle = struct.pack('<I', va)
    votes = Counter()
    for m in re.finditer(re.escape(needle), rimg):
        at = m.start()
        lo = max(0, at - win)
        pat = masked(rimg, rb, rsecs, lo, at - lo + 4 + win)
        hits = [h.start() for h in re.finditer(pat, timg, re.S)]
        if len(hits) == 1:
            got = struct.unpack_from('<I', timg, hits[0] + (at - lo))[0]
            votes[got] += 1
            print(f'ref 0x{rb + at:08X} -> target 0x{tb + hits[0] + (at - lo):08X} holds 0x{got:08X}')
        else:
            print(f'ref 0x{rb + at:08X}: {len(hits)} matches')
    print('votes:', ', '.join(f'0x{v:08X} x{n}' for v, n in votes.most_common(5)) or 'none')


if __name__ == '__main__':
    main()
