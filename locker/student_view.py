# [AI 사용] 클래스·함수 이름과 반환 형식(인터페이스)은 Claude로 설계 (권순욱, 2026-11-22)
import tkinter as tk
from models import EMPTY, PENDING, IN_USE


# [AI 사용]
# AI: ChatGPT
# 목적: 정혜승 담당 학생 화면의 1차 학생 신청 기능과 2차 랜덤 신청·내 상태 확인 기능 구현
# 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
# 사용자: 정혜승 / 날짜: 2026-11-25
def open_student_window(root, manager, student_id, on_change):
    """학생 사물함 신청 및 현재 상태를 보여주는 창을 연다."""
    window = tk.Toplevel(root)
    window.title("학생 사물함 관리")
    window.geometry("420x330")

    tk.Label(window, text=f"학생 학번: {student_id}",
             font=("맑은 고딕", 11)).pack(pady=(12, 5))

    status_label = tk.Label(window, text="내 상태: 신청 없음",
                            font=("맑은 고딕", 11, "bold"))
    status_label.pack(pady=8)

    message_label = tk.Label(window, text="사물함을 신청하거나 상태를 새로고침하세요.",
                             wraplength=370)
    message_label.pack(pady=6)

    number_entry = tk.Entry(window, width=18)
    number_entry.pack(pady=5)
    number_entry.insert(0, "A-01")

    # [AI 사용]
    # AI: ChatGPT
    # 목적: get_student_status 반환값을 화면에 표시할 문구로 바꾸기
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def refresh_status():
        status, detail = manager.get_student_status(student_id)
        if status == IN_USE:
            text = f"{detail} 사용중"
        elif status == PENDING:
            text = f"{detail} 신청중"
        elif status == "대기":
            text = f"대기 {detail}번째"
        else:
            text = "신청 없음"
        status_label.config(text=f"내 상태: {text}")

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 지정 사물함 신청 버튼 구현
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def apply_locker():
        number = number_entry.get().strip().upper()
        if not number:
            message_label.config(text="사물함 번호를 입력하세요.")
            return

        ok, msg = manager.apply(number, student_id)
        message_label.config(text=msg)
        if ok:
            on_change()
        refresh_status()

    # [AI 사용]
    # AI: ChatGPT
    # 목적: 2차 랜덤 신청 버튼 구현
    # 프롬프트: "싹 돌려봐 정혜승이 해야할 일의 1,2,3차 조건에 맞춰서"
    # 사용자: 정혜승 / 날짜: 2026-11-25
    def apply_random_locker():
        ok, msg = manager.apply_random(student_id)
        message_label.config(text=msg)
        if ok:
            on_change()
        refresh_status()

    tk.Label(window, text="신청할 사물함 번호").pack(pady=(8, 0))
    tk.Button(window, text="신청", width=20, command=apply_locker).pack(pady=4)
    tk.Button(window, text="랜덤 신청", width=20,
              command=apply_random_locker).pack(pady=4)
    tk.Button(window, text="새로고침", width=20,
              command=refresh_status).pack(pady=4)

    refresh_status()
    return window


if __name__ == "__main__":
    from models import LockerManager

    root = tk.Tk()
    root.title("학생 화면 단독 테스트")
    manager = LockerManager(["A-01", "A-02", "A-03"])
    open_student_window(root, manager, "student1",
                        lambda: print("변경됨"))
    root.mainloop()
