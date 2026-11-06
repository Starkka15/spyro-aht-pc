"""Turns an XBE's $$XTIMAGE title image (XPR0, one DXT texture) into an .ico and a .png.

usage: xbe_icon.py <default.xbe> <out.ico> [out.png]
Needs Pillow. Run with -I so nothing beside the game files is imported.
"""
import io
import struct
import sys

from PIL import Image


def section(xbe, name):
    base = struct.unpack_from('<I', xbe, 0x104)[0]
    count, hdr = struct.unpack_from('<II', xbe, 0x11C)
    for i in range(count):
        off = hdr - base + i * 56
        flags, va, vsize, raw, rsize, name_addr = struct.unpack_from('<6I', xbe, off)
        n = xbe[name_addr - base:].split(b'\0', 1)[0].decode('ascii', 'replace')
        if n == name:
            return xbe[raw:raw + rsize]
    raise SystemExit('no section ' + name)


def main():
    xbe = open(sys.argv[1], 'rb').read()
    xpr = section(xbe, '$$XTIMAGE')
    magic, total, hdr_size = struct.unpack_from('<4sII', xpr, 0)
    if magic != b'XPR0':
        raise SystemExit('not XPR0: %r' % magic)
    common, data, lock, fmt, size = struct.unpack_from('<5I', xpr, 12)
    color = (fmt >> 8) & 0xFF
    w, h = 1 << ((fmt >> 20) & 0xF), 1 << ((fmt >> 24) & 0xF)
    fourcc = {0x0C: b'DXT1', 0x0E: b'DXT3', 0x0F: b'DXT5'}.get(color)
    if not fourcc:
        raise SystemExit('format %02X not handled' % color)
    blocks = ((w + 3) // 4) * ((h + 3) // 4) * (8 if fourcc == b'DXT1' else 16)
    pixels = xpr[hdr_size + data:hdr_size + data + blocks]
    dds = (b'DDS ' + struct.pack('<7I', 124, 0x1007 | 0x80000, h, w, len(pixels), 0, 1) + b'\0' * 44
           + struct.pack('<2I4s5I', 32, 4, fourcc, 0, 0, 0, 0, 0)
           + struct.pack('<5I', 0x1000, 0, 0, 0, 0))
    img = Image.open(io.BytesIO(dds + pixels)).convert('RGBA')
    print('%ux%u %s' % (w, h, fourcc.decode()))
    img.save(sys.argv[2], sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128)])
    if len(sys.argv) > 3:
        img.save(sys.argv[3])


main()
