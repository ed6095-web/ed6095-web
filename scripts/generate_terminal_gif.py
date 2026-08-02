#!/usr/bin/env python3
"""
generate_terminal_gif.py
========================
Generates assets/terminal.gif — an animated terminal boot sequence
with crisp ASCII portrait for Eashan Darsh's GitHub profile README.
"""

import sys
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# ─── Configuration ──────────────────────────────────────────────────────────

BG_COLOR       = (13, 17, 23)        # #0D1117 — GitHub dark background
GREEN          = (63, 185, 80)       # #3FB950 — accent green
BLUE           = (88, 166, 255)      # #58A6FF — primary blue
WHITE          = (240, 246, 252)     # #F0F6FC — primary text
MUTED          = (139, 148, 158)     # #8B949E — secondary text
YELLOW         = (210, 153, 34)      # terminal yellow

GIF_WIDTH      = 720
GIF_HEIGHT     = 420
FONT_SIZE      = 13
CHAR_W         = 8    # approx monospace char width at font size 13
CHAR_H         = 16   # approx monospace char height at font size 13
FRAME_DELAY    = 60   # ms per frame

OUTPUT_PATH    = Path(__file__).parent.parent / "assets" / "terminal.gif"

# ─── Font Loading ────────────────────────────────────────────────────────────

def load_font(size: int):
    candidates = [
        "JetBrainsMono-Regular.ttf",
        "DejaVuSansMono.ttf",
        "Consolas.ttf",
        "CourierNew.ttf",
        "cour.ttf",
        "lucon.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    winfonts = Path("C:/Windows/Fonts")
    if winfonts.exists():
        for name in ["consola.ttf", "cour.ttf", "lucon.ttf", "courbd.ttf"]:
            p = winfonts / name
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except Exception:
                    pass
    return ImageFont.load_default()

# ─── ASCII Art Generation ────────────────────────────────────────────────────

def photo_to_ascii(photo_path: str, width: int = 34, height: int = 20) -> list[str]:
    """Convert photo into a sharp, perfectly-fitted 34x20 ASCII portrait."""
    img = Image.open(photo_path).convert("L")
    w, h = img.size

    # Crop tightly to head and shoulders
    crop_box = (int(w * 0.15), int(h * 0.00), int(w * 0.85), int(h * 0.85))
    img = img.crop(crop_box)

    # Resize to exact terminal portrait inner dimensions (34 cols x 20 rows)
    img_resized = img.resize((width, height), Image.LANCZOS)
    img_contrast = ImageEnhance.Contrast(img_resized).enhance(2.2)
    img_sharp = ImageEnhance.Sharpness(img_contrast).enhance(2.0)

    edges = img_resized.filter(ImageFilter.FIND_EDGES)

    try:
        pixels = list(img_sharp.get_flattened_data())
        edges_data = list(edges.get_flattened_data())
    except AttributeError:
        pixels = list(img_sharp.getdata())
        edges_data = list(edges.getdata())

    lines = []
    for r in range(height):
        row = ""
        for c in range(width):
            idx = r * width + c
            p_val = pixels[idx]
            e_val = edges_data[idx]

            # Background removal (>170 luminance & weak edge -> empty space)
            if p_val > 170 and e_val < 35:
                row += " "
            elif e_val > 65 and p_val < 150:
                row += "#"
            elif p_val < 40:
                row += "@"
            elif p_val < 70:
                row += "%"
            elif p_val < 100:
                row += "▓"
            elif p_val < 130:
                row += "▒"
            elif p_val < 160:
                row += "░"
            else:
                row += " "
        lines.append(row)
    return lines

# ─── Frame Renderer ──────────────────────────────────────────────────────────

class TerminalRenderer:
    def __init__(self):
        self.font      = load_font(FONT_SIZE)
        self.font_bold = load_font(FONT_SIZE + 1)
        self.frames    = []
        self.pad_x     = 18
        self.pad_y     = 38

    def new_frame(self) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        img  = Image.new("RGB", (GIF_WIDTH, GIF_HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        self._draw_chrome(draw)
        return img, draw

    def _draw_chrome(self, draw: ImageDraw.ImageDraw):
        draw.rounded_rectangle(
            [0, 0, GIF_WIDTH - 1, GIF_HEIGHT - 1],
            radius=10, outline=(48, 54, 61), width=1
        )
        draw.rectangle([1, 1, GIF_WIDTH - 2, 28], fill=(33, 38, 45))
        draw.line([1, 29, GIF_WIDTH - 2, 29], fill=(48, 54, 61))

        btns = [(16, 14, (255, 95, 86)), (36, 14, (255, 189, 46)), (56, 14, (39, 201, 63))]
        for bx, by, bc in btns:
            draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=bc)

        title = "ed6095-web@github: ~"
        draw.text(
            (GIF_WIDTH // 2, 14), title,
            font=self.font, fill=MUTED, anchor="mm"
        )

    def text(self, draw, row: int, col: int, text: str, color=WHITE, bold=False):
        x = self.pad_x + col * CHAR_W
        y = self.pad_y + row * CHAR_H
        font = self.font_bold if bold else self.font
        draw.text((x, y), text, font=font, fill=color)

    def add_frame(self, img: Image.Image, repeat: int = 1):
        for _ in range(repeat):
            self.frames.append(img.copy())

    def save(self):
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        durations = [FRAME_DELAY] * len(self.frames)
        if durations:
            durations[-1] = 4000
        self.frames[0].save(
            str(OUTPUT_PATH),
            save_all=True,
            append_images=self.frames[1:],
            optimize=False,
            loop=0,
            duration=durations,
        )
        print(f"✓ Saved: {OUTPUT_PATH}")

# ─── Animation Sequences ─────────────────────────────────────────────────────

def build_animation(ascii_lines: list[str]) -> TerminalRenderer:
    r = TerminalRenderer()

    # ── Phase 1: BIOS / Boot sequence ─────────────────────────────────────
    boot_lines = [
        ("",               WHITE,  0),
        ("BIOS v2.6.1  |  ed6095-web Systems", MUTED, 0),
        ("",               WHITE,  0),
        ("[    0.000000] Kernel: Linux 6.8.0-gentoo x86_64", GREEN, 0),
        ("[    0.000001] CPU: Intel Core i7 @ 3.20GHz", GREEN, 0),
        ("[    0.000032] RAM: 16384 MB DDR5 — OK", GREEN, 0),
        ("[    0.000098] NVMe: /dev/sda — 512GB detected", GREEN, 0),
        ("",               WHITE,  0),
        ("[  OK  ] Mounting filesystems ...", GREEN, 0),
        ("[  OK  ] Starting network daemon ...", GREEN, 0),
        ("[  OK  ] Loading systemd units ...", GREEN, 0),
        ("[  OK  ] Starting SSH daemon ...", GREEN, 0),
        ("",               WHITE,  0),
        ("Loading user profile ...", YELLOW, 2),
    ]

    for i in range(len(boot_lines)):
        img, draw = r.new_frame()
        for j, (line, color, _) in enumerate(boot_lines[:i+1]):
            r.text(draw, j, 0, line, color)
        r.add_frame(img, repeat=max(1, boot_lines[i][2] + 1))

    # ── Phase 2: Loading bar ──────────────────────────────────────────────
    base_row = len(boot_lines)
    for pct in range(0, 101, 5):
        img, draw = r.new_frame()
        for j, (line, color, _) in enumerate(boot_lines):
            r.text(draw, j, 0, line, color)
        bar_filled = int(pct / 100 * 38)
        bar = "█" * bar_filled + "░" * (38 - bar_filled)
        r.text(draw, base_row, 0, f"  [{bar}] {pct:3d}%", BLUE)
        r.add_frame(img)

    # ── Phase 3: Blank pause ──────────────────────────────────────────────
    img, draw = r.new_frame()
    r.add_frame(img, repeat=6)

    # ── Phase 4: ASCII portrait appears line by line ───────────────────────
    ascii_w = len(ascii_lines[0])  # 34
    ascii_h = len(ascii_lines)     # 20

    start_row = 1

    for reveal in range(ascii_h + 1):
        img, draw = r.new_frame()
        r.text(draw, 0, 0, "┌─ ASCII PORTRAIT ─────────────────┐", MUTED)
        for ln in range(reveal):
            line_text = ascii_lines[ln]
            r.text(draw, start_row + ln, 0, "│ " + line_text + " │", GREEN)
        r.add_frame(img)

    # ── Phase 5: whoami info prints line by line ──────────────────────────
    whoami_lines = [
        ("$ whoami",                                         BLUE,   True),
        ("──────────────────────────────────────────",       MUTED,  False),
        ("  Name        :  Eashan Darsh",                    WHITE,  False),
        ("  Role        :  Backend Developer",               WHITE,  False),
        ("  Education   :  B.Tech CS Engg  (AI & ML)",       WHITE,  False),
        ("  Focus       :  Backend · System Design · AI",    WHITE,  False),
        ("  OS          :  Linux",                           GREEN,  False),
        ("  Editor      :  VS Code",                         BLUE,   False),
        ("  Location    :  Chennai, Tamil Nadu",              WHITE,  False),
        ("  Status      :  [ Building every day ]",          YELLOW, False),
        ("──────────────────────────────────────────",       MUTED,  False),
        ("$  _",                                             GREEN,  False),
    ]

    info_col_start = 39  # Perfectly spaced to the right of 36-col portrait box

    for i in range(len(whoami_lines) + 1):
        img, draw = r.new_frame()
        # Draw full 36-col portrait box on left
        r.text(draw, 0, 0, "┌─ ASCII PORTRAIT ─────────────────┐", MUTED)
        for ln in range(ascii_h):
            r.text(draw, 1 + ln, 0, "│ " + ascii_lines[ln] + " │", GREEN)
        r.text(draw, 1 + ascii_h, 0, "└──────────────────────────────────┘", MUTED)

        # Draw whoami info line by line on right
        for j, (line, color, bold) in enumerate(whoami_lines[:i]):
            r.text(draw, 1 + j, info_col_start, line, color, bold=bold)
        r.add_frame(img)

    # ── Phase 6: Blinking cursor final frame ──────────────────────────────
    for blink in range(8):
        img, draw = r.new_frame()
        r.text(draw, 0, 0, "┌─ ASCII PORTRAIT ─────────────────┐", MUTED)
        for ln in range(ascii_h):
            r.text(draw, 1 + ln, 0, "│ " + ascii_lines[ln] + " │", GREEN)
        r.text(draw, 1 + ascii_h, 0, "└──────────────────────────────────┘", MUTED)

        for j, (line, color, bold) in enumerate(whoami_lines[:-1]):
            r.text(draw, 1 + j, info_col_start, line, color, bold=bold)

        cursor_row = 1 + len(whoami_lines) - 1
        cursor_char = "$ █" if blink % 2 == 0 else "$  "
        r.text(draw, cursor_row, info_col_start, cursor_char, GREEN, bold=True)
        r.add_frame(img, repeat=5)

    return r

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Profile terminal GIF")
    parser.add_argument("--photo", default=None, help="Path to profile photo (JPG/PNG)")
    parser.add_argument("--output", default=None, help="Output GIF path")
    args = parser.parse_args()

    if args.output:
        global OUTPUT_PATH
        OUTPUT_PATH = Path(args.output)

    print("─" * 55)
    print("  GitHub Profile Terminal GIF Generator")
    print("  by: Eashan Darsh  @ed6095-web")
    print("─" * 55)

    if args.photo and Path(args.photo).exists():
        print(f"→ Converting photo to ASCII: {args.photo}")
        ascii_lines = photo_to_ascii(args.photo, width=34, height=20)
        print(f"  Generated {len(ascii_lines)} lines × {len(ascii_lines[0])} cols")
    else:
        print("→ No photo found")
        sys.exit(1)

    print("→ Building animation frames ...")
    renderer = build_animation(ascii_lines)
    print(f"  Total frames: {len(renderer.frames)}")

    print("→ Saving GIF ...")
    renderer.save()
    print("─" * 55)
    print("  Done!")

if __name__ == "__main__":
    main()
