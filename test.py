import csv
from openpyxl import Workbook
from openpyxl import load_workbook
from getWeatherFree import Wunderground

def writCsv(udata, file_name = 'db.csv'):
    with open(file_name, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(udata)


wb = load_workbook("160720_RIKA_CONTENT.xlsx")
ws = wb.get_sheet_by_name("CITIES")

i = 468
weather = Wunderground("")
if 1:
    while ws["A" + str(i)].value != None:
        city_name = ws['A' + str(i)].value.encode("utf-8")
        country_name = ws['B' + str(i)].value.encode("utf-8")
        print(i, "req: ", weather.req_cnt)
        print(city_name, country_name)
        try:
            city_info = weather.get_year_weather(country_name, city_name)
            try:
                udata = [
                    city_info['city_name'],
                    city_info['country_name'],
                    city_info['lat'],
                    city_info['lon'],
                    city_info['temp1'],
                    city_info['temp2'],
                    city_info['temp3'],
                    city_info['temp4'],
                    city_info['temp5'],
                    city_info['temp6'],
                    city_info['temp8'],
                    city_info['temp7'],
                    city_info['temp9'],
                    city_info['temp10'],
                    city_info['temp11'],
                    city_info['temp12'],
                    city_info['city_url']
                ]
                writCsv(udata)
            except:
                print(" >> can't write to the file")
        except NameError as e:
            print(" >> ", e)
            udata = [
                city_name.decode('utf-8', 'ignore'),
                country_name.decode('utf-8', 'ignore'),
                'unknown'
                ]
            writCsv(udata, 'unknown.csv')
        except:
            udata = [
                city_name.decode('utf-8', 'ignore'),
                country_name.decode('utf-8', 'ignore'),
                'unknown'
            ]
            writCsv(udata, 'unknown.csv')
            print(" >> can't get", ws['A' + str(i)].value)
        i += 1

#wb_out.save('db.xlsx')