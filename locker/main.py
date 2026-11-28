# ==========================================================================
# [AI 사용 주석]
#  - AI 종류       : Claude (Anthropic, Claude Opus 5.5)
#  - 사용 목적     : 1차 — 파일 구조·함수 이름·연결 방식 설계, 줄별 작성 힌트 (실행 코드는 권순욱이 직접 작성)
#                    2차 — 저장 연결 코드 작성 (Claude 작성: storage import, on_change 함수,
#                          login 안 on_change 두 곳, load_manager 줄, result_label 처음 글자)
#                    정리 — 완성 후 힌트·연습용 주석 삭제
#  - 사용 프롬프트 :
#      (2026-11-22) "먼저 팀원들이 해야할 2차 할일을 적어주고
#                    그다음 내가 해야할 1,2차 할일을 하기 위해 뭘 해야하는지 적어줘
#                    풀 코드 해답은 따로 요청하지 않는 이상 알려주지말고"
#      (2026-11-23) "개인 프로젝트때 한것처럼 순욱(나) 1차 해야할것 시작해야해"
#  - 사용한 사람   : 권순욱
# ==========================================================================
# main.py — 프로그램 시작점 (담당: 권순욱)
#   창·manager·배치도를 하나씩 만들고, 로그인한 역할에 따라 학생 창 / 관리자 창을 연다.
#   화면에서 무언가 바뀌면 on_change 로 배치도를 다시 그리고 CSV 에 저장한다.

import tkinter as tk
from storage import load_manager, save_manager
from auth import get_role
from student_view import open_student_window
from admin_view import open_admin_window
from locker_map import LockerMap


LOCKER_NUMBERS = ["A-01", "A-02", "A-03", "A-04", "A-05", "A-06"]


# [AI 사용] Claude (Claude Opus 5.5) 작성 — 2차: 화면에서 신청·승인·반납이 성공하면 배치도 갱신 + CSV 저장

def on_change():
    lock_map.refresh()
    ok, message = save_manager(manager)
    if not ok:
        result_label.config(text=message)  # 예: 엑셀이 lockers.csv 를 열고 있을 때


def login():
    account = entry.get().strip()  
    role = get_role(account)
    if role == "학생":
        open_student_window(root, manager, account, on_change)
        result_label.config(text=f"{account} 로그인 (학생)")
    elif role == "관리자":
        open_admin_window(root, manager, on_change)
        result_label.config(text=f"{account} 로그인 (관리자)")
    else:
        result_label.config(text="없는 계정입니다")
        entry.delete(0, tk.END)  # 입력칸 비우기


if __name__ == "__main__":
    root = tk.Tk()
    root.title("7팀 사물함 관리")
    manager, load_message = load_manager(LOCKER_NUMBERS)  # CSV 가 있으면 불러오고, 없으면 새로 만든다
    lock_map = LockerMap(root, manager)

    account_label = tk.Label(root, text="계정")
    account_label.pack()
    entry = tk.Entry(root)
    entry.pack()
    login_button = tk.Button(root, text="로그인", command=login)
    login_button.pack()
    result_label = tk.Label(root, text=load_message)  # 불러오기 결과를 처음에 보여 준다
    result_label.pack()

    root.mainloop()
