import pandas as pd
df = pd.read_csv("./DataBase/res.csv")
df = df.drop('дата создания объекта', axis=1)
df = df.drop('Принадлежность к Юнеско', axis=1)
print(df.columns)
df['описание предмета охраны'] = df['описание предмета охраны'].fillna("").apply(lambda x: x[:9000])
df[:1000].to_csv('./DataBase/res1.csv', sep=',', encoding='utf-8', index=False)
