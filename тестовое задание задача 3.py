# Так как по неясной причине указанный сайт в задании не отвечает на запросы из Python, мне не удалось должным образом протестировать скрипт.

# Импорт библиотек.
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Получаем разрешение от сайта на получение данных. Если напечаталось response 200, значит разрешение есть.
page = requests.get('https://cargo.rzd.ru/ru/9800')

# Начинаем читать страницу
soup = BeautifulSoup(page.text, 'lxml')

# Находим на странице таблицу
table1 = soup.find('div', class_=('table-wrap')).find('table')

# # Создаем список для заголовков таблицы, для значений ячеек и для списков значений ячеек.
headers=[]
value=[]
list_for_value=[]

count=1
# Записываем заголовки в список
for i in table1.find_all('tr'):
    for j in i.find_all('td'):
        if count==1:
            headers.append(i.text)
            count=count+1
            continue
        value.append(j)
    list_for_value.append(value)
print(list_for_value)        

# Передаем данные в датафрейм.
data=pd.DataFrame(data=list_for_value, columns=headers)
print(data)