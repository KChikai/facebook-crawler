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

        # request
        response = graph.get_object(id=GROUP_ID + '/feed?limit=1000&since='
                                    + str(begin_unix) + '&until=' + str(end_unix), timeout=10)
        entry_ids = []
        for entry in response['data']:
            entry_ids.append(entry['id'])                      # idをlistに入れる
        print(str(month) + '月 feed数: ', len(entry_ids))

        # save feed's ids (API制限がかかったときのための保険)
        with open('./crawling_data/entry_ids_' + str(year) + '_' + str(month) + '.list', 'w') as f:
            json.dump(entry_ids, f)
