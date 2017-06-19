# Facebook Crawler

facebook から会話データをクロールするスクリプト．
facebook sdk for pythonを使用．

<br>

# How to create the environment

1. facebook開発者に[ここ](https://developers.facebook.com/docs/apps/register)から登録，
   アプリIDを作成する．

2. アクセストークンを[ここ](https://developers.facebook.com/tools/accesstoken/)から発行する．

3. pip で下記のパッケージをインストール．

```
    pip install requests
    pip install facebook-sdk
    pip install datetime
```


4. `access_token.py`というファイルを`feed_crawler.py`と同じディレクトリ下に作り，以下のように記述．

```python

TOKEN = '************'      # 2で取得したアクセストークンを記入
GROUP_ID = '123456789'      # クロールしたいグループIDを記入（調べ方はGET Methodを参照）

```


<br>

# GET Method

単純な`name`でのアクセスができなくなり，IDが必要となった．
従って，事前にIDを調べる必要がある．
調べることができるWebサイトは[これ](https://lookup-id.com/)．
上記URLのサイトで個人アカウント検索はこんな感じ

    https://www.facebook.com/name

グループはこんな感じ．

    https://www.facebook.com/groups/group_name

検索することで個人IDやグループIDを取得することができる．


IDが分かったことで，GETメソッドが使える．
グラフAPIリファレンスは[これ](https://developers.facebook.com/docs/graph-api/reference)．
下記に一例を示す．（アクセストークンは省略）
グループ内のfeedを取得する．

    http://graph.facebook.com/group_id/feed

新着データのデフォルト数は25個っぽい．それ以上のデータを取りたければ
`?limit=hoge`のように個数を指定する必要がある．API制限に注意．
また，UNIX時間を指定することで，指定期間内のデータを取得することができる．

エントリID（投稿ID）からそれに付随するコメント（返信）を取得する．

    http://graph.facebook.com/entry_id/comments

<br>

# Request Limit

facebook graph API のリクエスト制限は600秒に600回程度 (per IP) とからしい．
詳しくは[ここ](https://developers.facebook.com/docs/marketing-api/api-rate-limiting)，
または[ここ](https://developers.facebook.com/docs/graph-api/advanced/rate-limiting)．
あまり具体的な明言がなされていない（？）．
TwitterAPIに比べてゆるい（？）

feedで1000件取得の場合はちゃんとできる．
feedでのlimit指定を10000件に設定した場合，
`facebook/__init__.py`でエラーが吐き出される．

    line 269:  raise GraphAPIError('Maintype was not text, image, or querystring')

ちゃんとしたレスポンスが返っていないのでこのようなエラーが返ってくる．
試しに，raise文を`return response`に書き換えて中身を見る．

    b'{"error":{"code":1,"message":"Please reduce the amount of data you\'re asking for, then retry your request"}}'

量を減らしてや〜と言われている．

2017.6.14 追記：現時点ではリクエスト回数400回毎に600秒掛かるようにリクエスト制限をかけている．
これはあくまで，経験則的なものであるので全てのクローリング方法で通用するものではないと思う．


# Error

## Data Not Found

データクロールの際にidからデータを取得できなかった場合には，`facebook.GraphAPIError`が吐かれる．
実際の受け取ったデータの中身はこんな感じ．

    {'error': {'fbtrace_id': 'APCt0mvkOi5', 'type': 'GraphMethodException', 'code': 100, 'message': "Unsupported get request. Object with ID '116489408559957_237161279826102' does not exist, cannot be loaded due to missing permissions, or does not support this operation. Please read the Graph API documentation at https://developers.facebook.com/docs/graph-api"}}


このエラーコードを避けるには`facebook/__init__.py`の271行目を以下に変更

```python
if result and isinstance(result, dict) and result.get("error"):
    if result.get("error", {}).get("code") == 100:
        return result
    else:
        raise GraphAPIError(result)
```