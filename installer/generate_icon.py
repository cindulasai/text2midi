"""
Generate the text2midi app icon (music note on a gradient background).

Run once to create installer/text2midi.ico, then delete this script if desired.

Requires: Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

ICON_DIR = Path(__file__).resolve().parent
OUTPUT_ICO = ICON_DIR / "text2midi.ico"

# ── Sizes for multi-resolution ICO ─────────────────────────────────
SIZES = [16, 24, 32, 48, 64, 128, 256]

# ── Color palette (Catppuccin Mocha-inspired to match TUI) ─────────
BG_TOP = (30, 30, 46)       # Crust / deep navy
BG_BOTTOM = (49, 50, 68)    # Surface0
ACCENT = (137, 180, 250)    # Blue
ACCENT2 = (166, 227, 161)   # Green
NOTE_COLOR = (205, 214, 244) # Text / white-ish


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    r = radius
    # Corners
    draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill)
    # Rectangles to fill the middle
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)


def make_icon(size: int) -> Image.Image:
    """Render one icon frame at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Gradient rounded-rect background ───────────────────────────
    margin = max(1, size // 16)
    corner_r = max(2, size // 6)

    # Build gradient background
    for y in range(size):
        t = y / max(1, size - 1)
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        draw.line([(margin, y), (size - margin - 1, y)], fill=(r, g, b, 255))

    # Apply rounded mask
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    draw_rounded_rect(mask_draw, (margin, margin, size - margin, size - margin), corner_r, 255)
    img.putalpha(mask)

    # Redraw on masked image
    img2 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)

    # Gradient background within rounded rect
    for y in range(margin, size - margin):
        t = (y - margin) / max(1, size - 2 * margin - 1)
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        draw2.line([(0, y), (size - 1, y)], fill=(r, g, b, 255))

    # Apply the rounded rect mask
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(img2, mask=mask)
    draw = ImageDraw.Draw(bg)

    # ── Draw music note(s) ─────────────────────────────────────────
    # We'll draw a beamed eighth-note pair (♫)
    s = size  # shorthand

    if s <= 24:
        # For tiny sizes, draw a simpler single note
        # Note head (ellipse)
        cx, cy = s * 0.5, s * 0.65
        rx, ry = s * 0.15, s * 0.10
        draw.ellipse(
            [cx - rx, cy - ry, cx + rx, cy + ry],
            fill=NOTE_COLOR,
        )
        # Stem
        stem_x = cx + rx - max(1, s * 0.03)
        stem_top = s * 0.25
        stem_w = max(1, s * 0.06)
        draw.rectangle(
            [stem_x - stem_w/2, stem_top, stem_x + stem_w/2, cy],
            fill=NOTE_COLOR,
        )
    else:
        # Larger: draw beamed double eighth notes ♫
        # Two note heads connected by a beam
        note_w = s * 0.13   # note head horizontal radius
        note_h = s * 0.09   # note head vertical radius
        stem_w = max(2, s * 0.04)

        # Left note
        lx, ly = s * 0.32, s * 0.62
        # Right note
        rx_pos, ry_pos = s * 0.62, s * 0.68

        # Note heads (tilted ellipses via polygon)
        for nx, ny in [(lx, ly), (rx_pos, ry_pos)]:
            draw.ellipse(
                [nx - note_w, ny - note_h, nx + note_w, ny + note_h],
                fill=NOTE_COLOR,
            )

        # Stems (going up from right side of each note head)
        l_stem_x = lx + note_w - stem_w / 2
        r_stem_x = rx_pos + note_w - stem_w / 2
        beam_top = s * 0.22
        beam_top_r = s * 0.28  # right stem slightly lower for style

        draw.rectangle(
            [l_stem_x, beam_top, l_stem_x + stem_w, ly],
            fill=NOTE_COLOR,
        )
        draw.rectangle(
            [r_stem_x, beam_top_r, r_stem_x + stem_w, ry_pos],
            fill=NOTE_COLOR,
        )

        # Beam connecting the two stems at the top
        beam_h = max(2, s * 0.06)
        draw.polygon(
            [
                (l_stem_x, beam_top),
                (r_stem_x + stem_w, beam_top_r),
                (r_stem_x + stem_w, beam_top_r + beam_h),
                (l_stem_x, beam_top + beam_h),
            ],
            fill=NOTE_COLOR,
        )

        # Second beam (sixteenth-note style for flair)
        beam2_offset = beam_h + max(2, s * 0.04)
        draw.polygon(
            [
                (l_stem_x, beam_top + beam2_offset),
                (r_stem_x + stem_w, beam_top_r + beam2_offset),
                (r_stem_x + stem_w, beam_top_r + beam2_offset + beam_h),
                (l_stem_x, beam_top + beam2_offset + beam_h),
            ],
            fill=ACCENT,
        )

        # Subtle accent dot (bottom-right corner decorator)
        dot_r = max(1, s * 0.03)
        dot_cx = s * 0.78
        dot_cy = s * 0.78
        draw.ellipse(
            [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
            fill=ACCENT2,
        )

    return bg


def main():
    frames = [make_icon(s) for s in SIZES]
    # Save as multi-resolution ICO
    frames[0].save(
        str(OUTPUT_ICO),
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=frames[1:],
    )
    print(f"  [OK] Icon saved: {OUTPUT_ICO}")
    print(f"       Sizes: {', '.join(f'{s}x{s}' for s in SIZES)}")


if __name__ == "__main__":
    main()
