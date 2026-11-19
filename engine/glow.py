"""Glow style for The Money What Ifs (v2 look).

Dark stage, glowing faceless figures, spotlights, soft bokeh, thin outline icons,
small pill labels, big gold £ counters, 1-2 word captions, slow camera push.
A glow spec is a normal What If spec with "style": "glow"; each scene has
"type": "glow" and a list "els" of elements (see DRAW below). Timing fields
("at", "until", move "at") use the same rules as mwi: line index, [line, offset]
or float seconds from scene start.
"""
import math, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import mwi
from mwi import W, H, font, FB, FM, clamp, ease, back, Ctx

WHITE = (240, 240, 236); DIM = (92, 92, 98); MID = (150, 150, 156)
GOLD = (255, 196, 72); RED = (255, 86, 86); GREEN = (90, 230, 140)
CMAP = {"white": WHITE, "dim": DIM, "mid": MID, "gold": GOLD, "red": RED, "green": GREEN}
def col(c, default=WHITE):
    if c is None: return default
    return CMAP.get(c, c) if isinstance(c, str) else tuple(c)

def scale_c(c, k): return tuple(int(v * k) for v in c)

# ---------------- background ----------------
@lru_cache(1)
def base_bg():
    img = Image.new("RGB", (W, H), (7, 7, 9)); d = ImageDraw.Draw(img)
    for y in range(40, H, 46):  # faint dot grid
        for x in range(22, W, 46): d.point((x, y), fill=(26, 26, 30))
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse([-300, 200, W + 300, H - 100], fill=255)
    lift = Image.new("RGB", (W, H), (22, 22, 26))
    img.paste(lift, (0, 0), g.filter(ImageFilter.GaussianBlur(260)).point(lambda v: v // 2))
    return img

@lru_cache(1)
def bokeh_layer():
    rnd = random.Random(7); L = Image.new("RGB", (W + 200, H + 200), (0, 0, 0)); d = ImageDraw.Draw(L)
    for _ in range(16):
        r = rnd.uniform(30, 110); x = rnd.uniform(0, W + 200); y = rnd.uniform(0, H + 200); v = rnd.randint(6, 15)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, v + 2))
    return L.filter(ImageFilter.GaussianBlur(14))

@lru_cache(16)
def spot_sprite(top_w, bot_w, h, power):
    m = Image.new("L", (bot_w + 200, h), 0); d = ImageDraw.Draw(m); cx = (bot_w + 200) / 2
    d.polygon([(cx - top_w / 2, 0), (cx + top_w / 2, 0), (cx + bot_w / 2, h), (cx - bot_w / 2, h)], fill=power)
    d.ellipse([cx - bot_w / 2 - 20, h - 60, cx + bot_w / 2 + 20, h + 40], fill=power)
    return m.filter(ImageFilter.GaussianBlur(40))

def background(T):
    img = base_bg().copy()
    ox = int(100 + 60 * math.sin(T * 0.13)); oy = int(100 + 70 * math.cos(T * 0.09))
    img = ImageChops.add(img, bokeh_layer().crop((ox, oy, ox + W, oy + H)))
    return img

# ---------------- text helpers ----------------
def txt(d, xy, s, sz, fill, f=FB, anchor="mm"):
    d.text(xy, s, font=font(sz, f), fill=fill, anchor=anchor)

def caps(d, xy, s, sz, fill, spacing=0.22, f=FM):
    """letter-spaced small caps label centred on xy"""
    s = s.upper(); fo = font(sz, f); sp = sz * spacing
    widths = [d.textlength(ch, font=fo) for ch in s]; total = sum(widths) + sp * (len(s) - 1)
    x = xy[0] - total / 2
    for ch, w in zip(s, widths): d.text((x, xy[1]), ch, font=fo, fill=fill, anchor="lm"); x += w + sp

def pill(d, xy, s, sz=26, inv=False):
    s = s.upper(); fo = font(sz, FB); sp = sz * 0.14
    tw = sum(d.textlength(ch, font=fo) for ch in s) + sp * (len(s) - 1)
    w, h = tw + sz * 1.6, sz * 1.9; x, y = xy
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=h / 2, fill=(10, 10, 12) if inv else WHITE,
                        outline=WHITE if inv else None, width=3)
    cx = x - tw / 2
    for ch in s:
        d.text((cx, y), ch, font=fo, fill=WHITE if inv else (12, 12, 14), anchor="lm"); cx += d.textlength(ch, font=fo) + sp

def money(v, prefix="£", suffix="", dec=0):
    s = f"{abs(v):,.{dec}f}"
    return ("-" if v < 0 else "") + prefix + s + suffix

def fit(d, s, sz, maxw, f=FB):
    while sz > 10 and d.textlength(s, font=font(sz, f)) > maxw: sz -= 2
    return sz

# ---------------- figures and icons ----------------
def figure(d, x, y, s=1.0, c=WHITE, pose="stand", hat=None, t=0.0):
    hr = 30 * s; bw = 92 * s; bh = 118 * s
    bob = 0
    d.rounded_rectangle([x - bw / 2, y - bh + bob, x + bw / 2, y + bob], radius=int(bw * 0.48), fill=c, corners=(True, True, False, False))
    hy = y - bh - hr - 8 * s + bob
    d.ellipse([x - hr, hy - hr, x + hr, hy + hr], fill=c)
    lw = max(3, int(16 * s))
    if pose == "up":
        for sgn in (-1, 1): d.line([(x + sgn * bw * 0.36, y - bh * 0.72), (x + sgn * bw * 0.75, y - bh * 1.45)], fill=c, width=lw, joint="curve")
    elif pose == "point":
        d.line([(x + bw * 0.35, y - bh * 0.7), (x + bw * 1.05, y - bh * 0.95)], fill=c, width=lw)
    elif pose == "shrug":
        for sgn in (-1, 1):
            d.line([(x + sgn * bw * 0.4, y - bh * 0.7), (x + sgn * bw * 0.8, y - bh * 0.62), (x + sgn * bw * 0.9, y - bh * 0.95)], fill=c, width=lw, joint="curve")
    if hat == "grad":
        ty = hy - hr * 0.9
        d.polygon([(x - hr * 1.5, ty), (x, ty - hr * 0.55), (x + hr * 1.5, ty), (x, ty + hr * 0.55)], fill=c)
        d.rectangle([x - hr * 0.7, ty, x + hr * 0.7, ty + hr * 0.5], fill=c)
    elif hat == "crown":
        ty = hy - hr * 1.0
        d.polygon([(x - hr, ty), (x - hr, ty - hr * 0.8), (x - hr * 0.4, ty - hr * 0.3), (x, ty - hr), (x + hr * 0.4, ty - hr * 0.3),
                   (x + hr, ty - hr * 0.8), (x + hr, ty)], fill=GOLD)

def ring(d, x, y, s, c, t):
    rx, ry = 78 * s, 18 * s
    n = 28; ph = t * 0.6
    for i in range(n):
        if i % 2: continue
        a0 = 2 * math.pi * i / n + ph; a1 = 2 * math.pi * (i + 1) / n + ph
        d.line([(x + rx * math.cos(a0), y + ry * math.sin(a0)), (x + rx * math.cos(a1), y + ry * math.sin(a1))], fill=c, width=2)

def icon(d, kind, x, y, s=1.0, c=WHITE, w=4):
    w = max(2, int(w * s)); R = 40 * s
    if kind == "coin":
        d.ellipse([x - R, y - R, x + R, y + R], outline=c, width=w)
        d.ellipse([x - R * 0.72, y - R * 0.72, x + R * 0.72, y + R * 0.72], outline=c, width=max(2, w // 2))
        txt(d, (x, y + 2), "£", int(48 * s), c)
    elif kind == "cup":
        d.rounded_rectangle([x - R * 0.7, y - R * 0.6, x + R * 0.55, y + R * 0.8], radius=int(8 * s), outline=c, width=w)
        d.arc([x + R * 0.3, y - R * 0.3, x + R * 0.95, y + R * 0.35], -90, 90, fill=c, width=w)
        for k in (-0.35, 0, 0.35): d.line([(x + k * R, y - R * 0.95), (x + k * R + 6 * s, y - R * 0.75)], fill=c, width=max(2, w // 2))
    elif kind == "house":
        d.line([(x - R, y - R * 0.05), (x, y - R), (x + R, y - R * 0.05)], fill=c, width=w, joint="curve")
        d.rectangle([x - R * 0.72, y - R * 0.25, x + R * 0.72, y + R * 0.85], outline=c, width=w)
        d.rectangle([x - R * 0.2, y + R * 0.25, x + R * 0.2, y + R * 0.85], outline=c, width=max(2, w // 2))
    elif kind == "card":
        d.rounded_rectangle([x - R, y - R * 0.65, x + R, y + R * 0.65], radius=int(10 * s), outline=c, width=w)
        d.line([(x - R, y - R * 0.25), (x + R, y - R * 0.25)], fill=c, width=w)
        d.line([(x - R * 0.7, y + R * 0.3), (x - R * 0.2, y + R * 0.3)], fill=c, width=max(2, w // 2))
    elif kind == "phone":
        d.rounded_rectangle([x - R * 0.5, y - R, x + R * 0.5, y + R], radius=int(12 * s), outline=c, width=w)
        d.line([(x - R * 0.15, y + R * 0.75), (x + R * 0.15, y + R * 0.75)], fill=c, width=w)
    elif kind == "bag":
        d.rounded_rectangle([x - R * 0.75, y - R * 0.4, x + R * 0.75, y + R * 0.9], radius=int(8 * s), outline=c, width=w)
        d.arc([x - R * 0.4, y - R * 0.95, x + R * 0.4, y - R * 0.05], 180, 360, fill=c, width=w)
    elif kind == "car":
        d.rounded_rectangle([x - R, y - R * 0.1, x + R, y + R * 0.45], radius=int(10 * s), outline=c, width=w)
        d.line([(x - R * 0.6, y - R * 0.1), (x - R * 0.35, y - R * 0.55), (x + R * 0.35, y - R * 0.55), (x + R * 0.6, y - R * 0.1)], fill=c, width=w)
        for k in (-0.55, 0.55): d.ellipse([x + k * R - R * 0.2, y + R * 0.3, x + k * R + R * 0.2, y + R * 0.7], outline=c, width=w)
    elif kind == "chart":
        d.line([(x - R, y + R * 0.7), (x + R, y + R * 0.7)], fill=c, width=w)
        d.line([(x - R * 0.8, y + R * 0.4), (x - R * 0.2, y - R * 0.1), (x + R * 0.2, y + R * 0.15), (x + R * 0.85, y - R * 0.7)], fill=c, width=w, joint="curve")
    elif kind == "clock":
        d.ellipse([x - R, y - R, x + R, y + R], outline=c, width=w)
        d.line([(x, y), (x, y - R * 0.6)], fill=c, width=w); d.line([(x, y), (x + R * 0.45, y + R * 0.15)], fill=c, width=w)
    elif kind == "cross":
        d.line([(x - R * 0.6, y - R * 0.6), (x + R * 0.6, y + R * 0.6)], fill=c, width=w)
        d.line([(x - R * 0.6, y + R * 0.6), (x + R * 0.6, y - R * 0.6)], fill=c, width=w)
    elif kind == "check":
        d.line([(x - R * 0.6, y), (x - R * 0.15, y + R * 0.5), (x + R * 0.65, y - R * 0.55)], fill=c, width=w, joint="curve")
    elif kind == "question":
        d.ellipse([x - R, y - R, x + R, y + R], outline=c, width=w); txt(d, (x, y + 2), "?", int(50 * s), c)
    elif kind == "pound":
        txt(d, (x, y), "£", int(90 * s), c)
    elif kind == "mattress":
        d.rounded_rectangle([x - R * 1.4, y - R * 0.35, x + R * 1.4, y + R * 0.35], radius=int(16 * s), outline=c, width=w)
        for k in (-0.7, 0, 0.7): d.line([(x + k * R, y - R * 0.35), (x + k * R, y + R * 0.35)], fill=c, width=max(2, w // 2))
    elif kind == "arrow_up":
        d.line([(x, y + R), (x, y - R)], fill=c, width=w); d.line([(x - R * 0.5, y - R * 0.45), (x, y - R), (x + R * 0.5, y - R * 0.45)], fill=c, width=w, joint="curve")

# ---------------- element drawing ----------------
def appear(ctx, el):
    """returns visibility factor 0..1 for an element (fade/scale in, fade out)"""
    if not ctx.shown(el): return 0.0
    st = ctx.lt(el.get("at", 0))
    if ctx.instant and st <= 0.3: return 1.0
    return clamp((ctx.t - st) / 0.28)

def pos(ctx, el):
    x, y = el.get("x", 540), el.get("y", 900)
    mv = el.get("move")
    if mv:
        p = ease(clamp((ctx.t - ctx.lt(mv.get("at", 0))) / mv.get("dur", 1.0)))
        x = x + (mv["to"][0] - x) * p; y = y + (mv["to"][1] - y) * p
    return x, y

def keyed(ctx, el):
    """value of a counter: {from,to,at,dur} or keys [[at,value,dur],...]"""
    if "keys" in el:
        v = el.get("from", 0)
        for at, val, dur in el["keys"]:
            st = ctx.lt(at)
            if ctx.instant and st <= 0.3: v = val; continue
            p = ease(clamp((ctx.t - st) / max(dur, 1e-3))); v = v + (val - v) * p
        return v
    st = ctx.lt(el.get("at", 0)); dur = el.get("dur", 1.2)
    p = 1.0 if dur <= 0 else ease(clamp((ctx.t - st) / dur))
    return el.get("from", 0) + (el["to"] - el.get("from", 0)) * p

def E_fig(d, ctx, el, a, img):
    x, y = pos(ctx, el); s = el.get("s", 1.0)
    c = scale_c(col(el.get("c"), WHITE), a)
    if el.get("ring"): ring(d, x, y + 6, s, scale_c(MID, a), ctx.t)
    figure(d, x, y, s, c, el.get("pose", "stand"), el.get("hat"), ctx.t)
    if el.get("tag"): pill(d, (x, y + 52 * s), el["tag"], int(20 * s), inv=True)

def E_crowd(d, ctx, el, a, img):
    n = el.get("n", 5); x0, x1 = el.get("x0", 160), el.get("x1", 920); y = el.get("y", 1100); s = el.get("s", 0.7)
    hero = el.get("hero", -1)
    for i in range(n):
        x = x0 + (x1 - x0) * (i / max(1, n - 1))
        c = WHITE if i == hero else DIM
        if i == hero and el.get("hero_c"): c = col(el["hero_c"])
        figure(d, x, y, s, scale_c(c, a), el.get("pose", "stand"), el.get("hat") if i == hero else None)

def E_counter(d, ctx, el, a, img):
    v = keyed(ctx, el); x, y = el.get("x", 540), el.get("y", 420); sz = el.get("size", 150)
    s = money(v, el.get("prefix", "£"), el.get("suffix", ""), el.get("dec", 0))
    sz = fit(d, s, sz, el.get("maxw", 900))
    c = scale_c(col(el.get("c"), GOLD), a)
    txt(d, (x, y), s, sz, c)
    if el.get("label"): caps(d, (x, y - sz * 0.62 - 18), el["label"], 26, scale_c(MID, a))

def E_text(d, ctx, el, a, img):
    x, y = pos(ctx, el); sz = el.get("size", 80); s = el["text"]
    sz = fit(d, s, sz, el.get("maxw", 940), FB if el.get("f") != "m" else FM)
    txt(d, (x, y), s, sz, scale_c(col(el.get("c"), WHITE), a), FB if el.get("f") != "m" else FM)

def E_caps(d, ctx, el, a, img):
    caps(d, (el.get("x", 540), el.get("y", 300)), el["text"], el.get("size", 26), scale_c(col(el.get("c"), MID), a))

def E_pill(d, ctx, el, a, img):
    if a < 0.5: return
    pill(d, pos(ctx, el), el["text"], el.get("size", 26), el.get("inv", False))

def E_line(d, ctx, el, a, img):
    y = el.get("y", 1180); x0, x1 = el.get("x0", 90), el.get("x1", 990)
    p = ease(clamp((ctx.t - ctx.lt(el.get("at", 0))) / el.get("dur", 0.6))) if not (ctx.instant and ctx.lt(el.get("at", 0)) <= 0.3) else 1
    xe = x0 + (x1 - x0) * p; c = scale_c(MID, a)
    if el.get("dashed", True):
        x = x0
        while x < xe: d.line([(x, y), (min(x + 26, xe), y)], fill=c, width=3); x += 44
    else: d.line([(x0, y), (xe, y)], fill=c, width=3)
    if el.get("arrow") and p > 0.95: d.line([(x1 - 22, y - 14), (x1, y), (x1 - 22, y + 14)], fill=c, width=3)
    if el.get("label"): caps(d, (x1 - 90, y + 34), el["label"], 20, scale_c(DIM, a))

def E_stairs(d, ctx, el, a, img):
    n = el.get("n", 8); x0, y0 = el.get("x0", 160), el.get("y0", 1250); sw, sh = el.get("w", 92), el.get("h", 62)
    c = scale_c(MID, a)
    for i in range(n):
        x = x0 + i * sw; y = y0 - (i + 1) * sh
        d.line([(x, y + sh), (x, y), (x + sw, y)], fill=c, width=3)
    d.line([(x0 + n * sw, y0 - n * sh), (x0 + n * sw, y0)], fill=scale_c(DIM, a), width=2)
    cl = el.get("climb")
    if cl:
        p = clamp((ctx.t - ctx.lt(cl.get("at", 0))) / cl.get("dur", 3.0))
        if ctx.instant and ctx.lt(cl.get("at", 0)) <= 0.3 and cl.get("dur", 3) == 0: p = 1
        f = p * (n - 1); i = int(f); fr = f - i
        hop = math.sin(fr * math.pi) * 26
        fx = x0 + (i + 0.5 + fr) * sw; fy = y0 - (i + 1) * sh - (sh * fr) - hop
        figure(d, fx, fy, el.get("s", 0.7), scale_c(col(el.get("c"), WHITE), a), el.get("pose", "stand"), el.get("hat"))

def E_cards(d, ctx, el, a, img):
    items = el["items"]; n = len(items); cw, ch = el.get("w", 190), el.get("h", 230); gap = el.get("gap", 40)
    x0 = el.get("x", 540) - (n * cw + (n - 1) * gap) / 2; y = el.get("y", 700)
    for i, it in enumerate(items):
        ai = a * clamp((ctx.t - ctx.lt(it.get("at", el.get("at", 0)))) / 0.25) if not (ctx.instant and ctx.lt(it.get("at", 0)) <= 0.3) else a
        if ai <= 0: continue
        x = x0 + i * (cw + gap); c = scale_c(WHITE if it.get("lit") else MID, ai)
        d.rounded_rectangle([x, y - ch / 2, x + cw, y + ch / 2], radius=18, outline=c, width=3, fill=(14, 14, 17))
        icon(d, it.get("icon", "coin"), x + cw / 2, y - 18, 1.0, c)
        if it.get("label"):
            sz = fit(d, it["label"].upper(), 24, cw - 20, FM); caps(d, (x + cw / 2, y + ch / 2 - 34), it["label"], sz, c, 0.12)
        mk = it.get("mark")
        if mk and ctx.t >= ctx.lt(mk.get("at", 0)):
            pm = back(clamp((ctx.t - ctx.lt(mk.get("at", 0))) / 0.3))
            icon(d, mk["kind"], x + cw / 2, y - 18, 1.6 * pm, scale_c(col(mk.get("c"), RED if mk["kind"] == "cross" else GREEN), ai), 6)

def E_grid(d, ctx, el, a, img):
    rows, cols = el.get("rows", 2), el.get("cols", 5); cell = el.get("cell", 110); gap = 18
    x0 = el.get("x", 540) - (cols * cell + (cols - 1) * gap) / 2; y0 = el.get("y", 700) - (rows * cell + (rows - 1) * gap) / 2
    filled = 0
    for at, nn, dur in el.get("fill", []):
        p = clamp((ctx.t - ctx.lt(at)) / max(dur, 1e-3)); filled = max(filled, int(round(nn * p)) if p > 0 else filled)
    for k in range(rows * cols):
        r, cc = divmod(k, cols); x = x0 + cc * (cell + gap); y = y0 + r * (cell + gap)
        on = k < filled; c = scale_c(WHITE if on else DIM, a)
        d.rounded_rectangle([x, y, x + cell, y + cell], radius=12, outline=c, width=3, fill=scale_c((235, 235, 230), a) if on and el.get("solid") else None)
        if on: icon(d, el.get("mark", "cross"), x + cell / 2, y + cell / 2, cell / 110, (14, 14, 16) if el.get("solid") else scale_c(col(el.get("mc"), WHITE), a), 5)
    if el.get("label"): caps(d, (el.get("x", 540), y0 - 34), el["label"], 22, scale_c(MID, a))

def E_curve(d, ctx, el, a, img):
    x0, y0, x1, y1 = el.get("box", [130, 520, 950, 1180]); ys = el["ys"]; vmax = el.get("max", max(ys))
    st = ctx.lt(el.get("at", 0)); p = clamp((ctx.t - st) / el.get("dur", 3.0))
    if ctx.instant and st <= 0.3 and el.get("dur", 3) == 0: p = 1
    d.line([(x0, y1), (x1, y1)], fill=scale_c(DIM, a), width=2)
    for lab in el.get("xlabels", []):  # [frac, text]
        caps(d, (x0 + (x1 - x0) * lab[0], y1 + 34), lab[1], 22, scale_c(DIM, a), 0.1)
    n = len(ys); m = p * (n - 1); pts = []
    for i in range(int(m) + 1):
        pts.append((x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * ys[i] / vmax))
    if m < n - 1:
        i = int(m); fr = m - i; v = ys[i] + (ys[i + 1] - ys[i]) * fr
        pts.append((x0 + (x1 - x0) * m / (n - 1), y1 - (y1 - y0) * v / vmax))
    else: v = ys[-1]
    c = scale_c(col(el.get("c"), GOLD), a)
    if len(pts) > 1:
        if el.get("fill"):
            poly = pts + [(pts[-1][0], y1), (pts[0][0], y1)]
            lay = Image.new("L", (W, H), 0); ImageDraw.Draw(lay).polygon(poly, fill=int(46 * a))
            img.paste(Image.new("RGB", (W, H), col(el.get("c"), GOLD)), (0, 0), lay)
        d.line(pts, fill=c, width=6, joint="curve")
    if pts and p > 0:
        hx, hy = pts[-1]; d.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=c)
        if el.get("head"):
            s = money(v, el.get("prefix", "£"), "", 0); txt(d, (min(hx, x1 - 110), hy - 50), s, 46, c)

def E_bars(d, ctx, el, a, img):
    items = el["items"]; n = len(items); bw = el.get("w", 220); gap = el.get("gap", 120); base = el.get("y", 1220); hmax = el.get("h", 560)
    vmax = el.get("max", max(it["value"] for it in items)); x0 = el.get("x", 540) - (n * bw + (n - 1) * gap) / 2
    for i, it in enumerate(items):
        st = ctx.lt(it.get("at", el.get("at", 0))); p = ease(clamp((ctx.t - st) / it.get("dur", 1.4)))
        if ctx.instant and st <= 0.3: p = 1
        if ctx.t < st: continue
        x = x0 + i * (bw + gap); h = hmax * it["value"] / vmax * p; c = col(it.get("c"), GOLD)
        d.rectangle([x, base - h, x + bw, base], fill=scale_c(c, 0.22 * a), outline=scale_c(c, a), width=4)
        txt(d, (x + bw / 2, base - h - 48), money(it["value"] * p, it.get("prefix", "£")), fit(d, money(it["value"], "£"), 52, bw + 90), scale_c(c, a))
        caps(d, (x + bw / 2, base + 40), it["label"], 24, scale_c(WHITE, a), 0.12)
        if it.get("sub"): caps(d, (x + bw / 2, base + 76), it["sub"], 20, scale_c(MID, a), 0.12)

def E_icon(d, ctx, el, a, img):
    x, y = pos(ctx, el); s = el.get("s", 1.0)
    if el.get("pop"): s *= back(clamp((ctx.t - ctx.lt(el.get("at", 0))) / 0.35)) if not (ctx.instant and ctx.lt(el.get("at", 0)) <= 0.3) else 1
    icon(d, el["kind"], x, y, s, scale_c(col(el.get("c"), WHITE), a), el.get("lw", 4))
    if el.get("label"): caps(d, (x, y + 60 * el.get("s", 1.0) + 24), el["label"], 24, scale_c(MID, a), 0.14)

def E_box(d, ctx, el, a, img):
    x, y, w, h = el.get("x", 540), el.get("y", 700), el.get("w", 760), el.get("h", 300)
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=22, outline=scale_c(WHITE, a), width=3, fill=(13, 13, 16))
    lines = el.get("lines", []); yy = y - (len(lines) - 1) * 34
    for ln in lines:
        s = ln if isinstance(ln, str) else ln["text"]; c = WHITE if isinstance(ln, str) else col(ln.get("c"))
        sz = fit(d, s, 50 if isinstance(ln, str) else ln.get("size", 50), w - 60); txt(d, (x, yy), s, sz, scale_c(c, a)); yy += 68

def E_coins(d, ctx, el, a, img):
    """coins raining down into a pile (decor for growth moments)"""
    st = ctx.lt(el.get("at", 0)); rnd = random.Random(el.get("seed", 3)); n = el.get("n", 14)
    for i in range(n):
        t0 = st + rnd.uniform(0, el.get("dur", 2.0)); x = el.get("x", 540) + rnd.uniform(-260, 260)
        k = clamp((ctx.t - t0) / 0.8)
        if ctx.t < t0: continue
        y = el.get("y0", 300) + (el.get("y1", 1150) - el.get("y0", 300)) * (k * k)
        icon(d, "coin", x, y, 0.55, scale_c(GOLD, a * (1 - 0.5 * (k >= 1))), 3)

def E_divider(d, ctx, el, a, img):
    x = el.get("x", 540); d.line([(x, el.get("y0", 420)), (x, el.get("y1", 1300))], fill=scale_c(DIM, a), width=2)

DRAW = {"fig": E_fig, "crowd": E_crowd, "counter": E_counter, "text": E_text, "caps": E_caps, "pill": E_pill,
        "line": E_line, "stairs": E_stairs, "cards": E_cards, "grid": E_grid, "curve": E_curve, "bars": E_bars,
        "icon": E_icon, "box": E_box, "coins": E_coins, "divider": E_divider}

# ---------------- captions ----------------
def glow_chunks(TL):
    out = []
    for sc in TL:
        for ln in sc["lines"]:
            words = ln["text"].split(); wts = [len(w) + 2 for w in words]; tot = sum(wts)
            t = ln["start"]; dur = ln["end"] - ln["start"]; cur = []
            for w, wt in zip(words, wts):
                e = t + dur * wt / tot; cur.append((w, t, e)); t = e
                if len(cur) >= 2 or len(w) > 8 or w[-1] in ".?,!:" : out.append(cur); cur = []
            if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        end = out[i + 1][0][1] if i + 1 < len(out) else c[-1][2] + 0.6
        res.append((c[0][1], min(end, c[-1][2] + 0.5), c))
    return res

def draw_caps(d, T, chunks, y=1420):
    for st, en, words in chunks:
        if st <= T < en:
            s = " ".join(w[0] for w in words).strip("\"")
            gold = any(ch.isdigit() for ch in s) or "£" in s or "pound" in s.lower() or "thousand" in s.lower() or "million" in s.lower()
            sz = fit(d, s, 96, 940); p = ease((T - st) / 0.1)
            txt(d, (540, y + 8 * (1 - p)), s, sz, scale_c(GOLD if gold else WHITE, 0.5 + 0.5 * p))
            return

# ---------------- frame ----------------
def scene_ctx(spec, TL, k, T):
    sc = dict(spec["scenes"][k]); sc.update(TL[k]); sc["start"] = 0.0 if k == 0 else TL[k]["start"]
    return sc, Ctx(sc, T - sc["start"], instant=(k == 0))

def compose(spec, TL, k, T, captions=None, hide_top=False):
    sc, ctx = scene_ctx(spec, TL, k, T)
    img = background(T)
    for sp in sc.get("spots", []):  # [x, power]
        m = spot_sprite(160, 520, 1500, int((sp[1] if len(sp) > 1 else 70) * 0.85))
        img.paste(Image.new("RGB", m.size, (255, 250, 235)), (int(sp[0] - m.width / 2), -200), m)
    fg = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(fg)
    for el in sc.get("els", []):
        if hide_top and el["k"] in ("counter", "caps", "pill", "text") and el.get("y", 900) < 700: continue
        a = appear(ctx, el)
        if a <= 0: continue
        DRAW[el["k"]](d, ctx, el, a, fg)
    if spec.get("footnote") and sc.get("footnote"):
        txt(d, (540, 1500), spec["footnote"], fit(d, spec["footnote"], 26, 960, FM), (120, 120, 126), FM)
    if captions: draw_caps(d, T, captions)
    small = fg.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR)
    img = ImageChops.add(ImageChops.add(img, fg), ImageChops.multiply(small, Image.new("RGB", (W, H), (150, 150, 150))))
    # camera: slow push-in per scene, quick settle at scene start (not on the hook)
    dur = max(1.0, TL[k]["end"] - (0.0 if k == 0 else TL[k]["start"]))
    z = 1.0 + 0.045 * clamp(ctx.t / dur)
    if k > 0: z += 0.05 * (1 - ease(clamp(ctx.t / 0.35)))
    cx, cy = sc.get("focus", [540, 900])
    if z > 1.001:
        w2, h2 = int(W * z), int(H * z); img = img.resize((w2, h2), Image.BILINEAR)
        ox = int(clamp(cx * z - cx, 0, w2 - W)); oy = int(clamp(cy * z - cy, 0, h2 - H)); img = img.crop((ox, oy, ox + W, oy + H))
    # vignette
    return img

_CACHE = {}
def frame(spec, TL, k, T):
    key = id(TL)
    if key not in _CACHE: _CACHE.clear(); _CACHE[key] = glow_chunks(TL)
    return compose(spec, TL, k, T, _CACHE[key])

def thumbnail(spec, TL, out, slug):
    th = spec["thumbnail"]; k = th.get("scene", 0); sc = TL[k]
    T = th.get("t", (sc["start"] + sc["end"]) / 2)
    img = compose(spec, TL, k, T, None, hide_top=True); d = ImageDraw.Draw(img)
    y = th.get("top", 230)
    for ln in th["lines"]:
        sz = fit(d, ln["text"], ln.get("size", 100), 980)
        txt(d, (540, y + sz * 0.6), ln["text"], sz, col(ln.get("c"), WHITE)); y += sz * 1.18
    import os
    p = os.path.join(out, f"{slug}_thumbnail.png"); img.save(p); return p
