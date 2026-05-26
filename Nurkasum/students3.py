# Студент 3 Продвинутый анализ каталога фильмов

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Задание 1

# 1. Загрузка Excel файла
df = pd.read_excel("movies_catalog.xlsx")

# 2. Первые 10 рядов
print("FIRST 10 ROWS")
print(df.head(10))

# 3. Подсчет по Type
print("\nCOUNT BY TYPE")
type_counts = df["Type"].value_counts()
print(type_counts)

# 4. Statistics for Duration_min and Rating_IMDB
print("\nDURATION STATISTICS")
print(df["Duration_min"].describe())

print("\nRATING STATISTICS")
print(df["Rating_IMDB"].describe())


# Задание 2

# 1. Названия длиннее 12 букв
long_titles = [title for title in df["Title"] if len(str(title)) > 12]

print("\nLONG TITLES")
print(long_titles[:20])

# 2. Список жанров в верхнем регистре
genres_upper = [genre.upper() for genre in df["Genre"].dropna().unique()]

print("\nGENRES UPPER")
print(genres_upper)

# 3. Средняя длина названий фильмов жанра Action
action_movies = df[df["Genre"] == "Action"]

mean_length_action = action_movies["Title"].apply(len).mean()

print("\nMEAN TITLE LENGTH FOR ACTION")
print(mean_length_action)


# Задание 3

# 1. Генератор популярных фильмов
popular_movies = (
    (row["Title"], row["Rating_IMDB"], row["Votes_IMDB"])
    for _, row in df.iterrows()
    if row["Rating_IMDB"] >= 8 and row["Votes_IMDB"] >= 50000
)

# 2. Первые 15 популярных фильмов
print("\nFIRST 15 POPULAR MOVIES")

for i, movie in enumerate(popular_movies):
    if i >= 15:
        break
    print(movie)


# Задание 4

# 1. Словарь с количеством фильмов по платформам
platform_dict = df["Streaming_platform"].value_counts().to_dict()

print("\nPLATFORM COUNTS")
print(platform_dict)

# 2. Платформа с максимальным количеством фильмов
top_platform = max(platform_dict, key=platform_dict.get)

print("\nTOP PLATFORM")
print(top_platform)


# Задание 5

# 1. Уникальные комбинации Genre + Streaming_platform
genre_platform_set = set(
    zip(df["Genre"], df["Streaming_platform"])
)

# 2. Количество уникальных комбинаций
print("\nUNIQUE COMBINATIONS COUNT")
print(len(genre_platform_set))


# Задание 6

# 1. Создание столбца efficiency
df["efficiency"] = df.apply(
    lambda x: x["Revenue_million"] / x["Budget_million"]
    if x["Budget_million"] != 0 else np.nan,
    axis=1
)

# 2. Топ-10 фильмов по efficiency
top_efficiency = df.sort_values(
    by="efficiency",
    ascending=False
)[
    ["Title", "Budget_million", "Revenue_million", "efficiency"]
].head(10)

print("\nTOP 10 EFFICIENCY")
print(top_efficiency)


# Задание 7

# 1. Создание NumPy массива
num_data = df[
    [
        "Rating_IMDB",
        "Votes_IMDB",
        "Budget_million",
        "Revenue_million"
    ]
].to_numpy()

print("\nNUMPY ARRAY SHAPE")
print(num_data.shape)

# 2. Статистика по efficiency
eff_mean = np.nanmean(df["efficiency"])
eff_median = np.nanmedian(df["efficiency"])
eff_std = np.nanstd(df["efficiency"])

print("\nEFFICIENCY STATISTICS")
print("Mean:", eff_mean)
print("Median:", eff_median)
print("Std:", eff_std)

# 3. Индекс максимального efficiency
max_eff_index = np.nanargmax(df["efficiency"])

print("\nINDEX OF MAX EFFICIENCY")
print(max_eff_index)


# Задание 8

# 1. Создание сводной таблицы
pivot_table = pd.pivot_table(
    df,
    values="efficiency",
    index="Genre",
    columns="Streaming_platform",
    aggfunc="mean"
)

print("\nPIVOT TABLE")
print(pivot_table)

# 2. Сохранение сводной таблицы в CSV
pivot_table.to_csv("student3_efficiency_pivot.csv")


# Задание 9

# 1. Гистограмма распределения рейтингов IMDB
plt.figure(figsize=(8, 5))

plt.hist(df["Rating_IMDB"], bins=20)

plt.title("Distribution of IMDB Ratings")
plt.xlabel("Rating_IMDB")
plt.ylabel("Frequency")
plt.grid(True)

plt.savefig("rating_histogram.png")
plt.show()


# 2. Scatter plot: Budget vs Revenue
plt.figure(figsize=(8, 5))

types = df["Type"].unique()

for t in types:
    subset = df[df["Type"] == t]

    plt.scatter(
        subset["Budget_million"],
        subset["Revenue_million"],
        label=t,
        alpha=0.7
    )

plt.title("Budget vs Revenue")
plt.xlabel("Budget_million")
plt.ylabel("Revenue_million")
plt.grid(True)
plt.legend()

plt.savefig("budget_vs_revenue.png")
plt.show()


# Задание 10

# 1. Countplot по жанрам
plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Genre"
)

plt.title("Count of Movies by Genre")
plt.xticks(rotation=45)

plt.savefig("genre_countplot.png")
plt.show()


# 2. Boxplot efficiency по платформам
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="Streaming_platform",
    y="efficiency"
)

plt.title("Efficiency by Streaming Platform")
plt.xticks(rotation=45)

plt.savefig("platform_efficiency_boxplot.png")
plt.show()


# 3. Correlation heatmap
plt.figure(figsize=(10, 7))

corr = df.select_dtypes(include=np.number).corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig("correlation_heatmap.png")
plt.show()


print("\nALL TASKS COMPLETED SUCCESSFULLY")