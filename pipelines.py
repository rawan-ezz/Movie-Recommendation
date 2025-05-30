# Define your item pipelines here
#
# added the pipeline to the ITEM_PIPELINES setting in settings.py
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime


class SecondsToRealTimePipeline:                                                                                       
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
    
        if adapter.get('runtime_minutes'):
            try:
                # (HH:MM:SS)
                seconds = adapter['runtime_minutes']
                adapter['runtime'] = str(datetime.timedelta(seconds=seconds))
                
                del adapter['runtime_minutes']
            except Exception as e:
                spider.logger.error(f"Error converting runtime: {e}")
        return item

