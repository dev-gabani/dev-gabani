#!/usr/bin/env python3
"""
Prepare a photo for clean ASCII conversion:
  1. Grayscale conversion
  2. Bilateral filter smoothing to reduce texture/camera noise
  3. CLAHE (Contrast-Limited Adaptive Histogram Equalization) for crisp face features
  4. Subtle edge enhancement so eyes, hair, and contours stay distinct
  5. Save as source-prepped.png

Usage:
  python scripts/prep_photo.py [input.jpg/png] [output.png]
"""
import os
import sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

if not os.path.exists(INP):
    print(f"Error: input photo {INP} not found", file=sys.stderr)
    sys.exit(1)

# Load image
img = cv2.imread(INP)
if img is None:
    print(f"Error: could not read image {INP}", file=sys.stderr)
    sys.exit(1)

# Square center-crop if not already square
h, w = img.shape[:2]
min_side = min(h, w)
cy, cx = h // 2, w // 2
crop = img[cy - min_side//2 : cy + min_side//2, cx - min_side//2 : cx + min_side//2]
crop = cv2.resize(crop, (600, 600), interpolation=cv2.INTER_AREA)

# Grayscale
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

# Bilateral smoothing (preserves edges, removes grain)
smooth = cv2.bilateralFilter(gray, d=9, sigmaColor=50, sigmaSpace=9)

# CLAHE for local contrast
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
enhanced = clahe.apply(smooth)

# Subtle edge sharpening
blur = cv2.GaussianBlur(enhanced, (0, 0), 1.5)
sharp = cv2.addWeighted(enhanced, 1.4, blur, -0.4, 0)

# Save prepped image
cv2.imwrite(OUT, sharp)
print(f"Prepped photo saved to {OUT} ({sharp.shape[1]}x{sharp.shape[0]})")
