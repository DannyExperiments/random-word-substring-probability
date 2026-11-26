"""Render the path example as a rotating GIF and package the offline explorer."""

import math
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
W, H = 704, 835
BG, PANEL, EDGE = "#101b32", "#162640", "#385372"
TEXT, MUTED = "#f7faff", "#becbe1"
MINT, AMBER = "#6aead7", "#ffd086"
D = 16
PATH = ((0, 1), (1, 2))


def label(draw, xy, msg, size, color=TEXT, anchor="lt"):
    draw.text(xy, msg, font=ImageFont.load_default(size=size), fill=color, anchor=anchor)


def graph(draw, angle, bits):
    points = [(352 + 187 * math.cos(angle + j * 2 * math.pi / 3),
               400 + 83 * math.sin(angle + j * 2 * math.pi / 3)) for j in range(3)]
    assert all(abs(x - a) > 78 or abs(y - b) > 66
               for j, (x, y) in enumerate(points) for a, b in points[:j])
    platform = [(352 + 1.18 * (x - 352), 400 + 1.18 * (y - 400)) for x, y in points]
    draw.polygon(platform, fill="#203555", outline="#344d6d", width=2)
    for i, j in PATH:
        uncovered = not (bits[i] == "1" or bits[j] == "1")
        draw.line((points[i],points[j]),fill=AMBER if uncovered else MINT,width=9)
    for j in sorted(range(3), key=lambda j: points[j][1]):
        x, y = points[j]
        active = bits[j] == "1"
        draw.ellipse((x-31,y-24,x+31,y+5), fill="#0b1425")
        draw.line((x,y-29,x,y-12), fill=MINT if active else "#7189aa", width=10)
        draw.ellipse((x-30,y-60,x+30,y-1), fill="#167269" if active else "#40567a", outline=MINT if active else "#a0b1ca", width=3)
        label(draw, (x,y-32), str(j+1), 30, TEXT, "mm")
        label(draw, (x,y+12), bits[j], 25, MINT if active else MUTED, "mt")


def frame(angle, scene):
    bits = ("000","001","010","010")[scene]
    b = sum(bits[i] == bits[j] == "0" for i,j in PATH)
    subtotal = (D-1)**b * D**(2-b)
    assert (b,subtotal) == ((2,225),(1,240),(0,256),(0,256))[scene]
    image = Image.new("RGB", (W,H), BG)
    draw = ImageDraw.Draw(image)
    label(draw,(36,38),"EXACT SUBSTRING PROBABILITY",24,MINT)
    label(draw,(34,81),"The vertex-cover count",51)
    label(draw,(36,156),"One text block per edge of the path.",29,MUTED)
    draw.rounded_rectangle((32,208,672,529),21,fill=PANEL,outline=EDGE,width=2)
    label(draw,(52,233),"AMBER EDGE CAN MATCH",23,AMBER)
    label(draw,(652,233),"MINT EDGE IS COVERED",23,MINT,"rt")
    graph(draw,angle,bits)
    draw.rounded_rectangle((32,552,672,803),21,fill=PANEL,outline=EDGE,width=2)
    if scene < 3:
        label(draw,(55,578),f"Pattern bits {bits}",35)
        label(draw,(55,632),"Uncovered edges",29,MUTED)
        label(draw,(645,632),str(b),31,AMBER,"rt")
        label(draw,(55,685),"Text outcomes avoiding a match",27,MUTED)
        label(draw,(645,685),str(subtotal),31,TEXT,"rt")
        description = ("15 times 15 outcomes","15 times 16 outcomes","16 times 16 outcomes")[scene]
        label(draw,(55,742),description,27,MINT)
    else:
        label(draw,(55,578),"Sum over all 8 patterns",35)
        label(draw,(55,635),"Nonmatches",29,MUTED)
        label(draw,(645,635),"1985 of 2048",30,TEXT,"rt")
        label(draw,(55,686),"Match probability",29,MUTED)
        label(draw,(645,686),"63/2048",30,TEXT,"rt")
        label(draw,(55,742),"1985 mod 15 = 5 vertex covers",29,MINT)
    return image.convert("P",palette=Image.Palette.ADAPTIVE,colors=64)


def main():
    total = 72
    frames = [frame(2*math.pi*(index/total+.03),index//18) for index in range(total)]
    frames[0].save(HERE / "cover-residue.gif",save_all=True,append_images=frames[1:],
                   loop=0,duration=190,optimize=True)
    with ZipFile(HERE / "cover-residue-explorer.zip","w") as archive:
        for name in ("README.md","index.html"):
            info = ZipInfo(name,(1980,1,1,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info,(HERE / name).read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__ == "__main__":
    main()
