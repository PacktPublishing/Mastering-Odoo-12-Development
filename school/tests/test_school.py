from datetime import date

from odoo.exceptions import UserError, AccessError
from odoo.tests.common import SavepointCase, HttpCase
from odoo.tests import tagged
from odoo.tools import mute_logger


class SchoolTest(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(SchoolTest, cls).setUpClass()
        cls.group1 = cls.env['school.group'].create({
            'name': 'Group 1',
            'supervisor_id': cls.env.ref('base.user_admin_res_partner').id
        })
        cls.student1 = cls.env['res.partner'].create({
            'name': 'Amanda Spear',
            'school_group_id': cls.group1.id,
            'birthdate': date.today(),
            'student': True
        })
        cls.student2 = cls.env['res.partner'].create({
            'name': 'Johnny Cloud',
            'school_group_id': cls.group1.id,
            'student': True
        })
        cls.student3 = cls.env['res.partner'].create({
            'name': 'Rose Bluebox',
            'school_group_id': cls.group1.id,
            'student': True
        })
        cls.simple_user = cls.env['res.users'].create({
            'name': 'Dan User',
            'login': 'dan_user',
            'groups_id': [(4, cls.env.ref('school.group_user').id)]
        })

    def test_01_student_count_value(self):
        self.assertEqual(self.group1.student_count, 3, 'there should be 3 students')
    
    def test_02_student_count_value(self):
        self.student1.active = False
        self.assertEqual(self.group1.student_count, 2, 'there should be 2 students')

    def test_03_student_count_search(self):
        valid_searches = [
            ([('student_count', '=', 3)], self.assertIn),
            ([('student_count', '>=', 3)], self.assertIn),
            ([('student_count', '<=', 3)], self.assertIn),
            ([('student_count', '>', 3)], self.assertNotIn),
            ([('student_count', '<', 3)], self.assertNotIn),
            ([('student_count', '!=', 3)], self.assertNotIn),
        ]
        for search in valid_searches:
            search_result = self.env['school.group'].search(search[0])
            search[1](self.group1, search_result, 'wrong result for search %s' % search[0])

        invalid_searches = [
            [('student_count', 'in', [3])],
            [('student_count', 'like', "3")],
        ]
        for search in invalid_searches:
            with self.assertRaises(UserError):
                self.env['school.group'].search(search)

    @mute_logger('odoo.models')
    def test_04_access(self):
        student = self.student1.sudo(self.simple_user)
        self.assertEqual(student.name, self.student1.name)
        with self.assertRaises(AccessError):
            student.sudo(self.simple_user).birthdate


@tagged('-at_install', 'post_install')
class SchoolWebTests(HttpCase):
    def test_action(self):
        self.browser_js('/web/tests?module=School&failfast', "", "", login='admin', timeout=1800)

    def test_tour(self):
        self.start_tour("/web", 'school_tour', login="admin")
