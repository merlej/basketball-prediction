import csv
import requests
from bs4 import BeautifulSoup

def scrape_data(url):

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table')[0]
    
    row1 = table.select('thead > tr') # added
    rows = table.select('tbody > tr')
    
    header = [th.text.rstrip() for th in row1[1].find_all('th')] # added
    #header = [th.text.rstrip() for th in rows[0].find_all('th')]

    with open('ratings_00.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
    
        for row in rows[0:]:
            data1 = [th.text.rstrip() for th in row.find_all('th')] # added
            data = [th.text.rstrip() for th in row.find_all('td')]
            #writer.writerow(data)
            writer.writerow(data1 + data)

if __name__=="__main__":
   # url = "https://www.ncaa.com/stats/basketball-men/d1/current/team/168"
    url = "https://www.sports-reference.com/cbb/seasons/2000-ratings.html"
    scrape_data(url)
