# -*- coding: utf-8 -*-

import facebook
import json
import datetime
import time
from access_token import TOKEN, GROUP_ID, YEARS, MONTHS

graph = facebook.GraphAPI(TOKEN)

# グループidからfeedを取得
years = YEARS
months = MONTHS

for year in years:
    for month in months:

        # 期間指定
        begin = datetime.datetime(year, month, 1, 0, 0)
        end = begin + datetime.timedelta(weeks=4)
        begin_unix = int(time.mktime(begin.timetuple()))
        end_unix = int(time.mktime(end.timetuple()))

        # first request
        response = graph.get_object(id=GROUP_ID + '/feed?limit=1000&since='
                                    + str(begin_unix) + '&until=' + str(end_unix), timeout=10)
        all_entry_ids = []
        for index, entry in enumerate(response['data']):
            all_entry_ids.append(entry['id'])
            # 一番投稿日時が古い投稿のUNIX時間を取得
            if index + 1 == len(response['data']):
                datetime_obj = datetime.datetime.strptime(entry['updated_time'], '%Y-%m-%dT%H:%M:%S%z')
                end_unix = int(time.mktime(datetime_obj.timetuple()))

        # the condition to end
        if len(all_entry_ids) < 1000:
            crawl_flg = 0
        else:
            crawl_flg = 1

        # next crawl
        while crawl_flg:
            response = graph.get_object(id=GROUP_ID + '/feed?limit=1000&since='
                                        + str(begin_unix) + '&until=' + str(end_unix), timeout=10)
            entry_ids = []
            for index, entry in enumerate(response['data']):
                entry_ids.append(entry['id'])                      # idをlistに入れる
                # 一番投稿日時が古い投稿のUNIX時間を取得
                if index + 1 == len(response['data']):
                    datetime_obj = datetime.datetime.strptime(entry['updated_time'], '%Y-%m-%dT%H:%M:%S%z')
                    end_unix = int(time.mktime(datetime_obj.timetuple()))
            all_entry_ids += entry_ids

            # the condition to end
            print(len(entry_ids))
            if len(entry_ids) < 1000:
                crawl_flg = 0

        # save feed's ids (API制限がかかったときのための保険)
        print(str(month) + '月 feed数: ', len(all_entry_ids))
        with open('./crawling_data/entry_ids_' + str(year) + '_' + str(month) + '.list', 'w') as f:
            json.dump(all_entry_ids, f)
