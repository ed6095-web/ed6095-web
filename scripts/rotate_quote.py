#!/usr/bin/env python3
"""
rotate_quote.py
===============
Picks a random quote from the hardcoded list and regenerates assets/quote.svg.
Run manually or via the GitHub Action (.github/workflows/update_quote.yml).

Usage:
    python scripts/rotate_quote.py
"""

import random
import hashlib
from datetime import datetime
from pathlib import Path

QUOTES = [
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Abelson & Sussman"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("The best code is no code at all.", "Jeff Atwood"),
    ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
    ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Measuring programming progress by lines of code is like measuring aircraft progress by weight.", "Bill Gates"),
    ("The most disastrous thing you can ever learn is your first programming language.", "Alan Kay"),
    ("A good programmer is someone who always looks both ways before crossing a one-way street.", "Doug Linder"),
    ("Software is a great combination of artistry and engineering.", "Bill Gates"),
    ("The function of good software is to make the impossible possible.", "Douglas McIlroy"),
]

OUTPUT = Path(__file__).parent.parent / "assets" / "quote.svg"

def pick_quote() -> tuple[str, str]:
    """Pick today's quote deterministically (same quote all day)."""
    day_seed = datetime.utcnow().strftime("%Y-%m-%d")
    idx = int(hashlib.md5(day_seed.encode()).hexdigest(), 16) % len(QUOTES)
    return QUOTES[idx]

def wrap_text(text: str, max_chars: int = 58) -> list[str]:
    """Wrap text to lines of max_chars."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def generate_svg(quote: str, author: str) -> str:
    lines = wrap_text(f'"{quote}"')
    line_height = 22
    content_height = len(lines) * line_height + 60
    total_height = content_height + 40
    total_height = max(total_height, 110)

    line_svgs = []
    for i, line in enumerate(lines):
        y = 68 + i * line_height
        esc = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        line_svgs.append(f'  <text x="16" y="{y}" class="prompt white" font-size="13">{esc}</text>')

    author_y = 68 + len(lines) * line_height + 14
    author_esc = author.replace('&', '&amp;')
    line_svgs.append(f'  <text x="16" y="{author_y}" class="prompt muted" font-size="12">  — {author_esc}</text>')

    cursor_y = author_y + 20
    prompt_bottom = f'  <text x="16" y="{cursor_y}" class="prompt" font-size="12"><tspan class="green">ed6095-web</tspan><tspan class="muted">@github</tspan><tspan class="muted">:~$ </tspan><tspan class="cursor">█</tspan></text>'
    line_svgs.append(prompt_bottom)

    real_height = cursor_y + 12

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="780" height="{real_height}" viewBox="0 0 780 {real_height}">
  <defs>
    <style>
      .bg    {{ fill: #161b22; }}
      .border{{ stroke: #30363d; stroke-width:1; fill:none; }}
      .prompt{{ font-family: \'Courier New\', \'JetBrains Mono\', monospace; }}
      .green {{ fill: #3FB950; }}
      .blue  {{ fill: #58A6FF; }}
      .muted {{ fill: #8B949E; }}
      .white {{ fill: #F0F6FC; }}
      @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}
      .cursor{{ animation: blink 1.2s step-end infinite; fill: #3FB950; }}
    </style>
  </defs>
  <rect width="780" height="{real_height}" rx="8" class="bg"/>
  <rect width="780" height="{real_height}" rx="8" class="border"/>
  <rect width="780" height="26" rx="8" fill="#21262d"/>
  <rect y="18" width="780" height="8" fill="#21262d"/>
  <line x1="0" y1="26" x2="780" y2="26" stroke="#30363d" stroke-width="1"/>
  <circle cx="16" cy="13" r="5" fill="#FF5F56"/>
  <circle cx="34" cy="13" r="5" fill="#FFBD2E"/>
  <circle cx="52" cy="13" r="5" fill="#27C93F"/>
  <text x="390" y="17" text-anchor="middle" class="prompt muted" font-size="11">quote.md</text>
  <text x="16" y="48" class="prompt" font-size="13">
    <tspan class="green">ed6095-web</tspan><tspan class="muted">@github</tspan><tspan class="muted">:~$ </tspan><tspan class="blue">cat</tspan><tspan class="white"> quote.md</tspan>
  </text>
{chr(10).join(line_svgs)}
</svg>'''

def main():
    quote, author = pick_quote()
    svg = generate_svg(quote, author)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Updated quote: \"{quote[:50]}...\" — {author}")
    print(f"  Saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
