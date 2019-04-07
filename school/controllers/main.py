from odoo.http import Controller, request, route


class SchoolController(Controller):
    @route('/school/group/<model("school.group"):group_id>', auth='user')
    def group_list(self, group_id):
        return request.render('school.class_list', {'group_id': group_id})
