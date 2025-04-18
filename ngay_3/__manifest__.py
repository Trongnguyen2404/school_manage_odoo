# -*- coding: utf-8 -*-
{
    'name': 'ngay_3', # Đảm bảo đây là tên kỹ thuật đúng
    'version': '1.0',
    'category': 'Education',
    'summary': 'Quản lý thông tin sinh viên và OWL Widget',
    'depends': ['base', 'web', 'mail', 'website'], # 'web' là bắt buộc
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        # 'data/student_data.xml',
        'data/email_template.xml',
        'data/cron.xml',
        'views/student_views.xml', # File định nghĩa menu cha 'student_menu'
        'views/res_users_view.xml',
        'report/student_report.xml',
        'views/website_student_templates.xml',
        'views/student_client_action_views.xml', # <<< THÊM DÒNG NÀY VÀO ĐÂY
    ],
    'assets': {
        'web.assets_backend': [
            # 'static/src/scss/student_class_widget.scss',
            # 'static/src/js/student_class_widget.js',
            # 'static/src/xml/student_class_widget.xml',
            'ngay_3/static/src/scss/student_class_widget.scss',
            'ngay_3/static/src/js/student_class_widget.js',
            'ngay_3/static/src/xml/student_class_widget.xml'
        ],
    },
    'installable': True,
    'application': True,
}