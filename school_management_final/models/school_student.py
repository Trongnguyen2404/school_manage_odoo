from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'
    _order = 'name'

    name = fields.Char(string='Student Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True) # store=True để có thể tìm kiếm, lọc
    classroom_id = fields.Many2one('school.classroom', string='Classroom')
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
        help="The system user account associated with this student.",
        copy=False
    )
    @api.depends('birth_date')
    def _compute_age(self):
        for student in self:
            if student.birth_date:
                today = date.today()
                student.age = relativedelta(today, student.birth_date).years
            else:
                student.age = 0

    def compute_average_age(self):
        if not self:
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