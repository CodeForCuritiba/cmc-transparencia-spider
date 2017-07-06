# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CamaraPipeline(object):

    def process_item(self, item, spider):
        #Agora você pode realizar algum processamento com dado
        # O item tem os dados da requisição
        return item
