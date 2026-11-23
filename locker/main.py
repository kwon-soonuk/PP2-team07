# ==========================================================================
# [AI 사용 주석]
#  - AI 종류       : Claude (Anthropic, Claude Opus 5.5)
#  - 사용 목적     : 파일 구조·함수 이름·연결 방식(인터페이스) 설계, 작성 순서 힌트(주석) 제공
#                    → 실행 코드는 권순욱이 직접 작성
#  - 사용 프롬프트 :
#      (2026-11-22) "먼저 팀원들이 해야할 2차 할일을 적어주고
#                    그다음 내가 해야할 1,2차 할일을 하기 위해 뭘 해야하는지 적어줘
#                    풀 코드 해답은 따로 요청하지 않는 이상 알려주지말고"
#      (2026-11-23) "개인 프로젝트때 한것처럼 순욱(나) 1차 해야할것 시작해야해"
#  - 사용한 사람   : 권순욱
#  - 날짜          : 2026-11-23
#  - AI 추가 사용 기록 (힌트를 더 받거나 정답 줄을 받았으면 한 줄씩 추가):
#      (날짜) / (프롬프트 원문 그대로) / (도움 받은 줄 번호)
# ==========================================================================
#
# main.py — 프로그램 시작점 (1차, 담당: 권순욱)
#
# 이 파일이 하는 일 세 가지
#   ① 창(Tk), manager, 배치도를 "딱 하나씩" 만든다
#   ② 로그인한 계정의 역할에 따라 학생 창 / 관리자 창을 연다
#   ③ 화면들의 on_change 자리에 배치도의 refresh 를 넘겨서,
#      신청·승인이 성공하면 배치도가 다시 그려지게 한다
#
# 쓰는 법: 이 파일 내용을 통째로 locker/main.py 에 붙여넣고,
#          번호 순서(2-1 → 2-8)대로 '# 힌트' 아래에 직접 코드를 쓴다. 다 쓴 곳의 pass 는 지운다.
#          채점: 7team/순욱_1차 에서 python check_su1.py → 미션 2, 3, 4
#          (채점기는 팀원 파일 대신 가짜를 넣어서 검사하므로, 팀원 PR 병합 전에도 검사된다)
#
# 미션 구분
#   미션 2 화면 구성 : 2-1, 2-2, 2-4 ~ 2-8
#   미션 3 로그인 분기: 2-3 의 (a) (b) (c) (d)
#   미션 4 on_change : 2-3 (c) 에서 넘기는 배치도 refresh
# --------------------------------------------------------------------------

import tkinter as tk
from models import LockerManager
from auth import get_role
from student_view import open_student_window
from admin_view import open_admin_window
from locker.locker_map import LockerMap

# 2-1) 팀원 파일과 내 auth.py 에서 가져올 것 5개를 import 한다 (이름은 1차 약속 표 그대로)
#        models       → LockerManager
#        auth         → get_role
#        student_view → open_student_window
#        admin_view   → open_admin_window
#        locker_map   → LockerMap
#      형식: from 파일이름 import 가져올이름   (파일이름에 .py 를 붙이지 않는다!)
#      ※ 직접 python locker/main.py 로 실행해 보는 건 팀원 파일이 병합된 뒤에 가능하다.
#        그 전에는 채점기로만 확인한다 (import 줄을 주석 처리하지 않아도 된다)

LOCKER_NUMBERS = ["A-01", "A-02", "A-03", "A-04", "A-05", "A-06"]
# 2-2) 사물함 번호 6개 "A-01" ~ "A-06" 을 리스트 상수 하나로 만든다 (이름 예: LOCKER_NUMBERS)
#      상수는 대문자 이름. 2차에 CSV 불러오기로 바꿀 때 이 한 줄만 보면 되게 파일 위쪽에 둔다


def login():
    account = entry.get().strip()  
    role = get_role(account)
    if role == "학생":
        open_student_window(root, manager, account, lock_map.refresh)
        result_label.config(text=f"{account} 로그인 (학생)")
    elif role == "관리자":
        open_admin_window(root, manager, lock_map.refresh)
        result_label.config(text=f"{account} 로그인 (관리자)")
    else:
        result_label.config(text="없는 계정입니다")
        entry.delete(0, tk.END)  # 입력칸 비우기
    
    # 2-3) "로그인" 버튼을 누르면 실행되는 함수. 아래 (a) ~ (d) 순서대로.
    #      이 함수는 아래 2-4 ~ 2-7 에서 만드는 root, manager, lock_map, entry, result_label
    #      이름을 그대로 가져다 쓴다 (이름을 바꾸면 여기도 같이 바꾸기)
    #
    #   (a) entry 에 적힌 글자를 꺼내서 앞뒤 공백을 지운 것을 account 에 담는다
    #       - Entry 에서 글자를 꺼내는 메서드 (PE 9장)
    #       - 문자열 앞뒤 공백을 지우는 문자열 메서드
    #       - 공백을 안 지우면 " student1" 처럼 입력됐을 때 없는 계정이 된다
    #
    #   (b) get_role 에 account 를 넣어서 role 을 받는다
    #
    #   (c) role 에 따라 세 갈래 (if / elif / else)
    #       - "학생"   → open_student_window 에 (창, manager, 학번, 배치도의 refresh) 네 개를 넘긴다
    #       - "관리자" → open_admin_window 에 (창, manager, 배치도의 refresh) 세 개를 넘긴다
    #       - 그 외(None) → result_label 글자를 "없는 계정입니다" 같은 안내로 바꾼다
    #       ※ 배치도의 refresh 를 넘길 때 뒤에 괄호를 붙이지 않는다.
    #         괄호를 붙이면 지금 '한 번 부르고' 그 결과(None)를 넘기는 것이 된다.
    #         우리는 '나중에 부를 함수 자체'를 넘겨야 한다 (PP 6장, 버튼 command= 와 같은 원리)
    #
    #   (d) 학생/관리자일 때도 result_label 에 "student1 로그인 (학생)" 같은 안내를 띄운다
    #       - Label 글자를 바꾸는 메서드 (PE 9장)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("7팀 사물함 관리")
    manager = LockerManager(LOCKER_NUMBERS)
    lock_map = LockerMap(root, manager)
    
    # 2-4) 메인 창 root 를 만들고 제목을 붙인다 (예: "7팀 사물함 관리")
    #      Tk() 는 프로그램 전체에서 여기 한 번뿐이다. 학생·관리자 창은 팀원이 Toplevel 로 만든다

    # 2-5) 2-2 의 번호 리스트로 LockerManager 를 "하나만" 만들어 manager 에 담는다
    #      → 학생 창, 관리자 창, 배치도가 모두 이 객체 하나를 같이 쓴다 (PE 8장 객체)
    #      화면마다 따로 만들면 학생이 신청해도 관리자 창·배치도에 안 보인다

    # 2-6) LockerMap 에 (root, manager) 를 넘겨 배치도를 만들고, 변수 lock_map 에 담는다
    #      login 함수가 lock_map 의 refresh 를 화면들에 넘겨야 하므로 변수에 꼭 담아 둔다

    account_label = tk.Label(root, text="계정")
    account_label.pack()
    entry = tk.Entry(root)
    entry.pack()
    login_button = tk.Button(root, text="로그인", command=login)
    login_button.pack()
    result_label = tk.Label(root, text="")
    result_label.pack()

    # 2-7) 로그인 줄을 만든다. pack 으로 위에서 아래로 쌓으면 충분하다
    #      - "계정" 안내 Label
    #      - 입력칸 Entry → 변수 이름 entry
    #      - "로그인" Button → command 자리에 login (괄호 없이!)
    #      - 결과 안내 Label (처음엔 빈 글자) → 변수 이름 result_label
    #      ※ 버튼 글자에 '로그인' 이 들어가야 채점기가 찾는다

    # 2-8) 맨 마지막 줄: root 의 mainloop() 를 부른다
    root.mainloop()


# ==========================================================================
# 교수님 질문 대비 (답은 직접 정리해 보기 — 발표 때 자기 코드 설명용)
#   Q1. manager 를 학생 창·관리자 창에서 각각 새로 만들면 어떤 일이 생기나?
#   Q2. command=login 과 command=login() 은 무엇이 다른가?
#   Q3. on_change 자리에 lock_map.refresh 를 넘기는 이유는?
#       학생 창 파일이 locker_map.py 를 직접 import 하지 않아도 되는 이유와 연결해서
#   Q4. Tk() 를 두 번 만들면 어떻게 되나? 학생·관리자 창이 Toplevel 인 이유는?
#   Q5. strip() 을 빼면 어떤 입력에서 로그인이 실패하나?
#   Q6. login 함수 안에서 root, manager, entry 를 어떻게 쓸 수 있나? (전역 변수)
#   Q7. if __name__ == "__main__": 은 무슨 뜻인가? 이 파일에서는 왜 썼나?
#   Q8. 2차에 CSV 저장을 붙일 때 이 파일에서 무엇만 바꾸면 되나? (2-2, 2-5, on_change)
#   Q9. 사람마다 브랜치를 나누고 PR 로 합치는 이유는? (형상관리 질문 대비)
#   Q10. .gitignore 에 __pycache__/ 를 넣는 이유는?
# ==========================================================================
