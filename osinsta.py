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
    data = jsonResponse
    is_private= data['graphql']['user']['is_private']
    username = data['graphql']['user']['username']
    full_username = data['graphql']['user']['full_name']
    biography = data['graphql']['user']['biography']
    follower_count = data['graphql']['user']['edge_follow']['count']
    following_count = data['graphql']['user']['edge_followed_by']['count']
    posts_number = data['graphql']['user']['edge_owner_to_timeline_media']['count']
    
    results_table = BeautifulTable()
    results = [full_username,biography,follower_count,following_count,posts_number]
    results_table.rows.append(results)
    results_table.columns.header = ['Full name', 'Bio', 'Followers', 'Following', 'Posts']
        
    profile_pic_link = data['graphql']['user']['profile_pic_url_hd']

    if str(is_private) == 'False':
        images_links = []
        videos_links = []
        i = 0
        j = 0
        for edge in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            if edge['node']['__typename'] =='GraphImage' and i <= 2:
                images_links.append(edge['node']['display_url'])
                i += 1
            if edge['node']['__typename'] == 'GraphVideo' and j <= 2:
                videos_links.append(edge['node']['video_url'])
                j += 1
                
        for k in range(3-i):
            images_links.append('No image found')
        print(images_links)
        for k in range(3-j):
            videos_links.append('No video found')
        
        media_table = BeautifulTable()
        images = ['Images',images_links[0],images_links[1],images_links[2]]
        videos = ['Videos',videos_links[0],videos_links[1],videos_links[2]]
        media_table.rows.append(images)
        media_table.rows.append(videos)
        media_table.columns.header = ['Media type', 'Link 1', 'Link 2', 'Link 3']
    
    print('\n-------------------------------------USER INFORMATION--------------------------------------')
    print(results_table)
    print('\n------------------------------------LINK TO PROFILE PIC------------------------------------')
    print('Link to profile picture: ',profile_pic_link)
    
    if str(is_private == 'false'):
        print('\n-------------------------------------USER MEDIA LINKS--------------------------------------')
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
    
    if str(is_private) == 'False':
        
        images_req = []
        for url in images_links:
            if url != 'No image found':
                images_req.append(requests.get(url))
        for i in range(len(images_req)):
            with open('./'+username+'/image'+str(i)+'.jpg', 'wb') as f:
                f.write(images_req[i].content)
                print('-> Image ' + str(i) + ' downloaded')
        
        for i in range(len(videos_links)):
            url = videos_links[i]
            if url != 'No video found':
                rsp = urllib.request.urlopen(url)
                with open('./'+ username +'/video'+ str(i) + '.mp4','wb') as f:
                    f.write(rsp.read())
                    print('-> Video ' + str(i) + ' downloaded')
    
except HTTPError as http_err:
    if str(http_err)[0:3] == '404':
        print('\n+------------------------------------------+')
        print('|-------------Username not found-----------|')
        print('+------------------------------------------+')
