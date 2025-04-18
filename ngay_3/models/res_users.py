from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Dùng Char để lưu nhiều lớp, phân cách bằng dấu phẩy (ví dụ: "10A,11B")
    x_allowed_class = fields.Char(
        string="Danh sách lớp được phân công",
        help="Nhập các lớp phân cách bằng dấu phẩy (ví dụ: 10A,11B)"
    )

    @api.constrains('x_allowed_class', 'groups_id')
    def _check_teacher_class(self):
        for user in self:
            if user.has_group('ngay_3.group_teacher') and not user.x_allowed_class:
                raise ValidationError("Giáo viên phải có ít nhất 1 lớp được phân công!")