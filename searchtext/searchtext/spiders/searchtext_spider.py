import scrapy
# import pandas as pd
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from ..items import SearchTextSpiderItem
from urllib.parse import urljoin, urlencode
from searchtext.pipelines import SearchTextSpiderPipline

total_links_count_to_check_min = 500
total_links_count_to_check_max = 1000

# proxy_url = "http://api.proxiesapi.com/?auth_key=018e20db996de6b223344a5afc4321d5_sr98766_ooPq87&url="



def get_proxy_url(url):
 
    #Creates a ZenRows proxy URL for a given target_URL using the provided API key.
 
    payload = {'url': url}
    proxy_url = f'http://api.proxiesapi.com/?auth_key=018e20db996de6b223344a5afc4321d5_sr98766_ooPq87&url={url}'
    return proxy_url

class SearchTextSpider(scrapy.Spider):
    
    name = 'website_crawler'
    
    # start_urls = ['https://'+ wb_item +'/' for wb_item in wb_item.domain_name]
    def start_requests(self):

        self.links=[]
        self.checked_links=[]
        self.skiped_links=[]
        self.links_related = []

        settings = self.crawler.settings
        CRAWL_DOMAIN = settings.get('CRAWL_DOMAIN')
    
        self.domain = CRAWL_DOMAIN
        url = f"https://{CRAWL_DOMAIN}"

        yield scrapy.Request(url, callback=self.parse)
        # yield scrapy.Request(urljoin(proxy_url, url), callba ck=self.parse)


    def parse(self, response):

        continue_check = True
        if  len(self.links_related)>0 and len(self.checked_links)>total_links_count_to_check_min:
            continue_check = False
        elif len(self.checked_links)>total_links_count_to_check_max:
            continue_check = False
        
        if 'text/html' in response.headers['Content-Type'].decode('utf-8') and continue_check:
            for href in response.css('a::attr(href)'):
                # print(href)
                # print(href.extract())
                # yield None
                full_path = href.extract()
                if not 'https://' in href.extract() and not 'http://' in href.extract():
                    full_path = urljoin(response.request.url, href.extract())
                if full_path not in self.links:
                    if self.domain in full_path and 'https://' in full_path:
                        # print(full_path)
                        self.links.append(full_path)
                        print('href: ', href)
                        print('full_path: ', full_path)
                        
                        yield response.follow(full_path, self.parse)
                        # yield response.follow(urljoin(proxy_url, full_path), self.parse)
            
                    # elif not 'https://' in href.extract():
                    #     full_path = response.request.url + href.extract()
                    #     print(full_path)
                    #     self.links.append(full_path)
                    #     yield response.follow(href, self.parse)
                else:
                    yield None #href.extract()
        
            html_content = response.text

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all <p> elements that contain the text "Concrete"
            concrete_elements = soup.find_all(lambda tag: tag.name and 'concrete' in tag.get_text(strip=True).lower())

            # Find the parent element of each <p> element
            for c_element in concrete_elements:
                if len(c_element.find_all())==0:

                    # print("Element: ", c_element)

                    level_counter = 0
                    current_element = c_element
                    while level_counter<3:

                        c_parent_element = current_element.find_parent()
                        # print("Parent element: ", c_parent_element) 
                        if 'testing' in c_parent_element.get_text(strip=True).replace(current_element.get_text(strip=True), '').lower() or \
                            'inspection' in c_parent_element.get_text(strip=True).replace(current_element.get_text(strip=True), '').lower():
                            
                            # print('Parent element has Testing')
                            if response.request.url not in self.links_related:
                                self.links_related.append(response.request.url)
        
                            print(c_parent_element.get_text(strip=True).replace(current_element.get_text(strip=True), '').lower())
                            break
                        current_element = c_parent_element

                        level_counter +=1

            self.checked_links.append(response.request.url)

        else:
            self.skiped_links.append(response.request.url)
        
        # print('Skipped Links: ', self.skiped_links)
        # print('Qualified Links: ', self.links_related)

    def closed(self, reason):
        # This method is called when the spider is about to be closed down.
        # You can run your function here, e.g., to process the collected data.
        
        item = SearchTextSpiderItem()
        process_data = SearchTextSpiderPipline()

        log_stats = self.crawler.stats.get_stats()

        # domain_name = scrapy.Field()
        # total_links = scrapy.Field()

        item['domain_name'] = self.domain
        item['total_links'] = len(self.checked_links)
        item['related_links'] = len(self.links_related)

        process_data.process_item(item, log_stats)

