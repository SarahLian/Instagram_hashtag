# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
from igramscraper.instagram import Instagram
import re


# %%
str2 = str('@The.Holistic.Psychologist@kimberleyquinlan@theanxietyhealer@millennial.therapist@mindfulmft@LisaOliveraTherapy@NedraTawwab@SitWithWhit@LizListens@carity.community')
influencer_name = str2.split('@')
influencer_name.remove('')
print(influencer_name)


# %%
# If account is public you can query Instagram without auth
instagram = Instagram()

# getting information about account
for i in influencer_name:
    account = instagram.get_account(i)

# if we can get the data
    print('Username', account.username)
    print('Is private', account.is_private)
    print('\n')


# %%
list1 = []
for i in influencer_name:
    #print(i)
    medias = instagram.get_medias(i, 50)
    #list1 = []
    for i in range(50):
        media = medias[i]
        a = str(media)
        data = re.findall(r'#[a-z]+', a)
        list1.append(data)
print(list1)


# %%
#data = re.findall(r'#[a-z]+', list1[0])
#data = re.findall(r'#(.+?) ', list1[0])
#print(data)


# %%
hashtag = list1
len(hashtag)


# %%
hashtag = list(filter(None, hashtag))  #delete no hashtag post
print(hashtag)


# %%
len(hashtag)


# %%
list2 = []

for i in hashtag:
    if len(i) == 1:
        list2.append(i[0])
    else:
        for j in i:
            list2.append(j)
print(list2)
        


# %%
hashtag_name = list(set(list2))
print(hashtag_name)


# %%
str3 = '#exposuretherapy#mentalhealthrecovery#ocdrecovery#mentalhealthfirstaid#mentalhealthadvocate\
#depressionsupport#anxietymanagement#bipolarrecovery#mentalhealthawarness#teenmentalhealth'


# %%
new_has = re.findall(r'#[a-z]+', str3)
print('new_has length is:',len(new_has))
print('hashtag_name length is:',len(hashtag_name))
for i in new_has:
    hashtag_name.append(i)
print('new hashtag_name length is:', len(hashtag_name))


# %%
print(hashtag_name)

# %% [markdown]
# ### put hashtag_name into txt file

# %%
# hashtag_inventory=str(hashtag_name)    
# #print(hashtag_inventory)
# with open('hashtag_inventory.txt','a') as file_handle: 
#     hashtag_inventory = hashtag_inventory.replace("'",'').replace(',','') +' '
#     file_handle.write(hashtag_inventory)
#     file_handle.write('\n') 

# %% [markdown]
# ### find hot hashtag

# %%
#Analyze which hashtag appears the most --- more popular one
#updata inventory


# %%
taglist = [x for x in hashtag_name if x.startswith('#')]
#print(taglist)
index = 0
while index < len(taglist):
    taglist[index] = taglist[index].strip('#')
    index += 1
print(taglist)


# %%
get_ipython().system(' pip install ChromeDriver')
get_ipython().system(' pip install selenium')


# %%
#taglist.remove('anxietydisorder')


# %%
#taglist.remove('restrictionneverworks')


# %%
#taglist.remove('anxietymeme')


# %%
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime


# %%
driver = webdriver.Chrome('C:/Users/xinro/Downloads/新建文件夹/chromedriver.exe')


# %%
# Define dataframe to store hashtag information
tag_df  = pd.DataFrame(columns = ['Hashtag', 'Number of Posts', 'Posting Freq (mins)'])

# Loop over each hashtag to extract information
for tag in taglist:
    
    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")
    
    # Extract current hashtag name
    tagname = tag
    # Extract total number of posts in this hashtag
    # NOTE: Class name may change in the website code
    # Get the latest class name by inspecting web code
    nposts = soup.find('span', {'class': 'g47SY'}).text
        
    # Extract all post links from 'explore tags' page
    # Needed to extract post frequency of recent posts
    myli = []
    for a in soup.find_all('a', href=True):
        myli.append(a['href'])

    # Keep link of only 1st and 9th most recent post 
    newmyli = [x for x in myli if x.startswith('/p/')]
    del newmyli[:9]
    del newmyli[9:]
    del newmyli[1:8]

    timediff = []

    # Extract the posting time of 1st and 9th most recent post for a tag
    for j in range(len(newmyli)):
        driver.get('https://www.instagram.com'+str(newmyli[j]))
        soup = BeautifulSoup(driver.page_source,"lxml")

        for i in soup.findAll('time'):
            if i.has_attr('datetime'):
                timediff.append(i['datetime'])
                #print(i['datetime'])

    # Calculate time difference between posts
    # For obtaining posting frequency
    datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
    diff = datetime.datetime.strptime(timediff[0], datetimeFormat)        - datetime.datetime.strptime(timediff[1], datetimeFormat)
    pfreq= int(diff.total_seconds()/(9*60))
    
    # Add hashtag info to dataframe
    tag_df.loc[len(tag_df)] = [tagname, nposts, pfreq]
        
driver.quit()

# Check the final dataframe
print(tag_df)

# CSV output for hashtag analysis
#tag_df.to_csv('hashtag_list.csv')


# %%
posts_num = []
for tag in taglist:
    #print(tag)

    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")

    # Extract current hashtag name
    #tagname = tag
    # Extract total number of posts in this hashtag
    # NOTE: Class name may change in the website code
    # Get the latest class name by inspecting web code
    if soup.find('span', {'class': 'g47SY'}) is None:
        nposts = 'NA'
    else:
        nposts = soup.find('span', {'class': 'g47SY'}).text
    posts_num.append(nposts)
    #print(nposts)


# %%
tag_df  = pd.DataFrame(columns = ['Hashtag', 'Number of Posts'])
tag_df['Number of Posts'] = posts_num
tag_df['Hashtag'] = taglist


# %%
tag_df.to_csv('hashtag_list.csv')


# %%
aaa


# %%
frequency = []
for tag in ['selflovebringsbeauty']:
    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")
    if soup.find('span', {'class': 'g47SY'}) is None:
        pfreq = 'NA'
        print(tag,'no data')
    else:
        # Extract all post links from 'explore tags' page
        # Needed to extract post frequency of recent posts
        myli = []
        for a in soup.find_all('a', href=True):
            myli.append(a['href'])
        #print(myli)

        # Keep link of only 1st and 9th most recent post 
        newmyli = [x for x in myli if x.startswith('/p/')]
        #print(newmyli)
        #print(len(newmyli))
        if len(newmyli) < 21:
            pfreq = 'no enough post'
            print(tag, 'no enough post')
        else:
            del newmyli[:9]
            del newmyli[9:]
            del newmyli[1:8]
            print(newmyli)
            timediff = []

            # Extract the posting time of 1st and 9th most recent post for a tag
            for j in range(len(newmyli)):
                driver.get('https://www.instagram.com'+str(newmyli[j]))
                soup = BeautifulSoup(driver.page_source,"lxml")

                for i in soup.findAll('time'):
                    if i.has_attr('datetime'):
                        timediff.append(i['datetime'])
                        print('aaaa',i['datetime'])

            # Calculate time difference between posts
            # For obtaining posting frequency
            datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
            diff = datetime.datetime.strptime(timediff[0], datetimeFormat)                - datetime.datetime.strptime(timediff[3], datetimeFormat)
            pfreq= int(diff.total_seconds()/9)
            print(tag, 'pfreq is', pfreq)
    frequency.append(pfreq)
    print('diff is',diff)
    print('diff,total_secondes is',diff.total_seconds())
    print('timediff[0] is',timediff[0])
    print('timediff[3] is',timediff[3])
    #print('len(timediff) is',len(timediff))
    # Add hashtag info to dataframe
    #tag_df.loc[len(tag_df)] = [tagname, nposts, pfreq]
        
#driver.quit()

# Check the final dataframe
#print(tag_df)


# %%
a = 0
for i in taglist:
    if i == 'qoute':
        print(a)
    else:
        a+=1


# %%
len(taglist)


# %%
pfreq


# %%
taglist[539]


# %%
frequency


# %%
tag_df  = pd.DataFrame(columns = ['Hashtag','Frequency'])
#tag_df['Number of Posts'] = posts_num
tag_df['Hashtag'] = taglist
tag_df['Frequency'] = frequency
tag_df.to_csv('1_hashtag_list.csv')


# %%
tag_df


# %%
F = []
for tag in ['selflovebringsbeauty']:
    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")
    if soup.find('span', {'class': 'g47SY'}) is None:
        pfreq = 'NA'
        #print(tag,'no data')
    else:
        # Extract all post links from 'explore tags' page
        # Needed to extract post frequency of recent posts
        myli = []
        for a in soup.find_all('a', href=True):
            myli.append(a['href'])
        #print(myli)

        # Keep link of only 1st and 9th most recent post 
        newmyli = [x for x in myli if x.startswith('/p/')]
        print(newmyli)
        print(len(newmyli))
        if len(newmyli) < 21:
            pfreq = 'no enough post'
            #print(tag, 'no enough post')
        else:
            del newmyli[:9]
            del newmyli[9:]
            del newmyli[1:8]
            print(newmyli)
            timediff = []

            # Extract the posting time of 1st and 9th most recent post for a tag
            for j in range(len(newmyli)):
                driver.get('https://www.instagram.com'+str(newmyli[j]))
                soup = BeautifulSoup(driver.page_source,"lxml")

                for i in soup.findAll('time'):
                    if i.has_attr('datetime'):
                        timediff.append(i['datetime'])
                        print(i['datetime'])

            # Calculate time difference between posts
            # For obtaining posting frequency
            datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
            diff = datetime.datetime.strptime(timediff[0], datetimeFormat)                - datetime.datetime.strptime(timediff[3], datetimeFormat)
            pfreq= int(diff.total_seconds()/9)
            print(tag, 'pfreq is', pfreq)
   
    print('diff is',diff)
    print('diff,total_secondes is',diff.total_seconds())
    print('timediff[0] is',timediff[0])
    print('timediff[3] is',timediff[3])
    print('len(timediff) is',len(timediff))
    # Add hashtag info to dataframe
    #tag_df.loc[len(tag_df)] = [tagname, nposts, pfreq]
        
#driver.quit()

# Check the final dataframe
#print(tag_df)


# %%
frequency[602]


# %%
970*9


# %%



