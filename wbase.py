
from urllib.request import urlopen
from urllib.request import Request
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
from time import sleep

class weatherbase():

    def __init__(self):
        self.soup = ""
        self.url = ""

    def url_open(self, req):
        time = random.choice([3, 5, 7, 11, 13, 17, 19])
        #sleep(time)
        return urlopen(req)

    def find_city(self, city_name, country):
        self.url=self.find_url(city_name, country)
        print(self.url)
        req = Request(self.url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = self.url_open(req).read()
        self.soup = BeautifulSoup(html, "html.parser")
        return self.soup

    def find_url(self, city_name, country):
        url_head = "http://www.weatherbase.com/search/search.php3?query=" + quote(city_name) + "%2C+" + quote(country)
        i = 0
        while "search.php" in url_head:
            url_head = self.find_location(url_head, city_name, country)
            i += 1
            if i > 4:
                raise
        return url_head + "&units=metric"

    def find_location(self, url_head, city_name, country):
        req = Request(url_head)
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = self.url_open(req).read()
        self.soup = BeautifulSoup(html, "html.parser")
        print(url_head)
        try:
            elem = self.soup('a', text=city_name)[0]
        except IndexError:
            try:
                elem = self.soup('a', text=re.compile(city_name + ".*?"))[0]
            except:
                elem = self.soup('a', text=re.compile(".*" + country + ".*?"))[0]
        link = str(elem.get('href')).strip()
        url = quote("http://www.weatherbase.com" + link, safe="%/:=&?~#+!$,;'@()*[]")
        return url

    def __get_city_info(self):
        elem=self.soup.html.body.find('div', id='container').find('div', id='page-block').span.h1
        print(elem.text)
        list=self.soup.find_all('div', {'itemprop' : 'geo'})[0]
        lon = list.find('meta', {'itemprop' : 'longitude'})['content']
        lat = list.find('meta', {'itemprop' : 'latitude'})['content']
        city=self.soup.find('meta', {'name': 'city'})['content']
        country=self.soup.find('meta', {'name': 'country'})['content']
        print("city ", city)
        print("country", country)
        city_info = {}
        city_info['city_name'] = city
        city_info['country_name'] = country
        city_info['lat'] = lat
        city_info['lon'] = lon
        city_info['city_url'] = self.url
        return city_info

    def get_weather(self, city_name, country):
        self.find_city(city_name, country)
        city_info = self.__get_city_info()
        elem = self.soup(text=re.compile('ANNUAL.*?'))[0]
        table = elem.parent.parent.parent
        elem = table.find_all('tr')[1]
        data = elem.find_all('td', {'class': 'data'})
        weather = []
        for elem in data:
            weather.append(elem.text)
        print(weather[1:])
        month = 1
        for temp in weather[1:]:
            city_info['temp' + str(month)] = temp
            month += 1
        return city_info
