'''
Created on May 11, 2018

@author: John Ragone
'''

#Libraries
import requests
from jinja2 import Environment, PackageLoader, select_autoescape

#Create environment
env = Environment(
    loader=PackageLoader('package', 'templates'),
    autoescape=select_autoescape(['html'])
)

#Get data from web page
climbing_url = requests.get('https://www.reddit.com/r/climbing/.json')

#If there is an error, report it
if(not climbing_url.ok):
    print("Error " + str(climbing_url.status_code))
    #If the error is not a too_many_requests error, raise the error
    if(climbing_url.status_code != 429):
        print(climbing_url.raise_for_status())

#Request data until returned
while(not climbing_url.ok):
    #If the error is not a too_many_requests error, raise the error
    if(climbing_url.status_code != 429):
        print(climbing_url.raise_for_status())
    climbing_url = requests.get('https://www.reddit.com/r/climbing/.json')


print("Web data retrieved.")
#Decode JSON
climbing_json = climbing_url.json()

#Store list of posts
posts_list = climbing_json["data"]["children"]

#Template Description: This loops through each post
# and adds links to titles by accessing .data.url and .data.title
template = env.get_template('Page.html')
#Use template to read and write data to Output.html
with open("Output.html", "w") as output_file:
    output_file.write(template.render(posts_list = posts_list))
    
print("Complete.")
