# Installation & Deployment Guide

This repository contains the complete redesigned GitHub Profile README for **Eashan Darsh** (`@ed6095-web`).

---

## 📁 Repository Structure

```
ed6095-web/
├── README.md                           ← Main GitHub Profile README
├── INSTALLATION.md                     ← This deployment guide
├── assets/
│   ├── terminal.gif                    ← Animated terminal boot GIF (ASCII portrait from photo)
│   ├── header.svg                      ← Terminal window header SVG
│   ├── divider_matrix.svg              ← Matrix rain animated SVG divider
│   ├── divider_line.svg                ← Clean gradient separator SVG
│   ├── quote.svg                       ← Daily dev quote terminal SVG
│   └── profile.png                     ← Original profile photo
├── scripts/
│   ├── generate_terminal_gif.py        ← Python script to convert photo → ASCII terminal GIF
│   ├── rotate_quote.py                 ← Python script to rotate daily dev quotes
│   └── make_gif.sh                     ← Shell script helper for Linux/macOS
└── .github/
    └── workflows/
        └── update_quote.yml            ← GitHub Action to automatically rotate quotes daily
```

---

## 🚀 How to Apply to Your GitHub Profile

### Step 1: Clone your profile repository
```bash
git clone https://github.com/ed6095-web/ed6095-web.git
cd ed6095-web
```

### Step 2: Copy all files
Copy all the generated files and folders (`README.md`, `assets/`, `scripts/`, `.github/`) into your `ed6095-web` repository folder.

In PowerShell:
```powershell
Copy-Item -Recurse -Force "C:\Users\Eashan Darsh\.gemini\antigravity\scratch\github-profile-readme\*" .
```

### Step 3: Commit and Push
```bash
git add .
git commit -m "feat: complete redesign of profile README with terminal aesthetic"
git push origin main
```

Your GitHub profile at `https://github.com/ed6095-web` will immediately render the new terminal README!

---

## 🛠️ How to Regenerate the ASCII Terminal GIF

If you ever update your profile photo, you can regenerate `assets/terminal.gif`:

```bash
# Install Pillow
pip install Pillow

# Run the generator with your new photo
python scripts/generate_terminal_gif.py --photo assets/your_new_photo.png
```

---

## 🔄 Daily Dev Quote Rotation

The GitHub Action in `.github/workflows/update_quote.yml` runs automatically every night at 00:00 UTC to rotate the dev quote in `assets/quote.svg`.

You can also trigger it manually from the **Actions** tab on GitHub or locally with:
```bash
python scripts/rotate_quote.py
```
