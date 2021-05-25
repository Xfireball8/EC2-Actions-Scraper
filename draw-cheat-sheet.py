import urllib2
from bs4 import BeautifulSoup

ec2ResourceActionsConditionPage = urllib2.urlopen('https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-resources-for-iam-policies')

print(ec2ResourceActionsConditionPage)
