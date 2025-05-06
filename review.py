import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class QAReviewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QA Reviewer")

        # Верхняя панель с номером вопроса и временем обработки
        self.top_panel = tk.Frame(root)
        self.top_panel.pack(fill="x", padx=10, pady=5)

        self.index_label = tk.Label(self.top_panel, text="Вопрос: -/-", font=("Arial", 10))
        self.index_label.pack(side="left", padx=10)

        self.time_label = tk.Label(self.top_panel, text="Время обработки: -", font=("Arial", 10))
        self.time_label.pack(side="right", padx=10)

        # Основные элементы интерфейса
        self.question_label = tk.Label(root, text="Вопрос:", font=("Arial", 12, "bold"))
        self.question_label.pack(anchor="w", padx=10, pady=5)

        self.question_text = tk.Text(root, wrap="word", height=5, font=("Arial", 10))
        self.question_text.pack(fill="both", padx=10, pady=5)

        self.answer_label = tk.Label(root, text="Ответ:", font=("Arial", 12, "bold"))
        self.answer_label.pack(anchor="w", padx=10, pady=5)

        self.answer_text = tk.Text(root, wrap="word", height=10, font=("Arial", 10))
        self.answer_text.pack(fill="both", padx=10, pady=5)

        self.criteria_frame = tk.Frame(root)
        self.criteria_frame.pack(fill="x", padx=10, pady=5)

        self.criteria = {
            "точность": tk.IntVar(value=0),
            "грамотность": tk.IntVar(value=0),
            "полнота": tk.IntVar(value=0),
            "лаконичность": tk.IntVar(value=0)
        }

        for i, (crit, var) in enumerate(self.criteria.items()):
            label = tk.Label(self.criteria_frame, text=crit.capitalize())
            label.grid(row=0, column=i, padx=5)

            # Создаем Spinbox и добавляем логику перехода 0 → 10
            spinbox = ttk.Spinbox(
                self.criteria_frame,
                from_=0, to=10,
                textvariable=var,
                width=5,
                command=lambda v=var: self.handle_spinbox_wraparound(v)
            )
            spinbox.grid(row=1, column=i, padx=5)

        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack(fill="x", pady=10)

        self.prev_button = ttk.Button(self.navigation_frame, text="Предыдущий", command=self.prev_entry)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(self.navigation_frame, text="Следующий", command=self.next_entry)
        self.next_button.pack(side="left", padx=10)

        self.save_button = ttk.Button(self.navigation_frame, text="Сохранить", command=self.save_to_file)
        self.save_button.pack(side="right", padx=10)
        self.save_button = ttk.Button(self.navigation_frame, text="Открыть", command=self.load_results)
        self.save_button.pack(side="right", padx=10)
        # Загружаем JSON файл
        self.load_results()

    def load_results(self):
        self.results = []
        self.current_index = 0
        """Загружает файл results.json и отображает первый элемент."""
        file_path = filedialog.askopenfilename(
            title="Открыть файл JSON",
            filetypes=[("JSON files", "*.json")]
        )
        if not file_path:
            return
        self.root.title(f"QA Reviewer - {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.results = json.load(f)
                self.file_path = file_path
                if self.results:
                    self.show_entry(0)
                else:
                    messagebox.showinfo("Информация", "Файл пуст.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def show_entry(self, index):
        """Отображает запись по заданному индексу."""
        self.current_index = index
        entry = self.results[index]

        # Обновление текстов вопроса и ответа
        self.question_text.delete("1.0", "end")
        self.question_text.insert("1.0", entry.get("question", ""))

        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", entry.get("answer",  ""))

        # Обновление критериев оценки
        for crit, var in self.criteria.items():
            var.set(entry.get(crit, 0))

        # Обновление верхней панели
        total_questions = len(self.results)
        self.index_label.config(text=f"Вопрос: {index + 1}/{total_questions}")
        elapsed_time = entry.get("elapsed_time", "неизвестно")
        self.time_label.config(text=f"Время обработки: {elapsed_time} сек")


    def handle_spinbox_wraparound(self, var):
        current_value = var.get()
        if current_value == 0:  # Если текущее значение 0
            var.set(10)  # Устанавливаем значение 10

    def save_current_entry(self):
        """Сохраняет текущие оценки в results."""
        entry = self.results[self.current_index]
        for crit, var in self.criteria.items():
            entry[crit] = var.get()

    def prev_entry(self):
        """Переход к предыдущей записи."""
        if self.current_index > 0:
            self.save_current_entry()
            self.show_entry(self.current_index - 1)

    def next_entry(self):
        """Переход к следующей записи."""
        if self.current_index < len(self.results) - 1:
            self.save_current_entry()
            self.show_entry(self.current_index + 1)

    def save_to_file(self):
        """Сохраняет результаты в JSON файл."""
        self.save_current_entry()
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.results, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Файл успешно сохранен.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QAReviewerApp(root)
    root.mainloop()
