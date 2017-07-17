from pymongo import MongoClient

MongoConn = None

def config_mongo(conf):
    global MongoConn
    # mongouri = 'mongodb://{}:{}/{}'.format(
    #     conf.DB_HOST,
    #     int(conf.DB_PORT),
    #     conf.DB_NAME
    # )

    MongoConn = MongoClient(host=conf.DB_HOST, port=int(conf.DB_PORT))['yangqh']