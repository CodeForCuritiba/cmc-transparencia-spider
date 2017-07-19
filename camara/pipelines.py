# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
logger = logging.getLogger(__name__)

class MongoPipeline(object):

    collection_name = 'entities'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'camara')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[self.collection_name]

        found = collection.find_one({ 'id': item['id'] })
        doc = dict(item)

        if found:
            keyname = 'salaries.' + doc['mesano']

            collection.update_one({ '_id': found['_id'] }, {
                '$set': {
                    keyname: {
                        'gross': doc['salary_gross'],
                        'liquid': doc['salary_liquid']
                    }
                }
            })
        else:
            doc['salaries'] = {}
            doc['salaries'][doc['mesano']] = {
                'gross': doc['salary_gross'],
                'liquid': doc['salary_liquid']
            }

            del doc['salary_gross']
            del doc['salary_liquid']
            del doc['mesano']

            collection.insert_one(doc)
        return item
