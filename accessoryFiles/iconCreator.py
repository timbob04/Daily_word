
from PIL import Image, ImageDraw

img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))        # 40×40 transparent
draw = ImageDraw.Draw(img)
draw.rectangle((8, 8, 32, 32), fill=(255, 255, 255, 255))  # white square glyph
img.save("iconTemplate.png")   # saved in the current directory
