import scrapy
import sys

class ActionsScrapper(scrapy.Spider):
    name = 'actionsscraper'
    start_urls = ['https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies']
    
    def check(self, s, arr):
        result = []
        for i in arr:
            
            # for every character in char array
            # if it is present in string return true else false
            if i in s:
                result.append("True")
            else:
                result.append("False")
        return result


    # On parse les tables amazon : 
    #
    # La Table action est formatée en HTML comme ceci :
    #       Une Action s'appliquant à une unique resource contient son nom et le nom de sa
    #       resource dans la même ligne (<tr></tr>), la première colonne de la ligne contient
    #       le nom, et la quatrième contient la resource.
    #       
    #       Il est possible qu'une action s'applique à plusieurs resources alors la définition
    #       de cette action s'étends sur plusieurs lignes, les lignes qui suivent la première
    #       resource définie pour l'action ont un format différent : la première colonne correspond
    #       au nom de la resource.
    #       
    #       Un autre cas est possible lorsqu'une action s'applique à aucune resource mais que l'on
    #       peut appliquer des filtres de contrôle d'accès à celle-ci.
    #
    #       Il faut satisfaire l'ensemble de ces cas pour pouvoir parser la table action.
    #       TODO : Refactor le mauvais code fait à la volée pour comprendre ceci...
    def parse(self, response): 
        tables = response.xpath('//table')
        actionTable = tables[0]
        resourcesTable = tables[1]
        conditionsTables = tables[2]
        actions = list()
        resources = list()
        conditions = list()
        
        # Build Conditions Array (Indiviudals from Ec2Conditions class in our ontology)
#        for table_row in response.xpath('//table[@id="w87aab5b9d378c15b7"]/tr/td/a[@href]/text()'):
#            conditions.append(table_row.extract().strip())

        # Build Resources Array (Individuals from Ec2Resources class in our ontology)
        for table_row in resourcesTable.xpath('.//tr/td/a[@href]/text()'):
            resources.append(table_row.extract().strip())
        
        # Build Actions Array (Individuals from Ec2Actions class in our ontology)


        scrapedActionsRows = actionTable.xpath('./tr')
        scrapedActionsRowsLen = len(scrapedActionsRows)
        i = 0
        while i < scrapedActionsRowsLen:
            actionsRow = { 'actionName' : "", 'resources' : [], 'requires' : [] }
            
            scrapedActionsNameColumn = scrapedActionsRows[i].xpath('./td')[0].xpath('./a[@href]/text()')
            if 0 < len(scrapedActionsNameColumn):
                actionsRow["actionName"] = scrapedActionsNameColumn[0].extract().strip()
            else:
                i += 1
                continue

            scrapedResourcesColumn = scrapedActionsRows[i].xpath('./td')[3].xpath('./p/a/text()')
            if 0 < len(scrapedResourcesColumn):
                resourceName = scrapedResourcesColumn[0].extract().strip()
                if self.check(resourceName,['*'])[0]:
                    actionsRow["requires"].append(resourceName.rstrip('*'))
                else:
                    actionsRow["resources"].append(resourceName)
            
            offset = 1
            while   (
                    i < (scrapedActionsRowsLen-1) and 
                    len(scrapedActionsRows[i+offset].xpath('./td')[0].xpath('./p/a[@href]/text()')) > 0
                    ):
                resourceName = scrapedActionsRows[i+offset].xpath('./td')[0].xpath('./p/a/text()')[0].extract().strip()
                if self.check(resourceName,['*'])[0]:
                    actionsRow["requires"].append(resourceName.rstrip('*'))
                else:
                    actionsRow["resources"].append(resourceName)
                offset += 1
            
            actions.append(actionsRow)
            i += offset

        # Special attention is given to the nomenclatura behind the dict 
        # resulting from the operation as it is taken as is by the creator
        # script to create Ontology Classes.
        #
        # We want to get ServiceAbbreviation-(Resources|Actions|Conditions)
        # as class name
        #
        # Objects are put in an array because json_load can't have multiple object
        # in top level
        yield { 'res' : [{'Ec2Actions' : actions},{'Ec2Resources' : resources}]} #, 'Ec2Conditions' : conditions }
