import requests
import json

# ===== CẤU HÌNH KẾT NỐI =====
ODOO_URL = "http://localhost:8069"  # Đổi thành URL Odoo của bạn
DB_NAME = "learning_odoo"  # Tên database
USERNAME = "teacher"  # Tài khoản giáo viên
PASSWORD = "1111"  # Mật khẩu


# ===== 1. ĐĂNG NHẬP LẤY SESSION =====
def odoo_login():
    login_url = f"{ODOO_URL}/web/session/authenticate"
    headers = {'Content-Type': 'application/json'}
    data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'login': USERNAME,
            'password': PASSWORD,
            'db': DB_NAME
        }
    }
    response = requests.post(login_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200 and response.json().get('result'):
        session_id = response.cookies.get('session_id')
        return session_id
    else:
        print("❗ Đăng nhập thất bại! Kiểm tra lại thông tin.")
        return None


# ===== 2. LẤY DANH SÁCH SINH VIÊN =====
def get_students(session_id, class_filter=None):
    api_url = f"{ODOO_URL}/api/students"
    if class_filter:
        api_url += f"?class={class_filter}"

    cookies = {'session_id': session_id}
    response = requests.get(api_url, cookies=cookies)

    if response.status_code == 200:
        students = response.json()
        print("✅ Danh sách sinh viên:")
        for student in students.get('students', []):
            print(f"  - ID: {student['id']}, Tên: {student['name']}, Tuổi: {student['age']}, Lớp: {student['class']}")
    else:
        print(f"❗ Lỗi: {response.status_code} - {response.text}")


# ===== 3. THÊM SINH VIÊN MỚI =====
def create_student(session_id, name, age, student_class, status=0):
    api_url = f"{ODOO_URL}/api/students"
    cookies = {'session_id': session_id}
    headers = {'Content-Type': 'application/json'}

    payload = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'name': name,
            'age': age,
            'student_class': student_class,
            'status': status
        }
    }

    response = requests.post(
        api_url,
        cookies=cookies,
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        result = response.json()
        if result.get('result') and result['result'].get('success'):
            print(f"✅ Tạo sinh viên thành công! ID: {result['result']['student_id']}")
        else:
            print(f"❗ Lỗi: {result.get('result', {}).get('error')}")
    else:
        print(f"❗ Lỗi HTTP: {response.status_code} - {response.text}")

# ===== 4. XEM CHI TIẾT SINH VIÊN =====
def get_student_detail(session_id, student_id):
    api_url = f"{ODOO_URL}/api/students/{student_id}"
    cookies = {'session_id': session_id}
    response = requests.get(api_url, cookies=cookies)

    if response.status_code == 200:
        student = response.json()
        print(f"✅ Thông tin sinh viên ID {student_id}:")
        print(f"  - Tên: {student['name']}")
        print(f"  - Tuổi: {student['age']}")
        print(f"  - Lớp: {student['class']}")
    else:
        print(f"❗ Lỗi: {response.status_code} - {response.text}")


# ===== CHẠY CHƯƠNG TRÌNH CHÍNH =====
if __name__ == "__main__":
    # Bước 1: Đăng nhập lấy session
    session_id = odoo_login()
    if not session_id:
        exit()

    # Bước 2: Lấy danh sách sinh viên (có thể lọc theo lớp)
    get_students(session_id, class_filter="10A")  # Lọc sinh viên lớp 10A

    # Bước 3: Thêm sinh viên mới (chỉ giáo viên mới có quyền)
    create_student(
        session_id,
        name="Nguyễn Văn C",
        age=17,
        student_class="10A",
        status= "Đang học"
    )

    # Bước 4: Xem chi tiết sinh viên (ví dụ ID=1)
    get_student_detail(session_id, student_id=1)