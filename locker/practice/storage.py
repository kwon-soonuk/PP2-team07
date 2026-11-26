import csv
import os

try:
    from .models import LockerManager
except ImportError:  # Also allow running/importing storage.py from inside locker/.
    from models import LockerManager


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LOCKERS_FILE = os.path.join(DATA_DIR, "lockers.csv")
WAITING_FILE = os.path.join(DATA_DIR, "waiting.csv")
LOCKER_FIELDS = ("number", "status", "student_id")


def _read_lockers(path, messages):
    lockers = {}
    valid_statuses = {"빈자리", "신청중", "사용중"}
    try:
        with open(path, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header != list(LOCKER_FIELDS):
                messages.append("lockers.csv 헤더가 올바르지 않습니다.")
                return lockers
            for line_number, row in enumerate(reader, start=2):
                if len(row) != 3:
                    messages.append(f"lockers.csv {line_number}행을 건너뜁니다: 칸 수가 맞지 않습니다.")
                    continue
                number, status, student_id = row
                if not number or status not in valid_statuses:
                    messages.append(f"lockers.csv {line_number}행을 건너뜁니다: 번호 또는 상태 값이 올바르지 않습니다.")
                    continue
                if number in lockers:
                    messages.append(f"lockers.csv {line_number}행을 건너뜁니다: 중복 번호입니다.")
                    continue
                if status == "빈자리":
                    student_id = None
                elif not student_id:
                    messages.append(f"lockers.csv {line_number}행을 건너뜁니다: 학생 번호가 없습니다.")
                    continue
                lockers[number] = {
                    "status": status,
                    "student_id": student_id or None,
                    "door_open": False,
                }
    except FileNotFoundError:
        raise
    except (OSError, csv.Error) as error:
        messages.append(f"lockers.csv를 읽지 못했습니다: {error}")
    return lockers


def _read_waiting(path, messages):
    waiting = []
    try:
        with open(path, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header != ["student_id"]:
                messages.append("waiting.csv 헤더가 올바르지 않습니다.")
                return waiting
            for line_number, row in enumerate(reader, start=2):
                if len(row) != 1 or not row[0]:
                    messages.append(f"waiting.csv {line_number}행을 건너뜁니다: 학생 번호가 없습니다.")
                    continue
                waiting.append(row[0])
    except FileNotFoundError:
        pass
    except (OSError, csv.Error) as error:
        messages.append(f"waiting.csv를 읽지 못했습니다: {error}")
    return waiting


def load_manager(numbers, data_dir=None):
    """Load a manager from CSV, or initialize it from numbers if absent."""
    folder = data_dir or DATA_DIR
    lockers_path = os.path.join(folder, "lockers.csv")
    waiting_path = os.path.join(folder, "waiting.csv")
    messages = []
    try:
        lockers = _read_lockers(lockers_path, messages)
    except FileNotFoundError:
        manager = LockerManager(numbers)
        messages.append("처음 실행: 새로 만듦")
        return manager, messages

    manager = LockerManager([])
    manager.lockers = lockers
    manager.waiting = _read_waiting(waiting_path, messages)
    return manager, messages


def save_manager(manager, data_dir=None):
    """Save lockers and the ordered waiting list as UTF-8 CSV files."""
    folder = data_dir or DATA_DIR
    os.makedirs(folder, exist_ok=True)
    lockers_path = os.path.join(folder, "lockers.csv")
    waiting_path = os.path.join(folder, "waiting.csv")

    with open(lockers_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(LOCKER_FIELDS)
        for number, locker in manager.lockers.items():
            writer.writerow((number, locker["status"], locker["student_id"] or ""))

    with open(waiting_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(("student_id",))
        for student_id in manager.waiting:
            writer.writerow((student_id,))