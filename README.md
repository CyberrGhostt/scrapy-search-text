# scrapy-search-text
Search websites for specific text


Basically, I have a control table in an Azure SQL database that keeps track of processed websites along with their status, logs, the total number of links and table contains information about new websites that are ready to be processed.
My main Python script retrieves the domains of these new websites and passes them as parameters to a Scrapy crawler using the subprocess library. It runs a set of command scripts, which in turn start the Scrapy crawler for each domain.
The crawler's primary task is to explore all the links within the given domain by inspecting the href attributes of anchor tags (<a> tags) on the websites. It collects these links and stores them in a list. Then, the crawler visits each of these links and searches for the word 'Concrete' within the context of paragraph tags (<p> tags).
If the word 'Concrete' is found on a specific page, the crawler goes up three levels to check the parent elements of the paragraph tag for the presence of 'Testing' or 'Inspection' keywords. If any of these keywords are found, the link is considered qualified.
The crawler continues to search all the qualified links and, in the end, writes the results into the database, including the status of the domain, the total number of links, and the logs generated during the Scrapy crawling process. Finally, the entire process is completed.
