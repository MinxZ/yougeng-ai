import json
import time

import leancloud
import requests
from PIL import Image

# paste logo on tshirt
img_path = 'data/images/ori_tshirt.png'
img_mask_path = 'data/images/tshirt_mask.png'
logo_path = 'data/images/WechatIMG38.jpg'
img = Image.open(img_path)
width, height = img.size 

logo = Image.open(logo_path)
width, height = logo.size 
ratio = 600/width
logo = logo.resize((600, int(height*ratio)))
# logo.save('data/images/WechatIMG32_300.png')
# 553 434
# 764 733
# weight = 733-434

offset = (434*2, 530*2)
img.paste(logo, offset)
tshirt_path = 'data/images/tshirt.png'
img.crop((322, 652, 2002, 2400)).save('data/images/tshirt.png')
# img.save(tshirt_path)

# save img to leancloud
app_id = 'Db7SYRSourdqRRckhnk89ykR-MdYXbMMI'
app_key = '5qJj7R3ijhUcc8ldKDFKUOQT'
leancloud.init(app_id, app_key)

# img_path = '/Users/z/Downloads/openai.jpg'

def upload(img_path):
    with open(img_path, 'rb') as f:
        file = leancloud.File(img_path.split('/')[-1], f)
        file.save()
        return file.url

img_cloth_dict = {}
cloth_img_path = tshirt_path
img_cloth_dict[cloth_img_path] = upload(cloth_img_path)
img_cloth_dict[img_path] = upload(img_path)
img_cloth_dict[img_mask_path] = upload(img_mask_path)


# paint with inpainting
url = "https://stablediffusionapi.com/api/v3/inpaint"
key = '3V0eoMvp959JMuTkVQC9vOPp9eu7oJO6m6alLXQLrS69Bz3GP08qpbAGJKjM'

payload = json.dumps({
  "key": key,
  "prompt": "best quality, ultra high res, wear jeans, wall background, (photorealistic:1.4), 1girl, (half body)",
  "negative_prompt": "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans,bikini, medium breast,,Nevus, skin spots,nsfw",
  "negative_prompt": "",
  "init_image": img_cloth_dict[tshirt_path],
  "mask_image": img_cloth_dict[img_mask_path],
  "width": "720",
  "height": "1080",
  "samples": "1",
  "num_inference_steps": "30",
  "safety_checker": "no",
  "enhance_prompt": "yes",
  "guidance_scale": 7.5,
  "strength": 0.7,
  "seed": 1234,
  "webhook": None,
  "track_id": None
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
obj = json.loads(response.text)    

if obj['status'] == 'processing':
    print(f"sleep {obj['eta']*3}")
    time.sleep(obj['eta']*3)
    url = obj['fetch_result']
    payload = json.dumps({
    "key": key
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    obj2 = json.loads(response.text)    
    url = obj2['output'][0]
    print(url)
else:
    url = obj['output'][0]
    print(url)
      
