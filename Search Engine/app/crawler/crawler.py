import json
import requests
from bs4 import BeautifulSoup
from urllib import robotparser
import re
from includes.urlbreak import get_domain,integrate_link

start_url = 'https://www.daraz.com.np/'

text_tags = ['p', 'h', 'div']
data = []
urls=[]
growth=[]
ses=[]
tmp1=[]
tmp2=[]
domain=[]
def crawl(url, depth):

    # Determining DNS

    base_url=get_domain(url=url)
    for link in domain:
        if(base_url in link):
            if(url[0:2]=='//'):
                url=link+url[len(base_url)+2:]
            else:
                url=link+url[len(base_url):]
            base_url=link
    if(base_url not in domain):
        domain.append(base_url)
    # Reading robots.txt file

    rp=robotparser.RobotFileParser()
    rp.set_url(base_url+'robots.txt')
    rp.read()
    check1=rp.can_fetch("msnbot",url)
    check2=rp.can_fetch("*",url)
    if(check1==True or check2==True):
        try:
            print('Crawling url: "%s" at depth: %d' % (url, depth))
            response = requests.get(url)
        except:
            print('failed to perform HTTP GET request on "%s"\n' % url)
            return

        # accessing DNS file

        content = BeautifulSoup(response.text, 'lxml')

        try:
            title = content.find('title').text
            description = ''
            
            for tag in content.find_all():
                if tag.name in text_tags:
                    description += tag.text.strip().replace('\n', '').replace('\r','')
                    description=' '.join(description.split())
        except:
            return

        
        result ={
            'url': url,
            'title': title,
            'description': description
        }
        #print('\n\nReturn:\n\n',json.dumps(result, indent=2))

        links = content.find_all('a',href=True)

        # urls=list(set([url['href'] for url in links]))
        tmp=[]
        tmp=[url['href'] for url in links]
        urls=[url for url in set(tmp)]
        growth=integrate_link(base_url=base_url,urls=urls)
        if(result not in data):
            data.append(result)
            if depth == 0:
                tmp2=[link for link in growth if link not in set(tmp1)]
                for link in growth:
                    tmp1.append(link)
                ses_dict={
                    'from':url,
                    'links':tmp2
                }
                ses.append(ses_dict)
                return

            print(str(len(urls))+" anchor tags found")
            for link in growth:
                try:
                    crawl(url=link, depth=depth - 1)
                except KeyError:
                    pass
            
            return
    else:
        return

crawl(start_url, 1)

with open('data.json', 'w') as json_file:

    file_content = (json.dumps(data, indent=2))
    json_file.write(file_content)

print('length of data:', len(data))

with open('ses.json', 'w') as json_ses:
    list_json=json.dumps(ses,indent=2)
    json_ses.write(list_json)
#print(json.dumps(result, indent=2))
