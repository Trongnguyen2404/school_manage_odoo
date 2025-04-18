from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Dùng Char để lưu nhiều lớp, phân cách bằng dấu phẩy (ví dụ: "10A,11B")
    # x_allowed_class = fields.Char(
    #     string="Danh sách lớp được phân công",
    #     help="Nhập các lớp phân cách bằng dấu phẩy (ví dụ: 10A,11B)"
    # )
    allowed_class_ids = fields.Many2many(
        'student.class',  # Model đích là lớp học
        'res_users_student_class_rel',  # Tên bảng trung gian (Odoo tự tạo nếu không có)
        'user_id',  # Cột trỏ về res.users trong bảng trung gian
        'class_id',  # Cột trỏ về student.class trong bảng trung gian
        string="Các Lớp được Phân công",
        help="Chọn các lớp mà giáo viên này được phép quản lý."
    )
    # @api.constrains('x_allowed_class', 'groups_id')
    # def _check_teacher_class(self):
    #     for user in self:
    #         if user.has_group('ngay_3.group_teacher') and not user.x_allowed_class:
    #             raise ValidationError("Giáo viên phải có ít nhất 1 lớp được phân công!")
    @api.constrains('allowed_class_ids', 'groups_id')  # Trigger khi danh sách lớp hoặc nhóm thay đổi
    def _check_teacher_class(self):
        # Lấy group Giáo viên (nên dùng ref thay vì has_group để an toàn hơn)
        teacher_group = self.env.ref('ngay_3.group_teacher', raise_if_not_found=False)
        if not teacher_group:
            return  # Bỏ qua nếu group chưa tồn tại

        for user in self:
            # Kiểm tra nếu user thuộc nhóm GV VÀ danh sách lớp được gán là rỗng
            if teacher_group in user.groups_id and not user.allowed_class_ids:
                raise ValidationError(f"Giáo viên '{user.name}' phải được phân công ít nhất một lớp!")