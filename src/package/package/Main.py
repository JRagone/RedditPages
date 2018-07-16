'''
Created on May 11, 2018

@author: John Ragone
'''

#Libraries
import requests
from jinja2 import Environment, PackageLoader, select_autoescape

#Returns score for a given post
def returnPostScore(elem):
    return elem["data"]["score"]

#Create environment
env = Environment(
    loader = PackageLoader('package', 'templates'),
    autoescape = select_autoescape(['html'])
)
#Template Description: This loops through each post
# and adds links to titles by accessing .data.url and .data.title
template = env.get_template('Page.html')
#List of subreddits to visit
subreddits = ['climbing', 'MachineLearning', 'SpaceX']
#List to hold post JSON for summary page
summary_posts_list = []

#Loop through subreddits
for subreddit in subreddits:
    #Get data from web page
    web_url = requests.get('https://www.reddit.com/r/' + subreddit + '/.json')
    
    #If there is an error, report it
    if(not web_url.ok):
        print("Error " + str(web_url.status_code) + " from " + subreddit + " subreddit.")
        #If the error is not a too_many_requests error, raise the error
        if(web_url.status_code != 429):
            print(web_url.raise_for_status())
    
    #Request data until returned
    while(not web_url.ok):
        #If the error is not a too_many_requests error, raise the error
        if(web_url.status_code != 429):
            print(web_url.raise_for_status())
        web_url = requests.get('https://www.reddit.com/r/' + subreddit + '/.json')
    
    print("Web data retrieved for " + subreddit + " subreddit.")
    #Decode JSON
    web_json = web_url.json()
    
    #Store list of posts
    web_posts_list = web_json["data"]["children"]
    summary_posts_list.append(web_posts_list)
    
    #Use template to read and write data to subreddit.html
    with open(subreddit + '.html', "w") as output_file:
        output_file.write(template.render(posts_list = web_posts_list))
    
    #Check that file is closed
    if(output_file.closed == False):
        output_file.close()
    print(subreddit + " file closed: " + str(output_file.closed))
    
    #New line between subreddits
    print("\n")

#Turn each list of posts from a subreddit into one list
flat_summary_posts_list = [item for sublist in summary_posts_list for item in sublist]

#Sort the list in descending order based on score
flat_summary_posts_list.sort(key = returnPostScore, reverse = True)

#Use template to read and write data to Summary.html
with open('Summary.html', "w") as output_file:
    output_file.write(template.render(posts_list = flat_summary_posts_list))

print("Completed.")
