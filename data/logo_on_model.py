import json

from PIL import Image

# model_offset = {
#     'tshirt_mask': (571, 510, 1120),
#     'black': (100, 100, 1010),
#     'model1':  (516, 558, 776),
#     'model2':  (400, 518, 624),
#     'model5':  (385, 598, 654),
# }

# with open('data/model_offset.json', 'w') as f:
#     json.dump(model_offset, f)

def logo_on_img(logo_path):
    with open('data/model_offset.json', 'r') as f:
        model_offset = json.load(f)

    for model, value in model_offset.items():
        print(model, value)

        img_path = f'data/images/{model}.png'
        logo_path = 'data/images/WechatIMG38.jpg'
        img = Image.open(img_path)
        logo = Image.open(logo_path)
        width, height = logo.size 
        blur_ratio = 0.65
        size = int((model_offset[model][2]-model_offset[model][0])*blur_ratio)
        ratio = size/width
        logo = logo.resize((size, int(height*ratio)))
        logo_resize_path = 'data/images/WechatIMG32_300.png'
        logo.save(logo_resize_path)
        logo = Image.open(logo_resize_path)
        logo = logo.resize((int(size/blur_ratio), int(height*ratio/blur_ratio)))
        # logo = logo.filter(ImageFilter.GaussianBlur(radius=1.2))

        logo_path_name = logo_path.split('/')[-1].split('.')[0]

        img.paste(logo, model_offset[model][:2])
        img.save(f'data/items/tshirt_{model}_{logo_path_name}.png')