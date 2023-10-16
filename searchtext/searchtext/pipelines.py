# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from .dbqueries import dml_run_select, dml_run_update

class SearchTextSpiderPipline:
 
    def process_item(self, item, log_stats):

        print('Pipline Starting...')

        domain_name = item['domain_name']
        total_links = item['total_links']
        related_links = item['related_links']

	    # last_log_stats = 

        log_stats_dict = {key: value for key, value in log_stats.items()}
        log_stats_str = str(log_stats_dict)

        is_qualified = 'No'
        if related_links > 0:
            is_qualified = 'Yes'

        process_status = 'Completed'
        if total_links == 0:
            process_status = 'Failed'


        # print(domain_name)
        # print(total_links)
        # print(log_stats_str)
        # print(is_qualified)
        sql_query = f"""
                            UPDATE dbo.websites_data
                            SET
                                date_processed = GetDate(),
                                process_status = '{process_status}',
                                is_qualified = '{is_qualified}',
                                total_links = {total_links},
                                related_links = {related_links},
                                last_log_stats = '{log_stats_str.replace("'", "''")}'
                            WHERE
                                domain_name = '{domain_name}' AND process_status = 'Inprogress'
                    """
        
        dml_run_update(sql_query)

        print('Next run: ', dml_run_select('SELECT top 1 domain_name FROM dbo.websites_data where process_status is null order by date_loaded asc'))

        return item

