import requests
from bs4 import BeautifulSoup

location = 1
items = 100
url = f'https://hh.ru/search/vacancy?text=аналитик+данных&area={location}&items_on_page={items}'

headers = {'Host': 'hh.ru',
        'User-Agent': 'Chrome',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'}

def extract_max_page():    
    hh_request = requests.get(url, headers=headers)    
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')    
    pages_info = hh_soup.find("div", {'class': 'pager'})    
    pages = pages_info.find_all('a')        
    pages_links = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})    
    pages_number = []    
    for page in pages_links:
       pages_number.append(int(page.find('a').text))    
    return pages_number[-1]

def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').text
    company = company.replace(u'\xa0', ' ')
    metro = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    metro = metro.strip('Москва, ').replace(u'\xa0', ' ')
    
    return {'title': title, 'company': company, 'metro': metro, 'link': link} 
    
def extract_vacancies(last_page):
    jobs=[]
    for page in range(last_page):
        print(f'Данные по странице {page}')
        result = requests.get(f'{url}&page={page}', headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'vacancy-serp-item-body'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)            
    return jobs

def get_jobs():
    max_page = extract_max_page()
    jobs = extract_vacancies(max_page)
    return jobs