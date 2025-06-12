import os
from PIL import Image
import subprocess

def create_iconset():
    # Create iconset directory if it doesn't exist
    iconset_dir = "app_icon.iconset"
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)

    # Load the original icon
    original_icon = Image.open("iconTemplate_boldOutline.png")
    
    # Define the required sizes
    sizes = {
        "icon_16x16.png": 16,
        "icon_16x16@2x.png": 32,
        "icon_32x32.png": 32,
        "icon_32x32@2x.png": 64,
        "icon_128x128.png": 128,
        "icon_128x128@2x.png": 256,
        "icon_256x256.png": 256,
        "icon_256x256@2x.png": 512,
        "icon_512x512.png": 512,
        "icon_512x512@2x.png": 1024
    }

    # Generate each size
    for filename, size in sizes.items():
        resized = original_icon.resize((size, size), Image.Resampling.LANCZOS)
        output_path = os.path.join(iconset_dir, filename)
        resized.save(output_path, "PNG")
        print(f"Created {filename}")

    # Create the .icns file
    subprocess.run(["iconutil", "-c", "icns", iconset_dir])
    print("\nCreated app_icon.icns")

    # Clean up the iconset directory
    for filename in os.listdir(iconset_dir):
        os.remove(os.path.join(iconset_dir, filename))
    os.rmdir(iconset_dir)
    print("Cleaned up temporary files")

if __name__ == "__main__":
    create_iconset() 