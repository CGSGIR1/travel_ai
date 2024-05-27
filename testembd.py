import pandas as pd


df = pd.read_csv("./DataBase/res1.csv")
df = df.drop('дата создания объекта', axis=1)
print(df.columns)
df['описание предмета охраны'] = df['описание предмета охраны'].str.slice(0,10000) # или df.text = df.text.str[:512]
df[:20000].to_csv('./DataBase/res1.csv', sep=',', encoding='utf-8', index=False)
