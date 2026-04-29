import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        self.data_file = "movies.json"
        self.movies = self.load_data()

        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(root, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(root, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(root, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=5, pady=5)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5)
        self.genre_filter.bind("<KeyRelease>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, padx=5)
        self.year_filter = tk.Entry(filter_frame, width=10)
        self.year_filter.grid(row=0, column=3, padx=5)
        self.year_filter.bind("<KeyRelease>", self.apply_filters)

        # Таблица
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Прокрутка
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.refresh_table()

    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def validate_year(self, year):
        """Проверка года"""
        try:
            y = int(year)
            return 1888 <= y <= 2026  # reasonable range
        except:
            return False

    def validate_rating(self, rating):
        """Проверка рейтинга"""
        try:
            r = float(rating)
            return 0 <= r <= 10
        except:
            return False

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны!")
            return

        if not self.validate_year(year):
            messagebox.showerror("Ошибка", "Год должен быть числом (от 1888 до 2026)!")
            return

        if not self.validate_rating(rating):
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }

        self.movies.append(movie)
        self.save_data()
        self.refresh_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")

    def apply_filters(self, event=None):
        """Применение фильтров"""
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы с учётом фильтров"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        genre_filter = self.genre_filter.get().strip().lower()
        year_filter = self.year_filter.get().strip()

        filtered = self.movies
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except:
                pass  # игнорируем некорректный год в фильтре

        for movie in filtered:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()