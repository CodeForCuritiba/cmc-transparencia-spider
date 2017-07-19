# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os

import logging
logger = logging.getLogger(__name__)

GRUPO = os.environ['CMC_GRUPO']

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        entities_types = crawler.settings.get('ENTITIES_TYPES')
        collection_name = entities_types[GRUPO]

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'camara'),
            collection_name=collection_name
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

        # @TODO check for existing salary for the current mesano

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
