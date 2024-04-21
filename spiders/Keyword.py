from pathlib import Path
import scrapy
import json
import re
import datetime
from spiders.parse import parse_tweet_info, parse_long_tweet, parse_time

class keywordSpider(scrapy.Spider):
    name = 'keyword'
    excessiveTweetWindows = []
    def start_requests(self): 
        start_time = datetime.datetime(year=self.year, month=1, day=1, hour=0)
        end_time = datetime.datetime(year=self.year, month=12, day=31, hour=23)
             
        time_cur = start_time
        while time_cur < end_time:
            _start_time = time_cur.strftime("%Y-%m-%d-%H")
            _end_time = (time_cur + datetime.timedelta(hours=self.searchWindowHour)).strftime("%Y-%m-%d-%H")
            url = f"https://s.weibo.com/weibo?q={self.keyword}&timescope=custom%3A{_start_time}%3A{_end_time}&page=1"
            yield scrapy.Request(url, callback=self.parse, meta={'keyword': self.keyword, '_start_time': _start_time, '_end_time':_end_time})
            time_cur = time_cur + datetime.timedelta(hours=self.searchWindowHour)
    
      
    def parse(self, response, **kwargs):
        """
        parsing website
        """
        html = response.text
        if '<p>抱歉，未找到相关结果。</p>' in html:
            self.logger.info(f'no search result. url: {response.url}')
            return

        request_page = response.meta.get("depth", 0) + 1
        print(request_page)
        if request_page == 50:
            _start_time = response.meta['_start_time']
            _end_time = response.meta['_end_time']
            self.excessiveTweetWindows.append(_start_time + '<->' + _end_time)

            
        tweet_ids = re.findall(r'weibo\.com/\d+/(.+?)\?refer_flag=1001030103_" ', html)
        tweet_ids = list(set(tweet_ids))
        
        for tweet_id in tweet_ids:
            url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
            yield scrapy.Request(url, callback=self.parse_tweet, meta=response.meta, priority=10, cb_kwargs={'self_year': self.year})
        
        next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
        if next_page:
            url = "https://s.weibo.com" + next_page.group(1)
            yield scrapy.Request(url, callback=self.parse, meta=response.meta)     
            
    @staticmethod
    def parse_tweet(response, **kwargs):
        data = json.loads(response.text)
        item = parse_tweet_info(data)
        item['keyword'] = response.meta['keyword']
        item['yearmismatch'] = False
        if int(item['created_at'].split('-')[0]) != kwargs.get('self_year'):
            item['yearmismatch'] = True
            print('year mismatch') 
        if item['isLongText']:
            url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
            yield scrapy.Request(url, callback= parse_long_tweet, meta={'item': item}, priority=20)
        else:
            yield item  

                

