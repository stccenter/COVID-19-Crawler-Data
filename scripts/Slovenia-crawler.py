import os
import datetime
import tabula
from pathlib import Path
import re
from datetime import datetime as dt
#######
mkfile_time = dt.strftime(dt.now(), '%Y%m%d%H%M')
folder_path = './data/Slovenia/' + mkfile_time + '/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
#first_date = datetime.date(2020, 7, 28)
curr_date = datetime.date(2020, 10, 14)
#last_date = datetime.date(2020, 10, 14)

# while curr_date <= last_date:
curr_date_str = curr_date.strftime('%Y-%m-%d')
file_name = curr_date_str + '.csv'
if not file_name in folder_path:
    pdf_link_base = 'https://www.nijz.si/sites/www.nijz.si/files/uploaded/covid_obcine_'
    pdf_link = pdf_link_base + curr_date.strftime('%d%m%Y') + '.pdf'
    # print(curr_date.strftime('%d%m%Y'))
    temp_file = folder_path + file_name + '_tmp'
    try:
        tabula.convert_into(pdf_link, temp_file,
                            output_format="csv", pages='all', stream=True)
        temp_f = open(temp_file, 'r')
        f = open(folder_path + file_name, 'w')
        lines = temp_f.readlines()
        lines = [re.compile('(\d)\s(\d)').sub(r'\1,\2', line) for line in lines
                 if not line.startswith('"')]
        lines = [line.replace(',,', ',') for line in lines]
        f.writelines(lines)
        temp_f.close()
        f.close()
    except:
        print('Cannot parse Solvenia data for ' + curr_date_str)

    # next day
    #curr_date += datetime.timedelta(days=1)

# clean temp files
for p in Path(folder_path).glob("*.csv_tmp"):
    p.unlink()
