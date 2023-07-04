from fastapi import FastAPI 
import requests
from bs4 import BeautifulSoup
import random
import time
app = FastAPI()


user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',

]

def get_info(isbn):
    # Making a GET request
    custom_headers = {
            'user-agent':  random.choice(user_agent_list),
            'Accept-Language': 'en-US,en;q=0.9'
    }
    r = requests.get('https://www.amazon.com/dp/'+isbn, headers= custom_headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    output = {
        'title' : " ",
        'edition': "",
        'price': "",
        'description': ""
    }

    count = 0
    timeout = time.time() + 20 
    while soup.find('span', attrs={'id':'productTitle'}) == None:
        custom_headers = {
            'user-agent':  random.choice(user_agent_list),
            'Accept-Language': 'en-US,en;q=0.9'
        }
        r = requests.get('https://www.amazon.com/dp/'+isbn, headers= custom_headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        count+=1
        print(count)
        if time.time() > timeout:
            break
        if r.status_code != 200:
            break
        time.sleep(0.1)
    try:
        output['price'] = float(soup.find('span', attrs={'class':'a-offscreen'}).contents[0][1:])
    except:
        output['price'] = 2 * float(soup.find('span', attrs={'class':'a-size-base a-color-price offer-price a-text-normal'}).contents[0][1:])
    output['title'] = soup.find('span', attrs={'id':'productTitle'}).contents[0][2:]
    date_element = soup.findChildren('div', attrs={'id':"rpi-attribute-book_details-publication_date"})[0]
    output['edition'] = int(date_element.find('div', attrs={'class': 'a-section a-spacing-none a-text-center rpi-attribute-value'}).span.text[-4:])
    desc_element=soup.findChildren('div', attrs={'data-a-expander-name':"book_description_expander"})[0]
    output['description'] = (list(desc_element)[1].span.text)
    return(output)



@app.get("/")
async def root():
    return {"message": "hello im steve"}

@app.get("/{id}")
async def get_id(id: str):
    data = get_info(id)
    return {"data": data}

#hi
