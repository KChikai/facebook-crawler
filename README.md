# Facebook Crawler

facebook から会話データをクロールするスクリプト．


# How to create the environment

1. facebook開発者に[ここ](https://developers.facebook.com/docs/apps/register)から登録，
   アプリIDを作成する．

2. アクセストークンを[ここ](https://developers.facebook.com/tools/accesstoken/)から発行する．

3. pip で下記のパッケージをインストール．

```
    pip install requests
    pip install facebook-sdk
```


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

    http://www.facebook.com/group_id/feed

エントリID（投稿ID）からそれに付随するコメント（返信）を取得する．

    http://www.facebook.com/entry_id/comments




