import tkinter as tk
from tkinter import messagebox, filedialog
import random, time, winsound, threading, os, sys
from datetime import datetime
from PIL import Image, ImageTk

# ========== НАСТРОЙКИ РАЗМЕРОВ КАРТИНОК ==========
BOY_SIZE = (450, 450)    # размер мальчика
DOG_SIZE = (250, 250)    # размер собак (dog.png и dog1.png)
# =================================================

def resource_path(relative_path):
    """Ищет файл сначала в папке assets, потом в корне (для сборки и разработки)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    candidate = os.path.join(base_path, "assets", relative_path)
    if os.path.exists(candidate):
        return candidate
    candidate2 = os.path.join(base_path, relative_path)
    if os.path.exists(candidate2):
        return candidate2
    return os.path.join(base_path, "assets", relative_path)

class MathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математический тренажер")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#004d00")

        self.diff = tk.StringVar(value="Средний")
        self.use_pm = tk.BooleanVar(value=True)
        self.use_md = tk.BooleanVar(value=False)

        self.click_count = 0
        self.dog_label = None
        self.dog_image = None
        self.boy_image = None

        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_sound(self, file_name):
        path = resource_path(file_name)
        try:
            if not os.path.exists(path):
                print(f"Звук не найден: {path}")
                return
            threading.Thread(target=winsound.PlaySound, args=(path, winsound.SND_FILENAME), daemon=True).start()
        except Exception as e:
            print(f"Ошибка звука: {e}")

    def load_image(self, filename, size):
        """Загружает картинку, сжимает до size (сохраняя пропорции)"""
        try:
            path = resource_path(filename)
            if not os.path.exists(path):
                print(f"Файл не найден: {path}")
                return None
            pil_img = Image.open(path)
            pil_img.thumbnail(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return None

    def main_menu(self):
        self.clear_screen()
        self.click_count = 0

        tk.Label(self.root, text="МАТЕМАТИЧЕСКИЙ ТРЕНАЖЕР", font=("Arial", 45, "bold"), bg="#004d00", fg="white").pack(pady=20)

        # Загружаем мальчика с размером BOY_SIZE
        self.boy_image = self.load_image("boy.png", BOY_SIZE)
        if self.boy_image:
            img_label = tk.Label(self.root, image=self.boy_image, bg="#004d00")
            img_label.place(x=50, y=50)
        else:
            img_label = tk.Label(self.root, text="[Место для\nрисунка]", font=("Arial", 12), bg="#004d00", fg="white")
            img_label.place(x=50, y=50)

        img_label.bind("<Button-1>", self.on_boy_click)

        # ---------- ВСЁ МЕНЮ (без изменений) ----------
        f = tk.Frame(self.root, bg="#004d00")
        f.pack(expand=True)

        label_opt = {"font": ("Arial", 22, "bold"), "bg": "#004d00", "fg": "white"}
        entry_opt = {"font": ("Arial", 25), "width": 15}

        tk.Label(f, text="Ваше имя:", **label_opt).grid(row=0, column=0, sticky="e", pady=10)
        self.n_ent = tk.Entry(f, **entry_opt)
        self.n_ent.grid(row=0, column=1, pady=10, padx=20)
        self.n_ent.insert(0, "Ученик")

        tk.Label(f, text="Время (сек):", **label_opt).grid(row=1, column=0, sticky="e", pady=10)
        self.t_ent = tk.Entry(f, **entry_opt)
        self.t_ent.grid(row=1, column=1, pady=10, padx=20)
        self.t_ent.insert(0, "60")

        tk.Label(f, text="Кол-во примеров:", **label_opt).grid(row=2, column=0, sticky="e", pady=10)
        self.c_ent = tk.Entry(f, **entry_opt)
        self.c_ent.grid(row=2, column=1, pady=10, padx=20)
        self.c_ent.insert(0, "10")

        tk.Label(f, text="Операции:", **label_opt).grid(row=3, column=0, sticky="e", pady=10)
        ops_f = tk.Frame(f, bg="#004d00")
        ops_f.grid(row=3, column=1, sticky="w", padx=20)
        tk.Checkbutton(ops_f, text="+ и -", variable=self.use_pm, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left")
        tk.Checkbutton(ops_f, text="× и :", variable=self.use_md, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left", padx=20)

        tk.Label(f, text="Сложность:", font=("Arial", 22, "bold"), bg="#004d00", fg="yellow").grid(row=4, column=0, columnspan=2, pady=15)
        diff_f = tk.Frame(f, bg="#004d00")
        diff_f.grid(row=5, column=0, columnspan=2)
        for v in ["Легкий", "Средний", "Сложный"]:
            tk.Radiobutton(diff_f, text=v, variable=self.diff, value=v, font=("Arial", 18), bg="#004d00", fg="white", selectcolor="black").pack(side="left", padx=15)

        tk.Button(self.root, text="НАЧАТЬ ТЕСТ", command=self.start, bg="#4CAF50", fg="white", font=("Arial", 30, "bold"), padx=50, pady=10).pack(pady=20)

        btn_f = tk.Frame(self.root, bg="#004d00")
        btn_f.pack(side="bottom", pady=30)
        tk.Button(btn_f, text="ОБ АВТОРЕ", command=lambda: messagebox.showinfo("Автор", "Илья Катаев\nДля 4-х классов"), font=("Arial", 15)).pack(side="left", padx=20)
        tk.Button(btn_f, text="ВЫХОД", command=self.root.destroy, bg="#e74c3c", fg="white", font=("Arial", 15)).pack(side="left")

    def on_boy_click(self, event):
        self.click_count += 1
        if self.click_count >= 5:
            self.click_count = 0
            self.show_dog()

    def show_dog(self):
        self.play_sound("win.wav")
        self.hide_dog()

        dog_img = self.load_image("dog.png", DOG_SIZE)
        if dog_img:
            self.dog_image = dog_img
            self.dog_label = tk.Label(self.root, image=self.dog_image, bg="#004d00")
            self.dog_label.place(x=50, y=50)
            self.dog_label.lift()
            self.dog_label.bind("<Button-1>", self.on_dog_click)
        else:
            self.dog_label = tk.Label(
                self.root,
                text="🐶 СОБАКА!",
                font=("Arial", 40, "bold"),
                bg="#004d00",
                fg="white"
            )
            self.dog_label.place(x=50, y=50)
            self.dog_label.lift()
            self.dog_label.bind("<Button-1>", self.on_dog_click)

        self.root.after(2000, self.hide_dog)

    def on_dog_click(self, event):
        dog1_img = self.load_image("dog1.png", DOG_SIZE)
        if dog1_img:
            self.dog_label.config(image=dog1_img)
            self.dog_label.image = dog1_img
            self.dog_image = dog1_img
        else:
            print("dog1.png не загружен")

    def hide_dog(self):
        if self.dog_label:
            self.dog_label.destroy()
            self.dog_label = None
            self.dog_image = None

    # ---------- Остальные методы (start, game_screen, check, upd_timer, finish, save_result) без изменений ----------
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
                self.play_sound("lose.wav"); self.errors += 1; self.next_q()
        except: pass

    def upd_timer(self):
        if self.game_over: return
        rem = int(self.tm - (time.time() - self.st))
        if rem <= 0: self.finish(False)
        else: self.timer_l.config(text=f"ВРЕМЯ: {rem}"); self.root.after(1000, self.upd_timer)

    def finish(self, success):
        self.game_over = True; self.clear_screen()

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

        tk.Button(self.root, text="💾 СОХРАНИТЬ РЕЗУЛЬТАТ", command=self.save_result, font=("Arial", 20, "bold"), bg="#FF9800", fg="white", padx=30, pady=10).pack(pady=20)
        tk.Button(self.root, text="В МЕНЮ", command=self.main_menu, font=("Arial", 25, "bold"), padx=40, pady=15).pack(pady=20)

    def save_result(self):
        default_name = f"результат_{self.user}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовый файл", "*.txt")],
            initialfile=default_name,
            title="Сохранить результат"
        )
        if not file_path:
            return

        lines = []
        lines.append("=" * 40)
        lines.append("МАТЕМАТИЧЕСКИЙ ТРЕНАЖЕР")
        lines.append("=" * 40)
        lines.append(f"Имя: {self.user}")
        lines.append(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        lines.append(f"Всего примеров: {self.qc}")
        lines.append(f"Решено правильно: {self.solved}")
        lines.append(f"Ошибок: {self.errors}")
        if self.qc > 0:
            percent = round(self.solved / self.qc * 100, 1)
            lines.append(f"Процент правильных: {percent}%")
        if self.solved >= 7:
            lines.append("Оценка: МОЛОДЕЦ! 🎉")
        elif self.solved >= 1:
            lines.append("Оценка: ПОСТАРАЙСЯ ЕЩЕ! 📈")
        else:
            lines.append("Оценка: НУЖНО БОЛЬШЕ ПРАКТИКИ! 📚")
        lines.append("=" * 40)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Сохранено", f"Результат сохранён в файл:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathApp(root)
    root.mainloop()