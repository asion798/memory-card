import tkinter as tk
from tkinter import messagebox
import random
import time

class Question:
    def __init__(self, text, answers, correct):
        self.text = text
        self.answers = answers
        self.correct = correct

class MemoryCard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Card")
        self.window.geometry("500x530")
        
        self.questions = [
            Question("Самый сложный вопрос в мире!", 
                     ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"], 
                     "Вариант 1"),
            Question("Государственный язык Бразилии", 
                     ["Португальский", "Итальянский", "Бразильский", "Испанский"], 
                     "Португальский"),
            Question("Столица Франции", 
                     ["Лондон", "Берлин", "Париж", "Мадрид"], 
                     "Париж"),
            Question("Сколько планет в Солнечной системе?", 
                     ["7", "8", "9", "10"], 
                     "8"),
            Question("Самая большая планета Солнечной системы?", 
                     ["Земля", "Марс", "Юпитер", "Сатурн"], 
                     "Юпитер"),
            Question("Столица Японии?", 
                     ["Сеул", "Пекин", "Токио", "Бангкок"], 
                     "Токио")
        ]
        
        self.total = 0
        self.right = 0
        self.current_index = -1
        self.questions_done = 0
        self.time_left = 30
        self.timer_running = False
        self.timer_id = None
        self.game_finished = False
        
        self.selected = tk.StringVar()
        
        self.create_widgets()
        self.next_question()
        
    def create_widgets(self):
        self.header_frame = tk.Frame(self.window)
        self.header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        self.counter_label = tk.Label(self.header_frame, 
                                     text="Вопрос: 0/0",
                                     font=("Arial", 12, "bold"),
                                     fg="#2c3e50")
        self.counter_label.pack(side="left")
        
        self.timer_label = tk.Label(self.header_frame,
                                   text="⏱ 30 сек",
                                   font=("Arial", 12, "bold"),
                                   fg="#e74c3c")
        self.timer_label.pack(side="right")
        
        self.question_label = tk.Label(self.window, text="", 
                                      font=("Arial", 14, "bold"),
                                      wraplength=450,
                                      fg="#34495e")
        self.question_label.pack(pady=15)
        
        self.answers_frame = tk.LabelFrame(self.window, text="Варианты ответов",
                                          font=("Arial", 11, "bold"),
                                          bg="#ecf0f1")
        self.answers_frame.pack(pady=10, padx=20, fill="both")
        
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.answers_frame, text="", 
                               variable=self.selected, value="",
                               font=("Arial", 10),
                               bg="#ecf0f1")
            rb.pack(anchor="w", pady=4, padx=15)
            self.radio_buttons.append(rb)
        
        self.result_frame = tk.LabelFrame(self.window, text="Результат теста",
                                         font=("Arial", 11, "bold"),
                                         bg="#ecf0f1")
        
        self.result_text = tk.Label(self.result_frame, text="", 
                                   font=("Arial", 12, "bold"))
        self.result_text.pack(pady=8)
        
        self.correct_answer_text = tk.Label(self.result_frame, text="", 
                                           font=("Arial", 10))
        self.correct_answer_text.pack(pady=5)
        
        self.action_button = tk.Button(self.window, text="Ответить", 
                                      font=("Arial", 12, "bold"),
                                      bg="#3498db", fg="white",
                                      width=20, height=2,
                                      command=self.handle_click,
                                      relief="raised",
                                      cursor="hand2")
        self.action_button.pack(pady=15)
        
        self.stats_frame = tk.LabelFrame(self.window, text="Статистика",
                                        font=("Arial", 11, "bold"),
                                        bg="#f8f9fa")
        self.stats_frame.pack(pady=10, padx=20, fill="x")
        
        stats_grid = tk.Frame(self.stats_frame, bg="#f8f9fa")
        stats_grid.pack(pady=10, padx=10)
        
        tk.Label(stats_grid, text="Пройдено вопросов:", 
                font=("Arial", 10),
                bg="#f8f9fa").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.questions_done_label = tk.Label(stats_grid, text="0",
                                           font=("Arial", 10, "bold"),
                                           fg="#2980b9",
                                           bg="#f8f9fa")
        self.questions_done_label.grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(stats_grid, text="Всего вопросов:", 
                font=("Arial", 10),
                bg="#f8f9fa").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.total_label = tk.Label(stats_grid, text="0",
                                  font=("Arial", 10, "bold"),
                                  fg="#2980b9",
                                  bg="#f8f9fa")
        self.total_label.grid(row=0, column=3, sticky="w", padx=(0, 20))
        
        tk.Label(stats_grid, text="Правильные ответы:", 
                font=("Arial", 10),
                bg="#f8f9fa").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.right_label = tk.Label(stats_grid, text="0",
                                  font=("Arial", 10, "bold"),
                                  fg="#27ae60",
                                  bg="#f8f9fa")
        self.right_label.grid(row=1, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(stats_grid, text="Рейтинг:", 
                font=("Arial", 10),
                bg="#f8f9fa").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.rating_label = tk.Label(stats_grid, text="0%",
                                   font=("Arial", 10, "bold"),
                                   fg="#e74c3c",
                                   bg="#f8f9fa")
        self.rating_label.grid(row=1, column=3, sticky="w")
        
        self.progress_frame = tk.Frame(self.window)
        self.progress_frame.pack(pady=(5, 15), padx=20, fill="x")
        
        tk.Label(self.progress_frame, text="Прогресс:", 
                font=("Arial", 9),
                fg="#7f8c8d").pack(anchor="w")
        
        self.progress_canvas = tk.Canvas(self.progress_frame, height=20, 
                                        bg="#ecf0f1", highlightthickness=0)
        self.progress_canvas.pack(fill="x", pady=(3, 0))
        
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 20, 
                                                                 fill="#3498db", width=0)
        
    def show_final_results(self):
        self.game_finished = True
        self.stop_timer()
        
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.window.configure(bg="#2c3e50")
        
        final_frame = tk.Frame(self.window, bg="#2c3e50")
        final_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        tk.Label(final_frame, text="🎉 ВАШ РЕЗУЛЬТАТ 🎉", 
                font=("Arial", 24, "bold"),
                bg="#2c3e50",
                fg="#ffffff").pack(pady=(0, 30))
        
        results_frame = tk.Frame(final_frame, bg="#34495e", bd=2, relief="ridge")
        results_frame.pack(pady=20, padx=20, fill="both")
        
        rating = 0
        if self.total > 0:
            rating = (self.right / self.total) * 100
        
        color = "#27ae60" if rating >= 70 else "#f39c12" if rating >= 50 else "#e74c3c"
        
        tk.Label(results_frame, text=f"РЕЙТИНГ: {rating:.1f}%", 
                font=("Arial", 32, "bold"),
                bg="#34495e",
                fg=color).pack(pady=30)
        
        stats_frame = tk.Frame(results_frame, bg="#34495e")
        stats_frame.pack(pady=20, padx=40)
        
        stats_data = [
            ("✓ Правильных ответов:", str(self.right), "#27ae60"),
            ("✗ Неправильных ответов:", str(self.total - self.right), "#e74c3c"),
            ("📊 Всего вопросов:", str(self.total), "#3498db"),
            ("⏱ Пройдено вопросов:", str(self.questions_done), "#9b59b6"),
            ("📈 Процент правильных:", f"{rating:.1f}%", color)
        ]
        
        for i, (label_text, value_text, color) in enumerate(stats_data):
            row_frame = tk.Frame(stats_frame, bg="#34495e")
            row_frame.pack(fill="x", pady=8)
            
            tk.Label(row_frame, text=label_text, 
                    font=("Arial", 14),
                    bg="#34495e",
                    fg="#bdc3c7").pack(side="left", padx=(0, 10))
            
            tk.Label(row_frame, text=value_text, 
                    font=("Arial", 16, "bold"),
                    bg="#34495e",
                    fg=color).pack(side="right")
        
        grade_frame = tk.Frame(results_frame, bg="#34495e")
        grade_frame.pack(pady=30)
        
        if rating == 100:
            grade_text = "🏆 ОТЛИЧНО! ИДЕАЛЬНЫЙ РЕЗУЛЬТАТ!"
            grade_color = "#f1c40f"
        elif rating >= 80:
            grade_text = "👍 ОЧЕНЬ ХОРОШО!"
            grade_color = "#27ae60"
        elif rating >= 60:
            grade_text = "👌 ХОРОШО!"
            grade_color = "#2ecc71"
        elif rating >= 40:
            grade_text = "😐 УДОВЛЕТВОРИТЕЛЬНО"
            grade_color = "#f39c12"
        else:
            grade_text = "📚 НУЖНО ПОВТОРИТЬ МАТЕРИАЛ"
            grade_color = "#e74c3c"
        
        tk.Label(grade_frame, text=grade_text, 
                font=("Arial", 16, "bold"),
                bg="#34495e",
                fg=grade_color,
                wraplength=400).pack()
        
        button_frame = tk.Frame(final_frame, bg="#2c3e50")
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="🔄 НАЧАТЬ ЗАНОВО", 
                 font=("Arial", 14, "bold"),
                 bg="#3498db", fg="white",
                 width=20, height=2,
                 command=self.restart_game,
                 relief="raised",
                 cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(button_frame, text="🚪 ВЫЙТИ", 
                 font=("Arial", 14, "bold"),
                 bg="#e74c3c", fg="white",
                 width=20, height=2,
                 command=self.window.quit,
                 relief="raised",
                 cursor="hand2").pack(side="right", padx=10)
        
    def restart_game(self):
        self.window.destroy()
        self.__init__()
        self.run()
        
    def start_timer(self):
        self.time_left = 10
        self.timer_running = True
        self.update_timer()
        
    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None
            
    def update_timer(self):
        if not self.timer_running:
            return
            
        if self.time_left > 0:
            color = "#27ae60" if self.time_left > 10 else "#e74c3c"
            self.timer_label.config(text=f"⏱ {self.time_left} сек", fg=color)
            self.time_left -= 1
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="⏱ Время вышло!", fg="#e74c3c")
            self.time_up()
            
    def time_up(self):
        self.stop_timer()
        self.total += 1
        self.questions_done += 1
        self.result_text.config(text="⏰ Время вышло!", fg="#e74c3c")
        self.correct_answer_text.config(text=f"Правильный ответ: {self.current_correct}")
        self.update_stats()
        self.show_result()
        
    def ask(self, q):
        self.question_label.config(text=q.text)
        
        answers = q.answers.copy()
        random.shuffle(answers)
        
        for i in range(4):
            self.radio_buttons[i].config(text=answers[i], value=answers[i])
        
        self.current_correct = q.correct
        self.show_question()
        
    def show_question(self):
        self.answers_frame.pack(pady=10, padx=20, fill="both")
        self.result_frame.pack_forget()
        self.action_button.config(text="Ответить", bg="#3498db")
        self.selected.set("")
        self.update_counter()
        self.start_timer()
        
    def show_result(self):
        self.stop_timer()
        self.answers_frame.pack_forget()
        self.result_frame.pack(pady=10, padx=20, fill="both")
        if self.questions_done < len(self.questions):
            self.action_button.config(text="Следующий вопрос", bg="#2ecc71")
        else:
            self.action_button.config(text="Показать результаты", bg="#9b59b6", 
                                     command=self.show_final_results)
        
    def check_answer(self):
        if not self.timer_running:
            return
            
        answer = self.selected.get()
        
        if not answer:
            messagebox.showwarning("Внимание", "Выберите вариант ответа!")
            return
            
        self.total += 1
        self.questions_done += 1
        
        if answer == self.current_correct:
            self.result_text.config(text="✓ Правильно!", fg="#27ae60")
            self.right += 1
        else:
            self.result_text.config(text="✗ Неправильно!", fg="#e74c3c")
            
        self.correct_answer_text.config(text=f"Правильный ответ: {self.current_correct}")
        self.update_stats()
        self.show_result()
        
    def next_question(self):
        if self.questions_done >= len(self.questions):
            self.show_final_results()
            return
            
        self.stop_timer()
        self.current_index = random.randint(0, len(self.questions) - 1)
        
        print(f"\n=== Статистика ===")
        print(f"Пройдено вопросов: {self.questions_done}")
        print(f"Всего вопросов: {self.total}")
        print(f"Правильных ответов: {self.right}")
        
        if self.total > 0:
            rating = (self.right / self.total) * 100
            print(f"Рейтинг: {rating:.1f}%")
        
        q = self.questions[self.current_index]
        self.ask(q)
        
    def handle_click(self):
        if self.game_finished:
            return
            
        if self.action_button.cget("text") == "Ответить":
            self.check_answer()
        else:
            self.next_question()
            
    def update_counter(self):
        total_questions_in_pool = len(self.questions)
        self.counter_label.config(
            text=f"Вопрос: {self.questions_done + 1}/{total_questions_in_pool}"
        )
        
    def update_stats(self):
        rating = 0
        if self.total > 0:
            rating = (self.right / self.total) * 100
        
        self.questions_done_label.config(text=str(self.questions_done))
        self.total_label.config(text=str(self.total))
        self.right_label.config(text=str(self.right))
        self.rating_label.config(text=f"{rating:.1f}%")
        
        progress_width = 460
        if self.total > 0:
            progress = (self.questions_done / self.total) * progress_width
        else:
            progress = 0
        
        self.progress_canvas.coords(self.progress_bar, 0, 0, progress, 20)
        
        print(f"\n=== Новая статистика ===")
        print(f"Пройдено вопросов: {self.questions_done}")
        print(f"Всего вопросов: {self.total}")
        print(f"Правильных ответов: {self.right}")
        print(f"Рейтинг: {rating:.1f}%")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MemoryCard()
    app.run()