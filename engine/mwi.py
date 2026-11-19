#!/usr/bin/env python3
"""The Money What Ifs - video engine.

Usage:  python3 mwi.py spec.json OUTDIR [--stills]
Builds voiceover (Kokoro TTS), renders scenes from templates, adds captions,
music bed + SFX, joins to OUTDIR/<slug>.mp4 and makes OUTDIR/<slug>_thumbnail.png.
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.environ.get("MWI_TTS_DIR", os.path.expanduser("~/kokoro"))
W, H, FPS = 1080, 1920, 30
SR = 24000
VOICE_POLISH = ("highpass=f=70,equalizer=f=200:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,"
                "acompressor=threshold=-18dB:ratio=3:attack=5:release=80")
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
_fc = {}
def font(sz, f=FB):
    sz = max(4, int(sz)); k = (sz, f)
    if k not in _fc: _fc[k] = ImageFont.truetype(f, sz)
    return _fc[k]

NAVY = (17, 22, 48); NAVY2 = (28, 35, 72); RIM = (70, 82, 140)
COL = {"yellow": (255, 210, 60), "red": (255, 92, 92), "white": (245, 245, 250), "blue": (52, 120, 230),
       "grey": (150, 158, 195), "green": (80, 210, 130), "pink": (230, 120, 170), "navy": NAVY, "dark": (70, 70, 90)}
def C(c): return COL.get(c, c) if isinstance(c, str) else tuple(c)
YEL, RED, WHITE, GREY, GREEN, BLUE = C("yellow"), C("red"), C("white"), C("grey"), C("green"), C("blue")

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ---------------- backgrounds ----------------
def make_bg(top, bot):
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        f = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - f) + bot[i] * f) for i in range(3)))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for x in range(0, W, 60): gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 8))
    for y in range(0, H, 60): gd.line([(0, y), (W, y)], fill=(255, 255, 255, 8))
    bg.paste(g, (0, 0), g); return bg
BG = make_bg(NAVY2, NAVY)
BG_DARK = make_bg((12, 14, 30), (5, 6, 14))

def draw_char():
    """The channel mascot: black-headed figure peeking over a gold £ coin (transparent RGBA)."""
    S = 2160; img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    GD, GDD, GL, GO = (214, 150, 25), (160, 105, 10), (255, 228, 120), (255, 200, 55)
    cx, cy, R = 1080, 1340, 600; hx, hy, hr = 1080, 650, 330
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(8, 8, 12), outline=(80, 95, 160), width=14)
    for sx in (-1, 1):
        ex = hx + sx * 120 + 25; ey = hy - 30
        d.ellipse([ex - 78, ey - 78, ex + 78, ey + 78], fill=(248, 248, 252))
        d.ellipse([ex - 4, ey - 62, ex + 64, ey + 6], fill=(8, 8, 12))
        d.ellipse([ex + 38, ey - 60, ex + 52, ey - 46], fill=(255, 255, 255))
    d.arc([hx + 50, hy - 230, hx + 250, hy - 110], 200, 330, fill=(248, 248, 252), width=26)
    d.line([(hx - 235, hy - 150), (hx - 60, hy - 135)], fill=(248, 248, 252), width=26)
    sh = Image.new("L", (S, S), 0); ImageDraw.Draw(sh).ellipse([cx - R + 30, cy - R + 90, cx + R + 30, cy + R + 90], fill=150)
    img.paste(Image.new("RGBA", (S, S), (5, 6, 18, 255)), (0, 0), sh.filter(ImageFilter.GaussianBlur(50))); d = ImageDraw.Draw(img)
    d.ellipse([cx - R, cy - R + 50, cx + R, cy + R + 50], fill=GDD)
    for k in range(72):
        a = k * 2 * math.pi / 72
        if math.sin(a) > -0.2:
            x1 = cx + R * 0.985 * math.cos(a); y1 = cy + 50 + R * 0.985 * math.sin(a)
            d.line([(x1, y1 - 40), (x1, y1)], fill=(130, 85, 8), width=8)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=GD)
    d.ellipse([cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30], fill=GO)
    d.ellipse([cx - R + 95, cy - R + 95, cx + R - 95, cy + R - 95], outline=GD, width=16)
    for k in range(48):
        a = k * 2 * math.pi / 48; x = cx + (R - 140) * math.cos(a); y = cy + (R - 140) * math.sin(a)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=GD)
    f = font(720)
    d.text((cx + 18, cy + 50), "£", font=f, fill=GDD, anchor="mm"); d.text((cx - 8, cy + 22), "£", font=f, fill=GL, anchor="mm")
    d.text((cx, cy + 34), "£", font=f, fill=GD, anchor="mm")
    for hxp in (cx - 250, cx + 250):
        yy = (R - math.sqrt(R * R - (hxp - cx) ** 2)) + cy - R + 10
        d.ellipse([hxp - 85, yy - 70, hxp + 85, yy + 70], fill=(8, 8, 12), outline=(80, 95, 160), width=10)
        for fx in (-45, 0, 45): d.line([(hxp + fx, yy + 5), (hxp + fx, yy + 60)], fill=(80, 95, 160), width=8)
    q = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(q).text((1690, 470), "?", font=font(420), fill=(255, 210, 60, 255), anchor="mm", stroke_width=22, stroke_fill=(8, 8, 12))
    q = q.rotate(-14, center=(1690, 470), resample=Image.BICUBIC); img.paste(q, (0, 0), q)
    img = img.crop(img.getbbox()); img.thumbnail((900, 900), Image.LANCZOS); return img
CHAR = draw_char()

# ---------------- drawing helpers ----------------
def text_c(d, xy, s, sz, fill, f=FB, stroke=0, anchor="mm"):
    d.text(xy, s, font=font(sz, f), fill=C(fill), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))

def pop_text(img, xy, s, sz, fill, p, f=FB, stroke=6):
    if p <= 0: return
    text_c(ImageDraw.Draw(img), xy, s, sz * max(0.05, back(p)), fill, f, stroke)

def fit_size(s, sz, maxw=980, f=FB):
    while sz > 20 and font(sz, f).getlength(s) + 20 > maxw: sz -= 4
    return sz

def fmt(v, spec):
    pre, suf = spec.get("prefix", ""), spec.get("suffix", "")
    dec = spec.get("decimals", 0)
    if spec.get("short"):
        a = abs(v)
        if a >= 1e9: s = f"{v/1e9:.1f}".rstrip("0").rstrip(".") + "B"
        elif a >= 1e6: s = f"{v/1e6:.2f}".rstrip("0").rstrip(".") + "M"
        elif a >= 1e4: s = f"{v/1e3:.0f}K"
        else: s = f"{v:,.0f}"
    else:
        s = f"{v:,.{dec}f}"
    return pre + s + suf

def figure(d, cx, cy, s=1.0, shirt=BLUE, mood="neutral", arm="down", look=0, tie=False, sit=False):
    hr = 62 * s; lw = max(4, int(13 * s)); K = (10, 10, 16)
    bt = cy + hr * 0.9; bb = bt + 150 * s
    if sit:
        d.line([(cx - 14 * s, bb), (cx + 70 * s, bb), (cx + 70 * s, bb + 95 * s)], fill=K, width=lw)
        d.line([(cx + 14 * s, bb), (cx + 95 * s, bb), (cx + 95 * s, bb + 95 * s)], fill=K, width=lw)
    else:
        d.line([(cx - 10 * s, bb), (cx - 38 * s, bb + 150 * s)], fill=K, width=lw)
        d.line([(cx + 10 * s, bb), (cx + 38 * s, bb + 150 * s)], fill=K, width=lw)
    sh = bt + 22 * s
    A = {"down": [(-34, 0, -60, 120), (34, 0, 60, 120)], "up": [(-34, 0, -95, -110), (34, 0, 95, -110)],
         "hold": [(-34, 0, -20, 70), (34, 0, 90, 40)], "point": [(-34, 0, -60, 120), (34, 0, 150, -10)],
         "shrug": [(-34, 0, -110, -20), (34, 0, 110, -20)]}[arm]
    for a, b, c_, e in A: d.line([(cx + a * s, sh + b * s), (cx + c_ * s, sh + e * s)], fill=K, width=lw)
    d.rounded_rectangle([cx - 40 * s, bt, cx + 40 * s, bb + 6 * s], radius=int(30 * s), fill=C(shirt))
    if tie: d.polygon([(cx, bt + 8 * s), (cx - 12 * s, bt + 70 * s), (cx, bt + 92 * s), (cx + 12 * s, bt + 70 * s)], fill=RED)
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(8, 8, 12), outline=RIM, width=max(2, int(4 * s)))
    ey = cy - 8 * s; er = (17 if mood == "shock" else 13) * s
    for sx in (-1, 1):
        x = cx + sx * 22 * s + look * 10 * s
        d.ellipse([x - er, ey - er, x + er, ey + er], fill=WHITE)
        pr = er * 0.45; d.ellipse([x - pr + look * 4 * s, ey - pr, x + pr + look * 4 * s, ey + pr], fill=(8, 8, 12))
    my = cy + 28 * s; w5 = max(2, int(5 * s))
    if mood == "happy": d.arc([cx - 24 * s, my - 18 * s, cx + 24 * s, my + 14 * s], 10, 170, fill=WHITE, width=w5)
    elif mood == "sad": d.arc([cx - 20 * s, my, cx + 20 * s, my + 26 * s], 200, 340, fill=WHITE, width=w5)
    elif mood == "shock": d.ellipse([cx - 9 * s, my - 6 * s, cx + 9 * s, my + 14 * s], outline=WHITE, width=max(2, int(4 * s)))
    elif mood == "smug":
        d.arc([cx - 20 * s, my - 10 * s, cx + 24 * s, my + 10 * s], 20, 120, fill=WHITE, width=w5)
    else: d.line([(cx - 14 * s, my + 4 * s), (cx + 14 * s, my + 4 * s)], fill=WHITE, width=w5)

def mini_head(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 10, 20), outline=RIM, width=2)
    e = max(2, r // 4)
    for sx in (-1, 1): d.ellipse([cx + sx * r * .45 - e, cy - e, cx + sx * r * .45 + e, cy + e], fill=WHITE)

def icon(d, kind, x, y, s=1.0):
    if kind == "pint":
        d.polygon([(x - 80 * s, y - 150 * s), (x + 80 * s, y - 150 * s), (x + 62 * s, y + 150 * s), (x - 62 * s, y + 150 * s)], fill=(235, 170, 50))
        d.rectangle([x - 82 * s, y - 175 * s, x + 82 * s, y - 135 * s], fill=WHITE)
    elif kind == "bread":
        d.rounded_rectangle([x - 150 * s, y - 80 * s, x + 150 * s, y + 90 * s], radius=int(70 * s), fill=(205, 140, 70))
        for k in (-70, 0, 70): d.line([(x + (k - 20) * s, y - 60 * s), (x + (k + 20) * s, y + 10 * s)], fill=(240, 200, 130), width=int(10 * s))
    elif kind == "house":
        d.polygon([(x - 200 * s, y - 30 * s), (x, y - 190 * s), (x + 200 * s, y - 30 * s)], fill=RED)
        d.rectangle([x - 160 * s, y - 30 * s, x + 160 * s, y + 170 * s], fill=(235, 225, 205))
        d.rectangle([x - 40 * s, y + 60 * s, x + 40 * s, y + 170 * s], fill=NAVY)
        for k in (-105, 105): d.rectangle([x + (k - 35) * s, y + 10 * s, x + (k + 35) * s, y + 70 * s], fill=(120, 170, 230))
    elif kind == "coffee":
        d.polygon([(x - 90 * s, y - 120 * s), (x + 90 * s, y - 120 * s), (x + 70 * s, y + 130 * s), (x - 70 * s, y + 130 * s)], fill=WHITE)
        d.rectangle([x - 86 * s, y - 40 * s, x + 86 * s, y + 30 * s], fill=(140, 90, 50))
        d.rounded_rectangle([x - 100 * s, y - 160 * s, x + 100 * s, y - 115 * s], radius=int(12 * s), fill=(60, 60, 70))
    elif kind == "coin":
        d.ellipse([x - 120 * s, y - 110 * s, x + 120 * s, y + 130 * s], fill=(160, 105, 10))
        d.ellipse([x - 120 * s, y - 120 * s, x + 120 * s, y + 120 * s], fill=(255, 200, 55), outline=(214, 150, 25), width=int(10 * s))
        text_c(d, (x, y + 8 * s), "£", 150 * s, (214, 150, 25))
    elif kind == "cash":
        for i in range(12):
            r, c = divmod(i, 4); xx = x - 150 * s + c * 100 * s + (r % 2) * 50 * s; yy = y + 60 * s - r * 42 * s
            d.rounded_rectangle([xx - 46 * s, yy - 20 * s, xx + 46 * s, yy + 20 * s], radius=6, fill=(110, 170, 90), outline=(60, 110, 50), width=3)
    elif kind == "ticket":
        d.rounded_rectangle([x - 200 * s, y - 120 * s, x + 200 * s, y + 120 * s], radius=int(24 * s), fill=(250, 246, 232))
        d.rectangle([x - 200 * s, y - 120 * s, x + 200 * s, y - 60 * s], fill=YEL)
        text_c(d, (x, y - 90 * s), "LOTTERY", 34 * s, NAVY)
        for i in range(5):
            cx = x - 140 * s + i * 70 * s; d.ellipse([cx - 28 * s, y - 10 * s, cx + 28 * s, y + 46 * s], fill=RED if i % 2 else BLUE)
            text_c(d, (cx, y + 18 * s), str([7, 14, 22, 35, 41][i]), 26 * s, WHITE)

# ---------------- captions ----------------
def build_chunks(TL):
    chunks = []
    for sc in TL:
        for ln in sc["lines"]:
            words = ln["text"].split(); wts = [len(w) + 2 for w in words]; tot = sum(wts)
            t = ln["start"]; dur = ln["end"] - ln["start"]; times = []
            for w, wt in zip(words, wts): times.append((w, t, t + dur * wt / tot)); t += dur * wt / tot
            cur = []
            for w in times:
                cur.append(w); L = sum(len(x[0]) for x in cur) + len(cur)
                if len(cur) >= 3 or L > 15 or w[0][-1] in ".?,!": chunks.append(cur); cur = []
            if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0][1] if i + 1 < len(chunks) else 999
        out.append((c[0][1], min(end, c[-1][2] + 0.6), c))
    return out

def draw_captions(img, T, chunks):
    d = ImageDraw.Draw(img)
    for st, en, words in chunks:
        if st <= T < en:
            p = ease((T - st) / 0.12)
            txts = [w[0].upper() for w in words]
            sz = int(84 * (0.85 + 0.15 * p))
            sz = min(sz, fit_size(" ".join(txts), sz, 1000))
            f = font(sz); widths = [d.textlength(x, font=f) for x in txts]; sp = d.textlength(" ", font=f)
            x = W / 2 - (sum(widths) + sp * (len(txts) - 1)) / 2
            for (w, ws, we), tx, wd in zip(words, txts, widths):
                d.text((x, 1430), tx, font=f, fill=YEL if ws <= T < we + 0.05 else WHITE, anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0))
                x += wd + sp
            return

# ---------------- scene context ----------------
class Ctx:
    def __init__(self, sc, t, instant=False): self.sc, self.t, self.instant = sc, t, instant
    def lt(self, at):
        """at may be a line index (int), [line, offset] or a float time in seconds"""
        if isinstance(at, list): return self.lt(at[0]) + at[1]
        if isinstance(at, float): return at
        ls = self.sc["lines"]; i = min(at, len(ls) - 1)
        return ls[i]["start"] - self.sc["start"]
    def p(self, at, dur=0.35):
        if self.instant and self.lt(at) <= 0.3: return 1.0  # hook: claim on screen from frame 1
        return (self.t - self.lt(at)) / dur
    def shown(self, it):
        st = self.lt(it.get("at", 0))
        if self.instant and st <= 0.3: st = 0.0  # hook: visible from frame 1
        return self.t >= st and ("until" not in it or self.t < self.lt(it["until"]))

def counter_value(ctx, cs):
    """cs: {from, to, at, dur} or {keys:[[at, value, dur], ...], from}"""
    if "keys" in cs:
        v = cs.get("from", 0)
        for at, val, *dr in cs["keys"]:
            dur = dr[0] if dr else 1.0
            pr = ease((ctx.t - ctx.lt(at)) / dur)
            if pr <= 0: break
            v = v + (val - v) * pr
        return v
    return cs.get("from", 0) + (cs["to"] - cs.get("from", 0)) * ease((ctx.t - ctx.lt(cs.get("at", 0))) / cs.get("dur", 1.4))

def draw_hud(img, ctx, hud):
    d = ImageDraw.Draw(img)
    if hud.get("left"): d.text((60, 210), hud["left"], font=font(44), fill=RED)
    if hud.get("sub"): d.text((60, 262), hud["sub"], font=font(36, FM), fill=GREY)
    if hud.get("right"):
        r = hud["right"]
        d.text((W - 60, 210), r["label"], font=font(34, FM), fill=GREY, anchor="ra")
        v = r["text"] if "text" in r else fmt(counter_value(ctx, r), r)
        d.text((W - 60, 250), v, font=font(68), fill=C(r.get("color", "yellow")), anchor="ra")

# ---------------- templates ----------------
def items_stack(img, ctx, items, top=330, gap=1.0):
    """Vertical stack of text/counter items, auto-laid out from `top`."""
    y = top
    for it in items:
        sz = it.get("size", 80)
        if ctx.shown(it):
            s = it["text"] if "text" in it else fmt(counter_value(ctx, it["counter"]), it["counter"])
            if "counter" in it:  # size to the final value so it doesn't jump
                fin = fmt(it["counter"].get("to", it["counter"].get("keys", [[0, 0]])[-1][1]), it["counter"])
                sz = fit_size(fin, sz)
            else:
                sz = fit_size(s, sz)
            pop_text(img, (W / 2, y + sz * 0.6), s, sz, it.get("color", "white"), ctx.p(it.get("at", 0), 0.3), stroke=max(4, sz // 11))
        y += sz * 1.25 * gap + it.get("space", 0)
    return y

def T_stack(img, ctx, sc):
    d = ImageDraw.Draw(img)
    if sc.get("crowd"):
        rnd = random.Random(4)
        for i in range(220):
            x, y, dl = rnd.random(), rnd.random(), rnd.random() * 0.9
            pr = 1.0 if ctx.instant else ease((ctx.t - dl * 2.2) / 0.3)
            if pr > 0: mini_head(d, 40 + x * (W - 80), 300 + y * 900, int(26 * pr))
        ov = Image.new("RGBA", (W, H), (10, 12, 28, 150)); img.paste(ov, (0, 0), ov)
    y = items_stack(img, ctx, sc.get("items", []), sc.get("top", 330))
    d = ImageDraw.Draw(img)
    for ic in sc.get("icons", []):
        if ctx.shown(ic):
            pr = back(ctx.p(ic.get("at", 0), 0.35)); s = ic.get("scale", 1) * max(0.01, pr)
            icon(d, ic["kind"], ic.get("x", 540), ic.get("y", max(y + 160, 1000)), s)
    if "figure" in sc:
        f = sc["figure"]
        if ctx.shown(f):
            pr = ease(ctx.p(f.get("at", 0), 0.4))
            figure(d, f.get("x", 540), f.get("y", 1020) + (1 - pr) * 500, f.get("scale", 1.2), f.get("shirt", "blue"),
                   f.get("mood", "neutral"), f.get("arm", "down"), f.get("look", 0), f.get("tie", False))

def T_figures(img, ctx, sc):
    d = ImageDraw.Draw(img)
    for f in sc["figures"]:
        if not ctx.shown(f): continue
        pr = ease(ctx.p(f.get("at", 0), 0.4))
        mood = f.get("mood", "happy"); arm = f.get("arm", "down")
        for ch in f.get("changes", []):  # [{at, mood, arm}]
            if ctx.t >= ctx.lt(ch["at"]): mood = ch.get("mood", mood); arm = ch.get("arm", arm)
        x, y, s = f.get("x", 330), f.get("y", 640), f.get("scale", 1.5)
        figure(d, x, y + (1 - pr) * 600, s, f.get("shirt", "blue"), mood, arm, f.get("look", 0), f.get("tie", False))
        if f.get("label") and pr > 0.6: text_c(d, (x, y - 110 * s), f["label"], 50, YEL, stroke=6)
    for sg in sc.get("signs", []):  # cards that appear/replace each other
        if not ctx.shown(sg): continue
        pr = back(ctx.p(sg.get("at", 0), 0.35))
        x, y, w, h = sg.get("x", 780), sg.get("y", 620), sg.get("w", 440), sg.get("h", 200)
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=22, fill=WHITE)
        sz = fit_size(sg["text"], sg.get("size", 80), w - 30)
        text_c(d, (x, y + (sg.get("sub") and -25 or 0)), sg["text"], sz * max(0.05, pr), sg.get("color", "red"))
        if sg.get("sub"): text_c(d, (x, y + 55), sg["sub"], 34 * max(0.05, pr), GREY, FM)
    items_stack(img, ctx, sc.get("items", []), sc.get("top", 1050))

def T_phone(img, ctx, sc):
    d = ImageDraw.Draw(img); t = ctx.t
    pw, ph = 560, 1000; x0 = W / 2 - pw / 2; y0 = 250 + (1 - ease(t / 0.5)) * 300
    d.rounded_rectangle([x0 - 18, y0 - 18, x0 + pw + 18, y0 + ph + 18], radius=80, fill=(8, 8, 12), outline=RIM, width=4)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=64, fill=(232, 236, 248))
    d.rounded_rectangle([x0 + pw / 2 - 80, y0 + 22, x0 + pw / 2 + 80, y0 + 60], radius=20, fill=(8, 8, 12))
    text_c(d, (x0 + pw / 2, y0 + 140), sc.get("app", "MY BANK"), 44, NAVY)
    text_c(d, (x0 + pw / 2, y0 + 250), sc.get("balance_label", "Current balance"), 32, GREY, FM)
    b = sc["balance"]; v = counter_value(ctx, b)
    text_c(d, (x0 + pw / 2, y0 + 330), fmt(v, b), fit_size(fmt(v, b), 66, pw - 40), C(b.get("color", "navy")))
    n = sc.get("notification")
    if n and ctx.shown(n):
        pn = ease(ctx.p(n.get("at", 0), 0.4)); ny = y0 + 440 - (1 - pn) * 60
        d.rounded_rectangle([x0 + 30, ny, x0 + pw - 30, ny + 150], radius=30, fill=WHITE, outline=(210, 214, 230), width=2)
        d.ellipse([x0 + 55, ny + 40, x0 + 125, ny + 110], fill=GREEN); text_c(d, (x0 + 90, ny + 75), "£", 40, WHITE)
        d.text((x0 + 145, ny + 38), n["title"], font=font(30), fill=NAVY)
        d.text((x0 + 145, ny + 80), n["body"], font=font(28, FM), fill=GREY)
    f = sc.get("figure", {"at": 0.8, "mood": "shock"})
    if ctx.shown(f):
        pr = ease(ctx.p(f.get("at", 0), 0.4))
        figure(d, 170, 1180 + (1 - pr) * 400, 1.1, mood=f.get("mood", "shock"), look=1)

def T_bars(img, ctx, sc):
    d = ImageDraw.Draw(img)
    items_stack(img, ctx, sc.get("items", []), sc.get("top", 260))
    bars = sc["bars"]; base = sc.get("base", 1180); maxh = sc.get("maxh", 600)
    vmax = max(b["value"] for b in bars); n = len(bars); bw = 240 if n <= 2 else 200
    gapx = (W - 160) / n
    d.line([(100, base), (W - 100, base)], fill=WHITE, width=4)
    for i, b in enumerate(bars):
        pr = ease((ctx.t - ctx.lt(b.get("at", 0))) / b.get("dur", 1.2))
        if ctx.t < ctx.lt(b.get("at", 0)): continue
        cx = 80 + gapx * (i + 0.5); h = max(4, maxh * b["value"] / vmax * pr)
        d.rounded_rectangle([cx - bw / 2, base - h, cx + bw / 2, base], radius=12, fill=C(b.get("color", "yellow")))
        lab = fmt(b["value"] * pr, b)
        text_c(d, (cx, base - h - 50), lab, fit_size(fmt(b["value"], b), 58, gapx - 10), WHITE, stroke=5)
        text_c(d, (cx, base + 50), b["label"], fit_size(b["label"], 36, gapx - 10, FM), C(b.get("label_color", "grey")), FM)
        if b.get("sub"): text_c(d, (cx, base + 95), b["sub"], 30, GREY, FM)
    for it in sc.get("callouts", []):
        if ctx.shown(it): pop_text(img, (it.get("x", 540), it.get("y", 600)), it["text"], it.get("size", 110), it.get("color", "red"), ctx.p(it.get("at", 0), 0.3), stroke=9)

def T_tags(img, ctx, sc):
    d = ImageDraw.Draw(img)
    for i, tg in enumerate(sc["tags"]):
        if not ctx.shown(tg): continue
        y = tg.get("y", 560 + i * 450)
        if tg.get("icon"): icon(d, tg["icon"], 280, y, tg.get("icon_scale", 1.0) * ease(ctx.p(tg.get("at", 0), 0.4)))
        x = 720 if tg.get("icon") else 540
        v = counter_value(ctx, tg)
        hw = 230 if tg.get("icon") else 380
        d.rounded_rectangle([x - hw, y - 95, x + hw, y + 95], radius=24, fill=WHITE)
        d.ellipse([x - hw + 20, y - 15, x - hw + 50, y + 15], fill=NAVY)
        text_c(d, (x + 20, y - 45), tg["label"], fit_size(tg["label"], 34, 2 * hw - 110, FM), GREY, FM)
        s = fmt(v, tg); text_c(d, (x + 20, y + 25), s, fit_size(s, 78, 2 * hw - 110), C(tg.get("color", "red")))
    items_stack(img, ctx, sc.get("items", []), sc.get("top", 1150))

def series_vals(sr, x):
    k = sr["kind"]
    if k == "annuity":  # yearly payment pmt from x0, growth r
        n = max(0, x - sr["x0"]); r = sr["r"]
        return sr["pmt"] * ((1 + r) ** n - 1) / r if r else sr["pmt"] * n
    if k == "linear": return max(0, x - sr["x0"]) * sr["pmt"]
    if k == "decay": return sr["v0"] / (1 + sr["r"]) ** max(0, x - sr["x0"])
    if k == "points":  # piecewise-linear through [[x, y], ...]
        pts = sr["points"]
        if x <= pts[0][0]: return pts[0][1]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            if x <= xb: return ya + (yb - ya) * (x - xa) / (xb - xa)
        return pts[-1][1]
    return 0

def T_chart(img, ctx, sc):
    d = ImageDraw.Draw(img)
    items_stack(img, ctx, sc.get("items", []), sc.get("top", 260))
    ch = sc["chart"]; x0, x1 = ch["x0"], ch["x1"]; vmax = ch["ymax"]
    L, R, T_, B = 150, W - 90, ch.get("top", 520), ch.get("bottom", 1150)
    d.line([(L, B), (R, B)], fill=GREY, width=4); d.line([(L, T_), (L, B)], fill=GREY, width=4)
    for xt in ch.get("xticks", []):
        px = L + (xt - x0) / (x1 - x0) * (R - L)
        d.line([(px, B), (px, B + 14)], fill=GREY, width=3); text_c(d, (px, B + 50), str(xt), 34, GREY, FM)
    if ch.get("xlabel"): text_c(d, ((L + R) / 2, B + 105), ch["xlabel"], 32, GREY, FM)
    # reveal: [[at, x], ...] -> current x
    cur = x0
    for at, xv, *dr in ch["reveal"]:
        pr = ease((ctx.t - ctx.lt(at)) / (dr[0] if dr else 1.2))
        if pr <= 0: break
        cur = cur + (xv - cur) * pr
    for sr in ch["series"]:
        if ctx.t < ctx.lt(sr.get("at", 0)): continue
        xs = np.linspace(x0, cur, 160); pts = []
        for xv in xs:
            v = series_vals(sr, xv); pts.append((L + (xv - x0) / (x1 - x0) * (R - L), B - min(v, vmax) / vmax * (B - T_)))
        if len(pts) > 1: d.line(pts, fill=C(sr.get("color", "yellow")), width=12, joint="curve")
        v = series_vals(sr, cur); ex, ey = pts[-1]
        d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=C(sr.get("color", "yellow")))
        lab = fmt(v, sr); lx = min(max(ex, 220), W - 200)
        text_c(d, (lx, ey - 60 + sr.get("label_dy", 0)), lab, 56, C(sr.get("color", "yellow")), stroke=6)
        if sr.get("name"): text_c(d, (lx, ey - 112 + sr.get("label_dy", 0)), sr["name"], 30, GREY, FM, stroke=3)
    if ch.get("cursor_label"):
        text_c(d, (W - 60, 250), f"{ch['cursor_label']} {int(round(cur))}", 60, YEL, anchor="ra")

def T_twist(img, ctx, sc):
    img.paste(BG_DARK); t = ctx.t
    rad = 520 - 140 * ease((t - ctx.lt(len(sc["lines"]) - 1)) / 1.5)
    spot = Image.new("L", (W, H), 0)
    ImageDraw.Draw(spot).ellipse([540 - rad, 960 - rad * 1.1, 540 + rad, 960 + rad * 1.1], fill=70)
    img.paste(Image.new("RGB", (W, H), (255, 235, 170)), (0, 0), spot.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(img)
    if sc.get("prop"): icon(d, sc["prop"], 520, 1170, 1.4)
    mood = sc.get("mood", "sad")
    for ch in sc.get("changes", []):
        if t >= ctx.lt(ch["at"]): mood = ch.get("mood", mood)
    figure(d, 520, 860, 1.15, mood=mood, sit=sc.get("sit", True), arm=sc.get("arm", "down"))
    # text pages: each page = list of items; later page replaces earlier
    pages = sc["pages"]; cur = None
    for pg in pages:
        if t >= ctx.lt(pg["at"]): cur = pg
    if cur:
        y = 300
        for it in cur["items"]:
            sz = fit_size(it["text"], it.get("size", 96))
            pop_text(img, (W / 2, y + sz * 0.6), it["text"], sz, it.get("color", "white"), ctx.p(it.get("at", cur["at"]), 0.3), stroke=8)
            y += sz * 1.15

def T_choice(img, ctx, sc):
    d = ImageDraw.Draw(img); t = ctx.t
    items_stack(img, ctx, sc.get("items", []), 300)
    for i, (L, txt) in enumerate([("A", sc["a"]), ("B", sc["b"])]):
        col = RED if i == 0 else YEL
        p = ease((t - ctx.lt(sc.get("at", len(sc["lines"]) - 1)) - i * 0.25) / 0.35)
        if p <= 0: continue
        y = 700 + i * 220; x = 120 + (1 - p) * -900; glow = int(t * 2.5) % 2 == i
        d.rounded_rectangle([x, y, x + 840, y + 170], radius=26, fill=(20, 22, 40), outline=col, width=10 if glow else 6)
        d.rounded_rectangle([x + 30, y + 35, x + 130, y + 135], radius=14, fill=col)
        text_c(d, (x + 80, y + 85), L, 64, NAVY)
        d.text((x + 170, y + 85), txt, font=font(fit_size(txt, 60, 630)), fill=WHITE, anchor="lm")
    if t > ctx.lt(sc.get("at", len(sc["lines"]) - 1)) + 1.0:
        pop_text(img, (W / 2, 1210), "COMMENT A OR B", 52, GREY, (t - ctx.lt(sc.get("at", len(sc["lines"]) - 1)) - 1.0) / 0.3, stroke=4)


# ---------------- title banner ----------------
def draw_banner(img, text, highlight=None):
    """White rounded box near the top with the video's question; `highlight` words in blue."""
    d = ImageDraw.Draw(img)
    words = text.split(); hl = set((highlight or "").lower().split())
    sz = 64
    def lines_for(sz):
        f = font(sz); lines, cur = [], []
        for w in words:
            trial = " ".join(cur + [w])
            if cur and f.getlength(trial) > 900: lines.append(cur); cur = [w]
            else: cur.append(w)
        if cur: lines.append(cur)
        return lines
    lines = lines_for(sz)
    while len(lines) > 2 and sz > 36: sz -= 4; lines = lines_for(sz)
    f = font(sz); lh = sz * 1.15; h = lh * len(lines) + 44
    y0 = 170; d.rounded_rectangle([40, y0, W - 40, y0 + h], radius=28, fill=(250, 250, 252))
    for i, ln in enumerate(lines):
        sp = f.getlength(" "); tw = sum(f.getlength(w) for w in ln) + sp * (len(ln) - 1)
        x = W / 2 - tw / 2; y = y0 + 22 + lh * i + lh / 2
        for w in ln:
            col = (40, 110, 240) if w.lower().strip("?,.!:") in hl else (14, 16, 28)
            d.text((x, y), w, font=f, fill=col, anchor="lm"); x += f.getlength(w) + sp
    return y0 + h

# ---------------- data templates ----------------
UK = None
def uk_regions():
    global UK
    if UK is None: UK = json.load(open(os.path.join(HERE, "assets", "uk_regions.json")))
    return UK

STOPS = [(0, (40, 90, 255)), (0.3, (30, 200, 230)), (0.55, (60, 220, 130)), (0.8, (250, 210, 60)), (1, (255, 80, 80))]
def cmap(v):
    v = clamp(v)
    for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
        if v <= b:
            f = (v - a) / (b - a); return tuple(int(ca[i] + (cb[i] - ca[i]) * f) for i in range(3))
    return STOPS[-1][1]

def race_pos(ctx, sc):
    """Position in the keyframe list (float index) at scene time t: hold, then ease to next."""
    n = len(sc["years"]); hold, trans = sc.get("hold", 8.0), sc.get("trans", 1.5)
    t = ctx.t - sc.get("lead", 0.0)
    for i in range(n):
        if t < hold: return float(i)
        t -= hold
        if i == n - 1: return float(n - 1)
        if t < trans: return i + ease(t / trans)
        t -= trans
    return float(n - 1)

def race_len(sc):
    n = len(sc["years"]); return sc.get("lead", 0.0) + n * sc.get("hold", 8.0) + (n - 1) * sc.get("trans", 1.5)

def interp(vals, pos):
    i = int(pos); f = pos - i
    if i >= len(vals) - 1: return vals[-1]
    a, b = vals[i], vals[i + 1]
    if a is None or b is None: return a if f < 0.5 else b
    return a + (b - a) * f

def draw_overlay_pages(img, ctx, sc):
    """Pages of big text shown after the race (insight cards, call to action)."""
    after = sc.get("after", []); cur = None
    for pg in after:
        if ctx.t >= pg["at"]: cur = pg
    if not cur: return
    p = clamp((ctx.t - cur["at"]) / 0.3)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    ys = cur.get("y", 700); hgt = sum(fit_size(it["text"], it.get("size", 90)) * 1.25 for it in cur["items"]) + 60
    od.rounded_rectangle([60, ys - 30, W - 60, ys + hgt], radius=30, fill=(8, 10, 24, int(225 * p)))
    img.paste(ov, (0, 0), ov)
    y = ys
    for it in cur["items"]:
        sz = fit_size(it["text"], it.get("size", 90))
        pop_text(img, (W / 2, y + sz * 0.62), it["text"], sz, it.get("color", "white"), (ctx.t - cur["at"]) / 0.3, stroke=max(4, sz // 12))
        y += sz * 1.25

def T_map_race(img, ctx, sc):
    img.paste(BG_DARK); d = ImageDraw.Draw(img)
    regs = uk_regions(); pos = race_pos(ctx, sc)
    lon0, lat0 = -8.2, 49.9; k = math.cos(math.radians(54.5))
    bx0, by0, bw, bh = sc.get("box", [150, 380, 760, 1180])
    sx = bw / (10.1 * k); sy = bh / 11.0; s_ = min(sx, sy)
    P = lambda lon, lat: (bx0 + (lon - lon0) * k * s_, by0 + bh - (lat - lat0) * s_)
    vmin, vmax = sc["scale"]
    vals = {r: interp(v, pos) for r, v in sc["values"].items()}
    # glow layer
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for name, rings in regs.items():
        v = vals.get(name)
        col = cmap((v - vmin) / (vmax - vmin)) if v is not None else (70, 74, 96)
        for r in rings:
            pts = [P(*p) for p in r]
            gd.polygon(pts, fill=col + (150 if v is not None else 90,))
            gd.line(pts + [pts[0]], fill=tuple(min(255, c + 70) for c in col) + (255,), width=3)
    blur = glow.filter(ImageFilter.GaussianBlur(10))
    img.paste(blur, (0, 0), blur); img.paste(glow, (0, 0), glow); d = ImageDraw.Draw(img)
    # labels
    for name, (lon, lat, call) in sc["labels"].items():
        v = vals.get(name); short = sc.get("names", {}).get(name, name).upper()
        vs = sc.get("nodata_text", "NO DATA") if v is None else fmt(v, sc)
        x, y = P(lon, lat)
        if call:  # callout box
            cx, cy = call
            d.line([(x, y), (cx, cy)], fill=WHITE, width=3); d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=WHITE)
            wbox = max(font(30).getlength(short), font(48).getlength(vs)) + 40
            d.rounded_rectangle([cx - wbox / 2, cy - 50, cx + wbox / 2, cy + 50], radius=14, fill=(10, 12, 26),
                                outline=cmap((v - vmin) / (vmax - vmin)) if v is not None else GREY, width=4)
            text_c(d, (cx, cy - 22), short, 28, WHITE); text_c(d, (cx, cy + 16), vs, 46, WHITE)
        else:
            text_c(d, (x, y - 22), short, 26, WHITE, stroke=4); text_c(d, (x, y + 14), vs, 42, WHITE, stroke=5)
    # year + national average
    yi = int(round(pos)); year = sc["years"][min(yi, len(sc["years"]) - 1)]
    text_c(d, (W - 70, 470), str(year), 150, WHITE, stroke=6, anchor="rm")
    if "national" in sc:
        text_c(d, (W - 70, 570), sc.get("national_label", "UK AVERAGE"), 34, GREY, FM, anchor="rm")
        text_c(d, (W - 70, 630), fmt(interp(sc["national"], pos), sc), 72, C("blue") if False else (90, 170, 255), stroke=4, anchor="rm")
    # legend
    lx0, ly, lw = sc.get("legend_pos", [70, 440, 360])
    for i in range(lw):
        d.line([(lx0 + i, ly), (lx0 + i, ly + 22)], fill=cmap(i / lw))
    text_c(d, (lx0, ly - 26), sc.get("legend", ""), 30, WHITE, anchor="lm")
    text_c(d, (lx0, ly + 52), fmt(vmin, sc), 28, WHITE, anchor="lm"); text_c(d, (lx0 + lw, ly + 52), fmt(vmax, sc), 28, WHITE, anchor="rm")
    draw_overlay_pages(img, ctx, sc)

def T_bar_race(img, ctx, sc):
    img.paste(BG_DARK); d = ImageDraw.Draw(img); pos = race_pos(ctx, sc)
    items = sc["items_data"]  # [{name, values:[...], color}]
    cur = [(it, interp(it["values"], pos)) for it in items]
    vmax = max(v for _, v in cur if v is not None) * 1.08
    # rank interpolation: rank at floor and ceil keyframe, eased
    def ranks(i):
        i = min(i, len(sc["years"]) - 1)
        order = sorted(items, key=lambda it: -(it["values"][i] or 0))
        return {it["name"]: r for r, it in enumerate(order)}
    i0 = int(pos); f = pos - i0; r0, r1 = ranks(i0), ranks(i0 + 1)
    top, rowh, lab_w = sc.get("top", 420), sc.get("row", 92), 330
    maxw = W - lab_w - 210
    show = sc.get("show", 12)
    for it, v in cur:
        r = r0[it["name"]] * (1 - f) + r1[it["name"]] * f
        if r > show - 0.5 or v is None: continue
        y = top + r * rowh; w = max(6, maxw * v / vmax); col = C(it.get("color", "blue"))
        d.text((lab_w + 30, y + rowh * 0.42), it["name"], font=font(fit_size(it["name"], 34, lab_w - 10)), fill=WHITE, anchor="rm")
        d.rounded_rectangle([lab_w + 50, y + 8, lab_w + 50 + w, y + rowh - 14], radius=10, fill=col)
        d.text((lab_w + 66 + w, y + rowh * 0.42), fmt(v, sc), font=font(38), fill=WHITE, anchor="lm")
    yi = int(round(pos)); year = sc["years"][min(yi, len(sc["years"]) - 1)]
    text_c(d, (W - 80, top + rowh * show + 40), str(year), 150, (90, 170, 255), stroke=6, anchor="rm")
    draw_overlay_pages(img, ctx, sc)

def T_line_race(img, ctx, sc):
    img.paste(BG_DARK); d = ImageDraw.Draw(img); pos = race_pos(ctx, sc)
    yrs = sc["years"]; L, R, T_, B = 140, W - 260, sc.get("top", 420), sc.get("bottom", 1500)
    ymax = sc["ymax"]; ymin = sc.get("ymin", 0)
    X = lambda i: L + i / (len(yrs) - 1) * (R - L); Y = lambda v: B - (v - ymin) / (ymax - ymin) * (B - T_)
    for g in sc.get("yticks", []):
        d.line([(L, Y(g)), (R, Y(g))], fill=(40, 46, 70), width=2); text_c(d, (L - 12, Y(g)), fmt(g, sc), 28, GREY, FM, anchor="rm")
    for i, yv in enumerate(yrs):
        if i % sc.get("xstep", 1) == 0: text_c(d, (X(i), B + 36), str(yv), 28, GREY, FM)
    for sr in sc["series"]:
        col = C(sr.get("color", "yellow")); pts = []
        for j in range(0, int(pos * 20) + 1):
            p = j / 20; v = interp(sr["values"], p)
            if v is not None: pts.append((X(p), Y(v)))
        if len(pts) > 1: d.line(pts, fill=col, width=10, joint="curve")
        if pts:
            ex, ey = pts[-1]; d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=col)
            d.text((ex + 22, ey - 22), sr["name"], font=font(30), fill=col, anchor="lm")
            d.text((ex + 22, ey + 16), fmt(interp(sr["values"], pos), sc), font=font(36), fill=WHITE, anchor="lm")
    yi = int(round(pos)); text_c(d, (R - 10, T_ + 40), str(yrs[min(yi, len(yrs) - 1)]), 120, (60, 66, 96), anchor="rm")
    draw_overlay_pages(img, ctx, sc)

# ---------------- fast "DATA-style" templates (light chart, continuous motion) ----------------
LIGHT = (246, 244, 238); INK = (20, 22, 34); GRID_L = (226, 223, 214)
def light_canvas(img, band=370):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=LIGHT)
    for x in range(0, W, 60): d.line([(x, band), (x, H)], fill=GRID_L, width=1)
    for y in range(band, H, 60): d.line([(0, y), (W, y)], fill=GRID_L, width=1)
    d.rectangle([0, 0, W, band], fill=(10, 11, 18))
    return d

def lin_pos(ctx, sc, n):
    """Continuous position through n keyframes at sc['spy'] seconds per step."""
    return clamp((ctx.t - sc.get("lead", 0.5)) / sc.get("spy", 1.5), 0, n - 1)

def lin_len(sc, n): return sc.get("lead", 0.5) + (n - 1) * sc.get("spy", 1.5)

def T_bar_race2(img, ctx, sc):
    d = light_canvas(img)
    yrs = sc["years"]; items = sc["items_data"]; pos = lin_pos(ctx, sc, len(yrs))
    def val(it, p):
        v = interp(it["values"], p)
        return v
    def order_at(i):
        i = min(max(i, 0), len(yrs) - 1)
        live = [it for it in items if it["values"][i] is not None]
        live.sort(key=lambda it: -it["values"][i])
        return {it["name"]: r for r, it in enumerate(live)}
    i0 = int(pos); f = pos - i0; r0, r1 = order_at(i0), order_at(i0 + 1)
    cur = [(it, val(it, pos)) for it in items]
    vmax = max(v for _, v in cur if v is not None) * 1.02
    top, rowh, lab_w = sc.get("top", 420), sc.get("row", 98), sc.get("label_w", 360)
    maxw = W - lab_w - 250
    ff = f * f * (3 - 2 * f)
    for it, v in cur:
        if v is None or it["name"] not in r0 and it["name"] not in r1: continue
        ra = r0.get(it["name"], r1.get(it["name"])); rb = r1.get(it["name"], ra)
        r = ra * (1 - ff) + rb * ff
        y = top + r * rowh; w = max(8, maxw * v / vmax); col = C(it.get("color", "blue"))
        nm = it.get("label", it["name"])
        d.text((lab_w, y + rowh * 0.42), nm, font=font(fit_size(nm, 36, lab_w - 20)), fill=INK, anchor="rm")
        d.rectangle([lab_w + 16, y + 8, lab_w + 16 + w, y + rowh - 12], fill=col)
        d.text((lab_w + 30 + w, y + rowh * 0.42), fmt(v, sc), font=font(40), fill=INK, anchor="lm",
               stroke_width=3, stroke_fill=LIGHT)
    year = yrs[min(int(round(pos)), len(yrs) - 1)]
    text_c(d, (W - 60, sc.get("year_y", 1540)), str(year), 170, (40, 110, 240), anchor="rm", stroke=6)
    if sc.get("subtitle"): text_c(d, (60, sc.get("year_y", 1540) + 10), sc["subtitle"], 32, (110, 110, 120), FM, anchor="lm")
    draw_overlay_pages(img, ctx, sc)

def T_line_race2(img, ctx, sc):
    d = light_canvas(img)
    x0, x1 = sc["x0"], sc["x1"]; spy = sc.get("spy", 1.25); lead = sc.get("lead", 0.5)
    X_now = clamp(x0 + (ctx.t - lead) / spy, x0, x1)
    L, R, T_, B = 140, W - 250, sc.get("top", 440), sc.get("bottom", 1440)
    ymin, ymax = sc.get("ymin", 0), sc["ymax"]
    # x window: whole range (DATA-style shows the full timeline growing)
    X = lambda x: L + (x - x0) / (x1 - x0) * (R - L); Y = lambda v: B - (v - ymin) / (ymax - ymin) * (B - T_)
    # big faded year behind
    yr = int(X_now)
    d.text(((L + R) / 2, (T_ + B) / 2), str(yr), font=font(300), fill=(225, 221, 210), anchor="mm")
    for g in sc.get("yticks", []):
        d.line([(L, Y(g)), (R, Y(g))], fill=(210, 206, 196), width=2)
        d.text((L - 14, Y(g)), fmt(g, {"suffix": sc.get("suffix", ""), "decimals": 0}), font=font(30), fill=(90, 90, 100), anchor="rm")
    for xt in range(int(x0), int(x1) + 1, sc.get("xstep", 5)):
        d.text((X(xt), B + 34), str(xt), font=font(30), fill=(90, 90, 100), anchor="mm")
    d.line([(L, B), (R, B)], fill=INK, width=3)
    def series_at(sr, x):
        xs, ys = sr["xs"], sr["ys"]
        if x <= xs[0]: return ys[0]
        for i in range(1, len(xs)):
            if x <= xs[i]:
                f = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + (ys[i] - ys[i - 1]) * f
        return ys[-1]
    sh = sc.get("shade")
    if sh and X_now > x0:
        A = next(s_ for s_ in sc["series"] if s_["name"] == sh["above"]); Bs = next(s_ for s_ in sc["series"] if s_["name"] == sh["below"])
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); step = 0.04; x = max(x0, A["xs"][0], Bs["xs"][0])
        while x < X_now:
            a, b = series_at(A, x), series_at(Bs, x)
            if a > b: od.rectangle([X(x), Y(a), X(x + step) + 1, Y(b)], fill=tuple(sh.get("color", [255, 80, 80, 70])))
            x += step
        img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
    labels = []
    for sr in sc["series"]:
        col = C(sr.get("color", "blue")); xs = [x for x in sr["xs"] if x <= X_now]
        if not xs: continue
        pts = [(X(x), Y(y)) for x, y in zip(sr["xs"], sr["ys"]) if x <= X_now]
        pts.append((X(X_now), Y(series_at(sr, X_now))))
        if len(pts) > 1: d.line(pts, fill=col, width=sr.get("width", 9), joint="curve")
        ex, ey = pts[-1]; d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=col, outline=LIGHT, width=3)
        labels.append([ey, sr, col, series_at(sr, X_now)])
    labels.sort(key=lambda z: z[0])
    for i in range(1, len(labels)):  # keep end labels apart
        if labels[i][0] - labels[i - 1][0] < 90: labels[i][0] = labels[i - 1][0] + 90
    for ly, sr, col, v in labels:
        ex = X(X_now) + 24
        d.text((ex, ly - 22), sr["name"], font=font(30), fill=col, anchor="lm", stroke_width=3, stroke_fill=LIGHT)
        d.text((ex, ly + 18), fmt(v, {"suffix": sc.get("suffix", ""), "decimals": sr.get("decimals", 1)}), font=font(42), fill=INK, anchor="lm", stroke_width=3, stroke_fill=LIGHT)
    if sh and sh.get("label"):
        d.rectangle([L + 10, T_ - 70, L + 46, T_ - 40], fill=tuple(sh.get("color", [255, 80, 80, 70])[:3]))
        d.text((L + 60, T_ - 55), sh["label"], font=font(30), fill=INK, anchor="lm")
    for ev in sc.get("events", []):  # short callouts that pop as the line passes a date
        if ev["x"] <= X_now < ev["x"] + ev.get("dur", 3.0) / spy * 1.0:
            p = clamp((X_now - ev["x"]) * spy / 0.3)
            ex, ey = X(ev["x"]), Y(ev["y"])
            bw = max(font(34).getlength(ev["text"]), font(28).getlength(ev.get("sub", ""))) + 40
            bx = min(max(ex - bw / 2, 30), W - bw - 30); by = ey - 150
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle([bx, by, bx + bw, by + 96], radius=16, fill=(14, 16, 28, int(235 * p)))
            img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
            d.line([(ex, by + 96), (ex, ey - 14)], fill=INK, width=3)
            d.text((bx + bw / 2, by + 32), ev["text"], font=font(34), fill=WHITE, anchor="mm")
            if ev.get("sub"): d.text((bx + bw / 2, by + 70), ev["sub"], font=font(28, FM), fill=(200, 205, 220), anchor="mm")
    draw_overlay_pages(img, ctx, sc)

TEMPLATES = {"stack": T_stack, "figures": T_figures, "phone": T_phone, "bars": T_bars, "tags": T_tags,
             "chart": T_chart, "twist": T_twist, "choice": T_choice,
             "map_race": T_map_race, "bar_race": T_bar_race, "line_race": T_line_race,
             "bar_race2": T_bar_race2, "line_race2": T_line_race2}

# ---------------- pipeline ----------------
def tts(spec, out):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    model = os.path.join(TTS_DIR, "kokoro-v1.0.onnx")
    if not os.path.exists(model): model = os.path.join(TTS_DIR, "kokoro-v1.0.int8.onnx")
    k = Kokoro(model, os.path.join(TTS_DIR, "voices-v1.0.bin"))
    voice = spec.get("voice", "af_heart"); lang = "en-gb" if voice.startswith("b") else "en-us"
    speed = spec.get("speed", 1.0)
    def trim(a, thr=0.01):
        idx = np.where(np.abs(a) > thr)[0]
        return a[max(idx[0] - 240, 0): idx[-1] + 480] if len(idx) else a
    parts, TL, t = [np.zeros(int(0.05 * SR))], [], 0.05
    for sc in spec["scenes"]:
        st = t; lt = []
        for i, line in enumerate(sc["lines"]):
            a, _ = k.create(line, voice=voice, speed=speed, lang=lang); a = trim(a); dd = len(a) / SR
            lt.append({"text": line, "start": t, "end": t + dd}); parts.append(a); t += dd
            gap = 0.22 if i < len(sc["lines"]) - 1 else 0.45
            parts.append(np.zeros(int(gap * SR))); t += gap
        TL.append({"start": st, "end": t, "lines": lt})
    parts.append(np.zeros(int(1.2 * SR))); t += 1.2; TL[-1]["end"] = t
    a = np.concatenate(parts).astype(np.float32); a = a / max(1e-6, np.abs(a).max()) * 0.89
    raw = os.path.join(out, "voice_raw.wav"); sf.write(raw, a, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", VOICE_POLISH, "-ar", str(SR), os.path.join(out, "voice.wav")], check=True)
    json.dump(TL, open(os.path.join(out, "timeline.json"), "w"), indent=1)
    return TL

def frame(spec, TL, chunks, k, T):
    if spec.get("style") == "glow":
        import glow
        return glow.frame(spec, TL, k, T)
    sc = dict(spec["scenes"][k]); sc.update(TL[k]); sc["start"] = 0.0 if k == 0 else TL[k]["start"]
    t = T - sc["start"]; ctx = Ctx(sc, t, instant=(k == 0))
    img = BG.copy()
    TEMPLATES[sc["type"]](img, ctx, sc)
    if "hud" in sc: draw_hud(img, ctx, sc["hud"])
    data = spec.get("kind") == "data"
    banner = spec.get("banner")
    if banner and not data and k > 0:  # shrink the scene under a fixed question banner
        sc_img = img.resize((int(W * 0.8), int(H * 0.8)), Image.BILINEAR)
        img = BG.copy() if sc["type"] != "twist" else BG_DARK.copy()
        img.paste(sc_img, (int(W * 0.1), 345))
    if banner and (data or k > 0):
        b = banner if isinstance(banner, dict) else {"text": banner}
        draw_banner(img, b["text"], b.get("highlight"))
    if spec.get("footnote") and (data or sc.get("footnote", False)):
        fy = spec.get("footnote_y", 1600) if data else 1530
        text_c(ImageDraw.Draw(img), (W / 2, fy), spec["footnote"], min(28, fit_size(spec["footnote"], 28, 1000, FM)), (110, 110, 122) if spec.get("light") else GREY, FM)
    draw_captions(img, T, chunks)
    pz = 1.0 if k == 0 else ease(t / 0.25)  # no punch-in on the very first frames
    if pz < 1:
        z = 1.06 - 0.06 * pz; w2, h2 = int(W * z), int(H * z)
        img = img.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
    return img

def scene_range(TL, k):
    s = 0.0 if k == 0 else TL[k]["start"]; e = TL[k + 1]["start"] if k + 1 < len(TL) else TL[k]["end"]
    return round(s * FPS), round(e * FPS)

def render_scene(spec, TL, chunks, k, out):
    f0, f1 = scene_range(TL, k)
    final = os.path.join(out, "scenes", f"{k:02d}.mp4"); tmp = final.replace(".mp4", ".tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(f0, f1): p.stdin.write(frame(spec, TL, chunks, k, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f"ffmpeg failed on scene {k}")
    os.rename(tmp, final)


def music(n, bpm=100, seed=0, bright=1.0):
    """Original procedural backing track (Am-F-C-G): soft pad, bass, pluck arpeggio, light drums."""
    t = np.arange(n) / SR; out = np.zeros(n); rng = np.random.default_rng(seed)
    beat = 60 / bpm; bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    nbars = int(n / SR / bar) + 2
    for b in range(nbars):
        ch = chords[b % 4]; s0 = int(b * bar * SR); L = int(bar * SR)
        if s0 >= n: break
        L = min(L, n - s0); tt = np.arange(L) / SR
        env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
        pad = sum(np.sin(2 * np.pi * hz(m) * tt) + 0.3 * np.sin(2 * np.pi * hz(m) * 1.003 * tt + 1) for m in ch)
        out[s0:s0 + L] += 0.10 * pad * env
        for q in range(4):  # bass on each beat
            q0 = s0 + int(q * beat * SR); Lq = min(int(beat * SR), n - q0)
            if Lq <= 0: continue
            tq = np.arange(Lq) / SR
            out[q0:q0 + Lq] += 0.22 * np.sin(2 * np.pi * hz(ch[0] - 12) * tq) * np.exp(-tq * 4)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
        for e in range(8):  # pluck 8ths
            e0 = s0 + int(e * beat / 2 * SR); Le = min(int(0.3 * SR), n - e0)
            if Le <= 0: continue
            te = np.arange(Le) / SR
            out[e0:e0 + Le] += 0.07 * bright * np.sin(2 * np.pi * hz(arp[e % 4]) * te) * np.exp(-te * 9)
        for q in (0, 2):  # kick
            q0 = s0 + int(q * beat * SR); Lk = min(int(0.25 * SR), n - q0)
            if Lk <= 0: continue
            tk = np.arange(Lk) / SR; f = 50 + 70 * np.exp(-tk * 30)
            out[q0:q0 + Lk] += 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 12)
        for e in range(8):  # hats on off-beats
            if e % 2 == 0: continue
            e0 = s0 + int(e * beat / 2 * SR); Lh = min(int(0.04 * SR), n - e0)
            if Lh <= 0: continue
            out[e0:e0 + Lh] += 0.05 * rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / SR * 120)
    fade = np.minimum(1, np.minimum(t / 0.5, (t[-1] - t + 1e-3) / 1.5))
    out *= fade
    return out / (np.abs(out).max() + 1e-9)

def mix(spec, TL, out):
    import soundfile as sf
    v, _ = sf.read(os.path.join(out, "voice.wav")); n = len(v); t = np.arange(n) / SR; rng = np.random.default_rng(1)
    tw = next((TL[i]["start"] for i, s in enumerate(spec["scenes"]) if s["type"] == "twist" or s.get("twist")), TL[-1]["end"])
    if spec.get("kind") == "data":
        bed = music(n, bpm=spec.get("bpm", 104), seed=3) * 0.9
    else:
        bed = music(n, bpm=96, seed=1, bright=0.6) * 0.11 * np.where(t > tw, 0.55, 1.0)
    def add(at, sig):
        i = int(at * SR); j = min(n, i + len(sig))
        if 0 <= i < n: bed[i:j] += sig[:j - i]
    L = int(.35 * SR); x = np.convolve(rng.standard_normal(L), np.ones(30) / 30, "same")
    whoosh = 0.10 * x * np.sin(np.linspace(0, np.pi, L)) ** 2
    k_ = np.arange(int(.8 * SR)) / SR; ding = 0.09 * (np.sin(2 * np.pi * 1318 * k_) + .6 * np.sin(2 * np.pi * 1976 * k_)) * np.exp(-k_ * 6)
    for s in TL[1:]: add(s["start"] - 0.15, whoosh)
    for i, sc in enumerate(spec["scenes"]):
        for at in sc.get("dings", []):  # [line, offset]
            ln = TL[i]["lines"][min(at[0], len(TL[i]["lines"]) - 1)]; add(ln["start"] + at[1], ding)
    m = v * 0.95 + bed; m = m / np.abs(m).max() * 0.95
    sf.write(os.path.join(out, "mix.wav"), m.astype(np.float32), SR)

def thumbnail(spec, out, slug):
    th = spec["thumbnail"]; img = BG.copy(); d = ImageDraw.Draw(img)
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse([-160, 500, 1240, 1900], fill=130)
    img.paste(Image.new("RGB", (W, H), (52, 74, 170)), (0, 0), g.filter(ImageFilter.GaussianBlur(220)))
    rnd = random.Random(5); d = ImageDraw.Draw(img)
    for _ in range(140): mini_head(d, rnd.uniform(30, 1050), rnd.uniform(1500, 1900), 24)
    y = th.get("top", 260)
    for ln in th["lines"]:
        sz = fit_size(ln["text"], ln.get("size", 104), 1000)
        text_c(d, (540, y + sz * 0.6), ln["text"], sz, ln.get("color", "white"), stroke=max(5, sz // 13))
        y += sz * 1.2
    c = CHAR.resize((int(CHAR.width * 520 / CHAR.height), 520), Image.LANCZOS)
    img.paste(c, (540 - c.width // 2, max(int(y) + 60, 980)), c)
    p = os.path.join(out, f"{slug}_thumbnail.png"); img.save(p); return p

def make_thumb(spec, TL, out, slug):
    if spec.get("style") == "glow":
        import glow
        return glow.thumbnail(spec, TL, out, slug)
    return thumbnail(spec, out, slug)

def main():
    spec_path, out = sys.argv[1], sys.argv[2]; stills = "--stills" in sys.argv
    spec = json.load(open(spec_path)); slug = spec["slug"]
    os.makedirs(os.path.join(out, "scenes"), exist_ok=True)
    tl_path = os.path.join(out, "timeline.json")
    if spec.get("kind") == "data":  # no narration: timeline from scene durations, music only
        TL, t = [], 0.0
        for sc in spec["scenes"]:
            if sc["type"] == "bar_race2": dur = lin_len(sc, len(sc["years"])) + sc.get("tail", 0.0)
            elif sc["type"] == "line_race2": dur = sc.get("lead", 0.5) + (sc["x1"] - sc["x0"]) * sc.get("spy", 1.25) + sc.get("tail", 0.0)
            else: dur = sc.get("dur") or race_len(sc) + sc.get("tail", 0.0)
            TL.append({"start": t, "end": t + dur, "lines": []}); t += dur
        import soundfile as sf
        sf.write(os.path.join(out, "voice.wav"), np.zeros(int(t * SR) + SR // 10, dtype=np.float32), SR)
    else:
        TL = json.load(open(tl_path)) if os.path.exists(tl_path) and "--reuse-voice" in sys.argv else tts(spec, out)
    chunks = build_chunks(TL)
    total = TL[-1]["end"]; print(f"duration {total:.1f}s")
    if stills:  # a frame near the end of each scene, as a contact sheet
        ims = []
        for k in range(len(TL)):
            f0, f1 = scene_range(TL, k); ims.append(frame(spec, TL, chunks, k, (f1 - 8) / FPS).resize((270, 480)))
        cols = 5; sheet = Image.new("RGB", (270 * cols, 480 * ((len(ims) + cols - 1) // cols)))
        for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
        sheet.save(os.path.join(out, "stills.png")); make_thumb(spec, TL, out, slug); return
    from multiprocessing import Pool
    with Pool(min(os.cpu_count() or 2, 4)) as pool:
        pool.starmap(render_scene, [(spec, TL, chunks, k, out) for k in range(len(TL))])
    mix(spec, TL, out)
    with open(os.path.join(out, "list.txt"), "w") as f:
        for k in range(len(TL)): f.write(f"file 'scenes/{k:02d}.mp4'\n")
    vo = os.path.join(out, "video_only.mp4"); final = os.path.join(out, f"{slug}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(out, "list.txt"), "-c", "copy", vo], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", os.path.join(out, "mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", final], check=True)
    make_thumb(spec, TL, out, slug)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", final, "-vf", "fps=1/5,scale=180:-1,tile=7x2", "-frames:v", "1",
                    os.path.join(out, "check.png")], check=True)
    print("done", final)

if __name__ == "__main__":
    main()
