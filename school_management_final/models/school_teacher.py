import re # Thêm thư viện regex để kiểm tra email
from odoo import models, fields, api, _ # Thêm _ để dịch thuật thông báo lỗi (nên dùng)
from odoo.exceptions import ValidationError # Thêm để báo lỗi validation
from dateutil.relativedelta import relativedelta
from datetime import date

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'School Teacher'

    name = fields.Char(string='Teacher Name', required=True)
    classroom_ids = fields.One2many('school.classroom', 'teacher_id', string='Managed Classes')
    phone = fields.Char(string='Teacher Phone', required=True)
    email = fields.Char(string='Teacher Email', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection(
        selection=[
            ('male', 'Nam'),
            ('female', 'Nữ')
        ],
        string='Giới tính',
        required=True,
        default='male'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Related User',
        ondelete='set null',
        help="The system user account associated with this teacher.",
        copy=False
    )
    @api.depends('birth_date')
    def _compute_age(self):
        for teacher in self:  # Đổi tên biến student thành teacher cho đúng ngữ cảnh
            if teacher.birth_date:
                today = date.today()
                teacher.age = relativedelta(today, teacher.birth_date).years
            else:
                teacher.age = 0

    # --- Thêm Constraints ---
    @api.constrains('phone')
    def _check_phone_number(self):
        """Kiểm tra số điện thoại: 10 chữ số, bắt đầu bằng 0"""
        for teacher in self:
            # Chỉ kiểm tra nếu trường phone có giá trị
            if teacher.phone:
                phone = teacher.phone.strip()  # Xóa khoảng trắng thừa
                # Kiểm tra có phải 10 ký tự không
                if len(phone) != 10:
                    raise ValidationError(_("Số điện thoại '%s' phải có đúng 10 chữ số.", phone))
                # Kiểm tra có phải toàn chữ số không
                if not phone.isdigit():
                    raise ValidationError(_("Số điện thoại '%s' chỉ được chứa chữ số.", phone))
                # Kiểm tra có bắt đầu bằng số 0 không
                if not phone.startswith('0'):
                    raise ValidationError(_("Số điện thoại '%s' phải bắt đầu bằng số 0.", phone))

    @api.constrains('email')
    def _check_email_format(self):
        """Kiểm tra định dạng email hợp lệ"""
        # Biểu thức chính quy (regex) cơ bản để kiểm tra email
        # Có thể dùng regex phức tạp hơn nếu cần, nhưng regex này khá phổ biến
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for teacher in self:
            # Chỉ kiểm tra nếu trường email có giá trị
            if teacher.email:
                email = teacher.email.strip()  # Xóa khoảng trắng thừa
                if not re.match(email_regex, email):
                    raise ValidationError(_("Địa chỉ email '%s' không hợp lệ.", email))
