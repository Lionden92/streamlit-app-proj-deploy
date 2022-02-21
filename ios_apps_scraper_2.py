# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 16:07:33 2022

@author: liond
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random as rnd


priv_card_st = 'app-privacy__card'
d_cat_st = 'privacy-type__grid-content privacy-type__data-category-heading'
d_cat_prefixes = {'Data Used to Track You': 'tr_',
            'Data Linked to You': 'lk_',
            'Data Not Linked to You': 'nl_'}
not_clct_st = 'Data Not Collected'
no_dets_st = 'No Details Provided'
app_json = 'schema:software-application'
app_cat_st = 'information-list__item__definition'
app_cats = {'6018':'Books',
            '6000':'Business',
            '6022':'Catalogs',
            '6026':'Developer_Tools',
            '6017':'Education',
            '6016':'Entertainment',
            '6015':'Finance',
            '6023':'Food_Drink',
            '6014':'Games',
            '6027':'Graphics_Design',
            '6013':'Health_Fitness',
            '6012':'Lifestyle',
            '6021':'Magazines_Newspapers',
            '6020':'Medical',
            '6011':'Music',
            '6010':'Navigation',
            '6009':'News',
            '6008':'Photo_Video',
            '6007':'Productivity',
            '6006':'Reference',
            '6024':'Shopping',
            '6005':'Social_Networking',
            '6004':'Sports',
            '6025':'Stickers',
            '6003':'Travel',
            '6002':'Utilities',
            '6001':'Weather'}


def scrapeAppListing(url):
    rq_f, no_priv, no_rt, no_ct = 0,0,0,0
    # Random pause (1-1.5 s) before executing request to avoid continuous requests
    time.sleep(1.0 + 0.5*rnd.random())
    try:
        rsp = requests.get(url, timeout = 15)
    except:
        rq_f = 1
        return None, None, None, None, None, (rq_f, no_priv, no_rt, no_ct)
    if rsp.status_code < 200 or rsp.status_code >= 300:
        rq_f = 1
        return None, None, None, None, None, (rq_f, no_priv, no_rt, no_ct)
    soup = BeautifulSoup(rsp.content, 'html5lib')
    app_id = url[(url[30:].find('/id') + 33) :]
    # Get list of privacy data collected categories
    priv_cards = soup.findAll('div', attrs = {'class': priv_card_st})
    d_cats_lst = []
    try:
        for card in priv_cards:
            card_type = card.h3.text
            if card_type == no_dets_st:
                no_priv = 1
                app_id = None
                d_cats_lst = None
            if card_type == not_clct_st: d_cats_lst.append('no_data_collct')
            else:
                dcats = card.findAll('span', attrs = {'class': d_cat_st})
                for d in dcats:
                    new_d = d_cat_prefixes[card_type] + d.text.replace(' ','_')
                    new_d = new_d.replace(' &amp;','').lower()
                    d_cats_lst.append(new_d)
    except:
        no_priv = 1
        app_id = None
        d_cats_lst = None
    # Get ratings info
    try:
        json_str = soup.find('script', attrs = {'name': app_json}).contents[0].text
        json_dat = json.loads(json_str)
        avg_rt = json_dat['aggregateRating']['ratingValue']
        tot_rts = json_dat['aggregateRating']['reviewCount']
    except:
        no_rt = 1
        app_id = None
        avg_rt, tot_rts = None, None
    # Get app category
    item_defs = soup.findAll('dd', attrs = {'class': app_cat_st})
    cat_url = []
    try:
        for item in item_defs:
            if item.a is not None:
                cat_url.append(item.a['href'])
        app_cat_id = cat_url[0][-4:]
        app_ct = app_cats[app_cat_id]
    except:
        no_ct = 1
        app_id = None
        app_ct = None
    return app_id, avg_rt, tot_rts, app_ct, d_cats_lst, (rq_f, no_priv, no_rt, no_ct)


# Function to show a progress bar
def showProgress(c, n, seg, barTop):
    if c == 0: 
        print(barTop)
        print('=', end = '')
    c += 1
    if c >= n*seg:
        print('=', end = '')
        n += 1
    return c, n
