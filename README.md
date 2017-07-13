# 开发文档

### 爬虫部分开发
* 第一期

    爬取排行榜单的飙升榜、新歌榜、原创歌曲榜(榜单每天更新)。

    爬取所有的歌单。

### 后台部分开发
* 第一期

    提供接口

    http://yangqh.cn/api/new_songs_list?offset=1&limit=20
    Method:GET
    该接口用来获取新歌榜单的歌曲offset代表偏移量，limit代表从偏移量开始的限制个数

### 数据库设计
* MongoDB

    新歌榜表单

* music_list (这个collection每天更新)
```
    '_id': 1 主键自增
    'type': 1,2,3    1代表飙升榜，2代表新歌榜，3代表原创歌曲
    'name': '夜访吸血鬼'   存放歌曲名字
    'source_url':'xxxxxx'   存放歌曲url
    'comment_id': 1 对应comment表的id
    'update_time':ISODate("2017-07-28T12:19:28.975Z")
    'create_time':ISODate("2017-07-28T12:19:28.975Z")

    name, source_url，type加上索引
```

* comments collections
```
    '_id': 1主键自增
    'song_name': 'yellow' ##歌曲名
    'comments': [{
                  'name':'西蒙',
                  'content': 'xxxx',
                  'star': 100,
                  'reply_name': '尼亚'，
                  'reply_content': 'xxxx'
                },
                {

                }
                .......
                      ]
    'update_time': ISODate("2017-07-28T12:19:28.975Z")
    'create_time': ISODate("2017-07-28T12:19:28.975Z")

    song_name加上索引
```

* index collections  这个collection用来生成键值
```
    '_id': ObjectId()
    'music_index': Int
    'comment_index': Int
    'update_time': ISODate("2017-07-28T12:19:28.975Z")
    'create_time': ISODate("2017-07-28T12:19:28.975Z")
```
