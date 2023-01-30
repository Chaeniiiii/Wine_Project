
BOT_NAME = 'wine'

SPIDER_MODULES = ['wine.spiders']
NEWSPIDER_MODULE = 'wine.spiders'

ROBOTSTXT_OBEY = False

#한글 깨짐 방지
FEED_EXPORT_ENCODING = 'utf-8-sig'

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

ITEM_PIPELINES = {
  'wine.pipelines.MongoPipeline' : 300,
}

LOG_FILE='WINE.log'
