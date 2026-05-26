import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#ЗАДАЧА 1

current_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(current_dir, "movies_catalog.xlsx")

df = pd.read_excel(file_path)

print(df.head(10))

watched = (df["Is_Watched"] == 1).sum()
not_watched = (df["Is_Watched"] == 0).sum()

print("Watched:", watched)
print("Not Watched:", not_watched)

mean_rating = df["User_rating"].mean()

print("Mean User Rating:", mean_rating)
##############################################################################

#ЗАДАЧА 2

popular_series = df[(df["Type"] == "Series") & (df["User_rating"] >= 8)]

series_titles_upper = popular_series["Title"].str.upper().tolist()

print("\n--- Популярные сериалы в верхнем регистре ---")
print(series_titles_upper)

mean_title_length = popular_series["Title"].str.len().mean()

print("\n--- Статистика длин названий ---")
print("Средняя длина названия популярного сериала:", mean_title_length)
##############################################################################

#ЗАДАЧА 3

def netflix_shows_generator(dataframe):
    netflix_df = dataframe[(dataframe["Type"] == "Series") & (dataframe["Streaming_platform"] == "Netflix")]
    for row in netflix_df.itertuples(index=False):
        yield row

netflix_shows = netflix_shows_generator(df)

print("\n--- Первые 15 сериалов на Netflix из генератора ---")
print(f"{'Title':<30} | {'Seasons':<8} | {'Episodes':<8} | {'Rating':<6}")
print("-" * 65)

for _ in range(15):
    try:
        show = next(netflix_shows)
        print(f"{show.Title:<30} | {show.Seasons:<8} | {show.Episodes:<8} | {show.User_rating:<6}")
    except StopIteration:
        print("\n[Инфо]: Больше сериалов на Netflix не найдено.")
        break
##############################################################################

#ЗАДАЧА 4

awarded_movies = df[df["Awards_won"] > 0]

rating_counts = awarded_movies["Age_rating"].value_counts()

awards_dict = rating_counts.to_dict()

print("\n--- Распределение наград по возрастным рейтингам ---")
print(awards_dict)

top_2_ratings = list(awards_dict.keys())[:2]

print("\n--- Топ-2 возрастных рейтинга ---")
print(f"Top 2: {', '.join(top_2_ratings)}")

##############################################################################

#ЗАДАЧА 5

watched_movies = df[df["Is_Watched"] == 1]

unique_combinations = set(zip(watched_movies["Genre"], watched_movies["Type"]))

print("\n--- Уникальные комбинации (Жанр, Тип) ---")
print(unique_combinations)

combinations_count = len(unique_combinations)

print("\n--- Количество уникальных комбинаций ---")
print(f"Количество просмотренных уникальных комбинаций жанр+тип: {combinations_count}")

##############################################################################

#ЗАДАЧА 6

df["success_per_user"] = df.apply(
    lambda x: x["Revenue_million"] / x["Votes_IMDB"] if x["Votes_IMDB"] > 0 else 0,
    axis=1
)

top_10_success = df.sort_values(by="success_per_user", ascending=False).head(10)

print("\n--- Топ-10 по показателю 'успех на пользователя' ---")
print(top_10_success[["Title", "Revenue_million", "Votes_IMDB", "success_per_user"]])

##############################################################################

#ЗАДАЧА 7

series_df = df[df["Type"] == "Series"].reset_index(drop=True)

season_data = series_df[["Seasons", "Episodes", "Awards_won"]].to_numpy()

mean_seasons = np.mean(season_data[:, 0])
std_seasons = np.std(season_data[:, 0])

mean_episodes = np.mean(season_data[:, 1])
std_episodes = np.std(season_data[:, 1])

print("\n--- Статистика NumPy ---")
print(f"Сезоны -> Среднее: {mean_seasons:.2f}, Стандартное отклонение: {std_seasons:.2f}")
print(f"Эпизоды -> Среднее: {mean_episodes:.2f}, Стандартное отклонение: {std_episodes:.2f}")

max_episodes_idx = np.argmax(season_data[:, 1])

best_series = series_df.iloc[max_episodes_idx]

print("\n--- Сериал с максимальным количеством эпизодов ---")
print(f"Индекс в массиве: {max_episodes_idx}")
print(f"Название: {best_series['Title']}")
print(f"Количество эпизодов: {best_series['Episodes']}")

##############################################################################

#ЗАДАЧА 8

pivot_rating = df.pivot_table(
    index="Genre",
    columns="Age_rating",
    values="User_rating",
    aggfunc="mean"
)

print("\n--- Сводная таблица: Средний User_rating по Жанрам и Возрастным рейтингам ---")
print(pivot_rating.head())

pivot_success = df.pivot_table(
    index="Genre",
    columns="Age_rating",
    values="success_per_user",
    aggfunc="mean"
)

print("\n--- Сводная таблица: Средний success_per_user по Жанрам и Возрастным рейтингам ---")
print(pivot_success.head())

pivot_rating.to_csv("pivot_user_rating.csv", encoding="utf-8")
pivot_success.to_csv("pivot_success_per_user.csv", encoding="utf-8")

print("\n[Успех]: Обе сводные таблицы успешно сохранены в файлы 'pivot_user_rating.csv' and 'pivot_success_per_user.csv'!")

##############################################################################

#ЗАДАЧА 9

sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="User_rating", bins=15, color="skyblue", kde=True)
plt.title("Распределение пользовательских рейтингов (User Rating)")
plt.xlabel("Рейтинг пользователей")
plt.ylabel("Количество фильмов / сериалов")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("user_rating_histogram.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8, 5))
series_only = df[(df["Seasons"] > 0) & (df["Episodes"] > 0)]
sns.scatterplot(
    data=series_only,
    x="Seasons",
    y="Episodes",
    hue="Type",
    palette="Set1",
    alpha=0.8,
    s=70
)
plt.title("Зависимость количества эпизодов от количества сезонов")
plt.xlabel("Количество сезонов (Seasons)")
plt.ylabel("Количество эпизодов (Episodes)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Тип проекта")
plt.savefig("seasons_vs_episodes_scatter.png", dpi=300, bbox_inches="tight")
plt.close()

print("\n[Успех]: Оба графика успешно сгенерированы и сохранены как 'user_rating_histogram.png' и 'seasons_vs_episodes_scatter.png'!")

##############################################################################

#ЗАДАЧА 10

plt.figure(figsize=(10, 5))
watched_only = df[df["Is_Watched"] == 1]
sns.countplot(
    data=watched_only,
    x="Streaming_platform",
    hue="Type",
    palette="pastel"
)
plt.title("Количество просмотренных фильмов и сериалов по платформам")
plt.xlabel("Стриминговая платформа")
plt.ylabel("Количество просмотренных")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.savefig("watched_countplot.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(
    data=df,
    x="Genre",
    y="success_per_user",
    hue="Genre",          # Исправлено: добавили hue, чтобы убрать FutureWarning
    legend=False,         # Исправлено: отключили дублирующуюся легенду
    palette="vlag"
)
plt.title("Распределение показателя 'success_per_user' по жанрам")
plt.xlabel("Жанр")
plt.ylabel("Успех на пользователя")
plt.xticks(rotation=45)
plt.savefig("success_by_genre_boxplot.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(8, 6))
numeric_cols = df[["User_rating", "Revenue_million", "Votes_IMDB", "success_per_user", "Awards_won"]]
correlation_matrix = numeric_cols.corr()
sns.heatmap(
    data=correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.title("Матрица корреляции числовых показателей")
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()

print("\n[Успех]: Все три графика для Задачи 10 успешно сохранены в формате PNG!")