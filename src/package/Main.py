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

#List of subreddits to visit
subreddits = ['climbing', 'MachineLearning', 'SpaceX']

#Loop through subreddits
for subreddit in subreddits:
    #Get data from web page
    url = requests.get('https://www.reddit.com/r/' + subreddit + '/.json')
    
    #If there is an error, report it
    if(not url.ok):
        print("Error " + str(url.status_code) + " from " + subreddit + " subreddit.")
        #If the error is not a too_many_requests error, raise the error
        if(url.status_code != 429):
            print(url.raise_for_status())
    
    #Request data until returned
    while(not url.ok):
        #If the error is not a too_many_requests error, raise the error
        if(url.status_code != 429):
            print(url.raise_for_status())
        url = requests.get('https://www.reddit.com/r/climbing/.json')
    
    print("Web data retrieved for " + subreddit + " subreddit.")
    #Decode JSON
    json = url.json()
    
    #Store list of posts
    posts_list = json["data"]["children"]
    
    #Template Description: This loops through each post
    # and adds links to titles by accessing .data.url and .data.title
    template = env.get_template('Page.html')
    #Use template to read and write data to Output.html
    with open(subreddit + '.html', "w") as output_file:
        output_file.write(template.render(posts_list = posts_list))
    
    #Check that file is closed
    if(output_file.closed == False):
        output_file.close()
    print(subreddit + " file closed: " + str(output_file.closed))
    
    #New line between subreddits
    print("\n")
    
print("Complete.")
