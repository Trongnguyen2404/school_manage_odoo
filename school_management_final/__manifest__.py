# -*- coding: utf-8 -*-
{
    'name': "School Management Final",  # Tên hiển thị của module

    'summary': """
        Manage classrooms, teachers, students, and display school information on the website.
    """,  # Mô tả ngắn gọn

    'author': "final school",  # Tên tác giả
    'category': 'Education', # Phân loại module
    'version': '1.0', # Phiên bản module
    'depends': [
        'base',
        'website',
        ],

    # always loaded
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'views/school_classroom_views.xml',
        'views/school_teacher_views.xml',
        'views/school_student_views.xml',
        'views/school_menus.xml',
        'report/student_report.xml'
        # 'templates/website_school_templates.xml',
        # 'views/website_menus.xml'
    ],
    'installable': True, # Cho phép cài đặt
    'application': True,  # Đánh dấu là một ứng dụng chính
    'auto_install': False, # Không tự động cài đặt khi cài module phụ thuộc
    'license': 'LGPL-3',   # Giấy phép phần mềm (thường là LGPL-3 cho module cộng đồng)


    'icon': '/school_management_final/static/description/icon.png', # Icon hiển thị trên menu chính
}