import json
import datetime
import pytz


class WeatherConfig:
    config = {}

    def load(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except:
            config = {}

    def save(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def add_key(self, key):
        if 'keys' in self.config:
            b = True
            for k in self.config['keys']:
                if k == key:
                    b = False
                    break
            if b:
                self.config['keys'] += [key]
        else:
            self.config['keys'] = [key]
        return key

    def keys(self):
        if 'keys' in self.config:
            return self.config['keys']
        else:
            return []

    def inc_req(self, key):
        my_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
        cfg_date = my_date.strftime("%d/%m/%Y")
        try:
            if key in self.config[cfg_date]:
                self.config[cfg_date][key] += 1
            else:
                self.config[cfg_date][key] = 1
        except:
            self.config[cfg_date] = {key: 1}
        return self.config[cfg_date][key]

    def req_cnt(self, key):
        try:
            my_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
            cfg_date = my_date.strftime("%d/%m/%Y")
            return self.config[cfg_date][key]
        except:
            try:
                self.config[cfg_date][key] = 1
            except:
                self.config[cfg_date] = {key: 1}
            return 1
