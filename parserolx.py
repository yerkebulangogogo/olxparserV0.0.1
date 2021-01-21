#Димон excel не настороел еще, url с товароми завтра допилю, в логике есть нюанс есть
import requests
from bs4 import BeautifulSoup
import openpyxl
import sys

URL = 'https://www.olx.kz/elektronika/telefony-i-aksesuary/'
HEADER = {
    "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
HOST = 'https://www.olx.kz/'


def get_html(URL, params = None):
    request = requests.get(URL, headers = HEADER, params = params)
    return request


def get_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='offer-wrapper')
    name_content = []
    for item in items:
        try:
            name_content.append({
                'link': item.find('a', class_= 'marginright5 link linkWithHash detailsLink').get('href')
            })
        except Exception:
           pass

    return name_content


def get_len_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('a', class_ = 'lheight24')
    if item:
        i = int(input('Available PAGES: {}, HOW MACH DO YOU WANT PARSE?: '.format(item[-1].get_text())))
        return i
    else:
        return 1


def get_data(data):
    name_content = []
    for i in data:
        html_data = get_html(i['link'])
        html_data = html_data.text
        soup_data = BeautifulSoup(html_data, 'html.parser')
        items_data = soup_data.find_all('div', class_= 'offerdescription clr')
        print(items_data)
        for item in items_data:
            try:
                name_content.append({
                    'name': item.find('h1', class_ = None).get_text(strip=True),
                    'price': item.find('strong', class_= 'pricelabel__value arranged').get_text(strip=True)
                })
            except Exception:
                name_content.append({
                    'name': 'None',
                    'price': 'None'
                })
    return name_content


def write_excel(itmes):
    element = openpyxl.Workbook()
    sheet = element.active

    sheet['A1'] = 'NAME'
    sheet['B1'] = 'LINK'

    counter = 2
    for j in itmes:
        sheet[counter][0].value = j['title']
        sheet[counter][1].value = j['link']
        counter += 1

    element.save('Phone.xlsx')
    element.close()


def pars():

    urls_item = []
    html = get_html(URL)
    if html.status_code == 200:
        page_leng = get_len_urls(html.text)
        for i in range(1, page_leng+1):
            html = get_html(URL, params = {'page': i})
            datas = get_url(html.text)
            urls_item.append(datas)
            print(datas)
            get_url(html.text)
            urls_item.append(datas)
            data = get_data(datas)
        print(data, len(data))
        print(urls_item, len(urls_item))
        counter =0
        for i in range(len(urls_item)):
            for j in range(len(urls_item[i])):
                counter += j
        print(counter)
        # write_excel(data)
    else:
        print("Error! Cheack conenction to the internet.", sys.exc_info()[1])


pars()
