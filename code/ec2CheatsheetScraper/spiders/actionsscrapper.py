import scrapy

class ActionsScrapper(scrapy.Spider):
    name = 'actionsscraper'
    start_urls = ['https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies']
    
    def parse(self, response):
        # Build Resources Array (Individuals from EC2-Resources class in our ontology)
        resources = list()
        for table_row in response.xpath('//table[@id="w87aab5b9d378c13b5"]/tr/td/a[@href]/text()'):
            resources.append(table_row.extract().strip())
        
        # Special attention is given to the nomenclatura behind the dict 
        # resulting from the operation as it is taken as is by the creator
        # script to create Ontology Classes.
        #
        # We want to get ServiceAbbreviation-(Resources|Actions|Conditions)
        yield { 'EC2-Resources' : resources }
