# -*- coding: utf-8 -*-

import re
import json
import time
import facebook
from access_token import TOKEN

graph = facebook.GraphAPI(TOKEN)

# URLが入っている投稿に関してはデータに入れない
url_regex = re.compile(r"[https?|ftp]://[A-Za-z0-9\-.]{0,62}?\.([A-Za-z0-9\-.]{1,255})/?[A-Za-z0-9.\-?=#%/]*")

# グループidからfeed_ids_listをロード
years = [2013, 2014, 2015]
months = [month for month in range(4, 11)]                  # 4~10月のデータを対象にする (プロ野球のシーズン)

request_count = 0
t0 = time.time()
for year in years:
    for month in months:

        # load feed's ids
        with open('./crawling_data/entry_ids_' + str(year) + '_' + str(month) + '.list', 'r') as f_list:
            entry_ids = json.load(f_list)

        # comment内に返信しているcommentを取得
        with open('./crawling_data/conv_' + str(year) + '_' + str(month) + '.txt', 'w') as f:
            for index, entry_id in enumerate(entry_ids):                                                              # グループ内のEntry ID
                response = graph.get_object(id=entry_id + '/comments', timeout=10)                  # Entry内のcommentsを取得
                request_count += 1
                if request_count >= 450:
                    t1 = time.time()
                    rest = 600 - (t1 - t0) if 600 - (t1 - t0) > 0 else 0
                    print('***** sleep *****', rest, '[s]')
                    time.sleep(rest)
                    request_count = 0
                    t0 = time.time()

                if response.get("error", {}).get("code") != 100:
                    for entry in response['data']:
                        comment_id = str(entry['id'])
                        response_comments = graph.get_object(id=comment_id + '/comments', timeout=10)   # 各commentに付随するcommentsを取得(response)
                        request_count += 1
                        if request_count >= 450:
                            t1 = time.time()
                            rest = 600 - (t1 - t0) if 600 - (t1 - t0) > 0 else 0
                            print('***** sleep *****', rest, '[s]')
                            time.sleep(rest)
                            request_count = 0
                            t0 = time.time()
                        if len(response_comments['data']) != 0:
                            print('+++ start of talk +++')
                            print(entry['message'])                                                     # responseを持っているcommentを表示
                            post = re.sub(r"(\n|\r\n)",  " ", entry['message'])
                            m_post = url_regex.search(post)
                            if m_post is None:
                                for comment in response_comments['data']:
                                    print(comment['message'])                                           # commentに対するresponseを表示
                                    cmnt = re.sub(r"(\n|\r\n)",  " ", comment['message'])
                                    m_cmnt = url_regex.search(cmnt)
                                    if m_cmnt is None:
                                        f.write(post + '\t' + cmnt + '\n')
                                        post = cmnt
                                    else:
                                        break
                            print('+++ end of talk +++')
                            print('')
                else:
                    print(response)
                    print(entry_id, ' id not found...')
                print('------------ end of entry ---------------')
