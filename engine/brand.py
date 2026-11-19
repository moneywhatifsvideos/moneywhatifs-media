"""Premium brand assets for The Money What Ifs (glow style)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mwi import font, FB, FM
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/brand"
os.makedirs(OUT, exist_ok=True)
GOLD = (218, 178, 92); GOLD_D = (150, 118, 52); GOLD_HI = (240, 210, 130); WHITE = (242, 240, 234); MID = (150, 150, 156); BG = (7, 7, 9)

def glowify(base, fg, strength=1.0, radius_frac=0.012):
    w, h = fg.size; r = max(2, int(min(w, h) * radius_frac))
    g1 = fg.filter(ImageFilter.GaussianBlur(r)); g2 = fg.filter(ImageFilter.GaussianBlur(r * 4))
    out = ImageChops.add(base, fg)
    out = ImageChops.add(out, ImageChops.multiply(g1, Image.new("RGB", fg.size, tuple([int(170 * strength)] * 3))))
    out = ImageChops.add(out, ImageChops.multiply(g2, Image.new("RGB", fg.size, tuple([int(110 * strength)] * 3))))
    return out

def stage(w, h, spots=(), vign=True, grid=True):
    img = Image.new("RGB", (w, h), BG); d = ImageDraw.Draw(img)
    if grid:
        step = max(24, w // 45)
        for y in range(step // 2, h, step):
            for x in range(step // 2, w, step): d.point((x, y), fill=(24, 24, 28))
    for (cx, top_w, bot_w, hh, power) in spots:
        m = Image.new("L", (w, h), 0); md = ImageDraw.Draw(m)
        md.polygon([(cx - top_w / 2, -10), (cx + top_w / 2, -10), (cx + bot_w / 2, hh), (cx - bot_w / 2, hh)], fill=power)
        md.ellipse([cx - bot_w / 2 - 20, hh - hh * 0.05, cx + bot_w / 2 + 20, hh + hh * 0.06], fill=power)
        m = m.filter(ImageFilter.GaussianBlur(min(w, h) * 0.035))
        img.paste(Image.new("RGB", (w, h), (255, 246, 225)), (0, 0), m)
    if vign:
        v = Image.new("L", (w, h), 0); ImageDraw.Draw(v).ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
        v = v.filter(ImageFilter.GaussianBlur(min(w, h) * 0.18))
        img = Image.composite(img, Image.new("RGB", (w, h), (0, 0, 0)), v)
    return img

def figure(d, x, y, s, c):
    hr = 30 * s; bw = 92 * s; bh = 118 * s
    d.rounded_rectangle([x - bw / 2, y - bh, x + bw / 2, y], radius=int(bw * 0.48), fill=c, corners=(True, True, False, False))
    hy = y - bh - hr - 8 * s; d.ellipse([x - hr, hy - hr, x + hr, hy + hr], fill=c)

def coin_ring(d, cx, cy, rx, ry, c, wd):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=c, width=wd)

def spaced(d, xy, s, sz, fill, sp=0.18, f=FB):
    fo = font(sz, f); ws = [d.textlength(ch, font=fo) for ch in s]; tot = sum(ws) + sz * sp * (len(s) - 1)
    x = xy[0] - tot / 2
    for ch, w in zip(s, ws): d.text((x, xy[1]), ch, font=fo, fill=fill, anchor="lm"); x += w + sz * sp
    return tot

# ---------------- profile picture ----------------
def qmark_layer(S, sz, cx, top):
    """Poppins Bold '?' without its dot. Returns (L mask, dot centre x, dot bottom y)."""
    L = Image.new("L", (S, S), 0); d = ImageDraw.Draw(L)
    d.text((cx, top), "?", font=font(sz), fill=255, anchor="mt")
    a = L.load(); rows = [any(a[x, y] for x in range(S)) for y in range(S)]
    ys = [y for y in range(S) if rows[y]]; y0, y1 = ys[0], ys[-1]
    # find gap between hook and dot, scanning up from the bottom
    y = y1
    while y > y0 and rows[y]: y -= 1
    gap = y
    while y > y0 and not rows[y]: y -= 1
    stem_bot = y
    xs = [x for x in range(S) for yy in range(gap, y1 + 1, 3) if a[x, yy]]
    dcx = (min(xs) + max(xs)) / 2
    d.rectangle([0, gap, S, S], fill=0)
    return L, dcx, y1, stem_bot

def clamp01(v): return max(0.0, min(1.0, v))

def soft_pool(img, cx, cy, rx, ry, col, alpha, blur):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur)); img.paste(Image.new("RGB", img.size, col), (0, 0), m)

def profile(S=1080):
    img = Image.new("RGB", (S, S), (8, 8, 10))
    # spotlight cone
    m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
    md.polygon([(S * 0.44, -10), (S * 0.56, -10), (S * 0.78, S * 0.9), (S * 0.22, S * 0.9)], fill=34)
    img.paste(Image.new("RGB", (S, S), (255, 244, 220)), (0, 0), m.filter(ImageFilter.GaussianBlur(S * 0.04)))
    fig_h = S * 0.25; top = S * 0.10; GAPF = 0.05
    for k in range(40):  # size the ? so that the figure (as its dot) ends at ~0.87
        sz = int(S * (0.6 + k * 0.02)); q, dcx, dbot, gap = qmark_layer(S, sz, S * 0.47, top)
        if gap + S * GAPF + fig_h >= S * 0.84: break
    q, dcx, dbot, gap = qmark_layer(S, sz, S * 0.47 + (S * 0.5 - dcx), top)  # centre stem + figure under the beam
    ys = [y for y in range(S) if q.getpixel((int(dcx), y)) or any(q.getpixel((x, y)) for x in range(0, S, 6))]
    gy0, gy1 = min(ys), max(ys)
    grad = Image.new("RGB", (S, S)); gd = ImageDraw.Draw(grad)
    for y in range(S):
        f = clamp01((y - gy0) / max(1, gy1 - gy0)); c0, c1 = (242, 208, 130), (184, 142, 60)
        gd.line([(0, y), (S, y)], fill=tuple(int(c0[i] + (c1[i] - c0[i]) * f) for i in range(3)))
    qg = q.filter(ImageFilter.GaussianBlur(S * 0.008)).point(lambda v: int(v * 0.25))
    img.paste(Image.new("RGB", (S, S), GOLD), (0, 0), qg); img.paste(grad, (0, 0), q)
    # figure replaces the dot
    feet = gap + S * GAPF + fig_h; fs = fig_h / 186  # figure() height ~186*s
    soft_pool(img, dcx, feet, S * 0.12, S * 0.0175, GOLD, 140, S * 0.008)
    fg = Image.new("RGB", (S, S), (0, 0, 0)); d = ImageDraw.Draw(fg)
    figure(d, dcx, feet, fs, (244, 242, 236))
    g = fg.filter(ImageFilter.GaussianBlur(S * 0.015))
    img = ImageChops.add(img, fg); img = ImageChops.add(img, ImageChops.multiply(g, Image.new("RGB", (S, S), (128, 128, 128))))
    return img

# ---------------- YouTube banner ----------------
def banner(W=2560, H=1440):
    img = Image.new("RGB", (W, H), (8, 8, 10)); d0 = ImageDraw.Draw(img)
    for y in range(20, H, 46):
        for x in range(20, W, 46): d0.point((x, y), fill=(22, 22, 26))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([(W / 2 - 130, -10), (W / 2 + 130, -10), (W / 2 + 560, H * 0.74), (W / 2 - 560, H * 0.74)], fill=26)
    img.paste(Image.new("RGB", (W, H), (255, 244, 220)), (0, 0), m.filter(ImageFilter.GaussianBlur(70)))
    cy = H / 2
    # left prop: compound growth curve with gold gradient fill (inside desktop band, outside mobile-safe width)
    x0, x1, base, top = 200, 470, cy + 150, cy - 140
    pts = [(x0 + (x1 - x0) * i / 59, base - (base - top) * ((1.08 ** i - 1) / (1.08 ** 59 - 1))) for i in range(60)]
    fill = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fill); fd.polygon(pts + [(x1, base), (x0, base)], fill=255)
    grad = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(grad)
    for y in range(int(top), int(base) + 1): gd.line([(x0, y), (x1, y)], fill=int(88 * (1 - (y - top) / (base - top))))
    img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), ImageChops.multiply(fill, grad))
    fg = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(fg)
    d.line([(x0, base), (x1 + 20, base)], fill=(60, 56, 50), width=3)
    cl = ImageDraw.Draw(img); cl.line(pts, fill=GOLD, width=10, joint="curve"); hx, hy = pts[-1]; cl.ellipse([hx - 13, hy - 13, hx + 13, hy + 13], fill=GOLD_HI)
    cg = Image.new("RGB", (W, H)); ImageDraw.Draw(cg).line(pts, fill=GOLD, width=10, joint="curve")
    img = ImageChops.add(img, ImageChops.multiply(cg.filter(ImageFilter.GaussianBlur(9)), Image.new("RGB", (W, H), (64, 64, 64))))
    # right prop: crowd with lit hero on a gold pool
    soft_pool(img, 2230, cy + 150, 80, 16, GOLD, 120, 8)
    for i, x in enumerate((2120, 2230, 2340, 2440)):
        figure(d, x, cy + 150, 1.0 if i == 1 else 0.8, (244, 242, 236) if i == 1 else (78, 74, 70))
    # type
    spaced(d, (W / 2, cy - 62), "THE MONEY WHAT IFS", int(H * 0.064), (244, 242, 236), 0.12)
    d.line([(W / 2 - 70, cy + 6), (W / 2 + 70, cy + 6)], fill=GOLD, width=3)
    spaced(d, (W / 2, cy + 62), "UK MONEY, EXPLAINED IN 60 SECONDS", int(H * 0.022), GOLD, 0.25, FM)
    spaced(d, (W / 2, cy + 116), "NEW VIDEOS EVERY DAY", int(H * 0.0145), (140, 140, 146), 0.34, FM)
    g = fg.filter(ImageFilter.GaussianBlur(8))
    img = ImageChops.add(img, fg); img = ImageChops.add(img, ImageChops.multiply(g, Image.new("RGB", (W, H), (76, 76, 76))))
    return img

if __name__ == "__main__":
    p = profile(); p.save(os.path.join(OUT, "profile_1080.png"))
    p.resize((110, 110), Image.LANCZOS).save(os.path.join(OUT, "profile_small_preview.png"))
    b = banner(); b.save(os.path.join(OUT, "youtube_banner_2560x1440.png"))
    # previews: circle crop + banner safe areas
    m = Image.new("L", (1080, 1080), 0); ImageDraw.Draw(m).ellipse([0, 0, 1080, 1080], fill=255)
    c = Image.new("RGB", (1080, 1080), (255, 255, 255)); c.paste(p, (0, 0), m); c.save(os.path.join(OUT, "profile_circle_preview.png"))
    bp = b.copy(); bd = ImageDraw.Draw(bp)
    bd.rectangle([(2560 - 1546) / 2, (1440 - 423) / 2, (2560 + 1546) / 2, (1440 + 423) / 2], outline=(255, 0, 0), width=4)
    bd.rectangle([0, (1440 - 423) / 2, 2560, (1440 + 423) / 2], outline=(0, 160, 255), width=3)
    bp.resize((1280, 720)).save(os.path.join(OUT, "banner_safe_area_preview.png"))
    print("ok")
