import random

def get_inherited_color(parent_a, parent_b, color_wheel):
    color_names = [c["name"] for c in color_wheel]

    if parent_a not in color_names or parent_b not in color_names:
        raise ValueError(f"Parent colors '{parent_a}' or '{parent_b}' not found in color wheel")

    i1 = color_names.index(parent_a)
    i2 = color_names.index(parent_b)

    n = len(color_names)

    # Clockwise range
    if i1 <= i2:
        forward = color_names[i1:i2 + 1]
        backward = color_names[i2:] + color_names[:i1 + 1]
    else:
        forward = color_names[i1:] + color_names[:i2 + 1]
        backward = color_names[i2:i1 + 1]

    # Choose the shorter arc
    color_range = forward if len(forward) <= len(backward) else backward

    print(f"🎨 Inherited range from '{parent_a}' to '{parent_b}': {color_range}")
    return random.choice(color_range)
