# [AI 사용] 클래스·함수 이름과 반환 형식(인터페이스)은 Claude로 설계 (권순욱, 2026-11-22)
import tkinter as tk
from tkinter import ttk
from models import IN_USE


# [AI 사용]
# AI: ChatGPT
# 목적: 정혜승 담당 관리자 화면의 승인·반납·대기자 배정 기능 구현
# 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
# 사용자: 정혜승 / 날짜: 2026-11-25
def open_admin_window(root, manager, on_change):
    """관리자용 승인 대기·사용중·대기자 관리 창을 연다."""
    window = tk.Toplevel(root)
    window.title("관리자 사물함 관리")
    window.geometry("760x650")

    message_label = tk.Label(window, text="관리자 관리 화면",
                             font=("맑은 고딕", 11, "bold"))
    message_label.pack(pady=8)

    panels = tk.Frame(window)
    panels.pack(fill="both", expand=True, padx=10, pady=5)

    pending_frame = tk.LabelFrame(panels, text="① 승인 대기")
    pending_frame.pack(fill="both", expand=True, padx=5, pady=5)
    pending_list = tk.Listbox(pending_frame, height=6, exportselection=False)
    pending_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    pending_scroll = tk.Scrollbar(pending_frame, command=pending_list.yview)
    pending_scroll.pack(side="right", fill="y")
    pending_list.config(yscrollcommand=pending_scroll.set)

    pending_buttons = tk.Frame(pending_frame)
    pending_buttons.pack(fill="x", padx=5, pady=5)

    used_frame = tk.LabelFrame(panels, text="② 사용중 목록")
    used_frame.pack(fill="both", expand=True, padx=5, pady=5)
    used_list = tk.Listbox(used_frame, height=6, exportselection=False)
    used_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    used_scroll = tk.Scrollbar(used_frame, command=used_list.yview)
    used_scroll.pack(side="right", fill="y")
    used_list.config(yscrollcommand=used_scroll.set)

    waiting_frame = tk.LabelFrame(panels, text="③ 대기자 목록 및 배정")
    waiting_frame.pack(fill="both", expand=True, padx=5, pady=5)
    waiting_list = tk.Listbox(waiting_frame, height=6, exportselection=False)
    waiting_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    waiting_scroll = tk.Scrollbar(waiting_frame, command=waiting_list.yview)
    waiting_scroll.pack(side="right", fill="y")
    waiting_list.config(yscrollcommand=waiting_scroll.set)

    assign_controls = tk.Frame(waiting_frame)
    assign_controls.pack(fill="x", padx=5, pady=5)
    tk.Label(assign_controls, text="빈 사물함 번호").pack()
    locker_entry = tk.Entry(assign_controls, width=15)
    locker_entry.pack(pady=3)

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 1·2차 관리자 화면의 세 목록을 최신 데이터로 다시 표시하기
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def refresh_lists():
        pending_list.delete(0, tk.END)
        for locker in manager.get_pending():
            pending_list.insert(
                tk.END, f"{locker.number} / {locker.student_id}"
            )

        used_list.delete(0, tk.END)
        for locker in manager.get_all():
            if locker.status == IN_USE:
                used_list.insert(
                    tk.END, f"{locker.number} / {locker.student_id}"
                )

        waiting_list.delete(0, tk.END)
        for index, student_id in enumerate(manager.get_waiting(), start=1):
            waiting_list.insert(tk.END, f"{index}. {student_id}")

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 선택한 승인 대기 사물함을 승인 처리하기
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def approve_selected():
        selection = pending_list.curselection()
        if not selection:
            message_label.config(text="먼저 승인 대기 목록에서 항목을 고르세요.")
            return

        selected_text = pending_list.get(selection[0])
        number = selected_text.split(" / ", 1)[0]
        ok, msg = manager.approve(number)
        message_label.config(text=msg)
        refresh_lists()
        if ok:
            on_change()

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 사용중 목록에서 선택한 사물함을 반납 처리하기
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def return_selected():
        selection = used_list.curselection()
        if not selection:
            message_label.config(text="먼저 사용중 목록에서 항목을 고르세요.")
            return

        selected_text = used_list.get(selection[0])
        number = selected_text.split(" / ", 1)[0]
        ok, msg = manager.return_locker(number)
        message_label.config(text=msg)
        refresh_lists()
        if ok:
            on_change()

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 입력한 빈 사물함에 대기자 순서대로 배정하기
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def assign_waiting_student():
        number = locker_entry.get().strip().upper()
        if not number:
            message_label.config(text="배정할 사물함 번호를 입력하세요.")
            return

        ok, msg = manager.assign_from_waiting(number)
        message_label.config(text=msg)
        refresh_lists()
        if ok:
            on_change()

    tk.Button(pending_buttons, text="승인", command=approve_selected).pack(
        side="left", padx=4
    )
    tk.Button(pending_buttons, text="새로고침", command=refresh_lists).pack(
        side="left", padx=4
    )
    tk.Button(used_frame, text="반납 처리", command=return_selected).pack(
        side="bottom", pady=5
    )
    tk.Button(assign_controls, text="대기자 배정",
              command=assign_waiting_student).pack(pady=4)
    tk.Button(window, text="전체 새로고침", command=refresh_lists).pack(pady=8)

    refresh_lists()
    return window


if __name__ == "__main__":
    from models import LockerManager

    root = tk.Tk()
    root.title("관리자 화면 단독 테스트")
    manager = LockerManager(["A-01", "A-02", "A-03"])
    manager.apply("A-01", "student1")
    manager.apply_random("student2")
    open_admin_window(root, manager, lambda: print("변경됨"))
    root.mainloop()
