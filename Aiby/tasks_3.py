import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# ЗАГРУЗКА ДАННЫХ (используется во всех задачах)
# ============================================================
df = pd.read_excel('movies_catalog.xlsx')


# ============================================================
# ЗАДАЧА 1 — Преобразование данных в массивы NumPy
# ============================================================
print("=" * 60)
print("ЗАДАЧА 1 — NumPy массив")
print("=" * 60)

cols = [
    'Year', 'Duration_min', 'Rating_IMDB', 'Votes_IMDB',
    'Budget_million', 'Revenue_million', 'Seasons',
    'Episodes', 'Awards_won', 'Awards_nominated', 'User_rating'
]
numeric_data = df[cols].to_numpy()

print("Форма массива:", numeric_data.shape)
print("\nПервые 5 строк:")
print(numeric_data[:5])


# ============================================================
# ЗАДАЧА 2 — Статистика по колонкам
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 2 — Статистика")
print("=" * 60)

for col in ['Rating_IMDB', 'Budget_million', 'Revenue_million']:
    mean = df[col].mean()
    median = df[col].median()
    std = df[col].std()
    print(f"{col}: mean={mean:.2f}, median={median:.2f}, std={std:.2f}")


# ============================================================
# ЗАДАЧА 3 — Фильтрация через NumPy
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 3 — Фильтрация через NumPy")
print("=" * 60)

budget_arr = df['Budget_million'].to_numpy()
revenue_arr = df['Revenue_million'].to_numpy()

mask = (budget_arr > 200) & (revenue_arr > 500)
indices = np.where(mask)[0]

print(f"Найдено фильмов с Budget>200 и Revenue>500: {len(indices)}")
print("\nПервые 10:")
print(df.loc[indices[:10], ['Title', 'Budget_million', 'Revenue_million']].to_string(index=False))


# ============================================================
# ЗАДАЧА 4 — Dict и подсчёты по жанрам
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 4 — Dict жанров")
print("=" * 60)

genre_counts = df['Genre'].value_counts().to_dict()
print("Все жанры:", genre_counts)

top3 = sorted(genre_counts, key=genre_counts.get, reverse=True)[:3]
print("\nТоп-3 жанра:", top3)


# ============================================================
# ЗАДАЧА 5 — Set и уникальные значения
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 5 — Set платформ и директоров")
print("=" * 60)

platforms_set = set(df['Streaming_platform'])
directors_set = set(df['Director'])

print("Уникальные платформы:", platforms_set)
print(f"Количество уникальных директоров: {len(directors_set)}")


# ============================================================
# ЗАДАЧА 6 — Lambda и генераторы
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 6 — Lambda и генераторы")
print("=" * 60)

# Колонка profit через lambda
df['profit'] = df.apply(lambda row: row['Revenue_million'] - row['Budget_million'], axis=1)

# Генератор фильмов с рейтингом >= 8
def high_rated(dataframe):
    for _, row in dataframe.iterrows():
        if row['Rating_IMDB'] >= 8:
            yield row

gen = high_rated(df)
print("Первые 10 фильмов из генератора high_rated (Rating >= 8):")
print(f"{'Title':<20} {'Rating_IMDB':>12} {'Profit':>10}")
print("-" * 45)
for i, row in enumerate(gen):
    if i >= 10:
        break
    print(f"{row['Title']:<20} {row['Rating_IMDB']:>12.1f} {row['profit']:>10.1f}")


# ============================================================
# ЗАДАЧА 7 — Сводная таблица
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 7 — Сводная таблица")
print("=" * 60)

pivot = df.pivot_table(
    index='Genre',
    columns='Streaming_platform',
    values='profit',
    aggfunc='mean'
)
print(pivot.round(2))


# ============================================================
# ЗАДАЧА 8 — Сохранение и чтение файлов
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 8 — Сохранение файлов")
print("=" * 60)

# Сохранить DataFrame с profit в Excel
df.to_excel('student2_profit.xlsx', index=False)
print("Сохранено: student2_profit.xlsx")

# Сохранить сводную таблицу в CSV
pivot.to_csv('student2_pivot.csv')
print("Сохранено: student2_pivot.csv")

# Прочитать CSV обратно и проверить
pivot_check = pd.read_csv('student2_pivot.csv', index_col='Genre')
print("\nПрочитанный CSV совпадает с оригиналом:", pivot.round(2).equals(pivot_check.round(2)))
print(pivot_check.round(2))


# ============================================================
# ЗАДАЧА 9 — Визуализация Matplotlib
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 9 — Matplotlib")
print("=" * 60)

# График 1: Гистограмма Rating_IMDB
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df['Rating_IMDB'], bins=20, color='steelblue', edgecolor='white')
ax.set_title('Распределение рейтинга IMDB')
ax.set_xlabel('Rating IMDB')
ax.set_ylabel('Количество фильмов')
ax.grid(axis='y', alpha=0.4)
plt.tight_layout()
plt.savefig('student2_hist_rating.png', dpi=150)
plt.close()
print("Сохранено: student2_hist_rating.png")

# График 2: Scatter Budget vs Revenue
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(df['Budget_million'], df['Revenue_million'],
           alpha=0.3, s=15, color='steelblue')
ax.set_title('Бюджет vs Доход')
ax.set_xlabel('Бюджет (млн $)')
ax.set_ylabel('Доход (млн $)')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('student2_scatter_budget_revenue.png', dpi=150)
plt.close()
print("Сохранено: student2_scatter_budget_revenue.png")


# ============================================================
# ЗАДАЧА 10 — Визуализация Seaborn
# ============================================================
print("\n" + "=" * 60)
print("ЗАДАЧА 10 — Seaborn")
print("=" * 60)

sns.set_theme(style='whitegrid')

# График 1: Countplot жанров
fig, ax = plt.subplots(figsize=(9, 5))
sns.countplot(data=df, x="Genre", hue="Genre", palette="Blues_d", order=df["Genre"].value_counts().index, legend=False, ax=ax)
ax.set_title('Количество фильмов по жанрам')
ax.set_xlabel('Жанр')
ax.set_ylabel('Количество')
plt.tight_layout()
plt.savefig('student2_countplot_genre.png', dpi=150)
plt.close()
print("Сохранено: student2_countplot_genre.png")

# График 2: Boxplot profit по платформам
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="Streaming_platform", y="profit", hue="Streaming_platform", palette="Set2", legend=False, ax=ax)
ax.set_title('Прибыль по стриминговым платформам')
ax.set_xlabel('Платформа')
ax.set_ylabel('Прибыль (млн $)')
plt.tight_layout()
plt.savefig('student2_boxplot_profit.png', dpi=150)
plt.close()
print("Сохранено: student2_boxplot_profit.png")

# График 3: Heatmap корреляции
fig, ax = plt.subplots(figsize=(10, 7))
num_cols = ['Year', 'Duration_min', 'Rating_IMDB', 'Votes_IMDB',
            'Budget_million', 'Revenue_million', 'Seasons',
            'Episodes', 'Awards_won', 'Awards_nominated', 'User_rating', 'profit']
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, ax=ax)
ax.set_title('Матрица корреляций числовых признаков')
plt.tight_layout()
plt.savefig('student2_heatmap_corr.png', dpi=150)
plt.close()
print("Сохранено: student2_heatmap_corr.png")

print("\n✓ Все задачи выполнены!")