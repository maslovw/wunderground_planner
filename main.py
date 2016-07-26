
from getWeather import getYearWeather
from openpyxl import Workbook
from openpyxl import load_workbook
from getWeatherFree import Wunderground
wb = load_workbook("160720_RIKA_CONTENT.xlsx")
ws = wb.get_sheet_by_name("CITIES")

wb_out = Workbook()
ws_out = wb_out.active
i_out = 1
i = 468
weather = Wunderground()
if 1:
    while ws["A" + str(i)].value != None:
        print(i, "req: ", weather.req_cnt)
        print(ws['A' + str(i)].value, ws['B' + str(i)].value)
        try:
            city_info = weather.get_year_weather(ws['B' + str(i)].value.strip(), ws['A' + str(i)].value.strip())
            try:
                ws_out["A" + str(i_out)] = city_info['city_name']
                ws_out["B" + str(i_out)] = city_info['country_name']
                ws_out["C" + str(i_out)] = city_info['lat']
                ws_out["D" + str(i_out)] = city_info['lon']
                ws_out["F" + str(i_out)] = city_info['temp1']
                ws_out["G" + str(i_out)] = city_info['temp2']
                ws_out["H" + str(i_out)] = city_info['temp3']
                ws_out["I" + str(i_out)] = city_info['temp4']
                ws_out["J" + str(i_out)] = city_info['temp5']
                ws_out["K" + str(i_out)] = city_info['temp6']
                ws_out["L" + str(i_out)] = city_info['temp7']
                ws_out["M" + str(i_out)] = city_info['temp8']
                ws_out["N" + str(i_out)] = city_info['temp9']
                ws_out["O" + str(i_out)] = city_info['temp10']
                ws_out["P" + str(i_out)] = city_info['temp11']
                ws_out["Q" + str(i_out)] = city_info['temp12']
                ws_out["R" + str(i_out)] = city_info['city_url']
                i_out += 1
            except:
                print(" >> can't write to excel")
        except NameError as e:
            print(" >> ", e)
            ws_out["A" + str(i_out)] = ws['A' + str(i)].value
            ws_out["B" + str(i_out)] = ws['B' + str(i)].value
            ws_out["C" + str(i_out)] = 'unknown'

        except:
           print(" >> can't get", ws['A' + str(i)].value)
           break
        i += 1

wb_out.save('db.xlsx')
# getYearWeather("Italy", "Cagliari")

