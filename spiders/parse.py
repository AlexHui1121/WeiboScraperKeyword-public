import re
import dateutil.parser
import json

def parse_long_tweet(response):
    data = json.loads(response.text)['data']
    item = response.meta['item']
    item['content'] = data['longTextContent']
    print('stored: longtextitem, ')
    yield item
                      
def parse_tweet_info(data):
    tweet = {
        "_id": str(data['mid']),
        "mblogid": data['mblogid'],
        "created_at": parse_time(data['created_at']),
        "ip_location": data.get('region_name', None),
        "reposts_count": data['reposts_count'],
        "comments_count": data['comments_count'],
        "attitudes_count": data['attitudes_count'],
        "content": data['text_raw'].replace('\u200b', ''),
        "pic_urls": ["https://wx1.sinaimg.cn/orj960/" + pic_id for pic_id in data.get('pic_ids', [])],
        "pic_num": data['pic_num'],
        'isLongText': False,
        "user": parse_user_info(data['user']),
    }
    if 'page_info' in data and data['page_info'].get('object_type', '') == 'video':
        media_info = None
        if 'media_info' in data['page_info']:
            media_info = data['page_info']['media_info']
        elif 'cards' in data['page_info'] and 'media_info' in data['page_info']['cards'][0]:
            media_info = data['page_info']['cards'][0]['media_info']
        if media_info:
            tweet['video'] = media_info['stream_url']
    tweet['url'] = f"https://weibo.com/{tweet['user']['_id']}/{tweet['mblogid']}"
    if 'continue_tag' in data and data['isLongText']:
        tweet['isLongText'] = True
    return tweet

def parse_user_info(data):
    user = {
        "_id": str(data['id']),
        "nick_name": data['screen_name'],
        "verified": data['verified'],
    }
    keys = ['description', 'followers_count', 'friends_count', 'statuses_count',
            'gender', 'location', 'mbrank', 'mbtype', 'credit_score']
    for key in keys:
        if key in data:
            user[key] = data[key]
    if 'created_at' in data:
        user['created_at'] = parse_time(data.get('created_at'))
    if user['verified']:
        user['verified_type'] = data['verified_type']
        if 'verified_reason' in data:
            user['verified_reason'] = data['verified_reason']
    return user

    
def parse_time(t):
    # Wed Oct 19 23:44:36 +0800 2022 => 2022-10-19 23:44:36
    return dateutil.parser.parse(t).strftime('%Y-%m-%d %H:%M:%S')