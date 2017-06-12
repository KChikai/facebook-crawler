# -*- coding: utf-8 -*-

import facebook
import json
import datetime
import time
from access_token import TOKEN, GROUP_ID

graph = facebook.GraphAPI(TOKEN)

# グループidからfeedを取得
months = [month for month in range(4, 11)]                  # 4~10月のデータを対象にする (プロ野球のシーズン)

for i in range(len(months)):

    # 期間指定
    begin = datetime.datetime(2016, months[i], 1, 0, 0)
    end = begin + datetime.timedelta(weeks=4)
    begin_unix = int(time.mktime(begin.timetuple()))
    end_unix = int(time.mktime(end.timetuple()))

    # request
    response = graph.get_object(id=GROUP_ID + '/feed?limit=1000&since='
                                + str(begin_unix) + '&until=' + str(end_unix), timeout=10)
    entry_ids = []
    for entry in response['data']:
        entry_ids.append(entry['id'])                      # idをlistに入れる
    print(str(months[i]) + '月 feed数: ', len(entry_ids))

    # save feed's ids (API制限がかかったときのための保険)
    with open('./crawling_data/entry_ids_' + str(months[i]) + '.list', 'w') as f:
        json.dump(entry_ids, f)


# comment内に返信しているcommentを取得
# for entry_id in entry_ids:                                                              # グループ内のEntry ID
#     response = graph.get_object(id=entry_id + '/comments', timeout=10)                  # Entry内のcommentsを取得
#     for entry in response['data']:
#         comment_id = str(entry['id'])
#         response_comments = graph.get_object(id=comment_id + '/comments', timeout=10)   # 各commentに付随するcommentsを取得(response)
#         if len(response_comments['data']) != 0:
#             print('+++ start of talk +++')
#             print(entry['message'])                                                     # responseを持っているcommentを表示
#             for comment in response_comments['data']:
#                 print(comment['message'])                                               # commentに対するresponseを表示
#                 # print(comment)
#             print('+++ end of talk +++')
#             print('')
#     print('------------ end of entry ---------------')
