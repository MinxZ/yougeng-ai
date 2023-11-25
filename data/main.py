from logo_on_model import logo_on_img
from text_on_img import text_on_img


def out_images(logo, logo_type='text'):
    # logo = 'data/images/WechatIMG38.jpg'
    # logo = '原神启动'

    if logo_type == 'text':
        text_on_img(logo)
    elif logo_type == 'image':
        logo_on_img(logo)

if __name__ == '__main__':
    out_images('有梗启动', logo_type='text')
    # out_images('data/images/WechatIMG38.jpg', logo_type='image')
