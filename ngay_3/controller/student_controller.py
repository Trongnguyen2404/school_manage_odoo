from odoo import http
from odoo.http import request
import logging # Giữ lại import này nếu muốn dùng _logger

_logger = logging.getLogger(__name__) # Giữ lại nếu muốn log lỗi

class StudentWebsiteController(http.Controller):

    @http.route('/students', type='http', auth='public', website=True)
    def list_students(self, **kw):
        try:
            # Sử dụng sudo() để đảm bảo hoạt động ban đầu, cân nhắc bỏ sau khi test quyền
            students = request.env['student.record'].sudo().search([])
            return request.render('ngay_3.student_list_template', {
                'students': students,
                'page_title': 'Danh sách Sinh viên'
            })
        except Exception as e:
            _logger.error("Lỗi khi lấy danh sách sinh viên cho website: %s", e)
            return request.render('website.http_error', {'status_code': 500, 'status_message': 'Không thể tải danh sách sinh viên.'})


    @http.route('/student/add', type='http', auth='public', website=True, methods=['GET'])
    def add_student_form(self, **kw):
        return request.render('ngay_3.student_add_form_template', {
             'page_title': 'Thêm Sinh viên mới'
        })


    @http.route('/student/add', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def submit_student_form(self, **post):
        required_fields = ['student_name', 'student_age', 'student_email']
        missing_fields = [field for field in required_fields if not post.get(field)]

        if missing_fields:
            return request.render('ngay_3.student_add_form_template', {
                'error': 'Vui lòng điền đầy đủ các trường bắt buộc: %s' % ', '.join(missing_fields).replace('student_',''),
                'form_data': post,
                'page_title': 'Thêm Sinh viên mới'
            })

        try:
            vals = {
                'name': post.get('student_name'),
                'age': int(post.get('student_age')),
                'student_class': post.get('student_class'),
                'email': post.get('student_email'),
                'status': 'studying'
            }
            # Sử dụng sudo() để đảm bảo hoạt động ban đầu, cân nhắc bỏ sau khi test quyền
            new_student = request.env['student.record'].sudo().create(vals)
            return request.redirect('/students?submitted=1')

        except ValueError:
             return request.render('ngay_3.student_add_form_template', {
                'error': 'Tuổi phải là một con số.',
                'form_data': post,
                'page_title': 'Thêm Sinh viên mới'
            })
        except Exception as e:
            _logger.error("Lỗi khi tạo sinh viên từ website form: %s", e)
            return request.render('ngay_3.student_add_form_template', {
                'error': 'Đã có lỗi xảy ra khi thêm sinh viên. Vui lòng thử lại.',
                'form_data': post,
                'page_title': 'Thêm Sinh viên mới'
            })