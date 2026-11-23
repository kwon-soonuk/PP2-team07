lockers = [
    {"number": "A-01", "student_id": None, "door_open": False},
    {"number": "A-02", "student_id": "student1", "door_open": False},
    {"number": "A-03", "student_id": None, "door_open": False},
]

empty_count = 0

for locker in lockers:
    if locker["student_id"] is None:
        print(locker["number"], "빈자리")
        empty_count += 1
    else:
        print(locker["number"], "사용 중")

print("전체:", len(lockers), "칸")
print("빈자리:", empty_count, "칸")