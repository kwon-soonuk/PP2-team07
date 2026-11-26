import random


class LockerManager:
    def __init__(self, numbers):
        self.lockers = {
            number: {"status": "빈자리", "student_id": None, "door_open": False}
            for number in numbers
        }
        self.waiting = []

    def _has_application(self, student_id):
        """Return whether this student already has a locker or is waiting."""
        if any(locker["student_id"] == student_id for locker in self.lockers.values()):
            return True
        return student_id in self.waiting

    def apply(self, number, student_id):
        if self._has_application(student_id):
            return False, "이미 신청 중이거나 사용 중이거나 대기 중입니다."
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."

        locker = self.lockers[number]
        if locker["status"] != "빈자리":
            return False, "빈자리가 아닙니다."

        locker["status"] = "신청중"
        locker["student_id"] = student_id
        locker["door_open"] = False
        return True, f"{number} 사물함 신청이 완료되었습니다."

    def apply_random(self, student_id):
        if self._has_application(student_id):
            return False, "이미 신청 중이거나 사용 중이거나 대기 중입니다."

        available = [
            number
            for number, locker in self.lockers.items()
            if locker["status"] == "빈자리"
        ]
        if not available:
            self.waiting.append(student_id)
            return True, f"대기 {len(self.waiting)}번째로 등록되었습니다."

        number = random.choice(available)
        return self.apply(number, student_id)

    def approve(self, number):
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."
        locker = self.lockers[number]
        if locker["status"] != "신청중":
            return False, "신청중인 사물함이 아닙니다."
        locker["status"] = "사용중"
        return True, f"{number} 사물함 신청을 승인했습니다."

    def return_locker(self, number):
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."
        locker = self.lockers[number]
        if locker["status"] != "사용중":
            return False, "사용중인 사물함만 반납할 수 있습니다."

        locker["status"] = "빈자리"
        locker["student_id"] = None
        locker["door_open"] = False
        return True, f"{number} 사물함을 반납했습니다."

    def assign_from_waiting(self, number):
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."
        locker = self.lockers[number]
        if locker["status"] != "빈자리":
            return False, "빈자리가 아닙니다."
        if not self.waiting:
            return False, "대기자가 없습니다."

        locker["student_id"] = self.waiting.pop(0)
        locker["status"] = "사용중"
        locker["door_open"] = False
        return True, f"대기자에게 {number} 사물함을 배정했습니다."

    def get_waiting(self):
        return self.waiting.copy()

    def get_student_status(self, student_id):
        for number, locker in self.lockers.items():
            if locker["student_id"] == student_id:
                return locker["status"], number
        try:
            return "대기", self.waiting.index(student_id) + 1
        except ValueError:
            return None