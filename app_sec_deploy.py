'''
App Security Project

Deployment

Created by Liond 02-15-2022

'''

import streamlit as st
import pandas as pd
import pickle
from ios_apps_scraper_2 import scrapeAppListing

with open('intro.txt', 'r') as read_file:
    intro_str = read_file.read()
with open('finalized_model.sav', 'rb') as load_file:
    model = pickle.load(load_file)
with open('data_fields.txt', 'r') as read_file:
    fields = read_file.read().split('\n')

pg_mkd = '''
<style>
.stApp {
background-image: url("https://i.imgur.com/fyNvHjt.jpg");
background-size: cover;
}
</style>

<h1 style="text-align:center;color:white">App Security Model</h1>
'''
ft_mkd = '''
<footer style="text-align:center;color:white">
<img src="https://i.imgur.com/3Bk8Ndr.png"/>
<p>Copyright &copy; 2022, SynergisticIT</p>
</footer>
'''

art_f = 0.2
trt_f = 2.0291137234e-7
ini_str = 'Waiting to receive an App Store URL...'
nan_str = 'Unable to obtain necessary data from that URL'
pos_str = 'Model Prediction: The app will be BREACHED'
neg_str = 'Model Prediction: The app will NOT be breached'
scraped_dat = [None,]

x_row = []
acdat, app_cats = [0 for _ in range(25)], fields[2:27]
dcdat, dat_cats = [0 for _ in range(41)], fields[27:]

st.markdown(pg_mkd, unsafe_allow_html = True)
st.write('')
st.header('Predicting Whether An App Will Be Breached')
st.write('')
st.write('')
st.write(intro_str)
st.write('')
st.write('')
url = st.text_input('App Store URL', key='app_url')
st.write('')
st.write('')
st.write('')
output = st.subheader('')
try:
    if len(url) > 0:
        with st.spinner('Loading app data...'):
            scraped_dat = scrapeAppListing(url)
except:
    pass
if scraped_dat[0]:
    x_row.append(art_f*scraped_dat[1])
    x_row.append(trt_f*scraped_dat[2])
    app_cat = 'ct_' + scraped_dat[3]
    dat_lst = scraped_dat[4]
    for i in range(25):
        if app_cats[i] == app_cat: acdat[i] = 1
    x_row.extend(acdat)
    for i in range(41):
        if dat_cats[i] in dat_lst: dcdat[i] = 1
    x_row.extend(dcdat)
    X_in = pd.DataFrame(data = [x_row,], columns = fields)
    prediction = model.predict(X_in)
    output.subheader(pos_str if prediction[0] else neg_str)
else:
    output.subheader(nan_str if len(url) > 0 else ini_str)

st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.markdown(ft_mkd, unsafe_allow_html = True)
