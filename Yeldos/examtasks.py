import pandas as pd
import numpy as np

#1

df = pd.read_excel("movies_catalog (1).xlsx")
print(df.head())
print("============================================================")
print("Количество колонок")
print(len(df.columns))

print("===========================================================")
print("Типы данных")
print(df.dtypes)

print("===========================================================")
print("Посчитайте количество пропусков в каждой колонке")
print(df.isnull().sum())


#2
print('===========================================================')
print("Типы и жанры")
types_list = df["Type"].unique().tolist()
genres_list = df["Genre"].unique().tolist()

print("Type", types_list)
print("Genre", genres_list)

#3
print("==========================================================")
# upper_titles = df["Title"].str.upper().tolist()
title_lengths = len(df["Title"].str.len().tolist())
mean_length = df["Title"].str.len().mean()

# print("Список название фильмов в верхнем регистре", upper_titles)
print("Список длины каждого названия", title_lengths)
print("Средний длино название фильм", mean_length)

#4
print("=========================================================")
top_rated = df[df['Rating_IMDB'] >= 8.5]
print(top_rated[["Title", "Rating_IMDB", "Genre"]].head(10))

#5
print("========================================================")

df["Profit"] = df["Revenue_million"] - df["Budget_million"]

top_profit = df.sort_values(by="Profit", ascending=False)


print(top_profit[["Title", "Profit", "Rating_IMDB"]].head(10))
