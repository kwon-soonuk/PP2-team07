# ==========================================================================
# [AI 사용 주석]
#  - AI 종류       : Claude (Anthropic, Claude Opus 5.5)
#  - 사용 목적     : 함수 이름·반환 형식(인터페이스) 설계, 줄 단위 작성 힌트, 완성 후 힌트 주석 정리
#                    → 실행 코드는 힌트를 보고 권순욱이 직접 작성 (힌트 주석은 완성 후 삭제)
#  - 사용 프롬프트 :
#      (2026-11-22) "먼저 팀원들이 해야할 2차 할일을 적어주고
#                    그다음 내가 해야할 1,2차 할일을 하기 위해 뭘 해야하는지 적어줘
#                    풀 코드 해답은 따로 요청하지 않는 이상 알려주지말고"
#      (2026-11-24) "지금 locker 아래 storage.py를 만들었는데 지난번처럼 주석 최소화해줘"
#  - 사용한 사람   : 권순욱
#  - 날짜          : 2026-11-24
# ==========================================================================
# storage.py — 사물함 상태를 CSV(locker/data/lockers.csv, waiting.csv)로 저장하고 불러온다 (2차, 담당: 권순욱)
#   load_manager(numbers) → (manager, 메시지) / save_manager(manager) → (True/False, 메시지)

import csv
import os
from models import LockerManager, EMPTY, PENDING, IN_USE

# 경로는 실행 위치가 아니라 이 파일 위치 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOCKERS_FILE = os.path.join(DATA_DIR, "lockers.csv")
WAITING_FILE = os.path.join(DATA_DIR, "waiting.csv")


VALID_STATUS = (EMPTY, PENDING, IN_USE)


def save_manager(manager):
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)
        with open(LOCKERS_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["number", "status", "student_id"])
            for locker in manager.get_all():
                writer.writerow([locker.number, locker.status, locker.student_id or ""])
        with open(WAITING_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id"])
            for student_id in manager.waiting:
                writer.writerow([student_id])
    except PermissionError:
        return (False, "엑셀에서 파일을 닫고 다시 저장하세요")
    except OSError as e:
        return (False, f"파일 오류: {e}")
    return (True, f"저장 완료: 사물함 {len(manager.lockers)}칸, 대기 {len(manager.waiting)}명")


def load_manager(numbers):
    skipped = []
    lockers_data = []
    try:
        with open(LOCKERS_FILE, encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # 머리글 건너뛰기
            for line_num, row in enumerate(reader, start=2):  # 데이터 줄 번호는 2부터 시작
                if len(row) == 0:
                    continue  # 완전히 빈 줄은 조용히 넘김
                if len(row) != 3 or row[1].strip() not in VALID_STATUS or (row[1].strip() != EMPTY and not row[2].strip()):
                    skipped.append(line_num)
                    continue
                lockers_data.append([row[0].strip(), row[1].strip(), row[2].strip() or None])
    except FileNotFoundError:
        return (LockerManager(numbers), f"처음 실행: 사물함 {len(numbers)}칸 새로 만듦")
    except UnicodeDecodeError:
        return (LockerManager(numbers), "파일을 읽을 수 없어 새로 만듦")

    waiting_data = []
    try:
        with open(WAITING_FILE, encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # 머리글 건너뛰기
            waiting_data = [row[0].strip() for row in reader if row and row[0].strip()]
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        pass
    if not lockers_data:
        return (LockerManager(numbers), f"처음 실행: 사물함 {len(numbers)}칸 새로 만듦")
    manager = LockerManager([locker[0] for locker in lockers_data])
    for locker in lockers_data:
        manager.lockers[locker[0]].status = locker[1]
        manager.lockers[locker[0]].student_id = locker[2]
    manager.waiting.extend(waiting_data)
    message = f"불러옴: 사물함 {len(manager.lockers)}칸, 대기 {len(manager.waiting)}명"
    if skipped:
        message += " / 깨진 줄 건너뜀: " + ", ".join(f"{num}번째 줄" for num in skipped)
    return (manager, message)
