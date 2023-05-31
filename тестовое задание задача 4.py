# Импортируем библиотеки
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Читаем файлы.
data_g=pd.read_excel('Данные_моделирование.xlsx', sheet_name='g')
data_m=pd.read_excel('Данные_моделирование.xlsx', sheet_name='m')
data_rf=pd.read_excel('Данные_моделирование.xlsx', sheet_name='rf')
factor=pd.read_excel('факторы.xlsx')

def lin(group_goods:str):

    # Читаем значения соответствующие товарной группе.
    m=factor.loc[factor['Товарная группа']==group_goods, 'Factor_1'].values[0]
    rf=factor.loc[factor['Товарная группа']==group_goods, 'Factor_2'].values[0]

    # Соединяем таблицы и оставляем только необходимое. После удаляем лишние колонки с названием и годом. Логарифмируем значения и удаляем строки с пропусками.
    g=pd.merge(data_g[[group_goods, 'fullname', 'year']], data_m[[m, 'fullname', 'year']], how='inner', left_on=['fullname', 'year'], right_on=['fullname', 'year'])
    g=pd.merge(g, data_rf[[rf, 'fullname', 'year']], how='inner', left_on=['fullname', 'year'], right_on=['fullname', 'year'])
    g=g.drop(['fullname', 'year'], axis=1)
    g=g.dropna(axis=0)
    g=pd.DataFrame(np.log(g))

    # Делим выборку на признаки и таргеты.
    x=g.drop([group_goods], axis=1)
    y=g[group_goods]

    # Учим модель линейной регрессии.
    modelg=LinearRegression()
    modelg.fit(x, y)
    
    # Считаем метрику и выводим необходимую информацию.
    metric=r2_score(y, modelg.predict(x))
    print(f"Товарная группа - {group_goods}, статистика R2 = {metric}, значения коэффициентов = {modelg.coef_}, значение константы = {modelg.intercept_}")

for group_goods in factor['Товарная группа'].to_list():
    lin(group_goods)
