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
    r = requests.get('https://bookscouter.com/book/'+isbn)
    
    # check status code for response received
    # success code - 200
    # print(r)'
    output = {
        'title' : " ",
        'year-of-publication': "",
        'price': ""
    }

    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify())
    for link in soup.find_all('a'):
        if 'amazon' in link.get('href'):

            response = requests.get(link.get('href'), headers= custom_headers)
            # print(response)
            # print(link.get('href'))
            soup = BeautifulSoup(response.content, 'html.parser')
            output['price'] = float(soup.find('span', attrs={'class':'a-offscreen'}).contents[0][1:])
            output['title'] = soup.find('span', attrs={'id':'productTitle'}).contents[0][2:]
            date_element = soup.findChildren('div', attrs={'id':"rpi-attribute-book_details-publication_date"})[0]
            output['year-of-publication'] = date_element.find('div', attrs={'class': 'a-section a-spacing-none a-text-center rpi-attribute-value'}).span.text[-4:]
            return(output)

@app.get("/")
async def root():
    return {"message": "hello im steve"}

@app.get("/{id}")
async def get_id(id: int):
    id = str(id)
    data = get_info(id)
    return {"data": data}

#hi
