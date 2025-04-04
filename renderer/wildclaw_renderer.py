from PIL import Image, ImageChops
import os
from data.breed_colors.wildclaw_colors import WILDCLAW_COLOR_MAP

BREED = "Wildclaw"
IMAGE_DIR = f"assets/{BREED}/"
LAYER_ORDER = [
    "primary", "belly", "horns",
    "secondary", "feathers",
    "shadow", "eye-nostril", "lineart"
]

def safe_get_color(color_map, color_name, key, fallback="#CCCCCC"):
    """Safely retrieve a hex color for a layer."""
    try:
        return color_map[color_name][key]
    except KeyError:
        print(f"⚠️ Missing color '{color_name}' or key '{key}'")
        return fallback

def recolor_flat_layer(image, hex_color):
    """Recolors all non-transparent pixels with the exact given color."""
    image = image.convert("RGBA")
    r, g, b = Image.new("RGB", image.size, hex_color).split()
    _, _, _, alpha = image.split()
    return Image.merge("RGBA", (r, g, b, alpha))

def render_child_image(primary_color, secondary_color):
    canvas = None
    shadow_opacity = 0.6  # ✅ Adjust shadow strength here

    for layer in LAYER_ORDER:
        filename = f"{BREED.lower()}_{layer}.png"
        path = os.path.join(IMAGE_DIR, filename)

        if not os.path.exists(path):
            continue

        img = Image.open(path).convert("RGBA")

        # Recolor if needed
        if layer in ["primary", "belly", "horns"]:
            color_key = "base" if layer == "primary" else layer
            hex_color = safe_get_color(WILDCLAW_COLOR_MAP, primary_color, color_key)
            img = recolor_flat_layer(img, hex_color)

        elif layer in ["secondary", "feathers"]:
            color_key = "base" if layer == "secondary" else "feathers"
            hex_color = safe_get_color(WILDCLAW_COLOR_MAP, secondary_color, color_key)
            img = recolor_flat_layer(img, hex_color)

        if canvas is None:
            canvas = Image.new("RGBA", img.size)

        # ✅ Multiply shadow while preserving alpha gradient
        if layer == "shadow":
            base_rgb = canvas.convert("RGB")
            shadow_rgb = img.convert("RGB")
            multiplied = ImageChops.multiply(base_rgb, shadow_rgb)

            # Restore original shadow alpha
            alpha = img.getchannel("A")
            multiplied.putalpha(alpha)

            # Composite result over base with reduced opacity
            translucent_shadow = Image.new("RGBA", img.size)
            translucent_shadow = Image.alpha_composite(translucent_shadow, multiplied)

            # Adjust opacity of shadow
            mask = alpha.point(lambda p: int(p * shadow_opacity))
            canvas = Image.composite(translucent_shadow, canvas, mask)

        else:
            canvas = Image.alpha_composite(canvas, img)
            
    return canvas
