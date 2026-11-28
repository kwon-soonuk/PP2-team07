# ==========================================================================
# [AI 사용 주석]
#  - 원래 작성 : 김준서 (2026-11-25, PR #31 — locker/practice/models.py)
#      김준서 AI 사용 기록: (준서에게 받아서 적기 — AI 종류 / 목적 / 프롬프트 원문 / 날짜. 안 썼으면 "없음")
#  - 1·2차 약속에 맞게 수정 : 권순욱
#      ① AI 종류  : Claude (Anthropic, Claude Opus 5.5)
#         목적     : 약속과 다른 곳 찾기, 고칠 순서·줄별 힌트(models_guide.py) 제공, 이 AI 주석 정리
#         프롬프트 : (2026-11-28) "먼저 지금 팀원이 깃허브에 뭘 올렸더라고 확인하고 내가 뭘해야할지 알려줘"
#                    (2026-11-28) "줄별 힌트 가이드를 해주고 task.md 하나 만들어서 문제 작게 분해하고
#                                  가이드와 설명을 남겨줘 나중에 이파일 지우자"
#      사용자 : 권순욱 / 날짜 : 2026-11-28
#  - AI 추가 사용 기록 (힌트를 더 받거나 정답 줄을 받았으면 한 줄씩):
#      (날짜) / (프롬프트 원문 그대로) / (도움 받은 줄 번호)
# ==========================================================================
# models.py — 사물함 데이터와 규칙 (Locker = 한 칸, LockerManager = 전체)
#   모든 메서드는 print 없이 (True/False, 메시지) 또는 값만 돌려준다
import random


EMPTY = "빈자리"
PENDING = "신청중"
IN_USE = "사용중"


class Locker:
    def __init__(self, number):
        self.number = number
        self.status = EMPTY
        self.student_id = None
        self.door_open = False


class LockerManager:
    def __init__(self, numbers):
        self.lockers = {number: Locker(number) for number in numbers}
        self.waiting = []

    def _has_application(self, student_id):
        """Return whether this student already has a locker or is waiting."""
        if any(locker.student_id == student_id for locker in self.lockers.values()):
            return True
        return student_id in self.waiting

    def apply(self, number, student_id):
        if self._has_application(student_id):
            return False, "이미 신청 중이거나 사용 중이거나 대기 중입니다."
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."

        locker = self.lockers[number]
        if locker.status != EMPTY:
            return False, "빈자리가 아닙니다."

        locker.status = PENDING
        locker.student_id = student_id
        locker.door_open = False
        return True, f"{number} 사물함 신청이 완료되었습니다."

    def apply_random(self, student_id):
        if self._has_application(student_id):
            return False, "이미 신청 중이거나 사용 중이거나 대기 중입니다."

        available = [
            number
            for number, locker in self.lockers.items()
            if locker.status == EMPTY
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
        if locker.status != PENDING:
            return False, "신청중인 사물함이 아닙니다."
        locker.status = IN_USE
        return True, f"{number} 사물함 신청을 승인했습니다."

    def get_all(self):
        return list(self.lockers.values())

    def get_pending(self):
        return [locker for locker in self.lockers.values() if locker.status == PENDING]

    def count_empty(self):
        return sum(1 for locker in self.lockers.values() if locker.status == EMPTY)

    def return_locker(self, number):
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."
        locker = self.lockers[number]
        if locker.status != IN_USE:
            return False, "사용중인 사물함만 반납할 수 있습니다."

        locker.status = EMPTY
        locker.student_id = None
        locker.door_open = False
        return True, f"{number} 사물함을 반납했습니다."

    def assign_from_waiting(self, number):
        if number not in self.lockers:
            return False, "존재하지 않는 사물함 번호입니다."
        locker = self.lockers[number]
        if locker.status != EMPTY:
            return False, "빈자리가 아닙니다."
        if not self.waiting:
            return False, "대기자가 없습니다."

        locker.student_id = self.waiting.pop(0)
        locker.status = IN_USE
        locker.door_open = False
        return True, f"대기자에게 {number} 사물함을 배정했습니다."

    def get_waiting(self):
        return self.waiting.copy()

    def get_student_status(self, student_id):
        for number, locker in self.lockers.items():
            if locker.student_id == student_id:
                return locker.status, number
        try:
            return "대기", self.waiting.index(student_id) + 1
        except ValueError:
            return (None, None)