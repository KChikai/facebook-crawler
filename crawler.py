# -*- coding: utf-8 -*-

import facebook
from access_token import TOKEN

graph = facebook.GraphAPI(TOKEN)
response = graph.get_object('db.tech.showcase/posts')

for entry in response['data']:
    print(entry['message'])
