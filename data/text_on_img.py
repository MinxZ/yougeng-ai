import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def text_on_img(logo_text):
    logo_text_copy = logo_text
    with open('data/model_offset.json', 'r') as f:
        model_offset = json.load(f)

    l = len(logo_text)
    l_sqrt = int(round((np.sqrt(l))))
    
    logo_text = '\n'.join([logo_text[i:i+l_sqrt] for i in range(0, l, l_sqrt)])

    logo_len = len(logo_text.split('\n')[0])

    for model, value in model_offset.items():
        img_width = model_offset[model][2]-model_offset[model][0]

        if logo_len < len(logo_text.split('\n')):
            add_len = -img_width//10/logo_len*2
        else:
            add_len = img_width//10/logo_len/2

        fontsize = img_width//logo_len
        logo_width = logo_len * fontsize
        # font = ImageFont.load_default(fontsize)
        # font = ImageFont.truetype("/Library/Fonts/simsun.ttc", fontsize)
        font = ImageFont.truetype('data/images/No.39-ShangShouZhiZunShuFaTi-2.ttf', fontsize)

        print(model, value)
        img_path = f'data/images/{model}.png'
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        draw.text((model_offset[model][0], model_offset[model][1]+add_len), logo_text, font=font, fill=(255, 255, 255))
        img.save(f'data/items/tshirt_{model}_{logo_text_copy}.png')

