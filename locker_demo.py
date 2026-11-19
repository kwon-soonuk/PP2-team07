lockers  = [
    {"number": "A-01", "student_id": None, "door_open": False},
    {"number": "A-02", "student_id": "student1", "door_open": False},
    {"number": "A-03", "student_id": None, "door_open": False},
]

class Locker:
    def __init__(self, number):
        self.number = number
        self.student_id = None

    def assign(self, student_id):
        if self.student_id is None:
            self.student_id = student_id
        else:
            print("이미 배정된 사물함입니다")

    def return_locker(self):
        self.student_id = None


locker = Locker("A-01")
locker.assign("student1")
locker.assign("student2")
locker.return_locker()