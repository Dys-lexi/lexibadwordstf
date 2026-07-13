import base64
import os
from io import BytesIO
from urllib.request import Request, urlopen
import sys
sys.path.append("./wordcloud")
import numpy as np
from PIL import Image
import random
fallback = True
try:
    from wordcloudchanged import ImageColorGenerator, WordCloud
    fallback = False
except:
    print("ohno")
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

    mask = np.zeros(base_colors.shape[:2], dtype=np.uint32)
    mask[base_colors.sum(axis=2) == 0] = 256
    result = base_image.convert("RGBA")
    if frequencies:
        wc = WordCloud(
            # font_path=random.choice(list(map(lambda x: f"./fonts/{x}",(os.listdir("./fonts"))))),
            font_path= os.path.exists( "./fonts")and os.listdir("./fonts") and sorted(list(map(lambda x: f"./fonts/{x}",(os.listdir("./fonts")))),key = lambda x: os.path.getctime(x), reverse = True)[0] or None,

            max_words=100,
            mask=mask,
            max_font_size=250,
            random_state=42,
            relative_scaling=0.0 if  fallback else 0.7,
            mode="RGBA",
            background_color=None,
            min_font_size=5,
            repeat=fallback,
            normalize_plurals=True
        )
        # print(frequencies)
        wc.generate_from_frequencies(dict(sorted(list(frequencies.items()),key = lambda x: x[1],reverse = True)))

        inverted_colors = np.clip(255 - base_colors.astype(np.int16) - 20, 1, 255).astype(
            np.uint8
        )
        wc.recolor(color_func=ImageColorGenerator(inverted_colors))
        # wc.recolor(color_func=lambda *args, **kwargs: f"rgb({random.randint(254,255)},{random.randint(0,3)},{random.randint(200,255)})")
        word_layer = wc.to_image().convert("RGBA")
        
        result.alpha_composite(word_layer)

    if output_path:
        result.save(output_path)

    buffer = BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()

