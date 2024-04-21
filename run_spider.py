import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.Keyword import keywordSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

if __name__ == "__main__":
    os.environ["SCRAPY_SETTINGS_MODULE"] = "settings"
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # keywords = [r'girls help girls']
    # years = [2021]
    # searchWindowHour = 24*365
    # for keyword in keywords:
    #     for year in years:
    #         print('=====',keyword,year,'=====')
    #         process.crawl(keywordSpider, keyword=keyword, year = year, searchWindowHour=searchWindowHour)
    #         # the script will block here until the crawling is finished
    # process.start()
    # print('==========spider all done==============')

    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        # 米兔运动 metoo girls help girls
        # %23girls%20help%20girls%23
        keywords = [r"%23girls%20help%20girls%23"]
        # years = [2023,2022,2021,2020,2019,2018,2017]
        years = [2023]
        # years = [2021]
        for keyword in keywords:
            for year in years:
                print(
                    "\n\n\n==",
                    keyword,
                    year,
                    "===========================================",
                )
                yield runner.crawl(
                    keywordSpider, keyword=keyword, year=year, searchWindowHour=24
                )
                # the script will block here until the crawling is finished
        reactor.stop()

    crawl()
    reactor.run()  # the script will block here until the last crawl call is finishedA
