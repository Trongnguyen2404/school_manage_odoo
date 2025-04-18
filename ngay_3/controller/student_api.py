from odoo import http
from odoo.http import request, Response
import json


class StudentAPI(http.Controller):

    # Helper method để kiểm tra quyền
    def _check_teacher_permission(self):
        if not request.env.user.has_group('ngay_3.group_teacher'):
            return {
                'error': 'Chỉ giáo viên mới có quyền thực hiện thao tác này',
                'status': 403
            }
        return None

    # API lấy danh sách sinh viên
    @http.route('/api/students', auth='user', methods=['GET'], type='http')
    def get_students(self, **kwargs):
        try:
            # Kiểm tra quyền - cho phép cả user thường và giáo viên
            if not request.env.user.has_group('base.group_user'):
                return Response(
                    json.dumps({'error': 'Yêu cầu đăng nhập'}),
                    content_type='application/json;charset=utf-8',
                    status=401
                )

            # Lấy tham số từ URL (nếu có)
            class_filter = kwargs.get('class')

            # Xây dựng domain tìm kiếm
            domain = []
            if class_filter:
                domain.append(('student_class', '=', class_filter))

            # Giáo viên chỉ xem được sinh viên trong lớp được phân công
            if request.env.user.has_group('ngay_3.group_teacher'):
                teacher_classes = request.env.user.x_allowed_class.split(
                    ',') if request.env.user.x_allowed_class else []
                if teacher_classes:
                    domain.append(('student_class', 'in', teacher_classes))

            # Lấy danh sách sinh viên với quyền phù hợp
            students = request.env['student.record'].with_user(request.env.user).search(domain)

            student_list = []
            for student in students:
                student_list.append({
                    'id': student.id,
                    'name': student.name,
                    'age': student.age,
                    'class': student.student_class,
                    'status': student.status
                })

            return Response(
                json.dumps({'students': student_list}),
                content_type='application/json;charset=utf-8',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json;charset=utf-8',
                status=500
            )

    # API thêm sinh viên mới
    @http.route('/api/students', auth='user', methods=['POST'], type='json', csrf=False)
    def create_student(self, **post):
        try:
            # Kiểm tra quyền giáo viên
            permission_error = self._check_teacher_permission()
            if permission_error:
                return permission_error

            # Kiểm tra dữ liệu đầu vào
            required_fields = ['name', 'age', 'student_class']
            missing_fields = [field for field in required_fields if not post.get(field)]
            if missing_fields:
                return {
                    'error': f'Thiếu thông tin bắt buộc: {", ".join(missing_fields)}',
                    'status': 400
                }

            # Kiểm tra lớp học có trong danh sách được phân công không
            teacher_classes = request.env.user.x_allowed_class.split(',') if request.env.user.x_allowed_class else []
            if post['student_class'] not in teacher_classes:
                return {
                    'error': 'Bạn không được phân công quản lý lớp này',
                    'status': 403
                }

            # Tạo sinh viên mới
            student = request.env['student.record'].create({
                'name': post.get('name'),
                'age': post.get('age'),
                'student_class': post.get('student_class'),
                'status': post.get('status', 0)
            })

            return {
                'success': True,
                'student_id': student.id,
                'message': 'Tạo sinh viên thành công'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 500
            }

    # API lấy thông tin 1 sinh viên
    @http.route('/api/students/<int:student_id>', auth='user', methods=['GET'], type='http')
    def get_student_detail(self, student_id, **kwargs):
        try:
            # Kiểm tra quyền đọc
            if not request.env.user.has_group('base.group_user'):
                return Response(
                    json.dumps({'error': 'Yêu cầu đăng nhập'}),
                    content_type='application/json;charset=utf-8',
                    status=401
                )

            # Tìm sinh viên
            student = request.env['student.record'].with_user(request.env.user).browse(student_id)
            if not student.exists():
                return Response(
                    json.dumps({'error': 'Không tìm thấy sinh viên'}),
                    content_type='application/json;charset=utf-8',
                    status=404
                )

            # Kiểm tra quyền giáo viên với lớp học
            if request.env.user.has_group('ngay_3.group_teacher'):
                teacher_classes = request.env.user.x_allowed_class.split(
                    ',') if request.env.user.x_allowed_class else []
                if student.student_class not in teacher_classes:
                    return Response(
                        json.dumps({'error': 'Bạn không có quyền xem sinh viên này'}),
                        content_type='application/json;charset=utf-8',
                        status=403
                    )

            student_data = {
                'id': student.id,
                'name': student.name,
                'age': student.age,
                'class': student.student_class,
                'status': student.status
            }

            return Response(
                json.dumps(student_data),
                content_type='application/json;charset=utf-8',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json;charset=utf-8',
                status=500
            )