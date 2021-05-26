import scrapy

class ActionsScrapper(scrapy.Spider):
    name = 'actionsscraper'
    start_urls = ['https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies']
    
    def parse(self, response): 
        actions = list()
        resources = list()
        conditions = list()
        
        # Build Conditions Array (Indiviudals from Ec2Conditions class in our ontology)
        for table_row in response.xpath('//table[@id="w87aab5b9d378c15b7"]/tr/td/a[@href]/text()'):
            conditions.append(table_row.extract().strip())

        # Build Resources Array (Individuals from Ec2Resources class in our ontology)
        for table_row in response.xpath('//table[@id="w87aab5b9d378c13b5"]/tr/td/a[@href]/text()'):
            resources.append(table_row.extract().strip())
        
        # Build Actions Array (Individuals from Ec2Actions class in our ontology)
        for table_row in response.xpath('//table[@id="w87aab5b9d378c11b9"]/tr/td/a[@href]/text()'):
            actions.append(table_row.extract().strip())

        # Special attention is given to the nomenclatura behind the dict 
        # resulting from the operation as it is taken as is by the creator
        # script to create Ontology Classes.
        #
        # We want to get ServiceAbbreviation-(Resources|Actions|Conditions)
        # as class name
        #
        # Objects are put in an array because json_load can't have multiple object
        # in top level
        yield { 'res' : [{'Ec2Actions' : actions}, {'Ec2Resources' : resources}]} #, 'Ec2Conditions' : conditions }
