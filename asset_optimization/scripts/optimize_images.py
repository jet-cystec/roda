#!/usr/bin/env python3
"""
Performance & Asset Optimizer for Static Sites
==============================================
Provides automated WebP conversion, background transparency removal,
and remote asset downloading for high-performance static websites.

Requirements:
    pip install Pillow
"""

import os
import sys
from PIL import Image

def optimize_image(image_path, quality=85):
    """Converts a local image to WebP format."""
    try:
        if not os.path.exists(image_path):
            print(f"❌ Error: File '{image_path}' not found.")
            return False

        img = Image.open(image_path)
        filename, _ = os.path.splitext(image_path)
        output_path = f"{filename}.webp"
        
        print(f"🔄 Converting '{image_path}' to WebP...")
        img.save(output_path, 'WEBP', quality=quality)
        
        original_size = os.path.getsize(image_path)
        new_size = os.path.getsize(output_path)
        savings = ((original_size - new_size) / original_size) * 100
        
        print(f"✅ Success: {output_path} ({savings:.2f}% savings)")
        return True
    except Exception as e:
        print(f"❌ Error optimizing {image_path}: {e}")
        return False

def make_transparent(image_path, threshold=240):
    """Removes white/near-white backgrounds from images (icons)."""
    try:
        if not os.path.exists(image_path): return False
        
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(image_path, "PNG") # Keeps transparency in source
        print(f"✨ Transparency added to '{image_path}'")
        return True
    except Exception as e:
        print(f"❌ Error adding transparency: {e}")
        return False

def download_and_optimize(url, output_name, quality=80):
    """Downloads remote URL and optimizes to local WebP."""
    import urllib.request
    try:
        print(f"⬇️ Downloading asset to {output_name}...")
        temp_file = "temp_asset.jpg"
        urllib.request.urlretrieve(url, temp_file)
        
        success = optimize_image(temp_file, quality)
        if success and os.path.exists("temp_asset.webp"):
            os.rename("temp_asset.webp", output_name)
            
        if os.path.exists(temp_file): os.remove(temp_file)
        return success
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Use this script directly or import functions into your pipeline.")
    # Example usage:
    # optimize_image('logo.png')
    # make_transparent('icon.png')
    # download_and_optimize('https://example.com/bg.jpg', 'hero-bg.webp')
