# -*- coding: utf-8 -*-

import facebook
from access_token import TOKEN, GROUP_ID

graph = facebook.GraphAPI(TOKEN)

# グループidからfeedを取得
response = graph.get_object(id=GROUP_ID + '/feed')
print('feed数: ', len(response['data']))
entry_ids = []
for entry in response['data']:
    entry_ids.append(entry['id'])

# comment内に返信しているcommentを取得
for entry_id in entry_ids:                                                  # グループ内のEntry ID
    response = graph.get_object(id=entry_id + '/comments')                  # Entry内のcommentsを取得
    for entry in response['data']:
        comment_id = str(entry['id'])
        response_comments = graph.get_object(id=comment_id + '/comments')   # 各commentに付随するcommentsを取得(response)
        if len(response_comments['data']) != 0:
            print('+++ start of talk +++')
            print(entry['message'])                                         # responseを持っているcommentを表示
            for comment in response_comments['data']:
                print(comment['message'])                                   # commentに対するresponseを表示
                # print(comment)
            print('+++ end of talk +++')
            print('')
    print('------------ end of entry ---------------')
