import subprocess
import time
from searchtext.dbqueries import dml_run_select, dml_run_update
from selenium import webdriver

drivers_to_selenium= [
    ('Chrome', webdriver.Chrome),
    ('Firefox', webdriver.Firefox),
    ('Edge', webdriver.Edge),
    # Add more drivers to check as needed
]

# Get a list of website domains from your database
website_domains = None

def crawl_for_domain(domain_name):
    print(f"Crawling process has started for {domain_name}!")
    dml_run_update(f"UPDATE dbo.websites_data SET process_status = 'Inprogress' where domain_name = '{domain_name}'")

    # Define the Scrapy spider command as a list
    scrapy_command = ['scrapy', 'crawl', 'website_crawler', '-s', f'CRAWL_DOMAIN={domain_name}']

    # Run the Scrapy crawl in a separate process
    try:
        proc = subprocess.Popen(scrapy_command)
        proc.wait()
    except subprocess.CalledProcessError as e:
        dml_run_update(f"UPDATE dbo.websites_data SET process_status = 'Failed' where domain_name = '{domain_name}'")
        print(f"Error while crawling {domain_name}: {e}")

    print(f"Crawling process has finished for {domain_name}!")

def exec_for_all_domains():
    print("Crawling process has started for all available domains!")
    for domain_name in website_domains:
        crawl_for_domain(domain_name)
    print("Crawling process has finished for all available domains!")

if __name__ == "__main__":
    # Get a list of website domains from your database
    website_domains = dml_run_select('SELECT domain_name FROM dbo.websites_data where process_status is null order by date_loaded asc')
    website_domains = [domain[0] for domain in website_domains]
    
    # crawl_for_domain('cbbtraffic.com')
    exec_for_all_domains()

    pass
