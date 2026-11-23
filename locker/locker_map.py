import tkinter as tk
from models import EMPTY, PENDING, IN_USE


# [AI 사용]
# AI: Claude opus 5.5
# 목적: 배치도 화면 작성 — COLS·STATUS_COLOR 상수와 LockerMap 클래스(__init__ 칸 배치, refresh 상태별 글자·색·빈자리 줄 갱신)
# 프롬프트: 입력한 문장 없음. 팀장이 보낸 할 일 문서 파일("7팀 사물함 관리 프로그램 — 조하늘 할 일 (1차·2차)")을 그대로 첨부함.
#   결과에 쓰인 부분 중 "1차 할 일" 절 원문:
# `class LockerMap`의 `__init__(self, parent, manager)`: `self.frame = tk.Frame(parent)`를 만들고 `pack()`. 사물함마다 Label 하나를 3칸씩 `grid`로 놓고 `self.labels = {번호: Label}` 딕셔너리에 저장. 아래에 "빈자리 N / 전체 M칸" Label. 마지막에 `self.refresh()`
# `refresh(self)`: `manager.get_all()`을 돌면서 각 Label 글자를 "A-01\n빈자리"처럼 바꾸고, 배경색을 상태별로 바꾸고, `count_empty()`로 빈자리 줄을 갱신. `practice/locker_view_demo.py`에서 했던 빈자리 세기를 화면으로 옮기는 일이다
# 색은 `bg=` 옵션으로: 빈자리 `lightgreen`, 신청중 `khaki`, 사용중 `salmon`
# 파일 맨 위 AI 주석 한 줄, AI 도움 받은 부분마다 AI 주석
#   ("내가 만드는 것", "내가 가져다 쓰는 것" 절과 단독 테스트 예도 함께 참고됨.)
# 사용자: 조하늘 / 날짜: 2026-11-23
COLS = 3  # 한 줄에 놓을 칸 수

# 상태 → 배경색. 상태 문자열은 models.py 상수를 쓰고 직접 치지 않는다.
STATUS_COLOR = {
    EMPTY: "lightgreen",
    PENDING: "khaki",
    IN_USE: "salmon",
}


class LockerMap:
    def __init__(self, parent, manager):
        self.manager = manager            # refresh()에서 다시 쓰려고 저장
        self.frame = tk.Frame(parent)     # 배치도 전체를 담는 틀
        self.frame.pack(padx=10, pady=10)

        self.labels = {}                  # {"A-01": Label, ...}
        lockers = manager.get_all()
        for i, locker in enumerate(lockers):   # i = 0, 1, 2, ...
            row = i // COLS                    # 0,1,2 → 0줄 / 3,4,5 → 1줄
            col = i % COLS                     # 0,1,2,0,1,2 ...
            label = tk.Label(self.frame, width=10, height=3,
                             relief="ridge", borderwidth=2)
            label.grid(row=row, column=col, padx=3, pady=3)
            self.labels[locker.number] = label

        # 칸들 바로 아래 줄에 "빈자리 N / 전체 M칸"
        last_row = (len(lockers) + COLS - 1) // COLS   # 칸이 차지한 줄 수 (올림)
        self.summary = tk.Label(self.frame)
        self.summary.grid(row=last_row, column=0, columnspan=COLS, pady=(8, 0))

        self.refresh()                    # 처음 화면도 refresh로 채운다

    def refresh(self):
        # 몇 번을 불러도 manager의 지금 상태 그대로 다시 칠한다 (값은 읽기만 함)
        lockers = self.manager.get_all()
        for locker in lockers:
            label = self.labels[locker.number]
            color = STATUS_COLOR.get(locker.status, "lightgray")  # 모르는 상태면 회색
            label.config(text=f"{locker.number}\n{locker.status}", bg=color)

        empty = self.manager.count_empty()
        self.summary.config(text=f"빈자리 {empty} / 전체 {len(lockers)}칸")


if __name__ == "__main__":   # 이 파일만 실행할 때만 동작
    from models import LockerManager
    root = tk.Tk()
    m = LockerManager(["A-01", "A-02", "A-03", "A-04", "A-05", "A-06"])
    m.apply("A-02", "student1")
    lock_map = LockerMap(root, m)

    def approve_test():
        m.approve("A-02")
        lock_map.refresh()

    tk.Button(root, text="A-02 승인 테스트", command=approve_test).pack()
    root.mainloop()