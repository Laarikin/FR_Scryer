import streamlit as st
import random

from data.color_wheel import COLOR_WHEEL
from logic.color_logic import get_inherited_color
from renderer.wildclaw_renderer import render_child_image
from PIL import Image

# --- Settings ---
BREED = "Wildclaw"
CHILD_COUNT = 15
COLOR_NAMES = [c["name"] for c in COLOR_WHEEL]

# --- UI Setup ---
st.set_page_config(page_title="Flight Rising Scryer", layout="wide")
st.title("🧬 Flight Rising Scrying Tool")
st.caption("Preview randomly generated Wildclaw offspring based on parent colors.")

# --- Parent Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Parent A")
    parent_a = {
        "primary_color": st.selectbox("Primary Color", COLOR_NAMES, key="primary_color_a"),
        "secondary_color": st.selectbox("Secondary Color", COLOR_NAMES, key="secondary_color_a"),
        "tertiary_color": st.selectbox("Tertiary Color (Unused)", COLOR_NAMES, key="tertiary_color_a"),
    }

with col2:
    st.subheader("Parent B")
    parent_b = {
        "primary_color": st.selectbox("Primary Color", COLOR_NAMES, key="primary_color_b"),
        "secondary_color": st.selectbox("Secondary Color", COLOR_NAMES, key="secondary_color_b"),
        "tertiary_color": st.selectbox("Tertiary Color (Unused)", COLOR_NAMES, key="tertiary_color_b"),
    }

st.divider()

# --- Generate Button ---
# Generate button click logic
if st.button("🐣 Generate 12 Offspring"):
    st.subheader("Generated Offspring")
    cols = st.columns(5)

    for i in range(CHILD_COUNT):
        primary_color = get_inherited_color(
            parent_a["primary_color"], parent_b["primary_color"], COLOR_WHEEL
        )
        secondary_color = get_inherited_color(
            parent_a["secondary_color"], parent_b["secondary_color"], COLOR_WHEEL
        )

        image = render_child_image(primary_color, secondary_color)

        # ✅ Resize image before displaying
        resized_image = image.resize((350, 350), resample=Image.LANCZOS)

        with cols[i % 5]:
            st.image(resized_image, caption=f"{primary_color} / {secondary_color}", width=350)

