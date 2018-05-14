'''
Created on May 11, 2018

@author: John Ragone
'''

#Libraries
import requests
from jinja2 import Template, Environment, PackageLoader, select_autoescape

#Create environment
env = Environment(
    loader=PackageLoader('package', 'templates'),
    autoescape=select_autoescape(['html'])
)

#Get data from web page
climbing_json = requests.get('https://www.reddit.com/r/climbing/.json').json()

#Test printing title of second post
print(climbing_json["data"]["children"][1]["data"]["title"])
#Store list of posts
posts_list = climbing_json["data"]["children"]

#Template Description: This loops through each post
# and adds links to titles by accessing .data.url and .data.title
template = env.get_template('Page.html')
#Use template to read and write data to Output.html
with open("Output.html", "w") as output_file:
    output_file.write(template.render(posts_list = posts_list))


