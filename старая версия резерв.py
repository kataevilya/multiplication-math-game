import tkinter as tk
from tkinter import messagebox, PhotoImage
import random, time, winsound, threading, os, sys

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математический тренажер")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#004d00")

        # Переменные настроек
        self.diff = tk.StringVar(value="Средний")
        self.use_pm = tk.BooleanVar(value=True) # Плюс/Минус
        self.use_md = tk.BooleanVar(value=False) # Умножение/Деление
        
        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def play_sound(self, file_name):
        path = resource_path(file_name)
        try: threading.Thread(target=winsound.PlaySound, args=(path, winsound.SND_FILENAME), daemon=True).start()
        except: pass

    def main_menu(self):
        self.clear_screen()
        
        # Заголовок
        tk.Label(self.root, text="МАТЕМАТИЧЕСКИЙ ТРЕНАЖЕР", font=("Arial", 45, "bold"), bg="#004d00", fg="white").pack(pady=20)

        # Рисунок мальчика в углу (если файла нет, будет просто место)
        try:
            self.img = PhotoImage(file=resource_path("boy.png"))
            img_label = tk.Label(self.root, image=self.img, bg="#004d00")
            img_label.place(x=50, y=50) 
        except:
            tk.Label(self.root, text="[Место для\nрисунка]", font=("Arial", 12), bg="#004d00", fg="white").place(x=50, y=50)

        f = tk.Frame(self.root, bg="#004d00")
        f.pack(expand=True)

        # Увеличенные поля ввода
        label_opt = {"font": ("Arial", 22, "bold"), "bg": "#004d00", "fg": "white"}
        entry_opt = {"font": ("Arial", 25), "width": 15}

        tk.Label(f, text="Ваше имя:", **label_opt).grid(row=0, column=0, sticky="e", pady=10)
        self.n_ent = tk.Entry(f, **entry_opt); self.n_ent.grid(row=0, column=1, pady=10, padx=20)
        self.n_ent.insert(0, "Ученик")

        tk.Label(f, text="Время (сек):", **label_opt).grid(row=1, column=0, sticky="e", pady=10)
        self.t_ent = tk.Entry(f, **entry_opt); self.t_ent.grid(row=1, column=1, pady=10, padx=20)
        self.t_ent.insert(0, "60")

        tk.Label(f, text="Кол-во примеров:", **label_opt).grid(row=2, column=0, sticky="e", pady=10)
        self.c_ent = tk.Entry(f, **entry_opt); self.c_ent.grid(row=2, column=1, pady=10, padx=20)
        self.c_ent.insert(0, "10")

        # Выбор операций (Чек-боксы)
        tk.Label(f, text="Операции:", **label_opt).grid(row=3, column=0, sticky="e", pady=10)
        ops_f = tk.Frame(f, bg="#004d00")
        ops_f.grid(row=3, column=1, sticky="w", padx=20)
        tk.Checkbutton(ops_f, text="+ и -", variable=self.use_pm, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left")
        tk.Checkbutton(ops_f, text="× и :", variable=self.use_md, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left", padx=20)

        # Сложность
        tk.Label(f, text="Сложность:", font=("Arial", 22, "bold"), bg="#004d00", fg="yellow").grid(row=4, column=0, columnspan=2, pady=15)
        diff_f = tk.Frame(f, bg="#004d00")
        diff_f.grid(row=5, column=0, columnspan=2)
        for v in ["Легкий", "Средний", "Сложный"]:
            tk.Radiobutton(diff_f, text=v, variable=self.diff, value=v, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left", padx=15)

        tk.Button(self.root, text="НАЧАТЬ ТЕСТ", command=self.start, bg="#4CAF50", fg="white", font=("Arial", 30, "bold"), padx=50, pady=10).pack(pady=20)
        
        # Кнопки внизу
        btn_f = tk.Frame(self.root, bg="#004d00")
        btn_f.pack(side="bottom", pady=30)
        tk.Button(btn_f, text="ОБ АВТОРЕ", command=lambda: messagebox.showinfo("Автор", "Илья Катаев\nДля 4-х классов"), font=("Arial", 15)).pack(side="left", padx=20)
        tk.Button(btn_f, text="ВЫХОД", command=self.root.destroy, bg="#e74c3c", fg="white", font=("Arial", 15)).pack(side="left")

    def start(self):
        if not self.use_pm.get() and not self.use_md.get():
            messagebox.showwarning("Ошибка", "Выберите хотя бы одну операцию!"); return
        
        try:
            self.user = self.n_ent.get()
            self.tm = int(self.t_ent.get())
            self.qc = int(self.c_ent.get())
        except: return

        self.qs = []
        d = self.diff.get()
        
        for _ in range(self.qc):
            pool = []
            if self.use_pm.get(): pool.extend(["+", "-"])
            if self.use_md.get(): pool.extend(["*", "/"])
            op = random.choice(pool)

            # Настройка чисел под сложность
            if d == "Легкий": r = (1, 20)
            elif d == "Средний": r = (10, 100)
            else: r = (50, 500)

            if op == "+":
                a, b = random.randint(*r), random.randint(*r)
                self.qs.append((a, b, "+", a + b))
            elif op == "-":
                a, b = random.randint(*r), random.randint(*r)
                if a < b: a, b = b, a
                self.qs.append((a, b, "-", a - b))
            elif op == "*":
                r_m = (2, 5) if d == "Легкий" else (2, 10) if d == "Средний" else (2, 20)
                a, b = random.randint(*r_m), random.randint(*r_m)
                self.qs.append((a, b, "×", a * b))
            elif op == "/":
                r_m = (2, 5) if d == "Легкий" else (2, 10) if d == "Средний" else (2, 20)
                a, b = random.randint(*r_m), random.randint(*r_m)
                self.qs.append((a*b, a, ":", b))

        self.solved = 0; self.errors = 0; self.game_over = False; self.st = time.time()
        self.next_q()

    def next_q(self):
        if not self.qs: self.finish(True)
        else: self.curr = self.qs.pop(); self.game_screen()

    def game_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Решено: {self.solved} | Ошибок: {self.errors}", font=("Arial", 22), bg="#004d00", fg="white").pack(pady=10)
        self.timer_l = tk.Label(self.root, text="", font=("Arial", 25, "bold"), fg="yellow", bg="#004d00"); self.timer_l.pack()
        self.upd_timer()
        
        txt = f"{self.curr[0]} {self.curr[2]} {self.curr[1]} ="
        tk.Label(self.root, text=txt, font=("Arial", 120, "bold"), bg="#004d00", fg="white").pack(expand=True)
        
        self.ans_e = tk.Entry(self.root, font=("Arial", 70, "bold"), width=6, justify='center')
        self.ans_e.pack(pady=20); self.ans_e.bind('<Return>', lambda e: self.check()); self.ans_e.focus()
        
        tk.Button(self.root, text="ОТВЕТИТЬ", command=self.check, bg="#2196F3", fg="white", font=("Arial", 25, "bold"), padx=50, pady=10).pack(pady=30)

    def check(self):
        try:
            val = int(self.ans_e.get())
            if val == self.curr[3]:
                self.play_sound("win.wav"); self.solved += 1; self.next_q()
            else:
                self.play_sound("lose.wav"); self.errors += 1; self.next_q() # Считаем ошибку и идем дальше
        except: pass

    def upd_timer(self):
        if self.game_over: return
        rem = int(self.tm - (time.time() - self.st))
        if rem <= 0: self.finish(False)
        else: self.timer_l.config(text=f"ВРЕМЯ: {rem}"); self.root.after(1000, self.upd_timer)

    def finish(self, success):
        self.game_over = True; self.clear_screen()
        
        # Логика оценки
        if self.solved >= 7:
            res_txt = "МОЛОДЕЦ! 🎉"
            color = "lime"
        elif self.solved >= 1:
            res_txt = "ПОСТАРАЙСЯ ЕЩЕ! 📈"
            color = "orange"
        else:
            res_txt = "НУЖНО БОЛЬШЕ ПРАКТИКИ! 📚"
            color = "red"

        tk.Label(self.root, text=res_txt, font=("Arial", 60, "bold"), fg=color, bg="#004d00").pack(expand=True)
        tk.Label(self.root, text=f"Результат: {self.solved} из {self.qc}\nОшибок: {self.errors}", font=("Arial", 30), fg="white", bg="#004d00").pack(expand=True)
        tk.Button(self.root, text="В МЕНЮ", command=self.main_menu, font=("Arial", 25, "bold"), padx=40, pady=15).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk(); app = MathApp(root); root.mainloop()