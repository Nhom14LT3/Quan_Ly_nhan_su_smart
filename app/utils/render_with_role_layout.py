from flask import render_template
from flask_login import current_user

def render_with_role(template_name, **context):
    role = getattr(current_user, 'role', None)
    if role == 'admin':
        layout = 'layouts/base_admin.html'
    elif role == 'manager':
        layout = 'layouts/base_manager.html'
    else:
        layout = 'layouts/base_employee.html'
    
    return render_template(template_name, layout=layout, **context)
