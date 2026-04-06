---
name: Performance & Asset Optimization
description: Automated workflows for WebP conversion, favicon implementation, and high-performance static asset management.
---

# Performance & Asset Optimization Skill

This skill provides a standardized approach to auditing and optimizing visual assets for static websites (HTML/CSS/JS). It focuses on **Core Web Vitals** through next-gen formats and smart image handling.

## 🚀 Optimization Workflow

### 1. Image Conversion (WebP)
Convert all heavy PNG/JPG assets to WebP to reduce byte size by 50-80% without visible loss of quality.

**Usage:**
Run the provided script to process your assets:
```bash
python3 scripts/optimize_images.py
```

### 2. Smart Favicons (Mobile & Desktop)
Implement a universal icon system that looks professional in any browser theme (Dark/Light).

**Steps:**
1.  **Transparency**: Run `make_transparent('icon.png')` to remove white backgrounds.
2.  **Implementation**: Add the following to your `<head>`:

```html
<!-- Modern Favicon -->
<link rel="icon" type="image/webp" href="favicon.webp">
<!-- iOS/Apple Support -->
<link rel="apple-touch-icon" href="favicon.png">
```

### 3. Remote Hero Optimization
Avoid loading heavy external images directly from Unsplash/CDNs. Download and optimize them locally.

**Python Logic:**
```python
download_and_optimize('https://images.unsplash.com/...', 'hero-bg.webp')
```

## 🛠️ Tooling: `optimize_images.py`

Located at `scripts/optimize_images.py`, this script contains:
- `optimize_image()`: Single file conversion.
- `make_transparent()`: Background removal (Threshold-based).
- `download_and_optimize()`: Remote fetching + local optimization.

## 🎨 Best Practices
- **Threshold**: Use a transparency threshold of `240-250` for icons to handle anti-aliased white edges.
- **Fallbacks**: Keep original PNGs for Social Media meta tags (Open Graph).
- **Quality**: Use `quality=85` for Logos and `quality=75` for large background images.
