from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def create_gradient_image(width, height, color1, color2, output_path):
    """Create a vertical gradient image from color1 to color2."""
    image = Image.new("RGB", (width, height), color1)
    for y in range(height):
        for x in range(width):
            ratio = 0.5*(y / height + x / width)
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            image.putpixel((x, y), (r, g, b))
    image.save(output_path)

def color_function(x,lo,hi):
    x %= 1
    if x<1/6:
        return int(lo+(hi-lo)*x*6)
    elif x < 3/6:
        return hi
    elif x < 4/6:
        return int(lo+(hi-lo)*(1-(x-0.5)*6))
    return lo


def create_gradient_color_tupels(n):
    gradients = []
    lo = 120
    hi = 255
    for i in range(n):
        x1 = (i-1)/(n-1)
        r1 = color_function(x1,lo,hi)
        g1= color_function(x1+0.33,lo,hi)
        b1 = color_function(x1+0.66,lo,hi)

        x2 = (i+1)/(n-1)
        r2 = color_function(x2,lo,hi)
        g2 = color_function(x2+0.33,lo,hi)
        b2 = color_function(x2+0.66,lo,hi)
        gradients += [((r1,g1,b1), (r2,g2,b2))]
    return gradients

# ---- CONFIG ----
output_dir = "gradient_images"
os.makedirs(output_dir, exist_ok=True)

# Define some gradient color pairs
gradients = create_gradient_color_tupels(15)
#print(gradients)

# Create images
image_paths = []
for i, (start, end) in enumerate(gradients):
    path = os.path.join(output_dir, f"gradient_{i}.png")
    create_gradient_image(199, 144, start, end, path)
    image_paths.append(path)
