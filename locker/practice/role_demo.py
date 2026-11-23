accounts = {"student1": "학생", "admin1": "관리자"}
account = input("계정명을 입력하세요: ")
if account not in accounts:
    print("계정이 존재하지 않습니다.")

