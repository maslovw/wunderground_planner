from urllib.request import urlopen
from time import sleep
import json
import os.path
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote
from bs4 import BeautifulSoup
from config import WeatherConfig

class Wunderground:
    key = ""
    url_head = "http://api.wunderground.com/api/"
    sleep_time = 6
    max_req_a_day = 3
    req_cnt = 1
    url = ""
    dec_str = 'ascii'

    def __init__(self, key="", sleep_time=6, max_cnt=500, init_cnt=0):
        self.sleep_time = sleep_time
        self.max_req_a_day = max_cnt
        self.cfg = WeatherConfig()
        self.cfg.load()
        if key == "":
            self.key = self.cfg.keys()[0]
        else:
            self.key = self.cfg.add_key(key)
        self.req_cnt = self.cfg.req_cnt(self.key)

    def __get_weather_from_json(self, json_str):
        try:
            city_name = json_str['location']['city']
        except:
            raise NameError("Location error: ", self.url)
        country_name = json_str['location']['country_name']
        lat = json_str['location']['lat']
        lon = json_str['location']['lon']
        max_temp = json_str['trip']['temp_high']['avg']['C']
        min_temp = json_str['trip']['temp_low']['avg']['C']
        city_url = json_str['location']['wuiurl']
        return [city_name, country_name, lat, lon, max_temp, min_temp, city_url]

    def __getDirName(self, country, city):
        return "countrys/" + country.decode(self.dec_str, 'ignore') + "/" + city.decode(self.dec_str, 'ignore')

    def __get_weather_file(self, file_name):
        with open(file_name) as json_file:
            json_str = json.load(json_file)
        return self.__get_weather_from_json(json_str)


    def __getFileName(self, country, city, dates):
        return self.__getDirName(country, city) + "/" + ".".join([country.decode(self.dec_str, 'ignore'), city.decode(self.dec_str, 'ignore'), dates]) + ".json"

    def __saveJsonFile(self, html, country, city, dates):
        file_name = self.__getFileName(country, city, dates)
        if not os.path.exists(self.__getDirName(country, city)):
            os.makedirs(self.__getDirName(country, city))
        with open(file_name, "w") as json_file:
            json.dump(html, json_file, ensure_ascii=True)

    def __find_key(self, key):
        for item in self.cfg.keys():
            if item != key:
                if self.cfg.req_cnt(item) < self.max_req_a_day:
                    return item
        return None

    def __switch_key(self):
        new_key = self.__find_key(self.key)
        if not (new_key is None):
            self.key = new_key
            self.req_cnt = self.cfg.req_cnt(self.key)
            #print("!!! Key changed: ", self.key)
            return self.key
        return None


    def __get_weather_from_web(self, country, city, dates):
        #print("getting from the web")
        if self.req_cnt >= self.max_req_a_day:
            if self.__switch_key() is None:
                raise
        self.url = self.url_head + self.key + "/geolookup/planner_" + dates + "/q/" + quote(country) + "/" + quote(city) + ".json"
        html = urlopen(self.url).read()
        json_str = json.loads(html.decode("utf-8", errors="ignore"))
        self.__saveJsonFile(json_str, country, city, dates)
        self.req_cnt = self.cfg.inc_req(self.key)
        self.cfg.save()
        sleep(self.sleep_time)
        return self.__get_weather_from_json(json_str)

    def __get_weather_from_html(self, country, city, date):
        url_head = "https://www.wunderground.com/history/airport/EDDV/2016/6/1/PlannerHistory.html?dayend=0&monthend=0&yearend=0&activity=Golf"
        req = Request(url_head)
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", id='highBall')

    def get_weather(self, country, city, dates):
        file_name = self.__getFileName(country, city, dates)
        if os.path.isfile(file_name):
            try:
                return self.__get_weather_file(file_name)
            except NameError as e:
                raise e
            except:
                #os.remove(file_name)
                return self.__get_weather_from_web(country, city, dates)
        else:
            return self.__get_weather_from_web(country, city, dates)

    def print_city_info(self, country, city, dates):
        try:
            # city_info = getWeatherFile("")
            city_info = self.get_weather(country, city, dates)
            ret = "\t".join(city_info)
            print(ret)
            return city_info
        except:
            print("error")
            raise

    def get_year_weather(self, country, city):
        # date = "08010830"  # date MMDDMMDD
        dates = ["01010130",
                 "02010230",
                 "03010330",
                 "04010430",
                 "05010530",
                 "06010630",
                 "07010730",
                 "08010830",
                 "09010930",
                 "10011030",
                 "11011130",
                 "12011230"]
        city_info = {}
        month = 1
        for date in dates:
            city_name, country_name, lat, lon, max_temp, min_temp, city_url = self.get_weather(country, city, date)
            if month == 1:
                city_info['city_name'] = city_name
                city_info['country_name'] = country_name
                city_info['lat'] = lat
                city_info['lon'] = lon
                city_info['city_url'] = city_url
            elif city_info['city_name'] != city_name:
                print("error processing ", city_name, city_info['city_name'])
                raise
            city_info['temp' + str(month)] = max_temp
            month += 1
        return city_info
