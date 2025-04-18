# -*- coding: utf-8 -*-
from odoo import models, fields

class StudentClass(models.Model):
    _name = 'student.class'
    _description = 'Lớp Học'
    _order = 'name' # Sắp xếp theo tên lớp

    name = fields.Char(string='Tên Lớp', required=True, index=True)
    # Bạn có thể thêm các trường khác cho lớp học ở đây nếu cần

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tên lớp học phải là duy nhất!')
    ]

    # Hàm này giúp hiển thị tên khi chọn trong Many2one/Many2many
    def name_get(self):
        return [(record.id, record.name) for record in self]
