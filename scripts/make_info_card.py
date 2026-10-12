#!/usr/bin/env python3
"""
Generate a Neofetch-style terminal info card SVG for Dev Gabani.
Canvas is 840 x 880 (matches dev-ascii.svg and stats.svg).
Animates line-by-line using CSS keyframes.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 880
PAD = 28
TITLEBAR_H = 34
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#111722"
MUTED = "#7d8590"
INK = "#e6edf3"
CYAN = "#58a6ff"
GREEN = "#39d353"
PURPLE = "#bc8cff"
ORANGE = "#f0883e"
RED = "#ff7b72"
YELLOW = "#d29922"

LINE_DUR = 0.35
STAGGER = 0.12

info_lines = [
    ("OS", "Arch Linux x86_64", CYAN),
    ("Host", "Dev Gabani (Full-Stack & Security)", INK),
    ("Kernel", "Python 3.10 • Flask • TypeScript • PostgreSQL", GREEN),
    ("Uptime", "Building AI tools & high-impact web apps", YELLOW),
    ("Projects", "cyber-defense-simulator, smart-expense, f1-pitwall", ORANGE),
    ("Shell", "zsh 5.9 (dev@github)", PURPLE),
    ("Terminal", "kitty / alacritty", MUTED),
    ("Stack", "Python, JavaScript, Flask, HTML5/CSS3, OCaml, Render, Vercel", INK),
    ("Interests", "Cybersecurity, ML Detection, F1 Motorsport Telemetry 🏎️", CYAN),
    ("Status", "Open to collaboration, projects & internships", GREEN),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>'
    f'.line{{opacity:0;animation:slideIn {LINE_DUR}s ease-out both}}'
    '@keyframes slideIn{0%{opacity:0;transform:translateX(-10px)}100%{opacity:1;transform:translateX(0)}}'
    '@media (prefers-reduced-motion: reduce){.line{opacity:1!important;transform:none!important;animation:none!important}}'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">dev@github: ~$ neofetch</text>')

# Content start
content_y = TITLEBAR_H + 50
curr_delay = 0.1

# Prompt line
parts.append(f'<g class="line" style="animation-delay:{curr_delay:.2f}s">')
parts.append(f'<text x="{PAD+10}" y="{content_y}" font-size="24" font-weight="700">'
             f'<tspan fill="{GREEN}">dev@github</tspan>'
             f'<tspan fill="{MUTED}">:</tspan>'
             f'<tspan fill="{CYAN}">~</tspan>'
             f'<tspan fill="{INK}">$ neofetch</tspan></text>')
parts.append('</g>')

content_y += 38
curr_delay += STAGGER

# User banner
parts.append(f'<g class="line" style="animation-delay:{curr_delay:.2f}s">')
parts.append(f'<text x="{PAD+10}" y="{content_y}" font-size="28" font-weight="800">'
             f'<tspan fill="{CYAN}">dev</tspan>'
             f'<tspan fill="{MUTED}">@</tspan>'
             f'<tspan fill="{GREEN}">github</tspan></text>')
parts.append(f'<text x="{PAD+10}" y="{content_y+20}" fill="{FRAME}" font-size="22">--------------------------------------------------</text>')
parts.append('</g>')

content_y += 56
curr_delay += STAGGER

# Key-value rows
for key, val, color in info_lines:
    safe_key = html.escape(key)
    safe_val = html.escape(val)
    parts.append(f'<g class="line" style="animation-delay:{curr_delay:.2f}s">')
    parts.append(f'<text x="{PAD+10}" y="{content_y}" font-size="20">'
                 f'<tspan fill="{CYAN}" font-weight="700">{safe_key:10}</tspan> '
                 f'<tspan fill="{MUTED}">~</tspan> '
                 f'<tspan fill="{color}">{safe_val}</tspan></text>')
    parts.append('</g>')
    content_y += 46
    curr_delay += STAGGER

# Color palette blocks at the bottom
palette_y = H - 65
curr_delay += STAGGER
parts.append(f'<g class="line" style="animation-delay:{curr_delay:.2f}s">')
palette_colors = ["#161b22", "#f85149", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
for idx, col in enumerate(palette_colors):
    bx = PAD + 10 + idx * 48
    parts.append(f'<rect x="{bx}" y="{palette_y}" width="38" height="20" rx="4" fill="{col}"/>')
for idx, col in enumerate(palette_colors):
    bx = PAD + 10 + idx * 48
    parts.append(f'<rect x="{bx}" y="{palette_y + 24}" width="38" height="20" rx="4" fill="{col}" opacity="0.65"/>')
parts.append('</g>')

parts.append('</svg>')
svg = "".join(parts)
open(OUT, "w", encoding="utf-8").write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
