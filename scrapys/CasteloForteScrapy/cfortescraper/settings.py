# Scrapy settings for chocolatescraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cfortescraper'

SPIDER_MODULES = ['cfortescraper.spiders']
NEWSPIDER_MODULE = 'cfortescraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chocolatescraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# To Storing in AWS S3 Bucket
AWS_ACCESS_KEY_ID = 'myaccesskeyhere'
AWS_SECRET_ACCESS_KEY = 'mysecretkeyhere'

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'chocolatescraper.pipelines.ProdIDToListPipeline':300,
    #'chocolatescraper.pipelines.UrlAPIPipeline':400,
    #'chocolatescraper.pipelines.JsonsPipeline':500,
    #'chocolatescraper.pipelines.PriceToUSDPipeline': 100,
    #'chocolatescraper.pipelines.DuplicatesPipeline': 200,
    # 'chocolatescraper.pipelines.SavingToMySQLPipeline': 300,
     #'chocolatescraper.pipelines.SavingToPostgresPipelineCM': 500,
     #'chocolatescraper.pipelines.MyPipeline': 450,

}


