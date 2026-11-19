
import tkinter as tk

def apply_locker():
    result_label.config(text="A-01 신청을 접수했습니다")

window = tk.Tk()
window.title("사물함 신청")
window.geometry("300x200")

button = tk.Button(window, text="A-01 사물함 신청", command=apply_locker)
button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
