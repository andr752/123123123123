import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []
        self.load_data()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # --- Блок ввода данных ---
        tk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.sum_entry = tk.Entry(self.root)
        self.sum_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.cat_entry = tk.Entry(self.root)
        self.cat_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления расхода
        tk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(
            row=3, column=0, columnspan=2, padx=5, pady=10
        )

        # --- Блок фильтрации ---
        tk.Label(self.root, text="Фильтр по категории:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.filter_cat = ttk.Combobox(self.root)
        self.filter_cat.grid(row=4, column=1, padx=5, pady=5)
        self.update_category_filter()  # Инициализация фильтра при запуске

        tk.Label(self.root, text="Период с:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.date_from = tk.Entry(self.root)
        self.date_from.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="по:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.date_to = tk.Entry(self.root)
        self.date_to.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(
            row=7, column=0, columnspan=2, padx=5, pady=10
        )

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(self.root, columns=("sum", "category", "date"), show="headings")
        self.tree.heading("sum", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def add_expense(self):
        """Добавляет новый расход после проверки данных."""
        try:
            sum_ = float(self.sum_entry.get())
            if sum_ <= 0:
                raise ValueError("Сумма должна быть положительной")
            category = self.cat_entry.get()
            if not category:
                raise ValueError("Введите категорию")
            date_ = self.date_entry.get()
            datetime.strptime(date_, "%Y-%m-%d")  # Проверка формата даты

            # Добавление в список и сохранение
            self.data.append({"sum": sum_, "category": category.title(), "date": date_})
            self.save_data()

            # Обновляем интерфейс
            self.update_table()
            self.update_category_filter()  # Обновляем список категорий в фильтре

            # Очищаем поля ввода
            self.sum_entry.delete(0, tk.END)
            self.cat_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def update_table(self):
        """Очищает и полностью перерисовывает таблицу расходов."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.data:
            self.tree.insert("", tk.END, values=(item["sum"], item["category"], item["date"]))

    def apply_filter(self):
        """Применяет фильтры по категории и дате к данным."""
        cat = self.filter_cat.get()
        date_from = self.date_from.get()
        date_to = self.date_to.get()

        filtered = self.data.copy()

        if cat and cat != "Все":
            filtered = [x for x in filtered if x["category"] == cat]

        if date_from:
            filtered = [x for x in filtered if x["date"] >= date_from]

        if date_to:
            filtered = [x for x in filtered if x["date"] <= date_to]

        # Отрисовка отфильтрованных данных
        for i in self.tree.get_children():
            self.tree.delete(i)

        total_sum = sum(x["sum"] for x in filtered)

        for item in filtered:
            self.tree.insert("", tk.END, values=(item["sum"], item["category"], item["date"]))

    def update_category_filter(self):
         """Обновляет список категорий в выпадающем меню фильтра."""
         categories = ["Все"] + sorted({x["category"] for x in self.data})
         
         current_text = self.filter_cat.get()
         
         self.filter_cat['values'] = categories
         
         # Сохраняем выбранное значение или сбрасываем на "Все"
         if current_text in categories:
             self.filter_cat.set(current_text)
         else:
             self.filter_cat.current(0)

    def save_data(self):
         """Сохраняет данные в файл data.json."""
         with open("data.json", "w", encoding="utf-8") as f:
             json.dump(self.data, f, ensure_ascii=False, indent=2)

    def load_data(self):
         """Загружает данные из файла data.json."""
         try:
             with open("data.json", "r", encoding="utf-8") as f:
                 self.data = json.load(f)
         except FileNotFoundError:
             self.data = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
