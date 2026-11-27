#!/usr/bin/env python3
"""Draw "The World - 27 November 2026": a morning-edition front page.

One image summing up Friday 27 November 2026's world news, drawn from
scratch with PIL primitives only (no photos, no clipart, no copied art).
Design: a sunrise / morning-paper front page - warm cream paper, coral
and gold sunrise band, deep plum ink, teal tag chips.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette: sunrise morning paper -------------------------------------
CREAM = (251, 243, 228)      # paper
PAPER = (255, 252, 244)      # card white
INK = (43, 27, 61)           # deep plum ink
CORAL = (224, 84, 48)        # sunrise coral
GOLD = (242, 165, 65)        # sunrise gold
PEACH = (250, 205, 150)      # pale sunrise
TEAL = (31, 122, 109)        # tag teal
SKY = (127, 179, 213)        # pale sky blue
GREY = (96, 84, 96)          # muted text
RULE = (214, 196, 172)       # hairline

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_sunrise(draw):
    """Sunrise band: gradient sky, rising sun with rays, city skyline."""
    x0, y0, x1, y1 = 36, 196, 988, 296
    # vertical gradient peach -> gold -> coral
    steps = y1 - y0
    for i in range(steps):
        t = i / max(steps - 1, 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(PEACH[k] + (GOLD[k] - PEACH[k]) * u) for k in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(GOLD[k] + (CORAL[k] - GOLD[k]) * u) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    # sun: half disc rising over the horizon
    cx, horizon = 512, 268
    draw.ellipse([cx - 52, horizon - 52, cx + 52, horizon + 52], fill=(255, 244, 214))
    draw.ellipse([cx - 52, horizon - 52, cx + 52, horizon + 52], outline=(255, 255, 255), width=2)
    # rays
    import math
    for ang in range(200, 341, 20):
        r = math.radians(ang)
        x_a = cx + int(66 * math.cos(r))
        y_a = horizon + int(66 * math.sin(r))
        x_b = cx + int(84 * math.cos(r))
        y_b = horizon + int(84 * math.sin(r))
        draw.line([(x_a, y_a), (x_b, y_b)], fill=(255, 244, 214), width=4)
    # skyline silhouettes left and right of the sun
    for bx, bw, bh in [(52, 34, 34), (96, 26, 52), (130, 40, 26), (178, 30, 44),
                       (222, 36, 30), (760, 34, 30), (804, 28, 48), (842, 40, 28),
                       (892, 30, 42), (930, 34, 30)]:
        draw.rectangle([bx, horizon + 28 - bh, bx + bw, horizon + 28], fill=INK)
    # horizon line
    draw.line([(x0, horizon + 28), (x1, horizon + 28)], fill=INK, width=3)
    # thin frame
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def icon_drone(d, cx, cy, r, fg):
    """Quadcopter drone with a small blast star."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PEACH)
    d.rectangle([cx - 16, cy - 5, cx + 16, cy + 5], fill=fg)
    d.rectangle([cx - 5, cy - 16, cx + 5, cy + 16], fill=fg)
    for ox, oy in [(-18, -18), (18, -18), (-18, 18), (18, 18)]:
        d.ellipse([cx + ox - 8, cy + oy - 8, cx + ox + 8, cy + oy + 8],
                  outline=fg, width=3)
    # blast star
    sx, sy = cx + 26, cy - 24
    for dx, dy in [(0, -7), (5, -5), (7, 0), (5, 5), (0, 7), (-5, 5), (-7, 0), (-5, -5)]:
        d.line([(sx, sy), (sx + dx, sy + dy)], fill=CORAL, width=3)


def icon_storm(d, cx, cy, r, fg):
    """Storm cloud, rain and a lightning bolt."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY)
    d.ellipse([cx - 26, cy - 12, cx + 2, cy + 14], fill=fg)
    d.ellipse([cx - 8, cy - 20, cx + 22, cy + 8], fill=fg)
    d.ellipse([cx - 2, cy - 6, cx + 28, cy + 16], fill=fg)
    # lightning bolt
    d.polygon([(cx + 2, cy + 4), (cx + 12, cy + 4), (cx + 6, cy + 16),
               (cx + 14, cy + 16), (cx - 2, cy + 34), (cx + 4, cy + 18),
               (cx - 4, cy + 18)], fill=GOLD)
    # rain drops
    for dx in (-24, -10, 22):
        d.line([(cx + dx, cy + 22), (cx + dx - 3, cy + 30)], fill=TEAL, width=3)


def icon_grid(d, cx, cy, r, fg):
    """Power pylon with a warning bolt."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PEACH)
    # pylon: two legs and cross-arms
    d.line([(cx - 14, cy + 26), (cx - 4, cy - 20)], fill=fg, width=4)
    d.line([(cx + 14, cy + 26), (cx + 4, cy - 20)], fill=fg, width=4)
    d.line([(cx - 18, cy - 12), (cx + 18, cy - 12)], fill=fg, width=4)
    d.line([(cx - 12, cy - 2), (cx + 12, cy - 2)], fill=fg, width=3)
    # bolt
    d.polygon([(cx + 16, cy - 26), (cx + 24, cy - 26), (cx + 19, cy - 14),
               (cx + 25, cy - 14), (cx + 13, cy + 2), (cx + 17, cy - 12),
               (cx + 11, cy - 12)], fill=CORAL)


def icon_olive(d, cx, cy, r, fg):
    """Olive branch: stem with leaf pairs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 214))
    d.line([(cx - 24, cy + 24), (cx + 24, cy - 24)], fill=(90, 120, 70), width=4)
    for lx, ly in [(-16, 16), (-4, 4), (8, -8)]:
        ex, ey = cx + lx, cy + ly
        d.ellipse([ex - 12, ey - 12, ex + 2, ey - 2], fill=TEAL)   # upper leaf
        d.ellipse([ex - 2, ey + 2, ex + 12, ey + 12], fill=(46, 139, 87))  # lower leaf
    d.ellipse([cx + 22, cy - 26, cx + 30, cy - 18], fill=(46, 139, 87))


def icon_chart(d, cx, cy, r, fg):
    """Falling bars with a down arrow."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY)
    for bx, bh in [(-24, 18), (-8, 30), (8, 20), (24, 10)]:
        d.rectangle([cx + bx - 6, cy + 24 - bh, cx + bx + 6, cy + 24], fill=fg)
    # down arrow
    d.line([(cx - 26, cy - 26), (cx + 26, cy + 8)], fill=CORAL, width=4)
    d.polygon([(cx + 26, cy + 8), (cx + 12, cy + 6), (cx + 24, cy + 20)], fill=CORAL)


def icon_chess(d, cx, cy, r, fg):
    """Mini chessboard with a knight's crown."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PEACH)
    bx0, by0, s = cx - 22, cy - 22, 11
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                d.rectangle([bx0 + col * s, by0 + row * s,
                             bx0 + (col + 1) * s, by0 + (row + 1) * s], fill=INK)
    d.rectangle([bx0 - 2, by0 - 2, bx0 + 46, by0 + 46], outline=fg, width=2)


STORIES = [
    dict(tag="MIDDLE EAST", icon=icon_drone,
         head="Drone strike in Kuwait kills two Italians",
         deck="Iran denies responsibility for the attack.",
         src="BBC · The New York Times · NDTV"),
    dict(tag="USA", icon=icon_storm,
         head="Thanksgiving storm halts Macy's parade",
         deck="Flights cancelled; 500,000 homes lose power.",
         src="BBC"),
    dict(tag="UKRAINE", icon=icon_grid,
         head="Zelenskyy: US must push Russia harder",
         deck="Warns Moscow may strike the power grid again.",
         src="BBC"),
    dict(tag="GAZA", icon=icon_olive,
         head="Israel kills 10 in Gaza; Hamas weighs reply",
         deck="Ceasefire strained as mediators urge restraint.",
         src="Reuters"),
    dict(tag="BRITAIN", icon=icon_chart,
         head="UK net migration lowest since 1997",
         deck="Lowest level outside the pandemic years.",
         src="The New York Times"),
    dict(tag="SPORT", icon=icon_chess,
         head="Gukesh–Sindarov draw in marathon Game 3",
         deck="Still level after three games in the final.",
         src="India Today"),
]

ALSO = [
    "Tanker capsizes off Ibiza — one dead · BBC",
    "Depardieu to stand trial over 2018 rape · BBC",
    "Black Friday: bigger discounts · Salesforce",
    "Lille hand Bayern first defeat of season",
]


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    f_mast = font(SERIF_B, 92)
    f_kick = font(SANS_B, 20)
    d.text((W // 2, 26), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    d.text((W // 2, 122), "ONE DAY  ·  SIX STORIES  ·  FROM EVERY CORNER OF THE GLOBE",
           font=f_kick, fill=CORAL, anchor="ma")
    d.line([(36, 152), (988, 152)], fill=RULE, width=2)

    # --- date bar ------------------------------------------------------
    d.rounded_rectangle([36, 162, 988, 190], radius=6, fill=CORAL)
    f_date = font(SANS_B, 21)
    d.text((512, 176), "FRIDAY,  27  NOVEMBER  2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")
    d.text((52, 176), "MORNING EDITION", font=font(SANS_B, 15),
           fill=(255, 236, 214), anchor="lm")
    d.text((972, 176), "No. 27", font=font(SANS_B, 15),
           fill=(255, 236, 214), anchor="rm")

    # --- sunrise band --------------------------------------------------
    draw_sunrise(d)

    # --- six stories: 2 columns x 3 rows ------------------------------
    f_tag = font(SANS_B, 14)
    f_head = font(SANS_B, 23)
    f_deck = font(SANS, 17)
    f_src = font(SANS, 14)
    cw, ch, gap = 464, 182, 16
    x0, y0 = 36, 310
    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = y0 + row * (ch + 14)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                            fill=PAPER, outline=RULE, width=2)
        # tag chip
        tag = st["tag"]
        tw = d.textlength(tag, font=f_tag)
        d.rounded_rectangle([x + 16, y + 14, x + 28 + tw, y + 38], radius=11,
                            fill=TEAL)
        d.text((x + 22, y + 26), tag, font=f_tag, fill=(255, 255, 255),
               anchor="lm")
        # icon circle, top right
        icx, icy = x + cw - 48, y + 44
        st["icon"](d, icx, icy, 32, INK)
        # headline (max 2 lines; width leaves room for the icon)
        lines = wrap(d, st["head"], f_head, cw - 32 - 72)
        if len(lines) > 2:
            lines = lines[:2]
        ly = y + 52
        for ln in lines:
            d.text((x + 16, ly), ln, font=f_head, fill=INK, anchor="la")
            ly += 28
        # deck: one line, measured to fit the card width
        deck = st["deck"]
        while d.textlength(deck, font=f_deck) > cw - 32 and len(deck) > 10:
            deck = deck.rsplit(" ", 1)[0] + "…"
        d.text((x + 16, y + 122), deck, font=f_deck, fill=GREY, anchor="la")
        # source
        d.text((x + 16, y + ch - 20), "— " + st["src"], font=f_src,
               fill=TEAL, anchor="la")

    # --- ALSO TODAY strip ----------------------------------------------
    ay0, ay1 = 896, 966
    d.rounded_rectangle([36, ay0, 988, ay1], radius=10, fill=INK)
    f_also_h = font(SANS_B, 15)
    f_also = font(SANS, 15)
    d.text((56, ay0 + 12), "ALSO TODAY", font=f_also_h, fill=GOLD, anchor="la")
    for j, item in enumerate(ALSO):
        col, row = j % 2, j // 2
        ax = 56 + col * 470
        ay = ay0 + 34 + row * 22
        txt = "•  " + item
        while d.textlength(txt, font=f_also) > 450 and len(txt) > 10:
            txt = txt.rsplit(" ", 1)[0] + "…"
        d.text((ax, ay), txt, font=f_also, fill=(255, 252, 244), anchor="la")

    # --- footer ----------------------------------------------------------
    f_foot = font(SANS, 13)
    d.text((512, 984), "Sources: BBC, Reuters, The New York Times, NDTV, India Today — "
           "as first reported on 27 November 2026", font=f_foot, fill=GREY,
           anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
