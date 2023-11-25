import json

import leancloud

# img_path = '/Users/z/Downloads/openai.jpg'

def upload(img_path):
    app_id = 'b8lJaEKYlx8gGtM8SbUgOWPJ-gzGzoHsz'
    app_key = '0PmqcjGyAsWBdrpUgpNDx6ek'
    leancloud.init(app_id, app_key)

    with open(img_path, 'rb') as f:
        file = leancloud.File(img_path.split('/')[-1], f)
        file.save()
        return file.url

# img_cloth_dict = {}

# cloth_img_path = '/Users/z/Downloads/models/q_star.png'
# img_cloth_dict[cloth_img_path] = upload(cloth_img_path)

# for idx in [1, 2, 3, 4]:
#     ini_img_path = f'/Users/z/Downloads/models/model{idx}.png'
#     img_cloth_dict[ini_img_path] = upload(ini_img_path)
# img_cloth_dict[ini_img_path] = upload(ini_img_path)
# img_cloth_dict2 = {key.split('/')[-1]: value for key, value in img_cloth_dict.items()}
# img_cloth_dict3 = {key.split('.')[0]: value for key, value in img_cloth_dict2.items()}
# img_cloth_dict = img_cloth_dict3

# with open('img_cloth_dict2.json', 'w') as f:
#     json.dump(img_cloth_dict, f)
