import base64
import os
from io import BytesIO
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image
from wordcloud import ImageColorGenerator, WordCloud
import random

DEFAULT_URL = "https://avatars.fastly.steamstatic.com/0c337d8bb0fa932b3927aea319be0ad7787fe6f9_full.jpg"
IMAGE_SIZE = (1000, 1000)



def load_image_from_url(url, size=IMAGE_SIZE):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        image_data = response.read()

    return (
        Image.open(BytesIO(image_data))
        .convert("RGB")
        .resize(size, Image.Resampling.LANCZOS)
    )





def makewordcloud(url, frequencies, output_path=None, image_size=IMAGE_SIZE):
    base_image = load_image_from_url(url, image_size)
    base_colors = np.array(base_image)

    mask = np.zeros(base_colors.shape[:2], dtype=np.uint8)
    mask[base_colors.sum(axis=2) == 0] = 255
    result = base_image.convert("RGBA")
    if frequencies:
        wc = WordCloud(
            max_words=100,
            mask=mask,
            max_font_size=100,
            random_state=42,
            relative_scaling=0.0,
            mode="RGBA",
            background_color=None,
            min_font_size=10,
            repeat=True,
            normalize_plurals=True
        )

        wc.generate_from_frequencies(dict(list(frequencies.items())))

        inverted_colors = np.clip(255 - base_colors.astype(np.int16) - 20, 0, 255).astype(
            np.uint8
        )
        wc.recolor(color_func=ImageColorGenerator(inverted_colors))
        # wc.recolor(color_func=lambda *args, **kwargs: f"rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})")
        word_layer = wc.to_image().convert("RGBA")
        
        result.alpha_composite(word_layer)

    if output_path:
        result.save(output_path)

    buffer = BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()

