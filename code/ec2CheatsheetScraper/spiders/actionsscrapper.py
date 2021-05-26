import scrapy

class ActionsScrapper(scrapy.Spider):
    name = 'actionsscraper'
    start_urls = ['https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies']
    
    def parse(self, response):
        # Build Resources list
        resources = list()
        for table_row in response.xpath('//table[@id="w87aab5b9d378c13b5"]/tr/td/a[@href]/text()'):
            resources.append(table_row.extract().strip())
        yield { 'EC2_resources' : resources }
