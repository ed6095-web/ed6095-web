#!/usr/bin/env python3
"""
generate_terminal_gif.py
========================
Generates assets/terminal.gif — an animated terminal boot sequence
with ASCII portrait for Eashan Darsh's GitHub profile README.

Requirements:
    pip install Pillow numpy

Usage:
    # With profile photo (recommended):
    python scripts/generate_terminal_gif.py --photo assets/profile.jpg

    # Without photo (placeholder portrait):
    python scripts/generate_terminal_gif.py
"""

import os
import sys
import math
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
RED            = (248, 81, 73)       # terminal red

GIF_WIDTH      = 720
GIF_HEIGHT     = 420
FONT_SIZE      = 13
CHAR_W         = 8    # approx monospace char width at font size 13
CHAR_H         = 16   # approx monospace char height at font size 13
FRAME_DELAY    = 60   # ms per frame (≈16 fps)

ASCII_CHARS    = "█▓▒░ "   # Dense → light → empty
ASCII_CHARS_EX = "@#%&B8WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,. "

OUTPUT_PATH    = Path(__file__).parent.parent / "assets" / "terminal.gif"

# ─── Font Loading ────────────────────────────────────────────────────────────

def load_font(size: int):
    """Try to load a monospace font, fall back to default."""
    candidates = [
        "JetBrainsMono-Regular.ttf",
        "DejaVuSansMono.ttf",
        "Consolas.ttf",
        "CourierNew.ttf",
        "cour.ttf",           # Windows
        "lucon.ttf",          # Windows Lucida Console
        "UbuntuMono-R.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    # Try system font paths on Windows
    winfonts = Path("C:/Windows/Fonts")
    if winfonts.exists():
        for name in ["consola.ttf", "cour.ttf", "lucon.ttf", "courbd.ttf"]:
            p = winfonts / name
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except Exception:
                    pass
    # Absolute last resort
    return ImageFont.load_default()

# ─── ASCII Art Generation ────────────────────────────────────────────────────

def photo_to_ascii(photo_path: str, width: int = 36, height: int = 28) -> list[str]:
    """Convert photo to clean, sharp ASCII art with edge detection and background removal."""
    img = Image.open(photo_path).convert("L")
    w, h = img.size
    
    # Crop to head and upper body (top 92%)
    crop_box = (int(w * 0.10), int(h * 0.02), int(w * 0.90), int(h * 0.92))
    img = img.crop(crop_box)
    
    # Resize with correct aspect ratio for terminal font
    img_resized = img.resize((width, height), Image.LANCZOS)
    
    # Enhance contrast & sharpness
    img_contrast = ImageEnhance.Contrast(img_resized).enhance(2.0)
    img_sharp = ImageEnhance.Sharpness(img_contrast).enhance(1.8)
    
    # Find edges for facial feature sharpness (glasses, eyes, nose, mustache)
    edges = img_resized.filter(ImageFilter.FIND_EDGES)
    try:
        edges_data = list(edges.get_flattened_data())
        pixels = list(img_sharp.get_flattened_data())
    except AttributeError:
        edges_data = list(edges.getdata())
        pixels = list(img_sharp.getdata())
        
    lines = []
    for r in range(height):
        row = ""
        for c in range(width):
            idx = r * width + c
            p_val = pixels[idx]
            e_val = edges_data[idx]
            
            # Clean background removal (>175 luminance with weak edge -> blank space)
            if p_val > 175 and e_val < 30:
                row += " "
            elif e_val > 70 and p_val < 150:
                # Strong feature edge (glasses frame, facial contours)
                row += "#"
            elif p_val < 35:
                row += "@"
            elif p_val < 65:
                row += "%"
            elif p_val < 95:
                row += "▓"
            elif p_val < 125:
                row += "▒"
            elif p_val < 150:
                row += "░"
            elif p_val < 175:
                row += "-"
            else:
                row += " "
        lines.append(row)
    return lines



def placeholder_ascii() -> list[str]:
    """Return a hand-crafted ASCII portrait placeholder."""
    art = [
        "                                                       ",
        "             .:-=+*#%@@@@@@@@%#*+=:-.                 ",
        "           :*@@@@@@@@@@@@@@@@@@@@@@@@*:               ",
        "         .#@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.             ",
        "        =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=            ",
        "       *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*           ",
        "      #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#          ",
        "      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%          ",
        "      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%          ",
        "      %@@@@@@%*=:.         .:=*%@@@@@@@@@@%           ",
        "      *@@@@@@-               -@@@@@@@@@@@@*           ",
        "       %@@@@@  [##]     [##]  @@@@@@@@@@@%            ",
        "       +@@@@@+--++-   -+--++-+@@@@@@@@@@@+            ",
        "        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#             ",
        "         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%              ",
        "          *@@@@@@@@*======*@@@@@@@@@@@@*              ",
        "           =@@@@@@@@@@@@@@@@@@@@@@@@@@=               ",
        "            -%@@@@@@@@@@@@@@@@@@@@@@%-                ",
        "              :*@@@@@@@@@@@@@@@@@@*:                  ",
        "                .-+#@@@@@@@@@@#+-                     ",
        "              .=#@@@@@@@@@@@@@@@@#=.                  ",
        "            .*@@@@@@@@@@@@@@@@@@@@@@*.                ",
        "           +@@@@@@@@@@@@@@@@@@@@@@@@@@+               ",
        "          #@@@@@@@@@@@@@@@@@@@@@@@@@@@@#              ",
        "         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%             ",
        "        *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*            ",
        "       .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.           ",
        "        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@            ",
    ]
    return art

# ─── Frame Rendering ─────────────────────────────────────────────────────────

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
        # Window chrome
        self._draw_chrome(draw)
        return img, draw

    def _draw_chrome(self, draw: ImageDraw.ImageDraw):
        # Top bar
        draw.rounded_rectangle(
            [0, 0, GIF_WIDTH - 1, GIF_HEIGHT - 1],
            radius=10, outline=(48, 54, 61), width=1
        )
        draw.rectangle([1, 1, GIF_WIDTH - 2, 28], fill=(33, 38, 45))
        draw.line([1, 29, GIF_WIDTH - 2, 29], fill=(48, 54, 61))

        # Traffic light buttons
        btns = [(16, 14, (255, 95, 86)), (36, 14, (255, 189, 46)), (56, 14, (39, 201, 63))]
        for bx, by, bc in btns:
            draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=bc)

        # Title
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
        # Last frame lingers longer for readability
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
    MAX_COLS  = (GIF_WIDTH - 2 * r.pad_x) // CHAR_W
    MAX_ROWS  = (GIF_HEIGHT - r.pad_y - 4)  // CHAR_H
    ascii_w   = min(len(ascii_lines[0]) if ascii_lines else 55, MAX_COLS)
    ascii_h   = min(len(ascii_lines), MAX_ROWS - 4)

    # Center horizontally
    col_offset = max(0, (MAX_COLS - ascii_w) // 2)
    # Start at row 1
    start_row  = 1

    for reveal in range(ascii_h + 1):
        img, draw = r.new_frame()
        # Header label
        r.text(draw, 0, col_offset, "┌─ ASCII PORTRAIT ──────────────────────────────────┐", MUTED)
        for ln in range(reveal):
            line_text = ascii_lines[ln][:ascii_w]
            # Gradient brightness: top bright, bottom fades
            brightness = 1.0 - (ln / max(ascii_h, 1)) * 0.3
            shade = tuple(int(c * brightness) for c in GREEN)
            r.text(draw, start_row + ln, col_offset, "│ " + line_text.ljust(ascii_w - 2) + " │", shade)
        r.add_frame(img)

    # ── Phase 5: whoami info prints line by line ──────────────────────────
    whoami_lines = [
        ("$ whoami",                                         BLUE,   True),
        ("──────────────────────────────────────────────────", MUTED,  False),
        ("  Name        :  Eashan Darsh",                    WHITE,  False),
        ("  Role        :  Backend Developer",               WHITE,  False),
        ("  Education   :  B.Tech CS Engg  (AI & ML)",       WHITE,  False),
        ("  Focus       :  Backend · System Design · AI",    WHITE,  False),
        ("  OS          :  Linux",                           GREEN,  False),
        ("  Editor      :  VS Code",                         BLUE,   False),
        ("  Location    :  Chennai, Tamil Nadu",              WHITE,  False),
        ("  Status      :  [ Building every day ]",          YELLOW, False),
        ("──────────────────────────────────────────────────", MUTED,  False),
        ("$  _",                                             GREEN,  False),
    ]

    # Re-draw portrait at full, then add info lines
    for i in range(len(whoami_lines) + 1):
        img, draw = r.new_frame()
        # Reduced portrait on left (35 cols)
        portrait_cols = min(36, len(ascii_lines[0]) if ascii_lines else 36)
        info_col_start = portrait_cols + 3
        r.text(draw, 0, 0, "┌─ ASCII PORTRAIT ─────────────────────┐", MUTED)
        for ln in range(ascii_h):
            line_text = ascii_lines[ln][:portrait_cols]
            r.text(draw, 1 + ln, 0, "│ " + line_text.ljust(portrait_cols - 2) + " │", GREEN)

        # Info on right
        for j, (line, color, bold) in enumerate(whoami_lines[:i]):
            r.text(draw, 1 + j, info_col_start, line, color, bold=bold)
        r.add_frame(img)

    # ── Phase 6: Blinking cursor final frame ──────────────────────────────
    for blink in range(8):
        img, draw = r.new_frame()
        # Portrait
        r.text(draw, 0, 0, "┌─ ASCII PORTRAIT ─────────────────────┐", MUTED)
        portrait_cols = min(36, len(ascii_lines[0]) if ascii_lines else 36)
        info_col_start = portrait_cols + 3
        for ln in range(ascii_h):
            line_text = ascii_lines[ln][:portrait_cols]
            r.text(draw, 1 + ln, 0, "│ " + line_text.ljust(portrait_cols - 2) + " │", GREEN)
        # All info
        for j, (line, color, bold) in enumerate(whoami_lines[:-1]):
            r.text(draw, 1 + j, info_col_start, line, color, bold=bold)
        # Blinking cursor
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

    # Get ASCII lines
    if args.photo and Path(args.photo).exists():
        print(f"→ Converting photo to ASCII: {args.photo}")
        ascii_lines = photo_to_ascii(args.photo, width=55, height=28)
        print(f"  Generated {len(ascii_lines)} lines × {len(ascii_lines[0])} cols")
    else:
        print("→ No photo found — using placeholder ASCII portrait")
        print("  TIP: Run with --photo assets/profile.jpg for real portrait")
        ascii_lines = placeholder_ascii()

    print("→ Building animation frames ...")
    renderer = build_animation(ascii_lines)
    print(f"  Total frames: {len(renderer.frames)}")

    print("→ Saving GIF ...")
    renderer.save()
    print("─" * 55)
    print("  Done! Add to README.md:")
    print('  <img src="assets/terminal.gif" />')
    print("─" * 55)


if __name__ == "__main__":
    main()
