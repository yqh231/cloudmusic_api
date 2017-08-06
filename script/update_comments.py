import base
from pymongo.operations import InsertOne

from spider.database import get_single_comments, get_comments

class UpdateComments(object):

    def run(self):
        ## 每次处理100条评论
        r_conn = get_comments()
        w_conn = get_single_comments()
        count = 0
        while True:
            requests = []
            result = r_conn.find({}).skip(count).limit(count + 100)
            try:
                result.next()
            except Exception:
                break
            for item in result:
                if item.get('comments'):
                    for i in item['comments']:
                        requests.append(InsertOne(i))
            count += 100
            print ('writing!!')
            w_conn.bulk_write(requests)
        print ('..done')


if __name__ == '__main__':
    updater = UpdateComments()
    updater.run()