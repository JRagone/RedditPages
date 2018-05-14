'''
Created on May 11, 2018

@author: John Ragone
'''

import requests
from jinja2 import Template, Environment, PackageLoader, select_autoescape
import time

env = Environment(
    loader=PackageLoader('package', 'templates'),
    autoescape=select_autoescape(['html'])
)

r = requests.get('https://www.reddit.com/r/climbing/.json').json()

print(r)

print(r["data"]["children"][1]["data"]["title"])

#env = Environment(
#    loader = PackageLoader('yourapplication', 'templates')
#)


#template = Template('Hello {{ name }}')

#with open("Output.html", "w") as output_file:
#    output_file.write(template.render(name = 'Bill'))


#with open("Output.html", "w") as output_file:
#    for child in r["data"]["children"]:
#        output_file.write(child["data"]["title"])

children = r["data"]["children"]
template = env.get_template('Page.html')
#print(template.render(children = "children"))

with open("Output.html", "w") as output_file:
    output_file.write(template.render(children = children))


