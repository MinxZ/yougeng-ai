import leancloud


def upload_topic(topic, imgs, text):
    app_id = 'Db7SYRSourdqRRckhnk89ykR-MdYXbMMI'
    app_key = '5qJj7R3ijhUcc8ldKDFKUOQT'
    leancloud.init(app_id, app_key)
    
    # Topic_dict = leancloud.Object.extend('Topic_dict')
    # topic_dict = Topic_dict()
    # topic_dict.set('topic_dict', {})
    # topic_dict.set('topic_downloaded', {})
    # topic_dict.save()
    # id = '65627c52e98180051f0b81dd'
    
    # upload topic information, imgs 
    Topic_dict = leancloud.Object.extend('Topic_dict')
    tpd = Topic_dict()

    tpd.set('topic', topic)
    tpd.set('imgs', imgs)    
    tpd.set('text', text)    

    tpd.save()
    idx = tpd.id

    # update the topic id to a dict, also downloaded or now
    tpd_class = leancloud.Object.extend('Topic_dict')
    query = tpd_class.query
    topic_dict = query.get('65627c52e98180051f0b81dd')

    tpd_ids = topic_dict.get('topic_dict')
    tpd_ids[topic] = idx
    topic_dict.set('topic_dict', tpd_ids)

    tpd_dwld = topic_dict.get('topic_downloaded')
    tpd_dwld[topic] = False
    topic_dict.set('topic_downloaded', tpd_dwld)

    topic_dict.save()

    return idx


