import json
import time

import leancloud
import requests

with open('/Users/z/img_cloth_dict2.json') as f:
    img_cloth_dict = json.load(f)

# virtul_try_on
key = '3V0eoMvp959JMuTkVQC9vOPp9eu7oJO6m6alLXQLrS69Bz3GP08qpbAGJKjM'
url = "https://stablediffusionapi.com/api/v5/fashion"

app_id = 'Db7SYRSourdqRRckhnk89ykR-MdYXbMMI'
app_key = '5qJj7R3ijhUcc8ldKDFKUOQT'
leancloud.init(app_id, app_key)

def upload(img_path):
    with open(img_path, 'rb') as f:
        file = leancloud.File(img_path.split('/')[-1], f)
        file.save()
        return file.url

img_cloth_dict = {}

cloth_img_path = 'data/images/q_star.png'
img_cloth_dict[cloth_img_path] = upload(cloth_img_path)


init_image_url  = img_cloth_dict['model2']
cloth_image_url = img_cloth_dict['q_star']

headers = {
  'Content-Type': 'application/json'
}
payload = json.dumps({
   "key": key,
   "prompt": "A realistic photo of a model wearing a black top.",
   "negative_prompt": "Low quality, unrealistic, bad cloth, warped cloth",
   "init_image": init_image_url,
   "cloth_image": cloth_image_url,
   "cloth_type": "upper_body",
   "height": 512,
   "width": 384,
   "guidance_scale": 8.0,
   "num_inference_steps": 20,
   "seed": 128915590,
   "temp": "no",
   "webhook": None,
   "track_id": None 
})

response = requests.request("POST", url, headers=headers, data=payload)
obj = json.loads(response.text)    
print(obj)

if obj['status'] == 'processing':
    time.sleep(obj['eta']*5)
    url = obj['fetch_result']
    payload = json.dumps({
    "key": key
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    obj2 = json.loads(response.text)    
    print(obj2)
      

