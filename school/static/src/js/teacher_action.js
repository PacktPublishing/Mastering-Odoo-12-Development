odoo.define('school.my_students', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    
    var QWeb = core.qweb;
    var _t = core._t;
    
    
    var MyStudents = AbstractAction.extend({
        events: {
            'click .o_school_student': '_open_student',
        },    
        willStart: function() {
            var self = this;
            return $.when(
                this._rpc({
                    model: 'res.partner',
                    method: 'search_read',
                    args: [[['supervisor_id', '=', this.getSession().partner_id]], ['name']],
                }),
                this._rpc({
                    model: 'ir.ui.view',
                    method: 'search_read',
                    args: [[['name', '=', "student.form"]], ['id']],
                }),
                this._super())
            .then(function (students, view) {
                self.teacher_name = self.getSession().name;
                self.students = students;
                self.form_view = view[0].id;
            });
        },
        start: function () {
            var self = this;
            this._super().then(function() {
                self.$el.html(QWeb.render("SchoolStudents", {widget: self}));
            });
        },

        _open_student: function(e) {
            e.preventDefault();
            var student_id = $(e.currentTarget).data('studentId');
            this.do_action( {
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'res.partner',
                views: [[this.form_view, 'form']],
                res_id: student_id,
            });
        }
    });
    
    core.action_registry.add('school_my_students', MyStudents);
    
    return MyStudents;
    
    });