# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError # Giữ lại import này, hữu ích
import logging # Thêm import logging

_logger = logging.getLogger(__name__) # Khởi tạo logger cho file này

class Student(models.Model):
    _name = 'student.record'
    _description = 'Student Record'
    # Kế thừa mail.thread để có chatter (nên có)
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # --- Các trường dữ liệu ---
    # Thêm tracking=True để theo dõi thay đổi trong chatter
    name = fields.Char(string='Tên', required=True, tracking=True)
    age = fields.Integer(string='Tuổi', required=True, tracking=True)
    student_class = fields.Char(string='Lớp', tracking=True)
    status = fields.Selection([
        ('studying', 'Đang học'),
        ('graduated', 'Đã tốt nghiệp')
    ], string='Tình trạng', required=True, default='studying', tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True) # Email nên có widget="email" trong view

    # --- Các phương thức gốc ---
    def send_welcome_email(self):
        """Gửi email chào mừng."""
        template = self.env.ref('ngay_3.email_template_welcome_student', raise_if_not_found=False) # Giả sử bạn có template này

        for student in self:
            if student.email:
                if template:
                    try:
                        template.send_mail(student.id, force_send=True)
                        _logger.info(f"Sent welcome email template to {student.name} ({student.email})")
                    except Exception as e:
                         _logger.error(f"Failed to send welcome email template to {student.name}: {e}")
                else:
                    _logger.warning("Email template 'ngay_3.email_template_welcome_student' not found. Sending raw email.")
                    mail_values = {
                        'subject': f"Chào mừng {student.name} đến với trường!",
                        'body_html': f"""
                            <p>Chào {student.name}!</p>
                            <p>Chúc mừng bạn đã được nhập học vào lớp {student.student_class}.</p>
                            <p>Chúc bạn học tập tốt và thành công!</p>
                        """,
                        'email_from': self.env.user.company_id.email or 'no-reply@yourcompany.com',
                        'email_to': student.email,
                        'auto_delete': True,
                        'model': self._name,
                        'res_id': student.id,
                    }
                    try:
                        mail = self.env['mail.mail'].sudo().create(mail_values)
                        mail.send()
                        _logger.info(f"Sent raw welcome email to {student.name} ({student.email})")
                    except Exception as e:
                         _logger.error(f"Failed to send raw welcome email to {student.name}: {e}")

    @api.model
    def get_students_by_class(self, class_name):
        """Lấy danh sách sinh viên theo lớp (dùng nội bộ nếu cần)"""
        return self.search([('student_class', '=', class_name)])

    def compute_average_age(self):
        """Tính tuổi trung bình của các sinh viên được chọn"""
        if not self: # Kiểm tra self rỗng
             return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': "Vui lòng chọn ít nhất 1 sinh viên.",
                    'type': 'warning',
                    'sticky': False,
                }
            }
        selected_count = len(self)
        total_age = sum(student.age for student in self)
        avg_age = total_age / selected_count
        message = f"Tuổi trung bình của {selected_count} sinh viên được chọn: {avg_age:.1f}"
        alert_type = 'success'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thống kê tuổi',
                'message': message,
                'type': alert_type,
                'sticky': False,
            }
        }

    @api.model_create_multi # Sử dụng decorator này tốt hơn @api.model cho create
    def create(self, vals_list):
        students = super().create(vals_list)
        self.env.cr.commit()
        students.sudo().send_welcome_email() # Dùng sudo nếu cần quyền
        return students

    @api.model
    def update_student_status(self):
        """Cron Job: Cập nhật trạng thái sinh viên nếu tuổi >= 23"""
        _logger.info("Cron Job: Running update_student_status...")
        students_to_update = self.search([('status', '=', 'studying'), ('age', '>=', 23)])
        count = len(students_to_update)
        if count > 0:
            students_to_update.write({'status': 'graduated'})
            _logger.info(f"Cron Job: Updated {count} students to 'graduated'.")
        else:
            _logger.info("Cron Job: No students found to update status.")

    # === PHƯƠNG THỨC MỚI CHO OWL WIDGET ===

    @api.model
    def get_students_for_owl_widget(self, class_name=None):
        """
        Trả về danh sách sinh viên (dạng dict) theo lớp cho OWL Widget.
        """
        if not class_name:
            _logger.info("OWL Widget: No class selected, returning empty list.")
            return []

        domain = [('student_class', '=', class_name)]
        students = self.search(domain)
        student_data = students.read(['id', 'name', 'age', 'student_class', 'email', 'status'])
        status_selection = dict(self._fields['status'].selection)
        for student in student_data:
            student['status_display'] = status_selection.get(student['status'], student['status'])

        _logger.info(f"OWL Widget: Fetched {len(student_data)} students for class '{class_name}'.")
        return student_data

    @api.model
    def get_unique_classes_for_owl(self):
        """
        Lấy danh sách các tên lớp duy nhất cho dropdown trong OWL widget.
        """
        class_groups = self.read_group(
            domain=[('student_class', '!=', False), ('student_class', '!=', '')],
            fields=['student_class'],
            groupby=['student_class'],
            lazy=False
        )
        classes = sorted([group['student_class'] for group in class_groups if group.get('student_class')])
        _logger.info(f"OWL Widget: Fetched unique classes: {classes}")
        return classes


# --- Kế thừa ResPartner ---
class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_id = fields.Char(string='Mã sinh viên', copy=False)
    is_student = fields.Boolean(string='Là sinh viên', copy=False)

    _sql_constraints = [
        ('student_id_uniq', 'unique (student_id)', 'Mã sinh viên đã tồn tại!')
    ]