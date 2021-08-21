# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:50:38 2021

@author: Hiba Houhou
"""

import urllib.request
import requests
from beautifultable import BeautifulTable
import os
import shutil
from requests.exceptions import HTTPError

try:
    sessionid = input("Enter your instagram sessionid cookie: ")
    cookies = {'sessionid': '{}'.format(sessionid)}
    username = input("Enter profile username: ")
    response = requests.get('https://www.instagram.com/{}/?__a=1'.format(username),cookies=cookies)
    response.raise_for_status()
    jsonResponse = response.json()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

data = jsonResponse
username = data['graphql']['user']['username']
full_username = data['graphql']['user']['full_name']
biography = data['graphql']['user']['biography']
follower_count = data['graphql']['user']['edge_follow']['count']
following_count = data['graphql']['user']['edge_followed_by']['count']
posts_number = data['graphql']['user']['edge_owner_to_timeline_media']['count']
    
profile_pic_link = data['graphql']['user']['profile_pic_url_hd']
images_links = []
videos_links = []
i = 0
j = 0
for edge in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
    if edge['node']['__typename'] =='GraphImage' and i <= 2:
        images_links.append(edge['node']['image_url'])
        i += 1
    if edge['node']['__typename'] == 'GraphVideo' and j <= 2:
        videos_links.append(edge['node']['video_url'])
        j += 1
        
results_table = BeautifulTable()
results = [full_username,biography,follower_count,following_count,posts_number]
results_table.rows.append(results)
results_table.columns.header = ['Full name', 'Bio', 'Followers', 'Following', 'Posts']

media_table = BeautifulTable()
images = ['Images',images_links[0],images_links[1],images_links[2]]
videos = ['Videos',videos_links[0],videos_links[1],videos_links[2]]
media_table.rows.append(images)
media_table.rows.append(videos)
media_table.columns.header = ['Media type', 'Link 1', 'Link 2', 'Link 3']

print('\n-----------------------------USER INFORMATION------------------------------')
print(results_table)
print('\n----------------------------LINK TO PROFILE PIC----------------------------')
print('Link to profile picture: ',profile_pic_link)
print('\n-----------------------------USER MEDIA LINKS------------------------------')
print(media_table)

try:
    os.mkdir('./'+username)
except:
    try:
        shutil.rmtree('./'+username)
        os.mkdir('./'+username)
    except:
        print("Directory '% s' can not be removed" % username)

req = requests.get(profile_pic_link)
with open('./'+username+'/profile_pic.jpg', 'wb') as f:
    f.write(req.content)
    
images_req = []
for url in images_links:
    images_req.append(requests.get(url))
for i in range(3):
    with open('./'+username+'/image'+str(i)+'.jpg', 'wb') as f:
        f.write(images_req[i].content)

for i in range(3):
    url = videos_links[i]
    rsp = urllib.request.urlopen(url)
    with open('./'+ username +'/video'+ str(i) + '.mp4','wb') as f:
        f.write(rsp.read())
