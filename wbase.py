
from urllib.request import urlopen
from urllib.request import Request
import re
from bs4 import BeautifulSoup

class weatherbase():
    def find_city(self, city_name, country):
        url_head=self.find_url(city_name, country)
        req = Request(url_head)
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = urlopen(req).read()
        self.soup = BeautifulSoup(html, "html.parser")
        return self.soup

    def find_url(self, city_name, country):
        url_head="http://www.weatherbase.com/search/search.php3?query=" + city_name + "%2C+" + country
        print (url_head)
        req = Request(url_head)
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = urlopen(req).read()
        self.soup = BeautifulSoup(html, "html.parser")
        elem = self.soup('a', text=city_name)[0]
        #print(self.soup)
        print(elem.get('href'))
        print(elem.parent.parent)
        link=elem.get('href')
        url="http://www.weatherbase.com" + link + "&units=metric"
        return url

    def get_weather(self, city_name, country):
        w.find_city(city_name, country)
        elem=self.soup(text=re.compile('ANNUAL.*?'))[0]
        table = elem.parent.parent.parent
        elem=table.find_all('tr')[1]
        data=elem.find_all('td', {'class': 'data'})
        weather = []
        for elem in data:
            weather.append(elem.text)
        print(weather[1:])
        return weather[1:]

w=weatherbase()
# w.get_weather('Orenburg', 'Russia')
# w.get_weather('Samara', 'Russia')
w.get_weather('Marikina', 'Philippines')