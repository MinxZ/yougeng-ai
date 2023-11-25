import time

import leancloud
import requests


def dwld_img(image_url, file_path):
    img_data = requests.get(image_url).content
    with open(file_path, 'wb') as handler:
        handler.write(img_data)

def download():
    app_id = 'Db7SYRSourdqRRckhnk89ykR-MdYXbMMI'
    app_key = '5qJj7R3ijhUcc8ldKDFKUOQT'
    leancloud.init(app_id, app_key)
    tpd = leancloud.Object.extend('Topic_dict')
    query = tpd.query

    while True:
        topic_dict = query.get('65627c52e98180051f0b81dd')

        tpd_dwld = topic_dict.get('topic_downloaded')
        tpd_ids = topic_dict.get('topic_dict')
        for topic, downloaded in tpd_dwld.items():
            if not downloaded:
                idx = tpd_ids[topic]
                break

        if not downloaded: 
            time.sleep(60)           
        else:
            tpd_class = leancloud.Object.extend('Topic_dict')
            query = tpd_class.query
            tpd = query.get(idx)
            topic = tpd.get('topic')
            imgs = tpd.get('imgs')    
            text = tpd.get('text')

            # file_path_ori = 'C:\Users\jabys\Desktop\商品图'
            file_path_ori = 'C:/Users/jabys/Desktop/商品图'
            for i, img in enumerate(imgs):
                file_path = f'{file_path_ori}/{i}.png' 
                dwld_img(img, file_path)

        time.sleep(60)           








