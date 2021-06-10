# Author : Faisal Salhi
# Mail : admin@evolution.house
# Project : Cloud-Native App Infrastructure Development

import scrapy
import sys

class ActionsScrapper(scrapy.Spider):
    name = 'actionsscraper'
    start_urls = ['https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies']
    
    def parse(self, response): 
        tables = response.xpath('//table')
        actionTable = tables[0]
        actions = list()
        atp = actionTableParser()
        
        actions = atp.parseActionTable(actionTable)
        yield {'action' : actions}

class actionTableParser(): 
    # I am the method that parse Amazon Tables (Actions, Resources for the moment)
    #
    # The Action tables is formated in HTML as explained in the following paragraph :
    #       Also, in the following, when we are talking about an HTML row we are talking
    #       about content enclosed in a <tr></tr> tag. When we are talking about an HTML
    #       column, we are talking about content enclosed in a <td></td> tag. When we are
    #       talking about an "entry" in the table we are talking about the atomic unit of
    #       information about an action.
    #
    #       When an action in EC2 can be applied to one or zero resource. 
    #       the HTML row contains the name of the action in the first HTML column, and the name
    #       of the resource it can be applied to in the fourth HTML column.
    #       
    #       An action in EC2 can be applied to more than one resource. For such case, the entry in the
    #       table is formated as is :   
    #           - There is as much HTML rows as there is resources.
    #           - In the first HTML row, the data is formatted as explained in the precedent paragraph.
    #           - In the other HTML rows, the resource name can be scrapped at the first HTML column.
    #       
    #       Finally there is a last case in which an action applies to more than one resource, and
    #       has conditions filters that doesn't apply to any of the resource on which the action applies
    #       to (yes....) :
    #           - There is as much HTML rows as there is resources + 1 row for conditions filters.
    #           - In the first HTML row, //
    #           - In the other HTML rows until the last one, //
    #           - In the last HTML row, we get the filters that doesn't apply to any resource.
    #       
    #       To parse the action table and retrieve the entries our code needs to meet all these
    #       requirements.
    def parseActionTable(self, actionTable):
        actionTableHtmlRows = self.scrapActionTableHtmlRows(actionTable)
        actions = self.getActionsEntries(actionTableHtmlRows) 
        return actions

    #   I am the method that scrap HTML Rows from the 
    #   action Table.
    #
    #   Input : actionTable - The Selector to the HTML table of Action (Selector)
    #
    #   Output : Selector List - List of Selectors containing HTML Rows of the Table
    def scrapActionTableHtmlRows(self, actionTable):
        return actionTable.xpath('./tr')
    
    #   I am the method that takes the HTML Rows and extract the entries
    #   about actions in an atomic way.
    #
    #   Input : actionTableHtmlRows - List of Selectors containing HTML Rows of the Table
    #
    #   Ouput : Dictionnary List - List of Actions and resources it applies to.
    def getActionsEntries(self, actionTableHtmlRows):
        entries = list()
        index = 0
        
        while index < len(actionTableHtmlRows):
            entry = {'actionName' : "", 'resources' : ""}
            offsetToTheNextEntry = self.getOffsetToTheNextEntry(actionTableHtmlRows, index)
            entry['actionName'] = self.getActionName(actionTableHtmlRows, index)
            entry['resources'] = self.getResources(actionTableHtmlRows, index, offsetToTheNextEntry)

            entries.append(entry)
            index = index + offsetToTheNextEntry
        
        return entries

    # I am the method that calculate the offset to get to the next entry
    # of the action table.
    #
    #   Input : actionTableHtmlRows - Selector List of Html Rows (Selector List)
    #           index - Index of the Html Row that is the beginning of an Action Entry (Integer)
    #   Output : Integer - Offset to the next action Entry
    def getOffsetToTheNextEntry(self, actionTableHtmlRows, index):
        offset = 1
        
        if index < (len(actionTableHtmlRows) - 1):
            while not(self.isHtmlRowIsBeginningOfActionEntry(actionTableHtmlRows, index+offset)):
                offset += 1
        return offset

    # I am the method that use Scrapy Selectors to determine if the next HTML row
    # is about another entry in the action Table. To determine that i will see
    # if the xpath to action name returns a list of Selectors.
    #
    # Input : actionTableHtmlRows - Selector List of Html Rows (Selector List)
    #         index - Index of the HTML Row that we are checking (Integer)
    # Output : Boolean
    def isHtmlRowIsBeginningOfActionEntry(self, actionTableHtmlRows, index): 
        scrapedActionsNameColumn = actionTableHtmlRows[index].xpath('./td')[0].xpath('./a[@href]/text()')
        if len(scrapedActionsNameColumn) > 0:
            return True
        else:
            return False
    
    # I am the method that use Scrapy Selector to determine the name of the action resource
    # in a row that contains an action resource.
    # Input : actionTableHtmlRows - Scrapy Selector List of Html rows ( Selector List)
    #         index - Index of the HTML Row containing our action name. (Integer)
    # Output : String - Name of the Action
    def getActionName(self, actionTableHtmlRows, index):
        return actionTableHtmlRows[index].xpath('./td')[0].xpath('./a[@href]/text()')[0].extract().strip()

    # I am the method that extract the resource from the HTML Rows of an Action entry.
    #
    # Input  : actionTableHtmlRows - Scrapy Selector List of Html Rows (Selector List)
    #          index - Index of the first Html Row describing the Action Entry (Integer)
    #          offsetToTheNextEntry - Explicit (Integer)
    # Output : resources - List of resources (String List)
    def getResources(self, actionTableHtmlRows, index, offsetToTheNextEntry):
        resources = list()
        
        for offset in range(0,offsetToTheNextEntry):
                resources.append(self.getResourceFromHtmlRow(actionTableHtmlRows, index + offset))
        return resources

    # I am the method that use scrapy selectors to extract resources from the HTML Rows.
    #
    # Input : actionTableHtmlRows - Scrapy Selector List of Html Rows ( Selector List)
    #         index - Index of the Html row to extract the resource 
    # Output :  String - Resource Name
    def getResourceFromHtmlRow(self, actionTableHtmlRows, index):
#        print("DEBUG getResourceFromHtmlRow INDEX :" + str(index))
        if self.isHtmlRowIsBeginningOfActionEntry(actionTableHtmlRows, index):
            if self.hasBeginningOfEntryHtmlRowAResource(actionTableHtmlRows, index):
                return actionTableHtmlRows[index].xpath('./td')[3].xpath('./p/a/text()')[0].extract().strip()
        else:
            if self.hasOtherHtmlRowAResource(actionTableHtmlRows, index): 
                return actionTableHtmlRows[index].xpath('./td')[0].xpath('./p/a/text()')[0].extract().strip()

    # I am the method that use scrapy selector to see if we're on a HTML Row, that is
    # a beginning of an action entry and that has no resource described. (Action does not
    # apply to a resource)
    #
    #
    def hasBeginningOfEntryHtmlRowAResource(self, actionTableHtmlRows, index):
        return len(actionTableHtmlRows[index].xpath('./td')[3].xpath('./p/a/text()')) > 0

    # I am the method that use scrapy selector to see if we're on a HTML Row, that is 
    # a row that contains no resource information (mainly because it is a condition of
    # the action that does not apply to the resource).
    #
    #
    def hasOtherHtmlRowAResource(self, actionTableHtmlRows, index):
        return len(actionTableHtmlRows[index].xpath('./td')[0].xpath('./p/a/text()')) > 0
