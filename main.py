from fastapi import FastAPI 
import requests
from bs4 import BeautifulSoup

app = FastAPI()
custom_headers = {
    'user-agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}


def get_info(isbn):
    # Making a GET request
    r = requests.get('https://www.amazon.com/dp/'+isbn, headers= custom_headers)
    if r.status_code != 200:
        return r
    # check status code for response received
    # success code - 200
    # print(r)
    output = {
        'title' : " ",
        'edition': "",
        'price': "",
        'description': ""
    }

    # print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
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
