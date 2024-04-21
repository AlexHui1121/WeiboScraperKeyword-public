# -*- coding: utf-8 -*-
import datetime
import json
import os.path
import time
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class JsonWriterPipeline(object):   
    def __init__(self):
        if not os.path.exists('output'):
            os.mkdir('output')
    
    def open_spider(self, spider):
        print('======Spider Opened======')
        now = datetime.datetime.now()
        file_name = spider.name + "_" + spider.keyword +"_" + str(spider.year) +"_" +str(spider.searchWindowHour) + "h_" + now.strftime("%Y%m%d%H%M%S")
        spider.file_name = file_name
        spider.file_path = f'output/{file_name}'
        spider.file_path_with_format = spider.file_path + '.jsonl'
        spider.file = open(spider.file_path_with_format, 'wt', encoding='utf-8')
        spider.itemlist = []
        

    def close_spider(self, spider):
        spider.file.close()
        old_file_path = spider.file_path_with_format
        if spider.crawler.stats.get_value("request_depth_max") > 50:
            new_file_path = 'output/'+ '51_'+spider.file_name + '_finished.jsonl'
        else:
            new_file_path = 'output/'+ 'ok_'+spider.file_name + '_finished.jsonl'
        os.rename(old_file_path, new_file_path)
        
        WindowList = list(set(spider.excessiveTweetWindows))
        
        http200_count = spider.crawler.stats.get_value('downloader/response_status_count/200')
        total_requests = spider.crawler.stats.get_value('downloader/request_count')
        if total_requests:
            ratio = http200_count / total_requests
            ratio_string = "status 200 ratio: " + str(ratio)
            
        else:
            ratio_string = "status 200 ratio: no request"
        WindowList.insert(0, ratio_string)
            
        keywords = spider.keyword + '_' + str(spider.year) + '_' + str(spider.searchWindowHour) + 'h'
        keyword_dict = {keywords: WindowList}

        
        
        filename = 'output/excessiveTweetWindow.json'

        # Check if file exists
        if os.path.isfile(filename):
            # If file exists, open it and load the data
            with open(filename, 'r+', encoding='utf-8') as excessiveTweetWindowFile:
                data = json.load(excessiveTweetWindowFile)
        else:
            # If file doesn't exist, initialize data as an empty dictionary
            data = {}

        # Add new key-value pair to the data
        data.update(keyword_dict)

        # Write updated data back to the JSON file
        with open(filename, 'w', encoding='utf-8') as excessiveTweetWindowFile:
            json.dump(data, excessiveTweetWindowFile, indent=2)


        

    def process_item(self, item, spider):
        if item['yearmismatch']:
            raise DropItem
        else:
            del item['yearmismatch']
            
        if item in spider.itemlist:
            raise DropItem
        spider.itemlist.append(item)
        
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        spider.file.write(line)
        spider.file.flush()
        return item