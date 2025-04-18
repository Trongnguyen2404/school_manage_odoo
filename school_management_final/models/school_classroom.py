from odoo import models, fields

class SchoolClassroom(models.Model):
    _name = 'school.classroom'
    _description = 'School Classroom'

    name = fields.Char(string='Class', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Main Teacher')
    student_ids = fields.One2many('school.student', 'classroom_id', string='Students')